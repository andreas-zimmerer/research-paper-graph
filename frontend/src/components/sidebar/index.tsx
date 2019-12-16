import React, { Component } from 'react';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';
import { Form } from 'react-bootstrap';
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
        <Form>
          <Form.Group controlId="searchPaper" className="search-form-group">
            <Form.Label>Search for papers:</Form.Label>
            <AsyncTypeahead
              id="searchbar-paper"
              options={this.state.suggestedPapers}
              isLoading={this.state.isSearching}
              filterBy={() => true} // the backend filters for us
              labelKey={(p) => `${p.title} (${p.year})`}
              minLength={1}
              onSearch={this.handleSearch}
              placeholder="Search..."
              onChange={(selected: IPaper[]) => this.props.onSelectedPaperChanged(selected[0])}
              renderMenuItemChildren={(paper: IPaper, props) => (
                <PaperMenuItem key={paper.id} paper={paper} searchText={props.text} />
            )}/>
            <Form.Text className="text-muted">
              Input the title, the DOI or other keywords.
            </Form.Text>
          </Form.Group>

          <Form.Group controlId="displayOptionsPreSucc">
            <Form.Label>Which papers should be displayed:</Form.Label>
            <Form.Check
              type="checkbox"
              id="checkbox-display-preceding-papers"
              label="Preceding papers"
            />
            <Form.Check
              type="checkbox"
              id="checkbox-display-succeeding-papers"
              label="Succeeding papers"
            />
          </Form.Group>

          <Form.Group controlId="displayOptionsDate">
            <Form.Label>Date of the displayed papers:</Form.Label>
            <Form.Control type="range" />
            <Form.Text className="text-muted">
              Minimum year a paper was published.
            </Form.Text>
            <Form.Control type="range" />
            <Form.Text className="text-muted">
              Maximum year a paper was published.
            </Form.Text>
          </Form.Group>
        </Form>
      </div>
    );
  }

  private handleSearch = (query: string) => {
    this.setState({isSearching: true});
    fetch(`http://localhost:5000/paper/search?keyword=${query}`)
      .then((response) => response.json())
      .then((p: IPaper[]) => {
        this.setState({
          isSearching: false,
          suggestedPapers: p
        });
      });
  }
}
