import React from 'react'
import { connect } from 'react-redux';
import * as actions from '../actions';
import { helpers } from '../reducers';
import PublicRoute from '../hoc/PublicRoute';
import LoginForm from '../components/LoginForm';

export class Login extends React.Component {
  render() {
		const {
      loginUser,
      loginUsernameChanged,
      loginPasswordChanged,
      error
    } = this.props;
		return (
			<LoginForm
                onLoginButtonClick={loginUser}
                onUsernameChange={loginUsernameChanged}
                onPasswordChange={loginPasswordChanged}
                hasError={error}
            />
		);
	}
};

const mapStateToProps = (state, props) => {
	return {
    error: helpers.getIsLoginError(state)
  }
};

const ConnectedLogin = connect(
	mapStateToProps,
	actions
)(Login);

const PublicRouteLogin = PublicRoute(ConnectedLogin);

export default PublicRouteLogin;
