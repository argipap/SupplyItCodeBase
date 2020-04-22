// Merged into home

import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Button } from 'react-bootstrap';
import styled from 'styled-components';
import './mystyle.css';

const MainView = styled.div`
	/* background-color: rgba(255,255,255); */
	background: linear-gradient(rgba(255, 255, 255, .2), rgba(0, 0, 0, .7)),
		url(https://images.unsplash.com/photo-1543776231-5350211df62c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1650&q=80);
	background-size: cover;
	min-height: 100vh;
	min-width: 100vw;
	color: rgba(255, 255, 255);
	display: flex;
	text-align: right;

	.how-it-works {
	}
`;


function HowItWorks(props) {
	return (
		<MainView>
			<Container className="d-flex">
				<Row className="text-shadow align-content-center">
					<Col sm={4} />
					<Col className="" sm={8}>
						<h1>
							Η απόλυτη εμπειρία παραγγελίας<br />
						</h1>
						<hr />
						<h3>Όλοι οι αγαπημένοι προμηθευτές σας, σε ένα μέρος</h3>
						<p>
							Παραγγείλετε από όλους τους αγαπημένους προμηθευτές σας, με ένα κλίκ. Μεγάλη επιλογή
							προμηθευτών εάν θελήσετε να δοκιμάσετε καινούργιους!
						</p>
						<h1>Οι καλύτερες τιμές, εγγυημένα</h1>

						<p>
							Απολαύστε τις καλύτερες τιμές του κλάδου χάρη στις διαπραγματεύσεις μας με τους προμηθευτές.
						</p>

						<h3>Δωρεάν εργαλεία για να κάνουν τη ζωή σας εύκολη</h3>

						<p>
							Αναφορές κόστους, οργάνωση, λίστα με τις τελευταίες παραγγελίες μαζί με τα τιμολόγια τους,
							άμεση επικοινωνία με τους προμηθευτές και εύκολη διαχείρηση της λογιστικής σας - όπου κι αν
							βρίσκεστε και όποτε θέλετε.
						</p>
						<br />
						{!props.isAuthenticated() && (
							<Link to="/getStarted">
								<Button variant="info btn-square">Ξεκινήστε δωρεάν</Button>
							</Link>
						)}
						<Link to="#">
							<Button variant="info btn-square">Δοκιμάστε το δωρεάν</Button>
						</Link>
					</Col>
				</Row>
			</Container>
		</MainView>
	);
}

export default HowItWorks;
