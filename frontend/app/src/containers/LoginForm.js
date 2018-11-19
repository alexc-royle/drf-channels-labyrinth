import React, { Component } from 'react';
import { Container, Row, Col, Form, FormGroup, Label, Input, Button, Jumbotron } from 'reactstrap';
class LoginForm extends Component {
  render() {
    return (
      <div className="App">
        <Container>
          <Row>
            <Col>
              <Jumbotron>
                <h1>Login</h1>
                <Form>
                  <FormGroup>
                    <Label for="login-username">Username</Label>
                    <Input type="text" name="username" id="login-username" placeholder="Username" />
                  </FormGroup>
                  <FormGroup>
                    <Label for="login-password">Password</Label>
                    <Input type="password" name="password" id="login-password" placeholder="Password" />
                  </FormGroup>
                  <Button>Submit</Button>
                </Form>
              </Jumbotron>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default LoginForm;
