import React, { Component } from 'react';
import { Navbar, NavbarBrand, Nav, NavItem, NavLink } from 'reactstrap';

class NotLoggedInHeader extends Component {
  render() {
    return (
      <div>
        <Navbar color='light' light expand='md'>
          <NavbarBrand href='/'>Labyrinth</NavbarBrand>
          <Nav className='ml-auto' navbar>
            <NavItem>
              <NavLink href='/login/'>Login</NavLink>
              <NavLink href='/register/'>Register</NavLink>
            </NavItem>
          </Nav>
        </Navbar>
      </div>
    );
  }
}

export default NotLoggedInHeader;
