import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import LoggedInContent from './LoggedInContent';

class Content extends Component {
  render() {
    return (
      <div className="content">
        <Router>
            <Switch>
              <Route path="/login/" component={Login} />
              <Route path="/register/" component={Register} />
              <Route path="/" component={LoggedInContent} />
            </Switch>
        </Router>
      </div>
    );
  }
}

export default Content;
