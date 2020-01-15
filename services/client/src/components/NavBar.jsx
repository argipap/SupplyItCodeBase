import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { LinkContainer } from 'react-router-bootstrap';
import './NavBar.css';
import { Navbar, Container, NavbarBrand, NavLink, Nav, Button, Image } from 'react-bootstrap';
import Logo from '../logo.png';
import LoginModal from './LoginModal'

const NavBar = (props) => {
	let menu = (
		<Nav className="ml-auto">
			<LinkContainer to="/">
				<Nav.Link>Αρχική</Nav.Link>
			</LinkContainer>
			<LinkContainer to="/getStarted">
				<Nav.Link>Δοκιμάστε</Nav.Link>
			</LinkContainer>
			<LinkContainer to="/howItWorks">
				<Nav.Link>Πως δουλεύει</Nav.Link>
			</LinkContainer>
			<LinkContainer to="/becomeSupplier">
				<Nav.Link>Γίνετε προμηθευτής</Nav.Link>
			</LinkContainer>
			<LinkContainer to="/login">
				<Button className="btn-square" variant="outline-success" data-testid="nav-login">
					Σύνδεση
				</Button>
			</LinkContainer>
		</Nav>
	);
	if (props.isAuthenticated()) {
		menu = (
			<Nav className="ml-auto">
				<LinkContainer to="/status">
					<Nav.Link>Status</Nav.Link>
				</LinkContainer>
				<LinkContainer to="/howItWorks">
					<Nav.Link>Πως δουλεύει</Nav.Link>
				</LinkContainer>
				<LinkContainer to="/logout">
					<Button className="btn-square" variant="outline-danger" href="/logout">
						Αποσύνδεση
					</Button>
				</LinkContainer>
			</Nav>
		);
	}

	return (
		<Navbar role="navigation" aria-label="main navigation" expand="lg">
			<Navbar.Brand href="/">
				<Image src={Logo} className="d-inline-block align-top" alt="SupplyIT logo" width="100" />
			</Navbar.Brand>
			<Navbar.Toggle aria-controls="navbar-bar" />
			<Navbar.Collapse id="navbar-bar">{menu}</Navbar.Collapse>
		</Navbar>
	);
};

NavBar.propTypes = {
	title: PropTypes.string.isRequired,
	logoutUser: PropTypes.func.isRequired,
	isAuthenticated: PropTypes.func.isRequired
};

export default NavBar;
