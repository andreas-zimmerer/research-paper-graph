import React, { Component } from 'react';
import PaperGraph from '../components/graph';
import Sidebar from '../components/sidebar';
import { IPaper } from '../types/paper';

interface IProps {}

interface IState {
  selectedPaper?: IPaper;
  allPapers: IPaper[];
}

export default class PapersPage extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);

    this.state = {
      selectedPaper: undefined,
      allPapers: []
    };
  }

  public render() {
    return (
      <div className="page">
        <Sidebar onSelectedPaperChanged={this.handlePaperChanged} />
        <PaperGraph papers={this.state.allPapers}
                    selectedPaper={this.state.selectedPaper}
                    onSelectedPaperChanged={this.handlePaperChanged} />
      </div>
    );
  }

  private handlePaperChanged = (selectedPaper: IPaper) => {
    this.setState({selectedPaper});

    if (selectedPaper === undefined) {
      return;
    }

    // Fetch the family of papers that are connected to this paper
    fetch(`http://localhost:5000/family/${selectedPaper.title}`)
      .then((response) => response.json())
      .then((p: IPaper[]) => this.setState({allPapers: p}));
  }
}
