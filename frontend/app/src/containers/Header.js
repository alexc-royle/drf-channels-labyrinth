import React, { Component } from 'react';
import { connect } from 'react-redux';
import NotLoggedInHeader from '../components/NotLoggedInHeader';
import LoggedInHeader from '../components/LoggedInHeader';
import { getIsUserAuthenticated } from '../reducers';
import * as actions from '../actions';

class Header extends Component {
  render() {
    if(this.props.isUserAuthenticated) {
      return (
        <div className="header"><LoggedInHeader /></div>
      );
    }
    return (
      <div className="header"><NotLoggedInHeader /></div>
    );
  }
}

const mapStateToProps = (state, props) => {
  return {
    isUserAuthenticated: getIsUserAuthenticated(state),
  }
}

const ConnectedHeader = connect(
  mapStateToProps,
  actions
)(Header);

export default ConnectedHeader;
