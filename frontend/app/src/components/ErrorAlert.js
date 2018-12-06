import React, { Component } from 'react';
import { Alert } from 'reactstrap';

class ErrorAlert extends Component {
  render() {
    const { errors } = this.props;
    if (errors.length) {
      const errorList = errors.map((name, index) => <li key={ index }>{name}</li>);
      return (
        <Alert color="danger"><ul>{errorList}</ul></Alert>
      );
    }
    return (
      <div/>
    );
  }
}

export default ErrorAlert;
