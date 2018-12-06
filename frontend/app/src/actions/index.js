import { helpers } from '../reducers';

export const loginUser = (event) => (dispatch, getState) => {
  const state = getState();
  const alreadySubmitted = helpers.getIsAwaitingLoginResponse(state);
  if(!alreadySubmitted) {
    dispatch({
      type: 'LOGIN_REQUEST_SUBMITTED'
    });
    dispatch({
      type: 'API_REQUEST',
      body: {
        username: helpers.getLoginUsername(state),
        password: helpers.getLoginPassword(state)
      },
      url: 'user/authenticate',
      callback: (error, data) => {
        if (error) {
          dispatch({
            type: 'LOGIN_RESPONSE_ERROR_RECEIVED',
            error
          })
        } else {
          dispatch({
            type: 'LOGIN_RESPONSE_SUCCESS_RECEIVED',
            data
          });
          dispatch({
            type: 'SAVE_DATA_TO_LOCAL_STORAGE',
            data: getState().user
          })
        }
      }
    });
  }
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

export const logoutUser = () => (dispatch, getState) => {
  dispatch({ type: 'LOGGED_OUT' });
  dispatch({
    type: 'SAVE_DATA_TO_LOCAL_STORAGE',
    data: getState().user
  });
}

export const registerUser = (event) => (dispatch, getState) => {
  const state = getState();
  const alreadySubmitted = helpers.getIsAwaitingRegistrationResponse(state);
  if(!alreadySubmitted) {
    dispatch({
      type: 'REGISTER_REQUEST_SUBMITTED'
    });
    dispatch({
      type: 'API_REQUEST',
      body: {
        username: helpers.getRegistrationUsername(state),
        email: helpers.getRegistrationEmail(state),
        password: helpers.getRegistrationPassword(state)
      },
      url: 'user/create',
      callback: (error, data) => {
        if (error) {
          dispatch({
            type: 'REGISTER_RESPONSE_ERROR_RECEIVED',
            data: error.data
          })
        } else {
          dispatch({
            type: 'REGISTER_RESPONSE_SUCCESS_RECEIVED',
            data
          });
        }
      }
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
