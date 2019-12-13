import React, { Component } from 'react';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';
import PaperMenuItem from './PaperMenuItem';
import { IPaper } from '../../types/paper';
import './sidebar.css';

interface IProps {
  onSelectedPaperChanged: ((paper: IPaper) => void);
}

interface IState {
  suggestedPapers: IPaper[];
  isSearching: boolean;
}

export default class Sidebar extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);

    this.state = {
      suggestedPapers: [],
      isSearching: false
    };
  }

  public render() {
    return (
      <div className="sidebar">
          <AsyncTypeahead
            options={this.state.suggestedPapers}
            isLoading={this.state.isSearching}
            filterBy={() => true} // the backend filters for us
            labelKey={() => ""} // not needed because there is no frontend filtering
            minLength={1}
            onSearch={this.handleSearch}
            placeholder="Search for a paper..."
            onChange={(selected: IPaper[]) => this.props.onSelectedPaperChanged(selected[0])}
            renderMenuItemChildren={(paper: IPaper, props) => (
              <PaperMenuItem key={paper.id} paper={paper} searchText={props.text} />
          )}
        />
      </div>
    );
  }

  private handleSearch = (query: string) => {
    this.setState({isSearching: true});
    fetch(`http://localhost:5000/search?keyword=${query}`)
      .then((response) => response.json())
      .then((p: IPaper[]) => {
        this.setState({
          isSearching: false,
          suggestedPapers: p
        });
      })
  }
}
