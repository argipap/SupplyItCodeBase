import React, {Component} from 'react';
import axios from 'axios';
import './mystyle.css';
import RegisterForm from "./forms/RegisterForm";
import {Container, Row, Col} from 'react-bootstrap';

class GetStarted extends Component {
    constructor(props) {
        super(props);
        this.handleRegisterFormSubmit = this.handleRegisterFormSubmit.bind(this);
    }

    componentDidMount() {
        window.scrollTo(0, 0);
    }

    handleRegisterFormSubmit = data => {
        let user_type = "retail";
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${user_type}/register`;
        axios
            .post(url, data)
            .then(res => {
                this.props.confirmUser();
                // this.props.createMessage("success", res.data.message);
                this.props.createMessage(
                    "Επιβεβαίωση email",
                    "Παρακαλούμε ενεργοποιήστε τον λογαριασμό σας ακολουθώντας τον σύνδεσμο που σας έχουμε στείλει στο email σας."
                );
            })
            .catch(err => {
                this.props.createMessage('Συνέβη κάποιο σφάλμα!', err.response.data.message);
            });
    };

    render() {
        return (
            <div className="get-started">
                <Container fluid id="join-retail">
                    <Row className="vertical-align justify-content-md-center">
                        <Col className="btm-left-col-start text-left" xs={12} md={6}>
                            <h2>Συμπληρώστε την παρακάτω φόρμα για να εγγραφείτε</h2>
                            <RegisterForm
                                formType={this.props.formType}
                                createMessage={this.props.createMessage}
                                confirmUser={this.props.confirmUser}
                                isAuthenticated={this.props.isAuthenticated}
                                email_confirmation={this.props.email_confirmation}
                                handleRegisterFormSubmit={this.handleRegisterFormSubmit}
                            />
                        </Col>
                        <Col xs={12} md={6} className="btm-right-col-start"/>
                    </Row>
                </Container>
            </div>
        );
    }
}

export default GetStarted;
