import React, { Component } from 'react';
import { Route, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import * as actions from '../actions';
import { getIsUserAuthenticated } from '../reducers';

export class PrivateRoute extends Component {
  render() {
    if(this.props.isUserAuthenticated) {
      return (<Route {...this.props} />)
    }
    return (<Redirect to='/login' />);
  }
}

const mapStateToProps = (state, props) => {
  return {
    isUserAuthenticated: getIsUserAuthenticated(state),
  }
}

const ConnectedPrivateRoute = connect(
  mapStateToProps,
  actions
)(PrivateRoute);

export default ConnectedPrivateRoute;
