import React, { Component } from 'react';
import { Form, Nav, Modal } from 'react-bootstrap';
import { IPaper } from '../../types/paper';
import './sidebar.css';

interface IProps {
  // A callback function that is invoked, when we get new papers from the backend.
  papersUpdated: ((papers: IPaper[]) => void);
}

export default class Sidebar extends Component<IProps> {
  constructor(props: IProps) {
    super(props);
    this.props.papersUpdated(papers);
  }
  public render() {
    return (
      <div className="sidebar">
          <Nav>
            <Form.Control type="text" placeholder="Search for a paper" />
          </Nav>
      </div>
    );
  }
}
