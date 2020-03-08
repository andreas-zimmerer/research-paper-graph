import React, { Component } from 'react';
import { Highlighter } from 'react-bootstrap-typeahead';
import { IPaper } from '../../types/paper';
import './sidebar.css';

interface IProps {
  paper: IPaper;
  searchText?: string;
}

export default class PaperMenuItem extends Component<IProps> {
  public render() {
    return (
      <div>
          <div className="search-title">
            <Highlighter key="title" search={this.props.searchText}>
                {this.props.paper.title}
            </Highlighter>
          </div>
          <div className="search-sub">
            <Highlighter key="subtitle" search={this.props.searchText}>
                {
                  this.props.paper.year +
                  ((this.props.paper.authors) ? ' - ' + this.props.paper.authors.join(', ') : '') + '; ' +
                  'Citations: ' + this.props.paper.citations
                }
            </Highlighter>
          </div>
      </div>
    );
  }
}
