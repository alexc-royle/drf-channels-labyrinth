import { combineReducers } from 'redux';


const awaitingResponse = (state=false, action) => {
  switch(action.type) {
    case "LOGIN_REQUEST_SUBMITTED":
      return true;
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
    case "LOGIN_RESPONSE_ERROR_RECEIVED":
      return false;
    default:
      return state;
  }
}

const error = (state=false, action) => {
  switch(action.type) {
    case "LOGIN_RESPONSE_ERROR_RECEIVED":
      return true;
    case "ROUTE_CHANGED":
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
      return false;
    default:
      return state;
  }
}

const username = (state='', action) => {
  switch(action.type) {
    case 'LOGIN_USERNAME_UPDATED':
      return action.username;
    case 'ROUTE_CHANGED':
      return '';
    default:
      return state;
  }
}

const password = (state='', action) => {
  switch(action.type) {
    case 'LOGIN_PASSWORD_UPDATED':
      return action.password;
    case 'ROUTE_CHANGED':
      return '';
    default:
      return state;
  }
}

const login = combineReducers({
  awaitingResponse,
  error,
  username,
  password
});
export default login;

export const getUsername = (state) => state.username;
export const getPassword = (state) => state.password;
export const getIsError = (state) => state.error;
export const getIsAwaitingResponse = (state) => state.awaitingResponse;
