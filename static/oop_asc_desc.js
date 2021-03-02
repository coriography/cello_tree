// this code is adapted from justincy's example of a tree with both ancestors and descendants:
// https://github.com/justincy/d3-pedigree-examples

// set up zoom and pan
// ?? do I need this?? maybe not until second gen/third gen added?
var zoom = d3.behavior.zoom()
    // sets max zoom [out, in]
    .scaleExtent([.5, 2])
    .on('zoom', function () {
        svg.attr("transform", "translate(" + d3.event.translate + ") scale(" + d3.event.scale + ")");
    })
    // set to same offset as graphic so that first pan and zoom does not jump to cursor
    .translate([400, 200]);

// find DOM element and append graphic to it
var svg = d3.select("#double_tree_container").append("svg")
    .attr('width', 1000) //?? can this be dynamic - i.e. calculate viewport width?
    .attr('height', 500) //?? same here
    .call(zoom) // TODO: disable here if not using
    .append('g') // ?? what is this?

    // adjust tree so that the whole root node is on the screen (x, y)
    // TODO: adjust for mobile
    .attr("transform", "translate(400,200)");


// create one tree to display ancestors
// see Tree class definition in tree_class.js
var ancestorTree = new Tree(svg, 'ancestor', -1);
ancestorTree.children(function (person) {
    return person._parents;
});

// create a separate tree to display descendants
var descendantsTree = new Tree(svg, 'descendant', 1);
descendantsTree.children(function (person) {
    return person._children;
});

function rootProxy(root) {
    return {
        name: root.name,
        id: root.id,
        x0: 0,
        y0: 0,
        _children: root._children,
        _parents: root._parents,
        collapsed: false
    };
}

let rootCellistId = $("#root_cellist_id").first().attr("data-id");

$.get(`/api/oop_tree/${rootCellistId}`, (json) => {

    // the same node can't exist in two trees, 
    // but we need both trees (with different properties) to originate 
    // from the same root node. So we create two separate proxy nodes 
    // for the same root node only.
    var ancestorRoot = rootProxy(json.tree_data);
    var descendantRoot = rootProxy(json.tree_data);

    // TODO: use this code if adding second generation
        // ancestorRoot._parents.forEach(function (parents) {
        //     parents._parents.forEach(collapse);
        // });

        // Start with only one generation of descendants showing
        // descendantRoot._children.forEach(collapse);

    // set the root nodes
    ancestorTree.data(ancestorRoot);
    descendantsTree.data(descendantRoot);

    // draw the tree
    ancestorTree.draw(ancestorRoot);
    descendantsTree.draw(descendantRoot);
});