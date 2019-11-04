import 'whatwg-fetch';

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

const fetchData = ( url, body = {}, token = '', cb=() => {} ) => {
  const headers = new Headers({'Content-Type': 'application/json'});
  if (token) {
    headers.append('Authorization', `Token ${token}`)
  }
  fetch(url, {
    method: 'POST',
    credentials: 'include',
    headers,
    body: JSON.stringify(body)
  })
    .then(checkStatus)
    .then(parseJSON)
    .then((data) => {
      console.log('request succeeded with JSON response', data);
      cb(false, data);
    }).catch((error) => {
      console.log('request failed with error', error);
      cb(error);
    })
}

export default fetchData;
