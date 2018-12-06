import { combineReducers } from 'redux';


const awaitingResponse = (state=false, action) => {
  switch(action.type) {
    case "REGISTER_REQUEST_SUBMITTED":
      return true;
    case "REGISTER_RESPONSE_SUCCESS_RECEIVED":
    case "REGISTER_RESPONSE_ERROR_RECEIVED":
      return false;
    default:
      return state;
  }
}

const successful = (state=false, action) => {
  switch(action.type) {
    case "REGISTER_RESPONSE_SUCCESS_RECEIVED":
      return true;
    case "ROUTE_CHANGED":
    case "REGISTER_RESPONSE_ERROR_RECEIVED":
      return false;
    default:
      return state;
  }
}

const hasErrors = (state=false, action) => {
  switch(action.type) {
    case "REGISTER_RESPONSE_ERROR_RECEIVED":
      return true;
    case "ROUTE_CHANGED":
    case "REGISTER_RESPONSE_SUCCESS_RECEIVED":
      return false;
    default:
      return state;
  }
}

const username = (state='', action) => {
  switch(action.type) {
    case 'REGISTER_USERNAME_UPDATED':
      return action.username;
    case 'ROUTE_CHANGED':
      return '';
    default:
      return state;
  }
}

const email = (state='', action) => {
  switch(action.type) {
    case 'REGISTER_EMAIL_UPDATED':
      return action.username;
    case 'ROUTE_CHANGED':
      return '';
    default:
      return state;
  }
}

const password = (state='', action) => {
  switch(action.type) {
    case 'REGISTER_PASSWORD_UPDATED':
      return action.password;
    case 'ROUTE_CHANGED':
      return '';
    default:
      return state;
  }
}

const usernameErrors = (state=[], action) => {
  switch(action.type) {
    case "REGISTER_RESPONSE_ERROR_RECEIVED":
      return action.data.username ? action.data.username : [];
    case "ROUTE_CHANGED":
    case "REGISTER_RESPONSE_SUCCESS_RECEIVED":
      return [];
    default:
      return state;
  }
}

const emailErrors = (state=[], action) => {
  switch(action.type) {
    case "REGISTER_RESPONSE_ERROR_RECEIVED":
      return action.data.email ? action.data.email : [];
    case "ROUTE_CHANGED":
    case "REGISTER_RESPONSE_SUCCESS_RECEIVED":
      return [];
    default:
      return state;
  }
}

const passwordErrors = (state=[], action) => {
  switch(action.type) {
    case "REGISTER_RESPONSE_ERROR_RECEIVED":
      return action.data.password ? action.data.password : [];
    case "ROUTE_CHANGED":
    case "REGISTER_RESPONSE_SUCCESS_RECEIVED":
      return [];
    default:
      return state;
  }
}

const registration = combineReducers({
  awaitingResponse,
  successful,
  hasErrors,
  username,
  email,
  password,
  usernameErrors,
  emailErrors,
  passwordErrors
});
export default registration;

export const getUsername = (state) => state.username;
export const getEmail = (state) => state.email;
export const getPassword = (state) => state.password;
export const getHasErrors = (state) => state.hasErrors;
export const getIsAwaitingResponse = (state) => state.awaitingResponse;
export const getUsernameErrors = (state) => state.usernameErrors;
export const getEmailErrors = (state) => state.emailErrors;
export const getPasswordErrors = (state) => state.passwordErrors;
export const getIsSuccessful = (state) => state.successful;
