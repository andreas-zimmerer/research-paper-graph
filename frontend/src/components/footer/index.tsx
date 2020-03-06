import React, { Component } from 'react';
import './footer.css';

interface IProps {
  graph_layout_time: number;
  network_time: number;
  query_time: number;
  clustering_time: number;
}

export default class Footer extends Component<IProps> {
  constructor(props: IProps) {
    super(props);
  }

  public render() {
    return (
      <div className="footer">
        <span>Query: {this.props.query_time} ms</span>
        <span>Clustering: {this.props.clustering_time} ms</span>
        <span>Network Overhead: {this.props.network_time} ms</span>
        <span>Graph Layout: {this.props.graph_layout_time} ms</span>
      </div>
    );
  }
}
