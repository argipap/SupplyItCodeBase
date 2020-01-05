import React from "react";
import {Link} from "react-router-dom";
import PropTypes from "prop-types";

import "./NavBar.css";

const titleStyle = {
    fontWeight: "bold"
};

const NavBar = props => {
    let menu = (
        <div className="navbar-menu">
            <div className="navbar-start">
                <Link to="/" className="navbar-item">HOME</Link>
                <Link to="/getStarted" className="navbar-item">GET STARTED</Link>
                <Link to="/howItWorks" className="navbar-item">HOW IT WORKS</Link>
                <Link to="/becomeSupplier" className="navbar-item">BECOME A SUPPLIER</Link>
            </div>
            <div className="navbar-end">
                <Link to="/login" className="navbar-item" data-testid="nav-login">
                    <button className="button is-link">Sign In</button>
                </Link>
            </div>
        </div>
    );
    if (props.isAuthenticated()) {
        menu = (
            <div className="navbar-menu">
                <div className="navbar-start">
                    <Link to="/status" className="navbar-item">USER STATUS</Link>
                    <Link to="/howItWorks" className="navbar-item">HOW IT WORKS</Link>
                </div>
                <div className="navbar-end">
            <Link to="/logout" className="navbar-item">Log Out</Link>
                </div>
            </div>
        );
    }
    return (
        <nav
            className="navbar is-dark"
            role="navigation"
            aria-label="main navigation"
        >
            <section className="container">
                <div className="navbar-brand">
                    <Link to="/" className="navbar-item nav-title" style={titleStyle}>
                        {props.title}
                    </Link>
                    <span
                        className="nav-toggle navbar-burger"
                        onClick={() => {
                            let toggle = document.querySelector(".nav-toggle");
                            let menu = document.querySelector(".navbar-menu");
                            toggle.classList.toggle("is-active");
                            menu.classList.toggle("is-active");
                        }}
                    >
            <span/>
            <span/>
            <span/>
          </span>
                </div>
                {menu}
            </section>
        </nav>
    );
};

NavBar.propTypes = {
    title: PropTypes.string.isRequired,
    logoutUser: PropTypes.func.isRequired,
    isAuthenticated: PropTypes.func.isRequired
};

export default NavBar;
