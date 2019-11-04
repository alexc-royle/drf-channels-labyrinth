import React from 'react';
import ReactDOM from 'react-dom';
import Root from './components/Root';
import configureStore from './store/configureStore';
import 'bootstrap/dist/css/bootstrap.css';

const { store, persistor } = configureStore();

ReactDOM.render(
  <Root store={store} persistor={persistor} />,
  document.getElementById('root')
);
