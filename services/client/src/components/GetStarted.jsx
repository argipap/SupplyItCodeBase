import React, { Component } from 'react';
import './mystyle.css';
import Form from './forms/Form';
import { Container, Row, Col, Button } from 'react-bootstrap';

class GetStarted extends Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className="get-started">
				<Container fluid className="text-center">
					<Row className="vertical-align justify-content-md-center align-items-center">
						<Col className="d-none d-sm-flex left-col-start" sm={6} />
						<Col xs={12} sm={6} className="get-started-text text-left">
							<h1>Ξεκινήστε τώρα</h1>
							<h3>Καμία πίστωση, άμεση παραγγελία</h3>
							<br />
							<ul className="ticked-list">
								<li>Καμία πίστωση, άμεση παραγγελία</li>
								<li>Πρόσβαση σε εκατοντάδες προμηθευτές στις καλύτερες τιμές.</li>
								<li>Μια παραγγελία, μια πληρωμή, άκοπα.</li>
							</ul>
							<br />
							<Button className="justify-content-center" variant="danger btn-square">
								Εγγραφή
							</Button>
						</Col>
					</Row>
				</Container>

				<Container fluid id="join-retail">
					<Row className="vertical-align justify-content-md-center">
						<Col className="btm-left-col-start text-left" xs={12} md={6}>
							<h2>Συμπληρώστε την παρακάτω φόρμα για να εγγραφείτε</h2>
							<Form
								formType={this.props.formType}
								createMessage={this.props.createMessage}
								loginUser={this.props.loginUser}
								confirmUser={this.props.confirmUser}
								isAuthenticated={this.props.isAuthenticated}
								email_confirmation={this.props.email_confirmation}
							/>
						</Col>
						<Col xs={12} md={6} className="btm-right-col-start" />
					</Row>
				</Container>
			</div>
		);
	}
}

export default GetStarted;
