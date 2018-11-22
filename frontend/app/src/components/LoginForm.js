import React, { Component } from 'react';
import { Container, Row, Col, Form, FormGroup, Label, Input, Button, Jumbotron, Alert } from 'reactstrap';
class LoginForm extends Component {
  render() {
    const {
      onLoginButtonClick,
      onUsernameChange,
      onPasswordChange,
      hasError
    } = this.props;
    let alert = <div/>;
    if (hasError) {
      alert = <Alert color="danger">The username or password you have entered is invalid.</Alert>;
    }
    return (
      <Container>
        <Row>
          <Col>
            <Jumbotron>
              <h1>Login</h1>
              <Form>
                <FormGroup>
                  <Label for="login-username">Username</Label>
                  <Input type="text" name="username" id="login-username" placeholder="Username" onChange={onUsernameChange} />
                </FormGroup>
                <FormGroup>
                  <Label for="login-password">Password</Label>
                  <Input type="password" name="password" id="login-password" placeholder="Password" onChange={onPasswordChange} />
                </FormGroup>
                {alert}
                <Button onClick={onLoginButtonClick}>Submit</Button>
              </Form>
            </Jumbotron>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default LoginForm;
