import React, { Component } from 'react';
import PaperGraph from '../components/graph';
import Sidebar, { IPaperFilter, GraphContent } from '../components/sidebar';
import { IPaper } from '../types/paper';

interface IProps {}

interface IState {
  selectedPaper?: IPaper;
  currentFilter?: IPaperFilter;
  allPapers: IPaper[];
  graphContent: GraphContent;
}

export default class PapersPage extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);

    this.state = {
      selectedPaper: undefined,
      allPapers: [],
      graphContent: GraphContent.PRECEDING
    };
  }

  public render() {
    return (
      <div className="page">
        <Sidebar onSelectedPaperChanged={this.handlePaperChanged}
                 onPaperFilterChanged={this.handlePaperFilterChanged}
                 onGraphContentChanged={this.handleGraphContentChanged} />
        <PaperGraph papers={this.state.allPapers}
                    selectedPaper={this.state.selectedPaper}
                    onSelectedPaperChanged={this.handlePaperChanged} />
      </div>
    );
  }

  private handlePaperChanged = (selectedPaper: IPaper) => {
    this.setState({selectedPaper}, () => {
      if (selectedPaper === undefined) {
        return;
      }
      this.fetchNewPaper();
    });
  }

  private handlePaperFilterChanged = (filter: IPaperFilter) => {
    this.setState({currentFilter: filter}, () => {
      if (filter === undefined) {
        return;
      }
      this.fetchNewPaper();
    });
  }

  private handleGraphContentChanged = (content: GraphContent) => {
    this.setState({graphContent: content}, () => {
      this.fetchNewPaper();
    });
  }

  private fetchNewPaper = () => {
    const graphContent = this.state.graphContent.toLowerCase();
    fetch(`http://localhost:5000/family/${graphContent}/?paper=${encodeURIComponent(this.state.selectedPaper?.title || '')}&distance=${this.state.currentFilter?.maxDistance || 3}&year=${this.state.currentFilter?.minYear || 0}&citations=${this.state.currentFilter?.minCitations || 1}`)
      .then((response) => response.json())
      .then((p: IPaper[]) => this.setState({allPapers: p}));
  }
}
