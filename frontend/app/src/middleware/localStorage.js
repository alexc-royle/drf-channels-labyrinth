export const loadState = () => {
  try {
    const serializedState = localStorage.getItem('state');
    if (serializedState === null) {
      return undefined;
    }
    return JSON.parse(serializedState);
  } catch(err) {
    return undefined;
  }
}

export const saveState = (state) => {
  try {
    const serializedState = JSON.stringify(state);
    localStorage.setItem('state', serializedState);
  } catch(err) {
    // ignore for now.
  }
}

const localStorageMiddleware = store => next => action => {
  switch(action.type) {
    case '@@INIT_STORE':
      const state = loadState();
      if(state !== undefined) {
        store.dispatch({ type: 'LOADED_DATA_FROM_LOCAL_STORAGE', data: state });
      }
      break;
    case 'SAVE_DATA_TO_LOCAL_STORAGE':
      saveState(action.data);
      break;
    default:
      break;
  }
  return next(action);
}
export default localStorageMiddleware;
