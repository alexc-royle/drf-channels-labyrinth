import { combineReducers } from 'redux';
import login, * as fromLogin from './login';
import user, * as fromUser from './user';

const app = combineReducers({
  login,
  user
});
export default app;

export const getIsUserAuthenticated = (state) => fromUser.getIsUserAuthenticated(state.user);
export const getUserToken = (state) => fromUser.getUserToken(state.user);

export const getGivenUsername = (state) => fromLogin.getGivenUsername(state.login);
export const getGivenPassword = (state) => fromLogin.getGivenPassword(state.login);
export const getIsLoginError = (state) => fromLogin.getIsLoginError(state.login);
export const getIsAwaitingLoginResponse = (state) => fromLogin.getIsAwaitingLoginResponse(state.login);

export const helpers = {
  getIsUserAuthenticated,
  getUserToken,
  getGivenUsername,
  getGivenPassword,
  getIsLoginError,
  getIsAwaitingLoginResponse
};
