import React, {Component} from 'react';
import AnchorLink from 'react-anchor-link-smooth-scroll';
import {Container, Row, Col, Button, Nav} from 'react-bootstrap';
import Form from './forms/Form';
import styled from 'styled-components';
import howItWorksImg from '../Assets/howitworks-img.jpg';

import './mystyle.css';
import {LinkContainer} from "react-router-bootstrap";

const HowItWorks = styled.div`
	/* background-color: rgba(255,255,255); */
	background: linear-gradient(rgba(255, 255, 255, .2), rgba(0, 0, 0, .7)), url(${howItWorksImg});
	background-size: cover;
	min-height: 100vh;
	min-width: 100%;
	color: rgba(255, 255, 255);
	display: flex;
	text-align: right;
`;


const Fugaz = styled.span`font-family: 'Fugaz One', cursive;`;

class Home extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Container className="intro">
                    <Row className="justify-content-md-center align-items-center text-shadow">
                        <Col md={6}>
                            <h1>
                                <Fugaz>Supply It</Fugaz> - Όλοι οι αγαπημένοι προμηθευτές σας με ένα click!
                            </h1>
                            <hr/>
                            <p>
                                Το Supply It είναι ενα one-stop-shop για όλους τους προμηθευτές σας. Άμεση εγγραφή,
                                μία παραγγελία, μία πληρωμή, μηδέν σπαζοκεφαλιές.
                            </p>

                            <AnchorLink href="#getstarted">
                                <Button variant="info btn-square">Ξεκινήστε δωρεάν</Button>
                            </AnchorLink>
                        </Col>
                        <Col md={4}>
                            <img src="" alt=""/>
                        </Col>
                    </Row>
                </Container>

                <div className="get-started">
                    <Container fluid className="text-center" id="getstarted">
                        <Row className="vertical-align justify-content-md-center align-items-center">
                            <Col className="d-none d-sm-flex left-col-start" sm={6}/>
                            <Col xs={12} sm={6} className="get-started-text text-left">
                                <h1>Ξεκινήστε τώρα</h1>
                                <h3>Καμία πίστωση, άμεση παραγγελία</h3>
                                <br/>
                                <ul className="ticked-list">
                                    <li>Καμία πίστωση, άμεση παραγγελία</li>
                                    <li>Πρόσβαση σε εκατοντάδες προμηθευτές στις καλύτερες τιμές.</li>
                                    <li>Μια παραγγελία, μια πληρωμή, άκοπα.</li>
                                </ul>
                                <br/>
                                <LinkContainer to="/getStarted">
                                    <Button className="justify-content-center" variant="danger btn-square">
                                        Εγγραφή
                                    </Button>
                                </LinkContainer>
                            </Col>
                        </Row>
                    </Container>

                    <HowItWorks>
                        <Container id="howitworks" className="d-flex">
                            <Row className="text-shadow align-content-center">
                                <Col sm={4}/>
                                <Col className="" sm={8}>
                                    <h1>
                                        Η απόλυτη εμπειρία παραγγελίας<br/>
                                    </h1>
                                    <hr/>
                                    <h3>Όλοι οι αγαπημένοι προμηθευτές σας, σε ένα μέρος</h3>
                                    <p>
                                        Παραγγείλετε από όλους τους αγαπημένους προμηθευτές σας, με ένα κλίκ. Μεγάλη
                                        επιλογή προμηθευτών εάν θελήσετε να δοκιμάσετε καινούργιους!
                                    </p>

                                    <h3>Δωρεάν εργαλεία για να κάνουν τη ζωή σας εύκολη</h3>

                                    <p>
                                        Αναφορές κόστους, οργάνωση, λίστα με τις τελευταίες παραγγελίες μαζί με τα
                                        τιμολόγια τους, άμεση επικοινωνία με τους προμηθευτές και εύκολη διαχείρηση
                                        της λογιστικής σας - όπου κι αν βρίσκεστε και όποτε θέλετε.
                                    </p>
                                    <br/>
                                    {!this.props.isAuthenticated && (
                                        <LinkContainer to="/getStarted">
                                            <Nav.Link>Ξεκινήστε δωρεάν</Nav.Link>
                                        </LinkContainer>
                                    )}
                                    <LinkContainer to="/getStarted">
                                        <Button variant="info btn-square">Δοκιμάστε το δωρεάν</Button>
                                    </LinkContainer>
                                </Col>
                            </Row>
                        </Container>
                    </HowItWorks>
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
                            <Col xs={12} md={6} className="btm-right-col-start"/>
                        </Row>
                    </Container>
                </div>
            </div>
        );
    }
}

export default Home;
