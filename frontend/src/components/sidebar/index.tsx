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
      keyword: ""
    }
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

  onKeywordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const keyword = event.currentTarget.value;
    this.setState({keyword: keyword});

    fetch('http://localhost:5000/search?keyword=' + keyword)
      .then(response => response.json())
      .then((p: IPaper[]) => this.props.papersUpdated(p));
  }
}
