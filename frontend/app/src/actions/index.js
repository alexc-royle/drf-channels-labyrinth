import { helpers } from '../reducers';

export const loginUser = (event) => (dispatch, getState) => {
  const state = getState();
  const alreadySubmitted = helpers.getIsAwaitingLoginResponse(state);
  if(!alreadySubmitted) {
    dispatch({
      type: 'API_REQUEST',
      types: ['LOGIN_REQUEST_SUBMITTED', '', 'LOGIN_RESPONSE_ERROR_RECEIVED'],
      requests: [{
        url: 'user/authenticate',
        body: {
          username: helpers.getLoginUsername(state),
          password: helpers.getLoginPassword(state)
        },
        onSuccess: 'LOGIN_RESPONSE_SUCCESS_RECEIVED',
        method: 'post'
      }]
    });
  }
}

export const loadUserDataFromLocalStorage = () => {
  return {
    type: 'LOCAL_STORAGE_REQUEST',
    method: 'get',
    id: 'user',
    data: undefined,
    onSuccess: 'LOCAL_STORAGE_USER_DATA_LOAD_RESPONSE_SUCCESS_RECEIVED',
    onAttempt: 'LOCAL_STORAGE_USER_DATA_LOAD_ATTEMPTED'
  }
}

export const saveUserDataToLocalStorage = () => (dispatch, getState) => {
  dispatch({
    type: 'LOCAL_STORAGE_REQUEST',
    method: 'set',
    id: 'user',
    data: getState().user,
    onSuccess: 'LOCAL_STORAGE_USER_DATA_SAVE_RESPONSE_SUCCESS_RECEIVED',
    onAttempt: 'LOCAL_STORAGE_USER_DATA_SAVE_ATTEMPTED'
  });
}

export const loginUsernameChanged = (event) => {
  return {
    type: 'LOGIN_USERNAME_UPDATED',
    username: event.target.value
  }
}
export const loginPasswordChanged = (event) => {
  return {
    type: 'LOGIN_PASSWORD_UPDATED',
    password: event.target.value
  }
}

export const logoutUser = () => {
  return {
    type: 'LOGGED_OUT'
  };
}

export const registerUser = (event) => (dispatch, getState) => {
  const state = getState();
  const alreadySubmitted = helpers.getIsAwaitingRegistrationResponse(state);
  if(!alreadySubmitted) {
    dispatch({
      type: 'API_REQUEST',
      types: ['REGISTER_REQUEST_SUBMITTED', '', 'REGISTER_RESPONSE_ERROR_RECEIVED'],
      requests: [{
        url: 'user/create',
        body: {
          username: helpers.getRegistrationUsername(state),
          email: helpers.getRegistrationEmail(state),
          password: helpers.getRegistrationPassword(state)
        },
        onSuccess: 'REGISTER_RESPONSE_SUCCESS_RECEIVED',
        method: 'post'
      }]
    });
  }
}

export const registerUsernameChanged = (event) => {
  return {
    type: 'REGISTER_USERNAME_UPDATED',
    username: event.target.value
  }
}
export const registerEmailChanged = (event) => {
  return {
    type: 'REGISTER_EMAIL_UPDATED',
    username: event.target.value
  }
}
export const registerPasswordChanged = (event) => {
  return {
    type: 'REGISTER_PASSWORD_UPDATED',
    password: event.target.value
  }
}
