import PaperNode from './PaperNode';

/**
 * A link on a graph between two PaperNodes
 */
export default class CitationLink implements d3.SimulationLinkDatum<PaperNode> {
  constructor(public source: PaperNode, public target: PaperNode) {}
}
