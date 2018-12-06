import React, { Component } from 'react';
import { Container, Row, Col, Form, FormGroup, Label, Input, Button, Jumbotron } from 'reactstrap';
import ErrorAlert from './ErrorAlert';
class RegistrationForm extends Component {
  render() {
    const {
      onRegisterButtonClick,
      onUsernameChange,
      onEmailChange,
      onPasswordChange,
      usernameErrors,
      emailErrors,
      passwordErrors
    } = this.props;
    return (
      <div className="App">
        <Container>
          <Row>
            <Col>
              <Jumbotron>
                <h1>Registration</h1>
                <Form>
                  <FormGroup>
                    <Label for="registration-username">Username</Label>
                    <Input type="text" name="username" id="registration-username" placeholder="Username" onChange={onUsernameChange} />
                  </FormGroup>
                  <ErrorAlert errors={usernameErrors} />
                  <FormGroup>
                    <Label for="registration-email">Email</Label>
                    <Input type="text" name="email" id="registration-email" placeholder="Email" onChange={onEmailChange} />
                  </FormGroup>
                  <ErrorAlert errors={emailErrors} />
                  <FormGroup>
                    <Label for="registration-password">Password</Label>
                    <Input type="password" name="password" id="registration-password" placeholder="Password" onChange={onPasswordChange} />
                  </FormGroup>
                  <ErrorAlert errors={passwordErrors} />
                  <Button onClick={onRegisterButtonClick}>Submit</Button>
                </Form>
              </Jumbotron>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default RegistrationForm;
