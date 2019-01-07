import React from 'react'
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import * as actions from '../actions';

class Logout extends React.Component {
  render() {
	  const { logoutUser } = this.props;
    logoutUser();
	  return (<Redirect to='/login' />);
	}
};

const mapStateToProps = (state, props) => {
	return {}
};

const ConnectedLogout = connect(
	mapStateToProps,
	actions
)(Logout);

export default ConnectedLogout;
