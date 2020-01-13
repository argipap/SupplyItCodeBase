import React, { Component } from 'react';
import './mystyle.css';
import Form from './forms/Form';
import { Container, Row, Col, Button } from 'react-bootstrap';
import AnchorLink from 'react-anchor-link-smooth-scroll';

class GetStarted extends Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className="become-a-supplier">
				<Container fluid className="text-center">
					<Row className="vertical-align">
						<Col className="d-none d-sm-flex left-col" sm={6} />
						<Col xs={12} sm={6} className="supplier-text text-left">
							<h1>Γίνετε προμηθευτής στο Supply It</h1>
							<h3>Δωρεάν εγγραφή, ευκολόχρηστο</h3>
							<p>
								Διαχειριστείτε εύκολα τα προϊόντα σας, τις τιμές και τους πελάτες σας στο cloud! Δώστε
								στους πελάτες σας την καλύτερη εμπειρία παραγγελίας που έχουν ζήσει! Εύκολα και γρήγορα,
								σε υπολογιστές και κινητά. Όλα αυτά μόνο με μια μικρή χρέωση για τις πωλήσεις που
								λαμβάνουμε.
							</p>
							<h3>Νέους πελάτες, χωρίς κόπο</h3>
							<p>
								Η φανταστική ομάδα εξυπηρέτησης πελατών μας είναι εδώ για να βοηθήσει στην επίλυση
								οποιωνδήποτε ζητημάτων, πράγμα που σημαίνει ότι οι πωλήσεις σας μπορούν να αυξηθούν
								γρήγορα χωρίς ανησυχίες για την επιχείρησή σας.
							</p>
							<h3>Το προϊόν σας, η πωλήσεις μας & το marketing</h3>
							<p>
								Έχουμε πωλήσεις που εκτοξεύονται από την απίστευτη πλατφόρμα μάρκετινγκ και
								προώθησης που κατέχουμε. Με το Supply It τα προϊόντα σας θα προωθηθούν σαν ποτέ ξανά. Θα συνεργαστούμε μαζί σας για να βρούμε τους
								καλύτερους πελάτες για το προϊόν σας και θα βελτιώσουμε τις πωλήσεις σας.
							</p>
							<AnchorLink href="#join-us"><Button variant="danger btn-square ">Εγγραφή</Button></AnchorLink>
						</Col>
					</Row>
				</Container>

				<Container id="join-us">
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
