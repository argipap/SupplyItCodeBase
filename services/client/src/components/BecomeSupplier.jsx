import React, { Component } from 'react';
import './mystyle.css';
import Form from './forms/Form';
import { Container, Row, Col, Button, Image } from 'react-bootstrap';
import AnchorLink from 'react-anchor-link-smooth-scroll';
import SupplierImg from '../Assets/supplier-img.jpeg'
class BecomeSupplier extends Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className="become-a-supplier">
				<Container fluid>
					<Row className="">
						<Col sm={6} className="d-none d-lg-block left-col col-lg-6"/>
						<Col sm={6} className="py-5 supplier-text text-left d-none d-lg-block col-lg-6">
							<h1>Γίνετε προμηθευτής στο Supply It</h1>
							<h3>Δωρεάν εγγραφή, ευκολόχρηστο</h3>
							<p>
								Διαχειριστείτε εύκολα τα προϊόντα σας, τις τιμές και τους πελάτες σας στο cloud! Δώστε
								στους πελάτες σας την καλύτερη εμπειρία παραγγελίας που έχουν ζήσει! Εύκολα και γρήγορα,
								σε υπολογιστές και κινητά. Όλα αυτά μόνο με μια μικρή χρέωση για τις πωλήσεις που
								λαμβάνουμε.
							</p>
							<h3>Αποκτήστε νέους πελάτες, χωρίς κόπο</h3>
							<p>
								Η φανταστική ομάδα εξυπηρέτησης πελατών μας είναι εδώ για να βοηθήσει στην επίλυση
								οποιωνδήποτε ζητημάτων, πράγμα που σημαίνει ότι οι πωλήσεις σας μπορούν να αυξηθούν
								γρήγορα χωρίς ανησυχίες για την επιχείρησή σας.
							</p>
							<h3>Το προϊόν σας, οι πωλήσεις μας & το marketing</h3>
							<p>
								Έχουμε πωλήσεις που εκτοξεύονται από την απίστευτη πλατφόρμα μάρκετινγκ και προώθησης
								που κατέχουμε. Με το Supply It τα προϊόντα σας θα προωθηθούν σαν ποτέ ξανά. Θα
								συνεργαστούμε μαζί σας για να βρούμε τους καλύτερους πελάτες για το προϊόν σας και θα
								βελτιώσουμε τις πωλήσεις σας.
							</p>
							<AnchorLink href="#join-us">
								<Button variant="danger btn-square ">Εγγραφή</Button>
							</AnchorLink>
						</Col>
						<Col sm={10} className="mx-auto my-2 mt-1 supplier-text d-lg-none">
							<h1>Γίνετε προμηθευτής στο Supply It</h1>
							<Image
								src="${SupplierImg})"
								rounded
								fluid
								cover
							/>

							<ul className="ticked-list">
								<li>Δωρεάν εγγραφή και ευκολόχρηστο</li>
								<li>Αποκτήστε νέους πελάτες, χωρίς κόπο</li>
								<li>Το προϊόν σας, οι πωλήσεις μας & το marketing</li>
							</ul>
							<Button variant="danger btn-square">Εγγραφή</Button>
						</Col>
					</Row>
				</Container>
				<Container id="join-us" className="d-flex">
					<Row className="vertical-align justify-content-md-center align-items-center">
						<Col xs={12} md={6}>
							<h1>Συνεργαστείτε μαζί μας</h1>
							<p>Ενδιαφέρεστε να συμμετάσχετε στο δίκτυο μας ως προμηθευτής;</p>
							<p>Συμπληρώστε αυτήν τη φόρμα και θα επικοινωνήσουμε μαζί σας το συντομότερο δυνατόν.</p>
						</Col>
						<Col xs={12} md={6} className="p-5 text-left btm-right-col-supplier">
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

export default BecomeSupplier;
