import React, { Component } from 'react';
import { Navbar, NavbarBrand, Nav, NavItem, NavLink } from 'reactstrap';

class LoggedInHeader extends Component {
  render() {
    return (
      <div>
        <Navbar color='light' light expand='md'>
          <NavbarBrand href='/'>Labyrinth</NavbarBrand>
          <Nav className='ml-auto' navbar>
            <NavItem>
              <NavLink href='/logout/'>Logout</NavLink>
            </NavItem>
          </Nav>
        </Navbar>
      </div>
    );
  }
}

export default LoggedInHeader;
