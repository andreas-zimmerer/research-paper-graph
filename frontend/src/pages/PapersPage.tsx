import React, { Component } from 'react';
import PaperGraph from '../components/graph';
import Sidebar from '../components/sidebar';
import { IPaper } from '../types/paper';

interface IProps {
}

interface IState {
  papers: IPaper[];
}

export default class PapersPage extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);
    this.state = {
      papers: []
    };
  }

  public render() {
    return (
      <div className="page">
        <Sidebar papersUpdated={(p) => this.setState({papers: p})}/>
        <PaperGraph papers={this.state.papers} />
      </div>
    );
  }
}
