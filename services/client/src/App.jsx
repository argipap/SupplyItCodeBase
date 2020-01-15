import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';
import { Container, Row, Col } from 'react-bootstrap';
import styled from 'styled-components'

import UsersList from './components/UsersList';
import NavBar from './components/NavBar';
import Form from './components/forms/Form';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';
import Message from './components/Message';
import GetStarted from './components/GetStarted';
import Footer from './components/Footer';
import './components/Footer.css';
import Home from './components/Home';
import HowItWorks from './components/HowItWorks';
import BecomeSupplier from './components/BecomeSupplier';

class App extends Component {
	constructor() {
		super();
		this.state = {
			users: [],
			accessToken: null,
			email_confirmation: null,
			messageName: null,
			messageType: null,
			messageTitle: null,
            title: 'Supply It',
		};
		this.logoutUser = this.logoutUser.bind(this);
		this.loginUser = this.loginUser.bind(this);
		this.createMessage = this.createMessage.bind(this);
		this.removeMessage = this.removeMessage.bind(this);
		this.confirmUser = this.confirmUser.bind(this);
		this.validRefresh = this.validRefresh.bind(this);
		this.isAuthenticated = this.isAuthenticated.bind(this);
	}

	componentWillMount() {
		if (window.localStorage.getItem('refreshToken')) {
			this.setState({ email_confirmation: 'complete' });
		}
	}

	componentDidMount() {
		this.getUsers();
	}

	getUsers() {
		axios
			.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
			.then((res) => {
				this.setState({ users: res.data.data });
			})
			.catch((err) => {
				console.log(err);
			});
	}

	isAuthenticated = () => {
		if (this.state.accessToken || this.validRefresh()) {
			return true;
		}
		return false;
	};

	validRefresh = () => {
		const token = window.localStorage.getItem('refreshToken');
		if (token) {
			const options = {
				url: `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/refresh`,
				method: 'post',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				}
			};
			axios(options)
				.then((res) => {
					this.setState({ accessToken: res.data.access_token });
					this.getUsers();
					window.localStorage.setItem('refreshToken', res.data.refresh_token);
					return true;
				})
				.catch((err) => {
					return false;
				});
		}
		return false;
	};

	logoutUser = () => {
		window.localStorage.removeItem('refreshToken');
		this.setState({ accessToken: null });
		this.createMessage('Έχετε αποσυνδεθεί', 'Εις το επανιδείν!', 'danger');
	};

	loginUser(refresh_token, access_token) {
		if (refresh_token) {
			window.localStorage.setItem('refreshToken', refresh_token);
			this.setState({ accessToken: access_token });
			this.getUsers();
			this.createMessage('Καλώς Ήλθατε!', 'Η ομάδα του Supply IT σας ευχεται μια ευχάριστη διαμονή!', 'success');
		} else {
			this.state.email_confirmation = 'pending';
			this.createMessage(
				'Επιβεβαίωση email',
				'Παρακαλώ δείτε το inbox σας για να επιβεβαιώσετε το email σας.',
				'warning'
			);
		}
	}

	confirmUser() {
		this.state.email_confirmation = 'pending';
		this.createMessage(
			'Επιβεβαίωση email',
			'Παρακαλώ δείτε το inbox σας για να επιβεβαιώσετε το email σας.',
			'warning'
		);
	}

	createMessage(title = 'Title Check', name = 'Sanity Check', variant = 'success') {
		this.setState({
			messageTitle: title,
			messageName: name,
			messageType: variant
		});
		setTimeout(() => {
			this.removeMessage();
		}, 3000);
	}

	removeMessage() {
		this.setState({
			messageTitle: null,
			messageName: null,
			messageType: null
		});
    }


	render() {
		return (
			<main>
				<NavBar
					title={this.state.title}
					isAuthenticated={this.isAuthenticated}
					email={this.state.email}
					logoutUser={this.logoutUser}
				/>
				<content>


					{this.state.messageTitle &&
					this.state.messageName &&
					this.state.messageType && (
						<Message
							messageTitle={this.state.messageTitle}
							messageName={this.state.messageName}
							messageType={this.state.messageType}
							removeMessage={this.removeMessage}
						/>
					)}

					<Switch>
						<Route
							exact
							path="/"
							render={() => (
								<Home
									formType={'GetStarted'}
									loginUser={this.loginUser}
									createMessage={this.createMessage}
									removeMessage={this.removeMessage}
									isAuthenticated={this.isAuthenticated}
								/>
							)}
						/>
						<Route exact path="/users" render={() => <UsersList users={this.state.users} />} />
						<Route
							exact
							path="/howItWorks"
							render={() => <HowItWorks isAuthenticated={this.isAuthenticated} />}
						/>
						<Route
							exact
							path="/getStarted"
							render={() => (
								<GetStarted
									formType={'GetStarted'}
									loginUser={this.loginUser}
									confirmUser={this.confirmUser}
									createMessage={this.createMessage}
									isAuthenticated={this.isAuthenticated}
									email_confirmation={this.email_confirmation}
								/>
							)}
						/>
						<Route
							exact
							path="/becomeSupplier"
							render={() => (
								<BecomeSupplier
									formType={'BecomeSupplier'}
									isAuthenticated={this.isAuthenticated}
									loginUser={this.loginUser}
									confirmUser={this.confirmUser}
									createMessage={this.createMessage}
									email_confirmation={this.email_confirmation}
								/>
							)}
						/>
						<Route
							exact
							path="/login"
							render={() => (
								<Form
									formType={'Login'}
									isAuthenticated={this.isAuthenticated}
									loginUser={this.loginUser}
									createMessage={this.createMessage}
								/>
							)}
						/>
						<Route
							exact
							path="/logout"
							render={() => (
								<Logout logoutUser={this.logoutUser} isAuthenticated={this.isAuthenticated} />
							)}
						/>
						<Route
							exact
							path="/status"
							render={() => <UserStatus isAuthenticated={this.isAuthenticated} />}
						/>
					</Switch>
				</content>
				<Footer />
			</main>
		);
	}
}

export default App;
