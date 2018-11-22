import React, { Component } from 'react';
import { Container, Row, Col, Form, FormGroup, Label, Input, Button, Jumbotron } from 'reactstrap';
class RegistrationForm extends Component {
  render() {
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
                    <Input type="text" name="username" id="registration-username" placeholder="Username" />
                  </FormGroup>
                  <FormGroup>
                    <Label for="registration-email">Email</Label>
                    <Input type="text" name="email" id="registration-email" placeholder="Email" />
                  </FormGroup>
                  <FormGroup>
                    <Label for="registration-password">Password</Label>
                    <Input type="password" name="password" id="registration-password" placeholder="Password" />
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

export default RegistrationForm;
