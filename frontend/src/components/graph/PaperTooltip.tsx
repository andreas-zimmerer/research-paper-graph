import React, { Component } from 'react';
import { IPaper } from '../../types/paper';
import './graph.css';

interface IProps {
  paper?: IPaper;
}

export default class PaperTooltip extends Component<IProps> {
  public render() {
    if (this.props.paper === undefined) {
        return null;
    }
    return (
      <div className="paper-tooltip">
        <div className="title">
          {this.props.paper.title}
        </div>
        <div className="authors">
          {this.props.paper.authors.join(', ') + ` (${this.props.paper.year})`}
        </div>
        <div className="citations">
          Citations: {this.props.paper.citations}
        </div>
        <div className="abstract">
          <div className="subtitle">Abstract:</div>
          {this.props.paper.abstract}
        </div>
      </div>
    );
  }
}
