import { combineReducers } from 'redux';
import login, * as fromLogin from './login';
import registration, * as fromRegistration from './register';
import user, * as fromUser from './user';

const app = combineReducers({
  login,
  registration,
  user
});
export default app;

export const getIsUserAuthenticated = (state) => fromUser.getIsUserAuthenticated(state.user);
export const getUserToken = (state) => fromUser.getUserToken(state.user);

export const getLoginUsername = (state) => fromLogin.getUsername(state.login);
export const getLoginPassword = (state) => fromLogin.getPassword(state.login);
export const getIsLoginError = (state) => fromLogin.getIsError(state.login);
export const getIsAwaitingLoginResponse = (state) => fromLogin.getIsAwaitingResponse(state.login);

export const getRegistrationUsername = (state) => fromRegistration.getUsername(state.registration);
export const getRegistrationEmail = (state) => fromRegistration.getEmail(state.registration);
export const getRegistrationPassword = (state) => fromRegistration.getPassword(state.registration);
export const getHasRegistrationErrors = (state) => fromRegistration.getHasErrors(state.registration);
export const getIsAwaitingRegistrationResponse = (state) => fromRegistration.getIsAwaitingResponse(state.registration);
export const getRegistrationUsernameErrors = (state) => fromRegistration.getUsernameErrors(state.registration);
export const getRegistrationEmailErrors = (state) => fromRegistration.getEmailErrors(state.registration);
export const getRegistrationPasswordErrors = (state) => fromRegistration.getPasswordErrors(state.registration);
export const getIsRegistrationSuccessful = (state) => fromRegistration.getIsSuccessful(state.registration);

export const helpers = {
  getIsUserAuthenticated,
  getUserToken,
  getLoginUsername,
  getLoginPassword,
  getIsLoginError,
  getIsAwaitingLoginResponse,
  getRegistrationUsername,
  getRegistrationEmail,
  getRegistrationPassword,
  getHasRegistrationErrors,
  getIsAwaitingRegistrationResponse,
  getRegistrationUsernameErrors,
  getRegistrationEmailErrors,
  getRegistrationPasswordErrors,
  getIsRegistrationSuccessful
};
