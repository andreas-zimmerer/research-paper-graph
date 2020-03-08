import React, { Component } from 'react';
import * as d3 from 'd3';
import ReactTooltip from 'react-tooltip';
import { Form } from 'react-bootstrap';
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

  private paperNodes: PaperNode[] = [];
  private citationLinks: CitationLink[] = [];

  public render() {
    // We will paint on this SVG canvas
    return (
      <div className="graph">
        <svg ref={this.canvas} className="canvas" />

        <Form className="search-form">
          <Form.Label>Highlight Papers</Form.Label>
          <Form.Control type="text"
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => this.highlightPapers(e.target.value)} />
          <Form.Text className="text-muted">
              Search for papers inside the displayed graph.
          </Form.Text>
        </Form>

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
      for (const r of p.paper.references) {
        // Try to find the paper that is cited (this is super slow for large numbers of papers...)
        const citedPaper = paperNodes.find((n) => n.paper.id === r);
        if (citedPaper !== undefined) {
          // If the cited paper is available to us, we add a link
          citationLinks.push(new CitationLink(p, citedPaper));
        }
      }
    }

    this.paperNodes = paperNodes;
    this.citationLinks = citationLinks;
    this.drawGraph(paperNodes, citationLinks);
  }

  /**
   * Highlights a set of nodes in the graph based on a keyword without altering the graph.
   * @param keyword If the title of a paper contains this keyword (case-insensitive), it will be highlighted.
   */
  private highlightPapers(keyword: string) {
    const pattern = new RegExp(keyword, 'i');

    const canvas = d3.select(this.canvas.current);
    const nodes = canvas.selectAll('.node').data(this.paperNodes);

    nodes.attr('class', (p: PaperNode) => {
      if (this.props.selectedPaper && p.paper.id === this.props.selectedPaper.id) {
        return 'node node-selected';
      }
      if (keyword !== '' && p.paper.title.match(pattern)) {
        return 'node node-highlighted';
      }
      return 'node';
    });
  }

  /**
   * Actually draws nodes and edges on the screen.
   * @param papers The nodes that should be drawn.
   * @param links The links/edges between nodes.
   */
  private drawGraph(papers: PaperNode[], links: CitationLink[]) {
    const width = this.canvas.current!.clientWidth;
    const height = this.canvas.current!.clientHeight;

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
      .range([0, width]);

    // The background of the plot.
    // NOTE: because we only grab the pan&zoom event on the background,
    //       it is NOT possible to pan&zoom on the individual nodes!
    const zoom = d3.zoom<SVGRectElement, unknown>()
      .on('zoom', () => {
        // Pan&Zoom for nodes and edges:
        plot.attr('transform', d3.event.transform);
        // Pan&Zoom for axis and grid:
        const newXScale = d3.event.transform.rescaleX(xAxisScale);
        xAxisGroup.call(xAxis.scale(newXScale));
        gridLinesGroup.call(gridLines.scale(newXScale));
      })
      .scaleExtent([0.2, 3]);  // Limit zoom
    const background = canvas.append('rect')
        .attr('class', 'background')
        .attr('width', width)
        .attr('height', height)
        .call(zoom);

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
      .tickValues(Array.from({length: maxYear - minYear + 1 + 40}, (v, k) => k + minYear - 20))
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
      .attr('class', (l) => (l.source.paper.is_influential || l.target.paper.is_influential) ? 'line influential' : 'line');

    // Initialize the nodes.
    // A node is a "group" (g) consisting of a circle and text.
    const nodes = plot
      .selectAll('.node')
      .data(papers)
      .enter()
      .append('g')
      .attr('class', (p) => (this.props.selectedPaper && p.paper.id === this.props.selectedPaper.id) ? 'node node-selected' : 'node');
    nodes.append('circle')
      .attr('r', 18)
      .attr('class', 'node-circle')
      .attr('data-tip', (d) => d.paper.id)
      .on('click', (d) => this.props.onSelectedPaperChanged(d.paper));
    nodes.append('text')
      .attr('dx', 20)
      .attr('dy', -4)
      .attr('class', 'node-text')
      .text((d) => truncateString(d.paper.title, 20, true));

    const simulation = d3
      .forceSimulation(papers) // Force algorithm is applied to papers
      .force('link', d3
          .forceLink() // This force provides links between nodes
          .links(links) // and this the list of links
      )
      .force('y', d3.forceY<PaperNode>().strength(5).y( (d) => d.paper.cluster * 500 ))
      .force('center', d3.forceCenter().x(width / 2).y(height / 2)) // Attraction to the center of the svg area
      .force('charge', d3.forceManyBody().strength(-5000)) // Nodes are attracted one each other of value is > 0
      .force('collide', d3.forceCollide().strength(5).radius(32).iterations(1))
      .alphaDecay(0.1) // make the simulation converge faster, but less accurate
      .on('tick', ticked); // Force that avoids circle overlapping

    // Fits the graph onto the display pane according to its expansion on x-axis.
    function zoomFit() {
      const currentZoom = d3.zoomTransform(background.node() as Element).k;
      let maxYdist =  -999999;
      let minYdist =   999999;
      nodes.each((n) => {
        if (n.y > maxYdist) {
          maxYdist = n.y;
        }
        if (n.y < minYdist) {
          minYdist = n.y;
        }
      });
      if (!(maxYdist === -999999 || minYdist === 999999)) {
        const scale = height / ((maxYdist - minYdist) * currentZoom);
        background.call(zoom.scaleTo, Math.max(0.5, currentZoom * scale * 0.9));
      }
    }

    // This function is run at each iteration of the force algorithm, updating the nodes position.
    function ticked() {
      // Constrains/fixes x-position
      nodes.each((d) => { d.x = xAxisScale(d.paper.year); });

      edges
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

      nodes
        .attr('transform', (d) => 'translate(' + d.x + ', ' + d.y + ')');

      zoomFit();
    }

    // Make sure to register the new targets for tooltips after graph has been rebuilt.
    ReactTooltip.rebuild();
  }
}
