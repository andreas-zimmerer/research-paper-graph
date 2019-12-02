import React, { Component } from 'react';
import * as d3 from 'd3';
import { Paper } from '../../types/paper';
import './graph.css';

/**
 * A node on the graph representing a paper.
 * Also contains a reference to the original paper.
 */
class PaperNode implements d3.SimulationNodeDatum {
  public x: number = 0;
  public y: number = 0;
  constructor (public paper: Paper) {}
}

/**
 * A link on a graph between two PaperNodes
 */
class CitationLink implements d3.SimulationLinkDatum<PaperNode> {
  constructor (public source: PaperNode, public target: PaperNode)  {}
}

/**
 * Parameters that are passed from the parent to the PaperGraph.
 */
type Props = {
  // A list of papers that should be displayed.
  papers: Paper[];
};

/**
 * The PaperGraph displays a list of papers and their connections.
 * It uses D3 network graphs.
 * See also https://www.d3-graph-gallery.com/network.html
 */
export default class PaperGraph extends Component<Props> {
  private canvas = React.createRef<SVGSVGElement>();

  render() {
    // We will paint on this SVG canvas
    return <svg ref={this.canvas} className="canvas"></svg>;
  }

  componentDidMount() {
    // We got a "Paper" passed from the props.
    // To display a "Paper" on the graph, we need to convert it to a "PaperNode"
    const paperNodes = this.props.papers.map(p => new PaperNode(p));

    // Furthermore, we need to find out which links we want to display between "PaperNodes"
    let citationLinks: CitationLink[] = [];
    for (const p of paperNodes) {
      for (const c of p.paper.citations) {
        // Try to find the paper that is cited (this is super slow for large numbers of papers...)
        const citedPaper = paperNodes.find(n => n.paper.id == c);
        if (citedPaper != undefined) {
          // If the cited paper is available to us, we add a link
          citationLinks.push(new CitationLink(p, citedPaper))
        }
      }
    }

    this.drawGraph(paperNodes, citationLinks);
  }

  /**
   * Actually draws nodes and edges on the screen.
   * @param nodes The nodes that should be drawn.
   * @param links The links/edges between nodes.
   */
  drawGraph(nodes: PaperNode[], links: CitationLink[]) {
    // Initialize canvas
    const svg = d3.select(this.canvas.current);

    // Initialize the links between nodes
    const link = svg
      .selectAll("line")
      .data(links)
      .enter()
      .append("line")
      .style("stroke", "#aaa");

    // Initialize the nodes
    const node = svg
      .selectAll("circle")
      .data(nodes)
      .enter()
      .append("circle")
      .attr("r", 20)
      .style("fill", "#69b3a2");

    var simulation = d3
      .forceSimulation(nodes) // Force algorithm is applied to papers
      .force("link", d3
          .forceLink() // This force provides links between nodes
          .links(links) // and this the list of links
      )
      .force("charge", d3.forceManyBody().strength(-8000)) // This adds repulsion between nodes. Play with the number for the repulsion strength
      .force("center", d3.forceCenter(this.canvas.current!.clientWidth / 2, this.canvas.current!.clientHeight / 2)) // This force attracts nodes to the center of the svg area
      .on("end", ticked);

    // This function is run at each iteration of the force algorithm, updating the nodes position.
    function ticked() {
      link
        .attr("x1", function(d) {
          return d.source.x;
        })
        .attr("y1", function(d) {
          return d.source.y;
        })
        .attr("x2", function(d) {
          return d.target.x;
        })
        .attr("y2", function(d) {
          return d.target.y;
        });

      node
        .attr("cx", function(d) {
          return d.x + 6;
        })
        .attr("cy", function(d) {
          return d.y - 6;
        });
    }
  }
}
