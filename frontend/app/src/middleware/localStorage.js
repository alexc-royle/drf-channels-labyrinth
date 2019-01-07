export const loadState = (id) => {
  try {
    const serializedState = localStorage.getItem(id);
    if (serializedState === null) {
      return undefined;
    }
    return JSON.parse(serializedState);
  } catch(err) {
    return undefined;
  }
}

export const saveState = (id, state) => {
  try {
    const serializedState = JSON.stringify(state);
    localStorage.setItem(id, serializedState);
  } catch(err) {
    // ignore for now.
  }
}

const localStorageMiddleware = ({ dispatch, getState }) => next => action => {
  switch(action.type) {
    case 'LOCAL_STORAGE_REQUEST':
      const { method, id, data, onSuccess, onAttempt } = action;
      dispatch({ type: onAttempt });
      switch(method) {
        case 'get':
          const loadedState = loadState(id);
          if(loadedState !== undefined) {
            dispatch({ type: onSuccess, payload: loadedState });
          }
          break;
        case 'set':
          saveState(id, data);
          dispatch({ type: onSuccess });
          break;
        default:
          break;
      }
      break;
    default:
      break;
  }
  return next(action);
}

export default localStorageMiddleware;
