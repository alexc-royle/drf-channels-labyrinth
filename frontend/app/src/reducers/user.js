import { combineReducers } from 'redux';

const loggedIn = (state = false, action) => {
  switch(action.type) {
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
      return true;
    case "LOGGED_OUT":
      return false;
    case "LOADED_DATA_FROM_LOCAL_STORAGE":
      return action.data.loggedIn;
    default:
      return state;
  }
}

const id = (state='', action) => {
  switch(action.type) {
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
      return action.data.user_id;
    case "LOGGED_OUT":
      return '';
    case "LOADED_DATA_FROM_LOCAL_STORAGE":
      return action.data.id;
    default:
      return state;
  }
}

const token = (state='', action) => {
  switch(action.type) {
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
      return action.data.token;
    case "LOGGED_OUT":
      return '';
    case "LOADED_DATA_FROM_LOCAL_STORAGE":
      return action.data.token;
    default:
      return state;
  }
}

const username = (state='', action) => {
  switch(action.type) {
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
      return action.data.username;
    case "LOGGED_OUT":
      return '';
    case "LOADED_DATA_FROM_LOCAL_STORAGE":
      return action.data.username;
    default:
      return state;
  }
}

const email = (state='', action) => {
  switch(action.type) {
    case "LOGIN_RESPONSE_SUCCESS_RECEIVED":
      return action.data.email;
    case "LOGGED_OUT":
      return '';
    case "LOADED_DATA_FROM_LOCAL_STORAGE":
      return action.data.email;
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
