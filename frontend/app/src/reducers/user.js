import { combineReducers } from 'redux';

const loggedIn = (state = false, action) => {
  switch(action.type) {
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
      return true;
    case "LOGGED_OUT":
      return false;
    case "LOCAL_STORAGE_USER_DATA_LOAD_RESPONSE_SUCCESS_RECEIVED":
      return action.payload.loggedIn;
    default:
      return state;
  }
}

const id = (state='', action) => {
  switch(action.type) {
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
      return action.payload.user_id;
    case "LOGGED_OUT":
      return '';
    case "LOCAL_STORAGE_USER_DATA_LOAD_RESPONSE_SUCCESS_RECEIVED":
      return action.payload.id;
    default:
      return state;
  }
}

const token = (state='', action) => {
  switch(action.type) {
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
      return action.payload.token;
    case "LOGGED_OUT":
      return '';
    case "LOCAL_STORAGE_USER_DATA_LOAD_RESPONSE_SUCCESS_RECEIVED":
      return action.payload.token;
    default:
      return state;
  }
}

const username = (state='', action) => {
  switch(action.type) {
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
      return action.payload.username;
    case "LOGGED_OUT":
      return '';
    case "LOCAL_STORAGE_USER_DATA_LOAD_RESPONSE_SUCCESS_RECEIVED":
      return action.payload.username;
    default:
      return state;
  }
}

const email = (state='', action) => {
  switch(action.type) {
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
      return action.payload.email;
    case "LOGGED_OUT":
      return '';
    case "LOCAL_STORAGE_USER_DATA_LOAD_RESPONSE_SUCCESS_RECEIVED":
      return action.payload.email;
    default:
      return state;
  }
}

const user = combineReducers({
  loggedIn,
  id,
  token,
  username,
  email
});
export default user;

export const getIsUserAuthenticated = (state) => state.loggedIn;
export const getUserToken = (state) => state.token;
