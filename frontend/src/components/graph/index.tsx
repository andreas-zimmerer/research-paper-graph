import React, { Component } from 'react';
import * as d3 from 'd3';
import { IPaper } from '../../types/paper';
import CitationLink from './CitationLink';
import PaperNode from './PaperNode';
import './graph.css';

/**
 * Parameters that are passed from the parent to the PaperGraph.
 */
interface IProps {
  // A list of papers that should be displayed.
  papers: IPaper[];
}

/**
 * The PaperGraph displays a list of papers and their connections.
 * It uses D3 network graphs.
 * See also https://www.d3-graph-gallery.com/network.html
 */
export default class PaperGraph extends Component<IProps> {
  private canvas = React.createRef<SVGSVGElement>();

  public render() {
    // We will paint on this SVG canvas
    return <svg ref={this.canvas} className="canvas"></svg>;
  }

  public componentDidMount() {
    // We got a 'Paper' passed from the props.
    // To display a 'Paper' on the graph, we need to convert it to a 'PaperNode'
    const paperNodes = this.props.papers.map((p) => new PaperNode(p));

    // Furthermore, we need to find out which links we want to display between 'PaperNodes'
    const citationLinks: CitationLink[] = [];
    for (const p of paperNodes) {
      for (const c of p.paper.citations) {
        // Try to find the paper that is cited (this is super slow for large numbers of papers...)
        const citedPaper = paperNodes.find((n) => n.paper.id === c);
        if (citedPaper !== undefined) {
          // If the cited paper is available to us, we add a link
          citationLinks.push(new CitationLink(p, citedPaper));
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
  private drawGraph(nodes: PaperNode[], links: CitationLink[]) {
    const width = this.canvas.current!.clientWidth;
    const height = this.canvas.current!.clientHeight;

    // Compute the max and min years so we can adjust the scale
    let minYear = Number.MAX_VALUE;
    let maxYear = Number.MIN_VALUE;
    for (const n of nodes) {
      if (n.paper.year < minYear) {
        minYear = n.paper.year;
      }
      if (n.paper.year > maxYear) {
        maxYear = n.paper.year;
      }
    }

    // Initialize canvas
    const svg = d3.select(this.canvas.current);

    // Initialize the links between nodes
    const link = svg
      .selectAll('.line')
      .data(links)
      .enter()
      .append('line')
      .style('stroke', '#aaa');

    // Initialize the nodes.
    // A node is a "group" (g) consisting of a circle and text.
    const node = svg
      .selectAll('.node')
      .data(nodes)
      .enter()
      .append('g');
    node.append('circle')
      .attr('r', 20)
      .style('fill', '#69b3a2');
    node.append('text')
      .attr('dx', 20)
      .attr('dy', -10)
      .text((d) => d.paper.title);

    const simulation = d3
      .forceSimulation(nodes) // Force algorithm is applied to papers
      .force('link', d3
          .forceLink() // This force provides links between nodes
          .links(links) // and this the list of links
      )
      // This adds repulsion between nodes. Play with the number for the repulsion strength
      .force('charge', d3.forceManyBody().strength(-8000))
      // This force attracts nodes to the center of the svg area
      .force('center', d3.forceCenter(width / 2, height / 2))
      .on('end', ticked);

    // This function is run at each iteration of the force algorithm, updating the nodes position.
    function ticked() {
      // Constrains/fixes x-position
      node.each((d) => { d.x = (d.paper.year - minYear) * width / (maxYear - minYear); });

      link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

      node
        .attr('transform', (d) => 'translate(' + d.x + ', ' + d.y + ')');
    }

    // Create an x-axis with years
    const xAxis = d3.axisBottom(
      d3.scaleLinear()
        .domain([minYear, maxYear])
        .range([0, width]))
      .tickFormat(d3.format('d'));
    svg.append('g')
      .call(xAxis);
  }
}
