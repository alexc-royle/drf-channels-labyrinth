import 'whatwg-fetch';
import { helpers } from '../reducers';

export const checkStatus = (response) => {
  if (response.status >= 200 && response.status < 300) {
    return response;
  } else {
    const error = new Error(response.statusText);
    error.response = response;
    throw error;
  }
}

export const parseJSON = (response) => {
  return response.json();
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

const APIMiddleware = store => next => action => {
  switch(action.type) {
    case 'API_REQUEST':
      const { url = '', callback = () => {} } = action;
      const requestBody = setupRequest(action, store.getState());
      fetch(`http://localhost:8080/api/v1/${url}`, requestBody)
        .then(checkStatus)
        .then(parseJSON)
        .then((data) => {
          console.log('request succeeded with JSON response', data);
          callback(false, data);
        }).catch((error) => {
          store.dispatch({ type: 'API_RESPONSE_ERROR', error });
          console.log('request failed with error', error);
          callback(error);
        })
        break;
    default:
      break;
  }
  return next(action);
}
export default APIMiddleware;
