import React from 'react';
import { Provider } from 'react-redux';
import LocalStorage from '../containers/LocalStorage';

const Root = ({ store }) => (
  <Provider store={store}>
    <LocalStorage/>
  </Provider>
);
export default Root;
