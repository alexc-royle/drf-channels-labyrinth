import { createStore, applyMiddleware } from 'redux';
import logger from 'redux-logger';
import thunk from 'redux-thunk';
import localStorageMiddleware from '../middleware/localStorage';
import APIMiddleware from '../middleware/api';
import app from '../reducers/index';

const configureStore = () => {
  const middlewares = [thunk, localStorageMiddleware, APIMiddleware];
  if(process.env.NODE_ENV !== 'production') {
    middlewares.push(logger);
  }
  return createStore(
    app,
    applyMiddleware(...middlewares)
  );
}
export default configureStore;
