import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import { Container, Row, Col,Jumbotron, Alert } from 'reactstrap';
class RegistrationSuccess extends Component {
  render() {
    return (
      <div className="App">
        <Container>
          <Row>
            <Col>
              <Jumbotron>
                <h1>Registration</h1>
                <Alert color="info">You have successfully registered. <NavLink to="/login/">Please login</NavLink>.</Alert>
              </Jumbotron>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default RegistrationSuccess;
