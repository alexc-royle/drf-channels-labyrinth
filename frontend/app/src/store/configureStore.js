import { applyMiddleware, compose, createStore } from 'redux';
import { createLogger } from 'redux-logger';
import { persistStore } from 'redux-persist';
import thunkMiddleware from 'redux-thunk';
import FetchAPI from '../middleware/fetchapi';
import reducers from '../reducers/index';

export default () => {
  const logger = createLogger({});
  let enhancers;
  if (process.env.NODE_ENV !== 'production') {
    enhancers = compose(applyMiddleware(thunkMiddleware, FetchAPI, logger));
  } else {
    enhancers = compose(applyMiddleware(thunkMiddleware, FetchAPI));
  }
  const configureStore = initialState => (
    createStore(reducers, initialState, enhancers)
  );

  // Create store
  const store = configureStore({});
  const persistor = persistStore(store);
  return { store, persistor };
};
