import React, { Component } from 'react';
import PaperGraph from '../components/graph';
import Sidebar, { IPaperFilter } from '../components/sidebar';
import { IPaper } from '../types/paper';

interface IProps {}

interface IState {
  selectedPaper?: IPaper;
  currentFilter?: IPaperFilter;
  allPapers: IPaper[];
}

export default class PapersPage extends Component<IProps, IState> {
  graph: React.RefObject<PaperGraph>;

  constructor(props: IProps) {
    super(props);
    this.graph = React.createRef();

    this.state = {
      selectedPaper: undefined,
      allPapers: []
    };
  }

  public render() {
    return (
      <div className="page">
        <Sidebar onSelectedPaperChanged={this.handlePaperChanged}
                 onPaperFilterChanged={this.handlePaperFilterChanged}
                 onHighlightKeywordchanged={(k) => this.graph.current?.highlightPapers(k)} />
        <PaperGraph papers={this.state.allPapers}
                    selectedPaper={this.state.selectedPaper}
                    onSelectedPaperChanged={this.handlePaperChanged}
                    ref={this.graph} />
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

  private fetchNewPaper = () => {
    fetch(`http://localhost:5000/family?paper=${encodeURIComponent(this.state.selectedPaper?.title || '')}&distance=${this.state.currentFilter?.maxDistance || 3}&year=${this.state.currentFilter?.minYear || 0}&citations=${this.state.currentFilter?.minCitations || 1}`)
      .then((response) => response.json())
      .then((p: IPaper[]) => this.setState({allPapers: p}));
  }
}
