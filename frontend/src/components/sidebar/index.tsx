import React, { Component } from 'react';
import { Form, Nav } from 'react-bootstrap';
import { IPaper } from '../../types/paper';
import './sidebar.css';

interface IProps {
  // A callback function that is invoked, when we get new papers from the backend.
  papersUpdated: ((papers: IPaper[]) => void);
}

interface IState {
  keyword: string;
}

export default class Sidebar extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);

    this.onKeywordChange = this.onKeywordChange.bind(this);

    this.state = {
      keyword: ''
    };

    // Initially fetch a list of papers without any filters.
    fetch('http://localhost:5000/search?keyword=')
      .then((response) => response.json())
      .then((p: IPaper[]) => this.props.papersUpdated(p));
  }

  public render() {
    return (
      <div className="sidebar">
          <Nav>
            <Form.Control type="text" placeholder="Search for a paper"
              value={this.state.keyword}
              onChange={this.onKeywordChange} />
          </Nav>
      </div>
    );
  }

  // Get an updated list of papers from the backend when the keyword changes.
  private onKeywordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const keyword = event.currentTarget.value;
    this.setState({keyword});

    fetch(`http://localhost:5000/search?keyword=${keyword}`)
      .then((response) => response.json())
      .then((p: IPaper[]) => this.props.papersUpdated(p));
  }
}
