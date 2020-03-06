import React, { Component } from 'react';
import PaperGraph from '../components/graph';
import Sidebar, { IPaperFilter } from '../components/sidebar';
import Footer from '../components/footer';
import { IPaper } from '../types/paper';

interface IProps {}

interface IState {
  selectedPaper?: IPaper;
  currentFilter?: IPaperFilter;
  allPapers: IPaper[];

  graph_layout_time: number;
  network_time: number;
  query_time: number;
  clustering_time: number;
}

export default class PapersPage extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);

    this.state = {
      selectedPaper: undefined,
      allPapers: [],

      graph_layout_time: 0,
      network_time: 0,
      query_time: 0,
      clustering_time: 0
    };
  }

  public render() {
    return (
      <div className="page">
        <Sidebar onSelectedPaperChanged={this.handlePaperChanged}
                 onPaperFilterChanged={this.handlePaperFilterChanged} />
        <PaperGraph papers={this.state.allPapers}
                    selectedPaper={this.state.selectedPaper}
                    onSelectedPaperChanged={this.handlePaperChanged}
                    onGraphLayoutEnd={(d) => this.setState({graph_layout_time: d})} />
        <Footer query_time={this.state.query_time}
                clustering_time={this.state.clustering_time}
                network_time={this.state.network_time}
                graph_layout_time={this.state.graph_layout_time} />
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
    const timeStart = performance.now();
    fetch(`http://localhost:5000/family?paper=${encodeURIComponent(this.state.selectedPaper?.title || '')}&distance=${this.state.currentFilter?.maxDistance || 3}&year=${this.state.currentFilter?.minYear || 0}&citations=${this.state.currentFilter?.minCitations || 1}`)
      .then((response) => response.json())
      .then((p: IPaper[]) => this.setState({
        allPapers: p,
        network_time: performance.now() - timeStart
      }));
  }
}
