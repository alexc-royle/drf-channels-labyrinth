import React, { Component } from 'react';
import { Navbar, NavbarBrand, Nav, NavItem } from 'reactstrap';

class LoggedInHeader extends Component {
  render() {
    const { logoutClicked } = this.props;
    return (
      <div>
        <Navbar color='light' light expand='md'>
          <NavbarBrand href='/'>Labyrinth</NavbarBrand>
          <Nav className='ml-auto' navbar>
            <NavItem>
              <button onClick={logoutClicked}>Logout</button>
            </NavItem>
          </Nav>
        </Navbar>
      </div>
    );
  }
}

export default LoggedInHeader;
