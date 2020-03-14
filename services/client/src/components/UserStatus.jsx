import React, {Component} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
import ListGroup from 'react-bootstrap/ListGroup';
import Container from 'react-bootstrap/Container';

class UserStatus extends Component {
    constructor(props) {
        super(props);
        this.state = {
            email: '',
            id: '',
            username: '',
            confirmed: '',
            admin: '',
            user_type: ''
        };
    }

    componentDidMount() {
        this.getUserStatus();
    }

    getUserStatus(event) {
        const options = {
            url: `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/status`,
            method: 'get',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${window.localStorage.refreshToken}`
            }
        };
        return axios(options)
            .then((res) => {
                this.setState({
                    email: res.data.data.email,
                    id: res.data.data.id,
                    username: res.data.data.username,
                    confirmed: String(res.data.data.confirmed),
                    admin: String(res.data.data.admin),
                    user_type: String(res.data.data.user_type)
                });
            })
            .catch((error) => {
                console.log(error);
            });
    }

    render() {
        if (!this.props.isAuthenticated()) {
            return (
                <div className="container">
                    <div className="row">
                        <div className="py-5 supplier-text text-left d-lg-block col-lg-6 col-sm-6">
                            <p>
                                You must be logged in to view this. Click <Link to="/login">here</Link> to log back in.
                            </p>
                        </div>
                    </div>
                </div>
            );
        }
        return (
            <Container className="mt-2">
                <ListGroup>
                    <ListGroup.Item>
                        <strong>User ID:</strong> {this.state.id}
                    </ListGroup.Item>
                    <ListGroup.Item>
                        <strong>Email:</strong> {this.state.email}
                    </ListGroup.Item>
                    <ListGroup.Item>
                        <strong>Username:</strong> {this.state.username}
                    </ListGroup.Item>
                    <ListGroup.Item>
                        <strong>Confirmed:</strong> {this.state.confirmed}
                    </ListGroup.Item>
                    <ListGroup.Item>
                        <strong>Admin:</strong> {this.state.admin}
                    </ListGroup.Item>
                    <ListGroup.Item>
                        <strong>User type:</strong> {this.state.user_type}
                    </ListGroup.Item>
                </ListGroup>
            </Container>
        );
    }
}

export default UserStatus;
