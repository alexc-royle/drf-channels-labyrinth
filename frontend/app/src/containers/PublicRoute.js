import React, { Component } from 'react';
import { Route, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import * as actions from '../actions';
import { getIsUserAuthenticated } from '../reducers';

export class PublicRoute extends Component {
  render() {
    if(this.props.isUserAuthenticated) {
      return (<Redirect to='/' />);
    }
    return (<Route {...this.props} />);
  }
}

const mapStateToProps = (state, props) => {
  return {
    isUserAuthenticated: getIsUserAuthenticated(state),
  }
}

const ConnectedPublicRoute = connect(
  mapStateToProps,
  actions
)(PublicRoute);

export default ConnectedPublicRoute;
