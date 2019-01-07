import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import PrivateRoute from './PrivateRoute';
import PublicRoute from './PublicRoute';
import Login from './Login';
import Register from './Register';

class Content extends Component {
  render() {
    return (
      <div className="content">
        <Router>
            <Switch>
              <PrivateRoute path="/" exact component={Home} />
              <PublicRoute path="/login/" component={Login} />
              <PublicRoute path="/register/" component={Register} />
              <Route component={NoPathMatch} />
            </Switch>
        </Router>
      </div>
    );
  }
}
const Home = () => <h2>Home</h2>;
const NoPathMatch = () => <h2>No Match</h2>;



export default Content;
