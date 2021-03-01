const boxWidth = 150,
    boxHeight = 40,
    nodeWidth = 100,
    nodeHeight = 200,

    // duration of transitions in ms
    duration = 500,

    // distance between nodes: node size mutiplied by "separation" value
    separation = .5;

// Setup zoom and pan
var zoom = d3.behavior.zoom()
    .scaleExtent([.1, 1])
    .on('zoom', function () {
        svg.attr("transform", "translate(" + d3.event.translate + ") scale(" + d3.event.scale + ")");
    })
    // Offset so that first pan and zoom does not jump back to the origin
    .translate([400, 200]);

var svg = d3.select("body").append("svg")
    .attr('width', 1000)
    .attr('height', 500)
    .call(zoom)
    .append('g')

    // Left padding of tree so that the whole root node is on the screen.
    // TODO: find a better way
    .attr("transform", "translate(400,200)");


// One tree to display the ancestors
var ancestorTree = new Tree(svg, 'ancestor', 1);
ancestorTree.children(function (person) {
    // If the person is collapsed then tell d3
    // that they don't have any ancestors.
    if (person.collapsed) {
        return;
    } else {
        return person._parents;
    }
});

// Use a separate tree to display the descendants
var descendantsTree = new Tree(svg, 'descendant', -1);
descendantsTree.children(function (person) {
    if (person.collapsed) {
        return;
    } else {
        return person._children;
    }
});

let rootCellistId = $("#root_cellist_id").first().attr("data-id");
// let rootCellistId = 2;

$.get(`/api/oop_tree/${rootCellistId}`, (json) => {

    // D3 modifies the objects by setting properties such as
    // coordinates, parent, and children. Thus the same node
    // node can't exist in two trees. But we need the root to
    // be in both so we create proxy nodes for the root only.
    var ancestorRoot = rootProxy(json.tree_data);
    var descendantRoot = rootProxy(json.tree_data);

    // Start with only the first few generations of ancestors showing
    // ancestorRoot._parents.forEach(function (parents) {
    //     parents._parents.forEach(collapse);
    // });

    // Start with only one generation of descendants showing
    descendantRoot._children.forEach(collapse);

    // Set the root nodes
    ancestorTree.data(ancestorRoot);
    descendantsTree.data(descendantRoot);

    // Draw the tree
    ancestorTree.draw(ancestorRoot);
    descendantsTree.draw(descendantRoot);
});