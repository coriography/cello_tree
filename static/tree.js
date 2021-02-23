"use strict";

var data = {
    "name": "parent node (hide)",
    "children": [{
        "name": "Janos Starker",
        "children": [{
                "name": "Anthony Elliott",
                "children": [{
                        "name": "Cori Lint",
                        "children": [{
                            "name": "CL1",
                            "children": [{
                                "name": "CL2"
                            }]
                        }]
                    },
                    {
                        "name": "Jonathan Butler"
                    },
                    {
                        "name": "Annabeth Shirley"
                    }
                ]
            },
            {
                "name": "Brant Taylor",
                "children": [{
                        "name": "Sonia Mantell"
                    },
                    {
                        "name": "Anita Graef"
                    }
                ]
            }
        ]
    }]
};


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

const svg = d3.select('#tree_layout').append('svg');

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
    .text((d) => {
        return d.data.name;
    }).clone(true).lower() // Copy text and give it a white outline
    .attr('stroke', 'white');