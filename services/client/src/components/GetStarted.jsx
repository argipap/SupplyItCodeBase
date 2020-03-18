// --Merged into Home.jsx--


import React, {Component} from 'react';
import './mystyle.css';
import Form from './forms/Form';
import {Container, Row, Col} from 'react-bootstrap';

class GetStarted extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        window.scrollTo(0, 0);
    }

    render() {
        return (
            <div className="get-started">
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
        );
    }
}

export default GetStarted;
