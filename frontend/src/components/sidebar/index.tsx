import React, { Component } from 'react';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';
import { Form } from 'react-bootstrap';
import { Range } from 'react-range';
import PaperMenuItem from './PaperMenuItem';
import { IPaper } from '../../types/paper';
import './sidebar.css';

export interface IPaperFilter {
  minYear: number;
  maxDistance: number;
  minCitations: number;
}

interface IProps {
  onSelectedPaperChanged: ((paper: IPaper) => void);
  onPaperFilterChanged: ((filter: IPaperFilter) => void);
}

interface IState {
  suggestedPapers: IPaper[];
  isSearching: boolean;

  yearSliderValues: number[];
  distanceSliderValues: number[];
  citationSliderValues: number[];

  currentFilter?: IPaperFilter;
}

export default class Sidebar extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);

    this.state = {
      suggestedPapers: [],
      isSearching: false,

      yearSliderValues: [2010],
      distanceSliderValues: [3],
      citationSliderValues: [1],

      currentFilter: undefined
    };

    this.handleFitlerUpdate();
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

          <Form.Group controlId="displayOptionsDate">
            <Form.Label>Show only papers recent papers:</Form.Label>
            <Range
              step={1}
              min={1900}
              max={new Date().getFullYear()}
              values={this.state.yearSliderValues}
              onChange={(values: number[]) => this.setState({yearSliderValues: values})}
              onFinalChange={(values: number[]) => this.handleFitlerUpdate()}
              renderTrack={({props, children}) => this.renderSliderTrack(props, children)}
              renderThumb={({props, isDragged}) =>
                this.renderSliderThumb(props, isDragged, this.state.yearSliderValues[0].toFixed(0))} />
            <Form.Text className="text-muted">
              Minimum year a paper was published.
              Helps to show only recent papers.
            </Form.Text>
          </Form.Group>

          <Form.Group controlId="displayOptionsDistance">
            <Form.Label>Limit the distance inside the graph:</Form.Label>
            <Range
              step={1}
              min={0}
              max={5}
              values={this.state.distanceSliderValues}
              onChange={(values: number[]) => this.setState({distanceSliderValues: values})}
              onFinalChange={(values: number[]) => this.handleFitlerUpdate()}
              renderTrack={({props, children}) => this.renderSliderTrack(props, children)}
              renderThumb={({props, isDragged}) =>
                this.renderSliderThumb(props, isDragged, this.state.distanceSliderValues[0].toFixed(0))} />
            <Form.Text className="text-muted">
              Maximum distance (indirect citations) a paper should have to be displayed.
              Helps to filter out irrelevant papers.
            </Form.Text>
          </Form.Group>

          <Form.Group controlId="displayOptionsCitations">
            <Form.Label>Display only papers with a certain number of citations:</Form.Label>
            <Range
              step={1}
              min={0}
              max={500}
              values={this.state.citationSliderValues}
              onChange={(values: number[]) => this.setState({citationSliderValues: values})}
              onFinalChange={(values: number[]) => this.handleFitlerUpdate()}
              renderTrack={({props, children}) => this.renderSliderTrack(props, children)}
              renderThumb={({props, isDragged}) =>
                this.renderSliderThumb(props, isDragged, this.state.citationSliderValues[0].toFixed(0))} />
            <Form.Text className="text-muted">
              Minimum number of citations a paper must have to be displayed.
              Helps to filter out unimportant papers.
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
            <Form.Text className="text-muted">
              Does not work yet.
            </Form.Text>
          </Form.Group>
        </Form>
      </div>
    );
  }

  private renderSliderTrack = (props: any, children: React.ReactNode) => {
    return (
      <div className="slider"
        onMouseDown={props.onMouseDown}
        onTouchStart={props.onTouchStart}
        style={props.style}>
        <div className="track" ref={props.ref}>
          {children}
        </div>
      </div>
    );
  }

  private renderSliderThumb = (props: any, isDragged: boolean, text: string) => {
    return (
      <div className="thumb" {...props} style={props.style}>
        <div className="thumb-label">
          {text}
        </div>
        <div className="thumb-inner"
          style={{
            backgroundColor: isDragged ? '#548BF4' : '#CCC'
          }} />
      </div>
    );
  }

  private handleFitlerUpdate = () => {
    const filter: IPaperFilter = {
      minYear: this.state.yearSliderValues[0],
      maxDistance: this.state.distanceSliderValues[0],
      minCitations: this.state.citationSliderValues[0]
    };
    this.props.onPaperFilterChanged(filter);
  }

  private handleSearch = (query: string) => {
    this.setState({isSearching: true});
    fetch(`${process.env.REACT_APP_BACKEND_URL}/paper/search/${query}`)
      .then((response) => response.json())
      .then((p: IPaper[]) => {
        this.setState({
          isSearching: false,
          suggestedPapers: p
        });
      });
  }
}
