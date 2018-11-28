import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import PrivateRoute from '../containers/PrivateRoute';
import PublicRoute from '../containers/PublicRoute';
import Login from '../containers/Login';
import Logout from '../containers/Logout';
class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Switch>
            <PrivateRoute path="/" exact component={Home} />
            <PrivateRoute path="/logout" exact component={Logout} />
            <PublicRoute path="/login/" component={Login} />
            <PublicRoute path="/register/" component={Register} />
            <Route component={NoPathMatch} />
          </Switch>
        </div>
      </Router>
    );
  }
}
const Home = () => <h2>Home</h2>;
const Register = () => <h2>Register</h2>;
const NoPathMatch = () => <h2>No Match</h2>;



export default App;
