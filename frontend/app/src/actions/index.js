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
        username: helpers.getGivenUsername(state),
        password: helpers.getGivenPassword(state)
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
