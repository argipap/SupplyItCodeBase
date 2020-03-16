import React from 'react';
import PropTypes from 'prop-types';
import './Footer.css';
import { Container, Col, Row } from 'react-bootstrap';
import { HashLink as Link } from 'react-router-hash-link';


const Footer = (props) => {

	let footer = (
		<ul className="footer-list">
			<li>
				<Link smooth to="/">Αρχική</Link>
			</li>
			<li>
				<Link smooth to="/#howitworks">Πως δουλεύει</Link>
			</li>
			<li>
				<Link smooth to="/#getstarted">Δοκιμάστε</Link>
			</li>
			<li>
				<Link to="/BecomeSupplier">Γίνετε προμηθευτής</Link>
			</li>
			<li>
				<Link to="/login">Σύνδεση</Link>
			</li>
		</ul>

	)

	if (props.isAuthenticated()) {
		footer = (
			<ul className="footer-list">
			<li>
				<Link smooth to="/">Αρχική</Link>
			</li>
			<li>
				<Link to="/status">Status</Link>
			</li>
			<li>
				<Link smooth to="/#howitworks">Πως δουλεύει</Link>
			</li>
			<li>
				<Link to="/logout">Αποσύνδεση</Link>
			</li>
		</ul>
		)
	}

	return (

		<Container className="">
			<div className="footer-trust_top">
				<p>Μας προτείνουν</p>
				<div className="trustlogos" />
			</div>
			<hr />
			<Row className="footer-main">
				<Col xs={12} md={3}>
					<h4>Περισσότερα</h4>
					{footer}
				</Col>
				<Col xs={12} md={6} className="footer-middle">
					<h4>Εγγραφείτε στο Newsletter μας</h4>
					<p>Εγγραφείτε για να λαμβάνετε τα νέα της πλατφόρμας και άλλα πολλά.</p>

					<form className="hero-cta__form">
						<div className="elcontainer">
							<div className="inner-wrap submit-container">
								<div className="hero-cta__input-wrap">
									<input
										type="email"
										name="data[email]"
										required=""
										id="hero-cta-email"
										placeholder="Το email σας"
									/>
								</div>
								<button type="submit" className="emailsignup">
									Εγγραφή
							</button>
							</div>
						</div>
					</form>
				</Col>

				<Col xs={12} md={3} className="footer-right">
					<div className="footerbox">
						<h4>Επικοινωνία</h4>
						<p>Είμαστε εδώ για εσάς</p>
						<ul className="footer-list">
							<li>Σταθερό</li>
							<li className="phone">+30 88888888</li>
							<li>Κινητό</li>
							<li className="phone">+30 23123123</li>
						</ul>
					</div>
				</Col>
			</Row>

			<Row className="footer-bottom">
				<Col lg={3} md={3} className="footer-copyright">
					<p>©2019 Supplyit.gr</p>
				</Col>

				<Col md={9} xs={12} className="footer-partners">
					<img src="https://www.authenticireland.com/wp-content/uploads/2018/04/Bottom_Trust2.png" alt="" />
				</Col>
			</Row>
		</Container>
	)
};

Footer.propTypes = {
    logoutUser: PropTypes.func.isRequired,
    isAuthenticated: PropTypes.func.isRequired
};

export default Footer;
