import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';
import LoginForm from '../containers/LoginForm';
class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Switch>
            <PrivateRoute path="/" exact component={Home} />
            <Route path="/login/" component={Login} />
            <Route path="/register/" component={Register} />
            <Route component={NoPathMatch} />
          </Switch>
          <LoginForm />
        </div>
      </Router>
    );
  }
}
const Home = () => <h2>Home</h2>;
const Login = () => <h2>Login</h2>;
const Register = () => <h2>Register</h2>;
const NoPathMatch = () => <h2>No Match</h2>;

const PrivateRoute = ({ component: Component, ...rest}) => (
  <Route {...rest} render={(props) => (
    false === true ? <Component {...props} /> : <Redirect to='/login' />
  )} />
);

export default App;
