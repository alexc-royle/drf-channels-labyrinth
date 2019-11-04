import 'whatwg-fetch';

export const lib = {
  checkStatus: (response) => {
    console.log(response);
    if (response.status >= 200 && response.status < 300) {
      return response.json();
    }
    const error = new Error(response.statusText);
    error.response = response;
    return error;
  },

  setupHeaders: (userToken) => {
    const headers = new Headers({ 'Content-Type': 'application/json' });
    if (userToken) {
      headers.append('Authorization', `Token ${userToken}`);
    }
    return headers;
  },

  setupPostRequest: (action) => {
    const { body = {}, userToken = '' } = action;
    return {
      headers: lib.setupHeaders(userToken),
      method: 'post',
      credentials: 'include',
      body: JSON.stringify(body)
    };
  },

  setupGetRequest: (action) => {
    const { userToken = '' } = action;
    return {
      headers: lib.setupHeaders(userToken),
      method: 'get',
      credentials: 'include'
    };
  },

  setupRequest: (action = {}) => {
    const { method = 'post' } = action;
    switch (method) {
      case 'get':
        return lib.setupGetRequest(action);
      default:
        return lib.setupPostRequest(action);
    }
  },

  performFetchRequest: (dispatch = () => {}, request = {}) => {
    const { url = '', onSuccess = '' } = request;
    const requestBody = lib.setupRequest(request);
    const fullUrl = `http://localhost:8080/api/v1/${url}`;
    return fetch(fullUrl, requestBody)
      .then(lib.checkStatus)
      .then((data) => {
        if (onSuccess) {
          dispatch({ type: onSuccess, payload: data });
        }
        return data;
      })
      .catch((err) => {
        console.log('performFetchRequest: error', err); // eslint-disable-line no-console
      });
  },

  manageAllRequests: (dispatch, promises, allSuccessType, allErrorType) => Promise.all(promises)
    .then(() => {
      if (allSuccessType) {
        dispatch({ type: allSuccessType });
      }
    })
    .catch((error) => {
      dispatch({ type: 'API_RESPONSE_ERROR', payload: error });
      if (allErrorType) {
        dispatch({ type: allErrorType, payload: error });
      }
    }),

  handleAPIRequestAction: (dispatch, action) => {
    const { types, requests } = action;
    const [allPendingType, allSuccessType, allErrorType] = types;
    dispatch({ type: allPendingType });
    const promises = requests.map(request => lib.performFetchRequest(dispatch, request));
    lib.manageAllRequests(dispatch, promises, allSuccessType, allErrorType);
  }
};

const FetchAPI = ({ dispatch }) => next => (action) => {
  switch (action.type) {
    case 'API_REQUEST': {
      lib.handleAPIRequestAction(dispatch, action);
      break;
    }
    default:
      break;
  }
  return next(action);
};

export default FetchAPI;
