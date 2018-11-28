import { createStore, applyMiddleware } from 'redux';
import logger from 'redux-logger';
import thunk from 'redux-thunk';
import localStorageMiddleware from '../middleware/localStorage';
import app from '../reducers/index';

const configureStore = () => {
  const middlewares = [thunk, localStorageMiddleware];
  console.log(process.env.NODE_ENV);
  if(process.env.NODE_ENV !== 'production') {
    middlewares.push(logger);
  }
  const store = createStore(
    app,
    applyMiddleware(...middlewares)
  );
  store.dispatch({ type: '@@INIT_STORE'});
  return store;
}
export default configureStore;
