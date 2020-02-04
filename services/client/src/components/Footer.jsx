import React from 'react';
import './Footer.css';
import { Container, Col, Row } from 'react-bootstrap';

const Footer = (props) => (
	<Container className="">
		<div className="footer-trust_top">
			<p>Μας προτείνουν</p>
			<div className="trustlogos" />
		</div>
		<hr />
		<Row className="footer-main">
			<Col xs={12} md={3}>
				<h4>Περισσότερα</h4>
				<ul className="footer-list">
					<li>
						<a href="/">Αρχική</a>
					</li>
					<li>
						<a href="/HowItWorks">Πως δουλεύει</a>
					</li>
					<li>
						<a href="/GetStarted">Δοκιμάστε</a>
					</li>
					<li>
						<a href="BecomeSupplier">Γίνετε προμηθευτής</a>
					</li>
					<li>
						<a href="/login">Σύνδεση</a>
					</li>
				</ul>
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
);

export default Footer;
