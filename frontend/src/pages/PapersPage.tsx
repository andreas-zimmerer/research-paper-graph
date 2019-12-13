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
    }

    // Initially fetch a list of papers without any filters.
    fetch('http://localhost:5000/search?keyword=')
      .then((response) => response.json())
      .then((p: IPaper[]) => this.setState({allPapers: p}));
  }

  public render() {
    return (
      <div className="page">
        <Sidebar onSelectedPaperChanged={(p) => this.setState({selectedPaper: p})}/>
        <PaperGraph papers={this.state.allPapers} />
      </div>
    );
  }
}
