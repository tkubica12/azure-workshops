import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import Books from './Books';
import Reviews from './Reviews';
import Lists from './Lists';
import { Navbar, Nav } from 'react-bootstrap';
import { ApplicationInsights } from '@microsoft/applicationinsights-web';

console.log('Application Insights Connection String:', window.REACT_APP_APPLICATION_INSIGHTS_CONNECTION_STRING);
console.log('test');

const appInsights = new ApplicationInsights({ config: {
  connectionString: window.REACT_APP_APPLICATION_INSIGHTS_CONNECTION_STRING
  /* ...Other Configuration Options... */
} });
appInsights.loadAppInsights();
appInsights.trackPageView(); // Manually call trackPageView to establish the current user/session/pageview

const App = () => {
  return (
    <Router>
      <Navbar bg="dark" variant="dark" expand="lg">
        <Navbar.Brand href="/">BookApp</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/books">Books</Nav.Link>
            <Nav.Link as={Link} to="/reviews">Reviews</Nav.Link>
            <Nav.Link as={Link} to="/lists">Lists</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      <div className="container mt-4">
        <Switch>
          <Route exact path="/books" component={Books} />
          <Route exact path="/reviews" component={Reviews} />
          <Route exact path="/lists" component={Lists} />
          <Route exact path="/" component={Books} /> {/* Redirect to Books as main page */}
        </Switch>
      </div>
    </Router>
  );
};

export default App;
