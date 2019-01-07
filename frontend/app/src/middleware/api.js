import 'whatwg-fetch';
import { helpers } from '../reducers';

export const checkStatus = (response) => {
  return response.json().then((data) => {
    if (response.status >= 200 && response.status < 300) {
      return data;
    } else {
      const error = new Error(response.statusText);
      error.response = response;
      error.data = data;
      throw error;
    }
  })
}

export const setupHeaders = (state) => {
  const userToken = helpers.getUserToken(state);
  const headers = new Headers({'Content-Type': 'application/json'});
  if (userToken) {
    headers.append('Authorization', `Token ${userToken}`)
  }
  return headers;
}
export const setupRequest = (action, state) => {
  const { body = {} } = action;
  return {
    headers: setupHeaders(state),
    method: 'POST',
    credentials: 'include',
    body: JSON.stringify(body)
  }
}

const APIMiddleware = ({ dispatch, getState }) => next => action => {
  switch(action.type) {
    case 'API_REQUEST':
      const { url = '', types } = action;
      const [pendingType, successType, errorType] = types;
      const requestBody = setupRequest(action, getState());
      dispatch({ type: pendingType });
      fetch(`http://localhost:8080/api/v1/${url}`, requestBody)
        .then(checkStatus)
        .then((data) => {
          console.log('request succeeded with JSON response', data);
          dispatch({ type: successType, payload: data});
        }).catch((error) => {
          dispatch({ type: 'API_RESPONSE_ERROR', payload: error });
          dispatch({ type: errorType, payload: error });
        })
        break;
    default:
      break;
  }
  return next(action);
}
export default APIMiddleware;
