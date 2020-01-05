import React, {Component} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';

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
    };

    componentDidMount() {
        this.getUserStatus();
    };

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
                })
            })
            .catch((error) => {
                console.log(error);
            });
    };

    render() {
        if (!this.props.isAuthenticated) {
            return (
                <p>You must be logged in to view this. Click <Link to="/login">here</Link> to log back in.</p>
            )
        }
        return (
            <div>
                <ul>
                    <li><strong>User ID:</strong> {this.state.id}</li>
                    <li><strong>Email:</strong> {this.state.email}</li>
                    <li><strong>Username:</strong> {this.state.username}</li>
                    <li><strong>Confirmed:</strong> {this.state.confirmed}</li>
                    <li><strong>Admin:</strong> {this.state.admin}</li>
                    <li><strong>User type:</strong> {this.state.user_type}</li>
                </ul>
            </div>
        )
    };
}

export default UserStatus;