import { IPaper } from '../../types/paper';

/**
 * A node on the graph representing a paper.
 * Also contains a reference to the original paper.
 */
export default class PaperNode implements d3.SimulationNodeDatum {
  public x: number = 0;
  public y: number = 0;
  constructor(public paper: IPaper) {}
}
