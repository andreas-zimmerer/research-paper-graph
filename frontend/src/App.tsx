import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Navbar, Nav } from 'react-bootstrap';
import { Switch, Route, Link } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';
import PapersPage from './pages/PapersPage';
import AreasPage from './pages/AreasPage';
import ScientistsPage from './pages/ScientistsPage';
import AboutPage from './pages/AboutPage';

const App: React.FC = () => {
  return (
    <div className="App">
      <BrowserRouter>
        <Navbar bg="light" expand="lg">
          <Navbar.Brand as={Link} to="/home">Research Paper Graph</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link as={Link} to="/papers">Papers</Nav.Link>
              <Nav.Link as={Link} to="/areas">Areas</Nav.Link>
              <Nav.Link as={Link} to="/scientists">Scientists</Nav.Link>
            </Nav>
          </Navbar.Collapse>
          <Navbar.Collapse className="justify-content-end">
            <Nav.Link as={Link} to="/about">About</Nav.Link>
          </Navbar.Collapse>
        </Navbar>

        <Switch>
          <Route exact path="/home" component={PapersPage} />
          <Route exact path="/papers" component={PapersPage}/>
          <Route exact path="/areas" component={AreasPage} />
          <Route exact path="/scientists" component={ScientistsPage} />
          <Route exact path="/about" component={AboutPage} />
        </Switch>
      </BrowserRouter>
    </div>
  );
};

export default App;
