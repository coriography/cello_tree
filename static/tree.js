"use strict";

var data = {
    "name": "Janos Starker",
    "children": [{
            "name": "Anthony Elliott",
            "children": [{
                    "name": "Cori Lint"
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
};

var treeLayout =
    d3.tree()
    .size([500, 500]);
var root = d3.hierarchy(data);

treeLayout(root);

// Nodes
d3.select('svg g.nodes')
    .selectAll('circle.node')
    .data(root.descendants())
    .enter()
    .append('circle')
    .classed('node', true)
    .attr('cx', function (d) {
        return d.x;
    })
    .attr('cy', function (d) {
        return d.y;
    })
    .attr('r', 4);

// Links
d3.select('svg g.links')
    .selectAll('line.link')
    .data(root.links())
    .enter()
    .append('line')
    .classed('link', true)
    .attr('x1', function (d) {
        return d.source.x;
    })
    .attr('y1', function (d) {
        return d.source.y;
    })
    .attr('x2', function (d) {
        return d.target.x;
    })
    .attr('y2', function (d) {
        return d.target.y;
    });