import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Button } from 'react-bootstrap';
import './mystyle.css';

class Home extends Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<Container className="intro">
				<Row className="justify-content-md-center align-items-center">
					<Col md={6}>
						<h1>Supply IT - Όλοι οι αγαπημένοι προμηθευτές σας!</h1>
						<hr />
						<p>
							Supplyit is a one-stop-shop for all your wholesale foodservice suppliers. Instant sign up,
							one order, one payment, zero headaches.
						</p>

						<Link to="/getStarted">
							<Button variant="info">GET STARTED</Button>
						</Link>
					</Col>
                    <Col md={4}>
                        <img src=""/>
                    </Col>
				</Row>
			</Container>
		);
	}
}

export default Home;
