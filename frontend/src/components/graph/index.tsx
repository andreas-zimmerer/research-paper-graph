import React, { Component } from 'react';
import * as d3 from 'd3';
import ReactTooltip from 'react-tooltip';
import { IPaper } from '../../types/paper';
import CitationLink from './CitationLink';
import PaperNode from './PaperNode';
import PaperTooltip from './PaperTooltip';
import './graph.css';

/**
 * Parameters that are passed from the parent to the PaperGraph.
 */
interface IProps {
  // A list of papers that should be displayed.
  papers: IPaper[];
  // One or none currently selected paper.
  selectedPaper?: IPaper;
  // Callback when a user selects a paper in the graph.
  onSelectedPaperChanged: ((paper: IPaper) => void);
}

/**
 * Truncates a string and appends "…" at the end.
 * Adapted from: https://stackoverflow.com/a/1199420/4777124
 * @param s The string to be truncated.
 * @param length The new length of the string.
 * @param useWordBoundary Whether to only split at word boundaries (might result in an even shorter string).
 */
const truncateString = (s: string, length: number, useWordBoundary: boolean) => {
    if (s.length <= length) { return s; }
    const subString = s.substr(0, length - 1);
    return (useWordBoundary ?
      subString.substr(0, subString.lastIndexOf(' '))
      : subString) + '…';
};

/**
 * The PaperGraph displays a list of papers and their connections.
 * It uses D3 network graphs.
 * See also https://www.d3-graph-gallery.com/network.html
 */
export default class PaperGraph extends Component<IProps> {
  private canvas = React.createRef<SVGSVGElement>();

  public render() {
    // We will paint on this SVG canvas
    return (
      <div className="graph">
        <svg ref={this.canvas} className="canvas" />

        <ReactTooltip clickable={true} getContent={(paperId) => {
          const paper = this.props.papers.find((p) => p.id === paperId);
          return <PaperTooltip paper={paper}/>;
        }}/>
      </div>
    );
  }

  public componentDidUpdate(prevProps: IProps) {
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
   * @param papers The nodes that should be drawn.
   * @param links The links/edges between nodes.
   */
  private drawGraph(papers: PaperNode[], links: CitationLink[]) {
    const width = this.canvas.current!.clientWidth;
    const height = this.canvas.current!.clientHeight;
    const padding = 20;

    // Compute the max and min years so we can adjust the scale
    let minYear = Number.MAX_VALUE;
    let maxYear = Number.MIN_VALUE;
    for (const p of papers) {
      if (p.paper.year < minYear) {
        minYear = p.paper.year;
      }
      if (p.paper.year > maxYear) {
        maxYear = p.paper.year;
      }
    }

    // Initialize canvas
    const canvas = d3.select(this.canvas.current);
    // Remove old elements from canvas
    canvas.selectAll('*').remove();

    // -------------------------------------------
    // Setup plot.
    // -------------------------------------------

    // Define a scale for the x-axis and the grid lines.
    const xAxisScale = d3.scaleLinear()
      .domain([minYear, maxYear])
      .range([padding, width - padding]);

    // The background of the plot.
    // NOTE: because we only grab the pan&zoom event on the background,
    //       it is NOT possible to pan&zoom on the individual nodes!
    const background = canvas.append('rect')
      .attr('class', 'background')
      .attr('width', width)
      .attr('height', height)
      .call(d3.zoom<SVGRectElement, unknown>().on('zoom', () => {
        // Pan&Zoom for nodes and edges:
        plot.attr('transform', d3.event.transform);
        // Pan&Zoom for axis and grid:
        const newXScale = d3.event.transform.rescaleX(xAxisScale);
        xAxisGroup.call(xAxis.scale(newXScale));
        gridLinesGroup.call(gridLines.scale(newXScale));
      }));

    // Create vertical grid lines
    const gridLines = d3.axisBottom(xAxisScale)
      .tickFormat(() => '')
      .tickSize(-height);
    const gridLinesGroup = canvas.append('g')
      .attr('class', 'grid')
      .attr('transform', `translate(0, ${height})`)
      .call(gridLines);

    // Nodes and edges will be drawn on a 'plot' (seperated from axis).
    const plot = canvas.append('g');

    // Create an x-axis with years
    const xAxis = d3.axisBottom(xAxisScale)
      .tickFormat(d3.format('d'));
    const xAxisGroup = canvas.append('g')
      .attr('class', 'axis')
      .call(xAxis);

    // -------------------------------------------
    // Now we need to populate the plot with data.
    // -------------------------------------------

    // Initialize the links between nodes
    const edges = plot
      .selectAll('.line')
      .data(links)
      .enter()
      .append('line')
      .attr('class', 'line');

    // Initialize the nodes.
    // A node is a "group" (g) consisting of a circle and text.
    const nodes = plot
      .selectAll('.node')
      .data(papers)
      .enter()
      .append('g')
      .attr('class', (p) => (this.props.selectedPaper && p.paper.id === this.props.selectedPaper.id) ? 'node-group node-selected' : 'node-group');
    nodes.append('circle')
      .attr('r', 20)
      .attr('class', 'node-circle')
      .attr('data-tip', (d) => d.paper.id)
      .on('click', (d) => this.props.onSelectedPaperChanged(d.paper));
    nodes.append('text')
      .attr('dx', 20)
      .attr('dy', -10)
      .attr('class', 'node-text')
      .text((d) => truncateString(d.paper.title, 20, true));

    const simulation = d3
      .forceSimulation(papers) // Force algorithm is applied to papers
      .force('link', d3
          .forceLink() // This force provides links between nodes
          .links(links) // and this the list of links
      )
      // This adds repulsion between nodes. Play with the number for the repulsion strength
      .force('charge', d3.forceManyBody().strength(-2000))
      // This force attracts nodes to the center of the svg area
      .force('center', d3.forceCenter(width / 2, height / 2))
      .on('tick', ticked);

    // This function is run at each iteration of the force algorithm, updating the nodes position.
    function ticked() {
      // Constrains/fixes x-position
      nodes.each((d) => { d.x = (d.paper.year - minYear) * (width - 2 * padding) / (maxYear - minYear) + padding; });

      edges
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

      nodes
        .attr('transform', (d) => 'translate(' + d.x + ', ' + d.y + ')');
    }

    // Make sure to register the new targets for tooltips after graph has been rebuilt.
    ReactTooltip.rebuild();
  }
}
