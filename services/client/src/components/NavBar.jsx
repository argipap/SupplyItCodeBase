import React from "react";
import {Link} from "react-router-dom";
import PropTypes from "prop-types";
import { LinkContainer } from "react-router-bootstrap"
import "./NavBar.css";
import { Navbar, Container, NavbarBrand, NavLink, Nav, Button, Image } from "react-bootstrap";
import Logo from "../logo.png"

const NavBar = props => {
    let menu = (
        <Nav className="ml-auto">
            <LinkContainer to="/"><Nav.Link>Αρχική</Nav.Link></LinkContainer>
            <LinkContainer to="/getStarted"><Nav.Link>Δοκιμάστε</Nav.Link></LinkContainer>
            <LinkContainer to="/howItWorks"><Nav.Link>Πως δουλεύει</Nav.Link></LinkContainer>
            <LinkContainer to="/becomeSupplier"><Nav.Link>Γίνετε προμηθευτής</Nav.Link></LinkContainer>
            <LinkContainer to="/login"><Button className="btn-square" variant="outline-success" data-testid="nav-login">Σύνδεση</Button></LinkContainer>
        </Nav>
        

        // Bulma version
        // <div className="navbar-menu">
        //     <div className="navbar-start">
        //         <Link to="/" className="navbar-item">HOME</Link>
        //         <Link to="/getStarted" className="navbar-item">GET STARTED</Link>
        //         <Link to="/howItWorks" className="navbar-item">HOW IT WORKS</Link>
        //         <Link to="/becomeSupplier" className="navbar-item">BECOME A SUPPLIER</Link>
        //     </div>
        //     <div className="navbar-end">
        //         <Link to="/login" className="navbar-item" data-testid="nav-login">
        //             <button className="button is-link">Sign In</button>
        //         </Link>
        //     </div>
        // </div>
       
    );
    if (props.isAuthenticated()) {
        menu = (
            <Nav className="ml-auto">
                <LinkContainer to="/status"><Nav.Link>Status</Nav.Link></LinkContainer>
                <LinkContainer to="/howItWorks"><Nav.Link>Πως δουλεύει</Nav.Link></LinkContainer>
               <LinkContainer to="/logout"><Button className="btn-square" variant="outline-danger" href="/logout">Αποσύνδεση</Button></LinkContainer> 
            </Nav>

            // Bulma version
            // <div className="navbar-menu">
            //     <div className="navbar-start">
            //         <Link to="/status" className="navbar-item">USER STATUS</Link>
            //         <Link to="/howItWorks" className="navbar-item">HOW IT WORKS</Link>
            //     </div>
            //     <div className="navbar-end">
            // <Link to="/logout" className="navbar-item">Log Out</Link>
            //     </div>
            // </div>
        );
    }

    // const icon = (
    //     <span className="logo">
    //         <a href="/">
    //             <img src="./logo.png" height="33" width="120" alt="Supply IT logo"/>
    //         </a>
    //     </span>
    // )
    return (
        <Navbar
            role="navigation"
            aria-label="main navigation"
            expand="lg"
        >
                <Navbar.Brand href="/"><Image 
                    src={Logo}
                    className="d-inline-block align-top"
                    alt="SupplyIT logo"
                    width="100"
                />
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="navbar-bar"></Navbar.Toggle>
                <Navbar.Collapse id="navbar-bar">
                {menu}    
                </Navbar.Collapse>
         </Navbar>

            // Bulma version
            // <nav
            // className="navbar is-dark"
            // role="navigation"
            // aria-label="main navigation"
            // >
            // <section className="container">
            //     <div className="navbar-brand">
            //         <Link to="/" className="navbar-item nav-title">
            //             {props.title}
            //         </Link>
            //         <span
            //             className="nav-toggle navbar-burger"
            //             onClick={() => {
            //                 let toggle = document.querySelector(".nav-toggle");
            //                 let menu = document.querySelector(".navbar-menu");
            //                 toggle.classList.toggle("is-active");
            //                 menu.classList.toggle("is-active");
            //             }}
            //         >
            // <span/>
            // <span/>
            // <span/>
            // </span>
            //     </div>
            //     {menu}
            // </section>
            // </nav>
    );
};


NavBar.propTypes = {
    title: PropTypes.string.isRequired,
    logoutUser: PropTypes.func.isRequired,
    isAuthenticated: PropTypes.func.isRequired
};

export default NavBar;
