import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import * as actions from '../actions';
import { getIsUserAuthenticated } from '../reducers';

const mapStateToProps = (state, props) => {
  return {
    isUserAuthenticated: getIsUserAuthenticated(state),
  }
}

const PublicRoute = (WrappedComponent) => {
    const innerClass = class extends Component {
        render() {
            const { isUserAuthenticated } = this.props;
            if (isUserAuthenticated) {
                return (<Redirect to='/' />);
            }
            return <WrappedComponent {...this.props} />;
        }
    }
    return connect(
        mapStateToProps,
        actions
    )(innerClass);
}

export default PublicRoute;
