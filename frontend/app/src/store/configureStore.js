import { createStore, applyMiddleware } from 'redux';
import logger from 'redux-logger';
import thunk from 'redux-thunk';
import app from '../reducers/index';

const configureStore = () => {
  const middlewares = [thunk];
  console.log(process.env.NODE_ENV);
  if(process.env.NODE_ENV !== 'production') {
    middlewares.push(logger);
  }
  return createStore(
    app,
    applyMiddleware(...middlewares)
  );
}
export default configureStore;
