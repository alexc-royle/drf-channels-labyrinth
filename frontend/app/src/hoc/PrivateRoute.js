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

const PrivateRoute = (WrappedComponent) => {
    const innerClass = class extends Component {
        render() {
            const { isUserAuthenticated } = this.props;
            if (isUserAuthenticated) {
                console.log('private route', 'component');
                return <WrappedComponent {...this.props} />;
            }
            console.log('private route', 'redirecting');
            return (<Redirect to='/login' />);
        }
    }
    return connect(
        mapStateToProps,
        actions
    )(innerClass);
}

export default PrivateRoute;
