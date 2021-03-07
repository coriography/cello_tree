// this file is taken from the Hackbright D3 example and is no longer in use.

"use strict";

const multiStudent = {
    "fname": "Multi",
    "lname": "Student",
    "children": [{
        "fname": "multistudent",
        "lname": "1",
        "children": [{
                "fname": "multistudent2",
                "lname": "2",
                "children": [{
                        "fname": "multistudent",
                        "lname": "3",
                        "children": [
                            {
                                "fname": "multistudent4",
                                "lname": "4",
                            },
                            {
                                "fname": "multistudent5",
                                "lname": "5",
                            }
                        ]
                    },
                    {
                        "fname": "multi",
                        "lname": "again",
                    }
                ],
            },
            {
                "fname": "multi",
                "lname": "another",
            },
            {
                "fname": "multi",
                "lname": "another",
            },
            {
                "fname": "multi",
                "lname": "another",
            },
            {
                "fname": "multi",
                "lname": "another",
            },
            {
                "fname": "multi",
                "lname": "another",
            },
            {
                "fname": "multi",
                "lname": "another",
            },
            {
                "fname": "multi",
                "lname": "another",
            }
        ]
    }]
};

const testData = {
    "fname": "parent node (hide)",
    "children": [{
        "fname": "Janos",
        "lname": "Starker",
        "children": [{
                "fname": "Anthony",
                "lname": "Elliott",
                "children": [{
                        "fname": "Cori",
                        "lname": "Lint",
                        "children": [{
                            "fname": "CL1",
                            "lname": "last",
                            "children": [{
                                "fname": "CL2",
                                "lname": "last",
                            }]
                        }]
                    },
                    multiStudent,
                    {
                        "fname": "Jonathan",
                        "lname": "Butler"
                    },
                    {
                        "fname": "Annabeth",
                        "lname": "Shirley"
                    }
                ]
            },
            {
                "fname": "Brant",
                "lname": "Taylor",
                "children": [{
                        "fname": "Sonia",
                        "lname": "Mantell"
                    },
                    {
                        "fname": "Anita",
                        "lname": "Graef"
                    }
                ]
            }
        ]
    }]
};


function growTree(data, svgElement) {
    const container = $('#tree_layout');
    const width = container.width();

    // restructure the data from data object as a hierarchical tree
    const root = d3.hierarchy(data);

    // Set coordinates for root node
    root.dx = 30; // This will determine how wide the tree is
    // Set `dy` to the middle of the container.
    // `root.height + 1` is the # of levels in the tree
    root.dy = width / (root.height + 1);

    // Create a tree based on root node's dimensions
    const treeLayout = d3.tree().nodeSize([root.dx, root.dy]);
    const tree = treeLayout(root);

    // Find the largest and smallest coordinates on the x-axis to calculate the
    // height of our parent container (#tree_layout)
    let min = Infinity;
    let max = -Infinity;
    root.each(d => {
        if (d.x > max) {
            max = d.x;
        }

        if (d.x < min) {
            min = d.x;
        }
    });
    container.height(max - min + root.dx * 2);

    // d3.scaleSequential will return a function that we'll use to color the
    // links of the tree
    // - https://github.com/d3/d3-scale#sequential-scales
    // - https://github.com/d3/d3-scale-chromatic#interpolateWarm
    const color = d3.scaleSequential(d3.interpolateYlGn)
        .domain([0, root.links().length - 1]);
    // const color = "#E3E3E3"; // or just 

    const svg = d3.select(svgElement).append('svg');

    // Create a group to cover the entire `svg`. This makes it easier to position
    // the nodes and links in the tree.
    const g = svg.append('g')
        .attr('transform', `translate(${root.dy / 3}, ${root.dx - min})`);

    const link = g.append('g')
        .attr('fill', 'none')
        .attr('stroke-width', 3)
        .selectAll('path')
        .data(root.links())
        .enter().append('path')
        .attr('stroke', (d, idx) => {
            return color(idx);
        })
        .attr(
            'd',
            // d3.linkHorizontal returns a function that automatically
            // generates paths between parent and child. We'll use this function as a callback.
            //
            // For more info see: https://github.com/d3/d3-shape#linkHorizontal
            d3.linkHorizontal()
            .x(d => d.y)
            .y(d => d.x)
        );

    const node = g.append('g') // Use a group to apply styles to all nodes
        .attr('stroke-linejoin', 'round')
        .attr('stroke-width', 3)
        .selectAll('g')
        // root.descendants() is all nodes except for the root.
        .data(root.descendants())
        .enter().append('g')
        .attr('transform', (d) => {
            return `translate(${d.y}, ${d.x})`;
        })
        .attr('onclick', (d) => {
            return `showNodeChildren(${d.data.id})`;
        })
        .attr('id', (d) => {
            return `node_${d.data.id}`;
        });

    node.append('circle')
        .attr('fill', 'white')
        .attr('stroke', 'black')
        .attr('stroke-width', 2.5)
        .attr('r', 4.5);

    node.append('text')
        .attr('dy', '0.31em')
        .attr('x', (d) => {
            // If the node has children, move text to the left of the .
            // Otherwise, move it to the right.
            if (d.children) {
                return -9;
            } else {
                return 9;
            }
        })
        .attr('text-anchor', (d) => {
            // This also helps us align text
            if (d.children) {
                return 'end';
            } else {
                return 'start';
            }
        })
        .attr('font-size', 14)
        .html((d) => {
            return `
                <a href="/tree/${d.data.id}">${d.data.fname} ${d.data.lname}</a>
            `;
        })
        .clone(true).lower() // Copy text and give it a white outline
        .attr('stroke', 'white');
}


$(document).ready(function () {

    let rootCellistId = $("#root_cellist_id").first().attr("data-id");

    $.get(`/api/tree/${rootCellistId}`, (res) => {
        growTree(res.tree_data, "#tree_layout");
    })
});


// !! not currently in use
function showNodeChildren(cellist_id) {

    $.get(`/api/tree/${cellist_id}`, (res) => {
        growTree(res.tree_data, `#node_${cellist_id}`);
        //!! this appends entire new svg w/ root
        // ?? can I make this append only the children
        // ?? by inserting new node w/ children as var into original data structure?
        // ?? for spacing to work I would prob have to re-render the whole thing
    });
};