import React, {Component} from 'react';
import axios from "axios";
import {Route, Switch} from 'react-router-dom';

import UsersList from "./components/UsersList";
import NavBar from "./components/NavBar";
import Form from "./components/forms/Form";
import Logout from "./components/Logout";
import UserStatus from "./components/UserStatus";
import Message from "./components/Message";
import GetStarted from "./components/GetStarted";
import Footer from "./components/Footer";
import './components/Footer.css';
import Home from "./components/Home";
import HowItWorks from "./components/HowItWorks";
import BecomeSupplier from "./components/BecomeSupplier";


class App extends Component {
    constructor() {
        super();
        this.state = {
            users: [],
            isAuthenticated: false,
            messageName: null,
            messageType: null,
            title: 'SUPPLYIT'
        };
        this.logoutUser = this.logoutUser.bind(this);
        this.loginUser = this.loginUser.bind(this);
        this.createMessage = this.createMessage.bind(this);
        this.removeMessage = this.removeMessage.bind(this);
    }

    componentWillMount() {
        if (window.localStorage.getItem('authToken')) {
            this.setState({isAuthenticated: true});
        }
    };

    componentDidMount() {
        this.getUsers();
    };

    getUsers() {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
            .then((res) => {
                this.setState({users: res.data.data});
            })
            .catch((err) => {
                console.log(err);
            });
    };

    logoutUser() {
        window.localStorage.clear();
        this.setState({isAuthenticated: false});
    };

    loginUser(token) {
        window.localStorage.setItem('authToken', token);
        this.setState({isAuthenticated: true});
        this.getUsers();
        this.createMessage('Welcome!', 'success');
    };

    createMessage(name = 'Sanity Check', type = 'success') {
        this.setState({
            messageName: name,
            messageType: type
        });
        setTimeout(() => {
            this.removeMessage();
        }, 3000);
    };

    removeMessage() {
        this.setState({
            messageName: null,
            messageType: null
        });
    };

    render() {
        return (
            <div>
                <NavBar
                    title={this.state.title}
                    isAuthenticated={this.state.isAuthenticated}
                />
                <section className="section">
                    <div className="container">
                        {this.state.messageName && this.state.messageType &&
                        <Message
                            messageName={this.state.messageName}
                            messageType={this.state.messageType}
                            removeMessage={this.removeMessage}
                        />
                        }
                        <div className="columns">
                            <div className="column is-three-fifths">
                                <br/>
                                <Switch>
                                    <Route exact path='/' render={() => (
                                        <Home
                                            formType={'GetStarted'}
                                            loginUser={this.loginUser}
                                            createMessage={this.createMessage}
                                            removeMessage={this.removeMessage}
                                            isAuthenticated={this.state.isAuthenticated}
                                        />
                                    )}/>
                                    <Route exact path='/users' render={() => (
                                        <UsersList
                                            users={this.state.users}
                                        />
                                    )}/>
                                    <Route exact path='/howItWorks' render={() => (
                                        <HowItWorks
                                            isAuthenticated={this.state.isAuthenticated}
                                        />
                                    )}/>
                                    <Route exact path='/getStarted' render={() => (
                                        <GetStarted
                                            formType={'GetStarted'}
                                            loginUser={this.loginUser}
                                            createMessage={this.createMessage}
                                            removeMessage={this.removeMessage}
                                            isAuthenticated={this.state.isAuthenticated}
                                        />
                                    )}/>
                                    <Route exact path='/becomeSupplier' render={() => (
                                        <BecomeSupplier
                                            formType={'BecomeSupplier'}
                                            isAuthenticated={this.state.isAuthenticated}
                                            loginUser={this.loginUser}
                                            createMessage={this.createMessage}
                                        />
                                    )}/>
                                    <Route exact path='/login' render={() => (
                                        <Form
                                            formType={'Login'}
                                            isAuthenticated={this.state.isAuthenticated}
                                            loginUser={this.loginUser}
                                            createMessage={this.createMessage}
                                        />
                                    )}/>
                                    <Route exact path='/logout' render={() => (
                                        <Logout
                                            logoutUser={this.logoutUser}
                                            isAuthenticated={this.state.isAuthenticated}
                                        />
                                    )}/>
                                    <Route exact path='/status' render={() => (
                                        <UserStatus
                                            isAuthenticated={this.state.isAuthenticated}
                                        />
                                    )}/>
                                </Switch>
                            </div>
                        </div>
                    </div>
                </section>
                <Footer/>
            </div>
        )
    }
}

export default App;