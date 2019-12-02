import React, { Component } from 'react';
import { Form, Nav, Modal } from 'react-bootstrap';
import './sidebar.css';

export default class Sidebar extends Component {
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
