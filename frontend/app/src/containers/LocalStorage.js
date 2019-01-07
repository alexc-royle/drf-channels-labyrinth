import React from 'react'
import { connect } from 'react-redux';
import * as actions from '../actions';
import { helpers } from '../reducers';
import App from '../components/App';

class LocalStorage extends React.Component {
  render() {
    return (<App />);
  }
  componentDidUpdate(prevProps) {
      if (prevProps.isUserAuthenticated !== this.props.isUserAuthenticated) {
          this.props.saveUserDataToLocalStorage();
      }
  }
  componentDidMount() {
    this.props.loadUserDataFromLocalStorage();
  }
};

const mapStateToProps = (state, props) => {
	return {
    isUserAuthenticated: helpers.getIsUserAuthenticated(state)
  }
};

const ConnectedLocalStorage = connect(
	mapStateToProps,
	actions
)(LocalStorage);

export default ConnectedLocalStorage;
