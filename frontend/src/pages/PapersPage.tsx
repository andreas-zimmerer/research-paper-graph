import React, { Component } from 'react';
import PaperGraph from '../components/graph';
import Sidebar from '../components/sidebar';
import { IPaper } from '../types/paper';

export default class PapersPage extends Component {
  public render() {
    const papers: IPaper[] = [
      {
        id: 1,
        title: 'Of Mice and Men',
        authors: ['Dagobert', 'Donald'],
        abstract: 'A long time ago, in a galaxy far, far away...',
        year: 2019,
        citations: [2, 3]
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
      }
    ];

    return (
      <div className="page">
        <Sidebar />
        <PaperGraph papers={papers} />
      </div>
    );
  }
}
