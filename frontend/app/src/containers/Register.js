import React from 'react'
import { connect } from 'react-redux';
import * as actions from '../actions';
import { helpers } from '../reducers';
import RegistrationForm from '../components/RegistrationForm';
import RegistrationSuccess from '../components/RegistrationSuccess';

class Register extends React.Component {
  render() {
		const {
      successfulRegistration,
      registerUser,
      registerUsernameChanged,
      registerEmailChanged,
      registerPasswordChanged,
      usernameErrors,
      emailErrors,
      passwordErrors
    } = this.props;
    if (!successfulRegistration) {
      return (
  			<RegistrationForm
          onRegisterButtonClick={registerUser}
          onUsernameChange={registerUsernameChanged}
          onEmailChange={registerEmailChanged}
          onPasswordChange={registerPasswordChanged}
          usernameErrors={usernameErrors}
          emailErrors={emailErrors}
          passwordErrors={passwordErrors}
        />
  		);
    }
		return (
      <RegistrationSuccess />
    )
	}
};

const mapStateToProps = (state, props) => {
	return {
    usernameErrors: helpers.getRegistrationUsernameErrors(state),
    emailErrors: helpers.getRegistrationEmailErrors(state),
    passwordErrors: helpers.getRegistrationPasswordErrors(state),
    successfulRegistration: helpers.getIsRegistrationSuccessful(state)
  }
};

const ConnectedRegister = connect(
	mapStateToProps,
	actions
)(Register);

export default ConnectedRegister;
