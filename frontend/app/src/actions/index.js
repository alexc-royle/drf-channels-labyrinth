import fetchData from '../api';
import { helpers } from '../reducers';

export const loginUser = (event) => (dispatch, getState) => {
  const state = getState();
  const alreadySubmitted = helpers.getIsAwaitingLoginResponse(state);
  if(!alreadySubmitted) {
    dispatch({
      type: 'LOGIN_REQUEST_SUBMITTED'
    });

    const userToken = helpers.getUserToken(state);

    const body = {
      username: helpers.getGivenUsername(state),
      password: helpers.getGivenPassword(state)
    }

    fetchData('http://localhost:8080/api/v1/user/authenticate', body, userToken, (error, data) => {
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
