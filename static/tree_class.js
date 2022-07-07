// this code is adapted from justincy's example of a tree with both ancestors and descendants:
// https://github.com/justincy/d3-pedigree-examples

const boxWidth = 180,
    boxHeight = 40,
    nodeWidth = 100,
    nodeHeight = 200,

    // duration of transitions in ms
    duration = 500,

    // distance between nodes: node size mutiplied by "separation" value
    separation = .5;

// TODO: set width, height, translate to variables that can be adjusted for responsiveness

// this code block draws ancestors or descendants
// selector is a class applied to links and nodes
// selector will be queried later when tree is redrawn
// "direction" is 1 (forward) or -1 (backward)

var Tree = function (svg, selector, direction) {
    this.svg = svg;
    this.selector = selector;
    this.direction = direction;

    this.tree = d3.layout.tree()

        // controls separation between nodes
        .nodeSize([nodeWidth, nodeHeight])

        // default behavior draws cousins further apart than siblings - 
        // returning the same value for siblings or cousins ensures
        // that all will be drawn the same distance apart
        // despite the default behavior
        .separation(function () {
            return separation;
        });
};


// set "children" function for tree
Tree.prototype.children = function (fn) {
    this.tree.children(fn);
    return this;
};


// set root of tree
Tree.prototype.data = function (data) {
    this.root = data;
    return this;
};


// set function to draw/redraw tree
Tree.prototype.draw = function (source) {
    if (this.root) {
        var nodes = this.tree.nodes(this.root),
            links = this.tree.links(nodes);
        this.drawLinks(links, source);
        this.drawNodes(nodes, source);
    } else {
        throw new Error('Missing root');
    }
    return this;
};


// draw/redraw lines between nodes
Tree.prototype.drawLinks = function (links, source) {

    var self = this;

    // update links (e.g. on page refresh)
    var link = self.svg.selectAll("path.link." + self.selector)

        // provide d3 with an id for each link
        .data(links, function (d) {
            return d.target.id;
        });

    // add new links
    // transition new links from old to new position
    link.enter().append("path")
        .attr("class", "link " + self.selector)
        .style("stroke", "#485511")
        .style("opacity", .2)
        .attr("d", function (d) {
            var o = {
                x: source.x0,
                y: self.direction * (source.y0 + boxWidth / 2)
            };
            return transitionElbow({
                source: o,
                target: o
            });
        });

    // update link positions
    link.transition()
        .duration(duration)
        .attr("d", function (d) {
            return elbow(d, self.direction);
        });

    // remove links that aren't needed
    // transition exit links from current position to source's new position
    link.exit()
        .transition()
        .duration(duration)
        .attr("d", function (d) {
            var o = {
                x: source.x,
                y: self.direction * (source.y + boxWidth / 2)
            };
            return transitionElbow({
                source: o,
                target: o
            });
        })
        .remove();
};


// draw/redraw the node rectangles and text inside them
Tree.prototype.drawNodes = function (nodes, source) {

    var self = this;

    // update nodes    
    var node = self.svg.selectAll("g.person." + self.selector)

        // provide d3 with an id for each node
        .data(nodes, function (person) {
            return person.id;
        });

    // add any new nodes
    var nodeEnter = node.enter().append("g")
        .attr("class", "person " + self.selector)
        .on('click', function (person) {
            location.href = `/cellist_profile/${person.id}#treeSection`;
        });

    // draw rectangles
    // set at size 0 for transitions, width, and height set elsewhere
    nodeEnter.append("rect")
        .attr({
            x: 0,
            y: 0,
            width: 0,
            height: 0
        });

    // draw name and position it inside their rectangle
    nodeEnter.append("text")
        .attr("dx", 0)
        .attr("dy", 0)
        .attr("text-anchor", "start")
        .attr('class', 'name')
        .style("fill", "#0e2002")
        .html(function (d) {
            return d.name;
        })
        .style('fill-opacity', 0);

    // Update the position of both old and new nodes
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function (d) {
            return "translate(" + (self.direction * d.y) + "," + d.x + ")";
        });

    // Grow boxes to their proper size    
    nodeUpdate.select('rect')
        .style("stroke", "#485511")
        .style("fill", "#8FAA22")
        .style("fill-opacity", ".4")
        .attr({
            x: -(boxWidth / 2),
            y: -(boxHeight / 2),
            width: boxWidth,
            height: boxHeight
        });

    // Move text to its proper position
    nodeUpdate.select('text')
        .attr("dx", -(boxWidth / 2) + 10)
        .style('fill-opacity', 1);

    // NOT CURRENTLY USING THIS TO END OF FUNCTION
    // Remove nodes we aren't showing anymore
    var nodeExit = node.exit()
        .transition()
        .duration(duration)

        // Transition exit nodes to the source's position
        .attr("transform", function (d) {
            return "translate(" + (self.direction * (source.y + boxWidth / 2)) + "," + source.x + ")";
        })
        .remove();

    // Shrink boxes as we remove them    
    nodeExit.select('rect')
        .attr({
            x: 0,
            y: 0,
            width: 0,
            height: 0,
        });

    // Fade out the text as we remove it
    nodeExit.select('text')
        .style('fill-opacity', 0)
        .attr('dx', 0);

    // Stash the old positions for transition.
    nodes.forEach(function (person) {
        person.x0 = person.x;
        person.y0 = person.y;
    });

};

/**
 * Update a person's state when they are clicked.
 * NOT CURRENTLY USING THIS
 */
Tree.prototype.togglePerson = function (person) {

    // Don't allow the root to be collapsed because that's
    // silly (it also makes our life easier)
    if (person === this.root) {
        return;
    }

    // Non-root nodes
    else {

        if (person.collapsed) {
            person.collapsed = false;
        } else {
            collapse(person);
        }

        this.draw(person);
    }
};

/**
 * NOT CURRENTLY USING THIS FEATURE
 * Collapse person (hide their ancestors). We recursively
 * collapse the ancestors so that when the person is
 * expanded it will only reveal one generation. If we don't
 * recursively collapse the ancestors then when
 * the person is clicked on again to expand, all ancestors
 * that were previously showing will be shown again.
 * If you want that behavior then just remove the recursion
 * by removing the if block.
 */
function collapse(person) {
    person.collapsed = true;
    if (person._parents) {
        person._parents.forEach(collapse);
    }
    if (person._children) {
        person._children.forEach(collapse);
    }
}

/**
 * Custom path function that creates straight connecting
 * lines. Calculate start and end position of links.
 * Instead of drawing to the center of the node,
 * draw to the border of the person profile box.
 * That way drawing order doesn't matter. In other
 * words, if we draw to the center of the node
 * then we have to draw the links first and the
 * draw the boxes on top of them.
 */
function elbow(d, direction) {
    var sourceX = d.source.x,
        sourceY = d.source.y + (boxWidth / 2),
        targetX = d.target.x,
        targetY = d.target.y - (boxWidth / 2);

    return "M" + (direction * sourceY) + "," + sourceX +
        "H" + (direction * (sourceY + (targetY - sourceY) / 2)) +
        "V" + targetX +
        "H" + (direction * targetY);
}

/**
 * Use a different elbow function for enter
 * and exit nodes. This is necessary because
 * the function above assumes that the nodes
 * are stationary along the x axis.
 */
function transitionElbow(d) {
    return "M" + d.source.y + "," + d.source.x +
        "H" + d.source.y +
        "V" + d.source.x +
        "H" + d.source.y;
}