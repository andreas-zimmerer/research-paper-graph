import React, { Component } from 'react';
import { Form, Nav, Modal } from 'react-bootstrap';
import { IPaper } from '../../types/paper';
import './sidebar.css';

const papers: IPaper[] = [
  {
    id: 1,
    title: 'Of Mice and Men',
    authors: ['Dagobert', 'Donald'],
    abstract: 'A long time ago, in a galaxy far, far away...',
    year: 2019,
    citations: [2, 3, 4]
  },
  {
    id: 2,
    title: 'A long story...',
    authors: ['Fred'],
    abstract: 'So here it began.',
    year: 2015,
    citations: []
  },
  {
    id: 3,
    title: 'Cinderella',
    authors: ['Disney'],
    abstract: 'wish, dress, prince, kiss',
    year: 2005,
    citations: [4]
  },
  {
    id: 4,
    title: 'FooBar',
    authors: ['Google'],
    abstract: 'A Foo walks into a Bar...',
    year: 2012,
    citations: [4]
  }
];


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
