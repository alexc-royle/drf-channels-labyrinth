import { normalize } from 'normalizr';
import * as schema from './schema';
import { helpers } from '../reducers';

export const loginUser = () => (dispatch, getState) => {
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

export const registerUser = () => (dispatch, getState) => {
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

export const getGamesList = () => (dispatch, getState) => {
    const state = getState();
    const userToken = helpers.getUserToken(state);
    dispatch({
      type: 'API_REQUEST',
      types: ['GAMES_LIST_REQUEST_SUBMITTED', '', 'GAMES_LIST_RESPONSE_ERROR_RECEIVED'],
      requests: [{
        url: 'game',
        userToken,
        onSuccess: (data) => {
          console.log(data);
            dispatch({
              type: 'GAMES_LIST_RESPONSE_RECEIVED',
              response: normalize(data, schema.gamesPaginationSchema)
            })
        },
        method: 'get'
      }]
    });
}

export const requestGame = (gameId) => (dispatch, getState) => {
    const state = getState();
    const userToken = helpers.getUserToken(state);
    dispatch({
      type: 'API_REQUEST',
      types: ['GAME_REQUEST_SUBMITTED', '', 'GAME_RESPONSE_ERROR_RECEIVED'],
      requests: [{
        url: `game/${gameId}/`,
        userToken,
        onSuccess: (data) => {
          dispatch({
            type: 'GAME_RESPONSE_RECEIVED',
            response: normalize(data, schema.gameSchema)
          })
        },
        method: 'get'
      }]
    });
}

export const requestGamePieces = (gameId) => (dispatch, getState) => {
  const state = getState();
  const userToken = helpers.getUserToken(state);
  dispatch({
    type: 'API_REQUEST',
    types: ['GAME_PIECES_REQUEST_SUBMITTED', '', 'GAME_PIECES_RESPONSE_ERROR_RECEIVED'],
    requests: [{
      url: `game/${gameId}/pieces`,
      userToken,
      onSuccess: (data) => {
        dispatch({
          type: 'GAME_PIECES_RESPONSE_RECEIVED',
          response: normalize(data, [schema.gamePieceSchema]),
          gameId
        })
      },
      method: 'get'
    }]
  });
}

export const requestGamePlayers = (gameId) => (dispatch, getState) => {
  const state = getState();
  const userToken = helpers.getUserToken(state);
  dispatch({
    type: 'API_REQUEST',
    types: ['GAME_PLAYER_REQUEST_SUBMITTED', '', 'GAME_PLAYER_RESPONSE_ERROR_RECEIVED'],
    requests: [{
      url: `game/${gameId}/player`,
      userToken,
      onSuccess: (data) => {
        dispatch({
          type: 'GAME_PLAYER_RESPONSE_RECEIVED',
          response: normalize(data, [schema.playerSchema]),
          gameId
        })
      },
      method: 'get'
    }]
  });
}

export const requestGameCollectableItems = (gameId) => (dispatch, getState) => {
  const state = getState();
  const userToken = helpers.getUserToken(state);
  dispatch({
    type: 'API_REQUEST',
    types: ['GAME_COLLECTABLE_ITEMS_REQUEST_SUBMITTED', '', 'GAME_COLLECTABLE_ITEMS_RESPONSE_ERROR_RECEIVED'],
    requests: [{
      url: `game/${gameId}/collectableitems`,
      userToken,
      onSuccess: (data) => {
        dispatch({
          type: 'GAME_COLLECTABLE_ITEMS_RESPONSE_RECEIVED',
          response: normalize(data, [schema.collectableItemSchema]),
          gameId
        })
      },
      method: 'get'
    }]
  });
}

export const requestOrientations = () => (dispatch, getState) => {
  const state = getState();
  const userToken = helpers.getUserToken(state);
  dispatch({
    type: 'API_REQUEST',
    types: ['ORIENTATION_REQUEST_SUBMITTED', '', 'ORIENTATION_RESPONSE_ERROR_RECEIVED'],
    requests: [{
      url: `orientation`,
      userToken,
      onSuccess: (data) => {
        dispatch({
          type: 'ORIENTATION_RESPONSE_RECEIVED',
          response: normalize(data, [schema.orientationSchema])
        })
      },
      method: 'get'
    }]
  });
}
