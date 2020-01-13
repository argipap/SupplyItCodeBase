import React, { Component } from 'react';
import './mystyle.css';
import Form from './forms/Form';
import { Container, Row, Col, Jumbotron } from 'react-bootstrap';

class GetStarted extends Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
            <div>
                <Jumbotron fluid className="intro">
					<Container>
						<h1>Supply IT - Όλοι οι αγαπημένοι προμηθευτές σας σ΄ένα μέρος! </h1>
						<p>This is a modified jumbotron that occupies the entire horizontal space of its parent.</p>
					</Container>
				</Jumbotron>
            
			<Container>
				
				<Row>
					<Col xs={12} md={6}>
						<h1>LET'S GET STARTED</h1>
						<hr />
						<p>No credit apps, instant ordering</p>
						<ul className="ticked-list">
							<li>FREE to use</li>
							<li>Access to your favourite suppliers near your region</li>
							<li>Orders history, last order ready to submit</li>
						</ul>
					</Col>
					<Col xs={12} md={6}>
						<h2>JOIN US</h2>
						<Form
							formType={this.props.formType}
							createMessage={this.props.createMessage}
							loginUser={this.props.loginUser}
							confirmUser={this.props.confirmUser}
							isAuthenticated={this.props.isAuthenticated}
							email_confirmation={this.props.email_confirmation}
						/>
					</Col>
				</Row>
			</Container>
            </div>
		);
	}
}

export default GetStarted;
