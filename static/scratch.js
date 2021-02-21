
{/* <svg width="500" height="500">
    <g transform="translate(5, 5)">
        <g class="links"></g>
        <g class="nodes"></g>
    </g>
</svg> */}


{/* <style>

.node {
    fill: #000000;
    stroke: none;
}

.link {
    fill: none;
    stroke: #ccc;
    stroke-width: 2px;
}
</style> */}
// var treeDisplay =
//     d3.tree()
//     .size([500, 500]);
// var root = d3.hierarchy(data);

// treeDisplay(root);

// // Nodes
// d3.select('svg g.nodes')
//     .selectAll('circle.node')
//     .data(root.descendants())
//     .enter()
//     .append('circle')
//     .classed('node', true)
//     .attr('cx', function (d) {
//         return d.x;
//     })
//     .attr('cy', function (d) {
//         return d.y;
//     })
//     .attr('r', 4);

// // Links
// d3.select('svg g.links')
//     .selectAll('line.link')
//     .data(root.links())
//     .enter()
//     .append('line')
//     .classed('link', true)
//     .attr('x1', function (d) {
//         return d.source.x;
//     })
//     .attr('y1', function (d) {
//         return d.source.y;
//     })
//     .attr('x2', function (d) {
//         return d.target.x;
//     })
//     .attr('y2', function (d) {
//         return d.target.y;
//     });