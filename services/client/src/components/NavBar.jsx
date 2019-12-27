import React from 'react';
import {Link} from 'react-router-dom';

const NavBar = (props) => (
    // eslint-disable-next-line
    <nav className="navbar is-dark" role="navigation" aria-label="main navigation">
        <section className="container">
            <div className="navbar-brand">
                <strong className="navbar-item">{props.title}</strong>
                <span
                    className="nav-toggle navbar-burger"
                    onClick={() => {
                        let toggle = document.querySelector(".nav-toggle");
                        let menu = document.querySelector(".navbar-menu");
                        toggle.classList.toggle("is-active");
                        menu.classList.toggle("is-active");
                    }}>
          <span></span>
          <span></span>
          <span></span>
        </span>
            </div>
            <div className="navbar-menu">
                <div className="navbar-start">
                    <Link to="/" className="navbar-item">HOME</Link>
                    {!props.isAuthenticated &&
                    <Link to="/getStarted" className="navbar-item">GET STARTED</Link>
                    }
                    {props.isAuthenticated &&
                    <Link to="/status" className="navbar-item">USER STATUS</Link>
                    }
                    <Link to="/howItWorks" className="navbar-item">HOW IT WORKS</Link>
                    {!props.isAuthenticated &&
                    <Link to="/becomeSupplier" className="navbar-item">BECOME A SUPPLIER</Link>
                    }
                </div>
                <div className="navbar-end">
                    {!props.isAuthenticated &&
                    <div className="navbar-item">
                        <Link to="/login" className="button is-link">Sign In</Link>
                    </div>
                    }
                    {props.isAuthenticated &&
                    <Link to="/logout" className="navbar-item">Log Out</Link>
                    }
                </div>
            </div>
        </section>
    </nav>
);

export default NavBar;