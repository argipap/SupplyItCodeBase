import React, { Component } from 'react';
import axios from 'axios';
import { Redirect } from 'react-router-dom';
import { loginFormRules, registerFormRules } from './form-rules';
import FormErrors from './FormErrors';
import ConfirmationPending from '../ConfirmationPending';
import { Form, Col, Button } from 'react-bootstrap';

class Forms extends Component {
	constructor(props) {
		super(props);
		this.state = {
			formData: {
				username: '',
				email: '',
				password: '',
				firstName: '',
				lastName: '',
				shopName: '',
				streetName: '',
				streetNumber: '',
				city: '',
				zipCode: '',
				storeName: '',
				storeType: '',
				companyName: '',
				companyType: ''
			},
			registration_email: '',
			registerFormRules: registerFormRules,
			loginFormRules: loginFormRules,
			valid: false
		};
		this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
		this.handleFormChange = this.handleFormChange.bind(this);
	}

	componentDidMount() {
		this.clearForm();
		this.resetRules();
	}

	// componentDidUpdate(nextProps) {
	//     const {propsFormType} = this.props.formType;
	//     if (nextProps.formType !== propsFormType) {
	//         if (propsFormType) {
	//             this.clearForm();
	//             this.resetRules();
	//         }
	//     }
	// };
	//
	// componentWillReceiveProps(nextProps) {
	//     console.log("change from: " + this.props.formType + " to: " + nextProps.formType);
	//     if (this.props.formType !== nextProps.formType) {
	//         console.log("change from: " + this.props.formType + " to: " + nextProps.formType);
	//         this.clearForm();
	//         this.resetRules();
	//     }
	// };

	clearForm() {
		this.setState({
			formData: {
				username: '',
				email: '',
				password: '',
				firstName: '',
				lastName: '',
				shopName: '',
				streetName: '',
				streetNumber: '',
				city: '',
				zipCode: '',
				storeName: '',
				storeType: '',
				companyName: '',
				companyType: ''
			}
		});
	}

	validateForm() {
		// define self as this
		const self = this;
		// get form data
		const formData = this.state.formData;
		// reset all rules
		self.resetRules();
		// validate register form
		if (self.props.formType === 'GetStarted' || self.props.formType === 'BecomeSupplier') {
			const formRules = self.state.registerFormRules;
			if (formData.username.length > 3) formRules[0].valid = true;
			if (formData.email.length > 5) formRules[1].valid = true;
			if (this.validateEmail(formData.email)) formRules[2].valid = true;
			if (formData.password.length > 7) formRules[3].valid = true;
			self.setState({ registerFormRules: formRules });
			if (self.allTrue()) self.setState({ valid: true });
		}
		// validate login form
		if (self.props.formType === 'Login') {
			const formRules = self.state.loginFormRules;
			if (formData.email.length > 0) formRules[0].valid = true;
			if (formData.password.length > 0) formRules[1].valid = true;
			self.setState({ loginFormRules: formRules });
			if (self.allTrue()) self.setState({ valid: true });
		}
	}

	allTrue() {
		let formRules = loginFormRules;
		if (this.props.formType === 'GetStarted' || this.props.formType === 'BecomeSupplier') {
			formRules = registerFormRules;
		}
		for (const rule of formRules) {
			if (!rule.valid) return false;
		}
		return true;
	}

	resetRules() {
		const registerFormRules = this.state.registerFormRules;
		for (const rule of registerFormRules) {
			rule.valid = false;
		}
		this.setState({ registerFormRules: registerFormRules });
		const loginFormRules = this.state.loginFormRules;
		for (const rule of loginFormRules) {
			rule.valid = false;
		}
		this.setState({ loginFormRules: loginFormRules });
		this.setState({ valid: false });
	}

	validateEmail(email) {
		// eslint-disable-next-line
		var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		return re.test(email);
	}

	handleFormChange(event) {
		const obj = this.state.formData;
		obj[event.target.name] = event.target.value;
		this.setState(obj);
		this.validateForm();
	}

	handleUserFormSubmit(event) {
		event.preventDefault();
		const formType = this.props.formType;
		const data = {
			email: this.state.formData.email,
			password: this.state.formData.password
		};
		let operation = formType.toLowerCase();
		let user_type = '';
		if (formType === 'GetStarted') {
			user_type = '/retail';
			data.store_name = this.state.formData.storeName;
			data.store_type = this.state.formData.storeType;
		} else if (formType === 'BecomeSupplier') {
			user_type = '/wholesale';
			data.company_name = this.state.formData.companyName;
			data.company_type = this.state.formData.companyType;
		}
		if (formType === 'GetStarted' || formType === 'BecomeSupplier') {
			data.username = this.state.formData.username;
			data.street_name = this.state.formData.streetName;
			data.street_number = this.state.formData.streetNumber;
			data.city = this.state.formData.city;
			data.zip_code = this.state.formData.zipCode;
			operation = 'register';
		}

		const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth${user_type}/${operation}`;
		axios
			.post(url, data)
			.then((res) => {
				this.setState({ registration_email: this.state.formData.email });
				this.clearForm();
				if (operation === 'login') {
					this.props.loginUser(res.data.refresh_token, res.data.access_token);
				} else {
					this.props.confirmUser();
				}
			})
			.catch((err) => {
				this.props.createMessage(err.response.data.message, 'Invalid Username/Password');
			});
	}

	render() {
		if (this.props.isAuthenticated()) {
			return <Redirect to="/users" />;
		}
		if (this.props.email_confirmation === 'pending') {
			return (
				<ConfirmationPending email={this.state.registration_email} createMessage={this.props.createMessage} />
			);
		}
		let formRules = this.state.loginFormRules;
		if (this.props.formType === 'GetStarted' || this.props.formType === 'BecomeSupplier') {
			formRules = this.state.registerFormRules;
		}
		return (
			<div className={this.props.formType === 'Login' ? '' : ''}>
				<FormErrors formType={this.props.formType} formRules={formRules} />
				{this.props.formType === 'Login' && <h1>Σύνδεση</h1>}
				<hr />
				{this.props.formType !== 'GetStarted' && this.props.formType !== 'BecomeSupplier' && <br />}
				<form onSubmit={(event) => this.handleUserFormSubmit(event)}>
					{this.props.formType !== 'Login' && (
						<Form.Row>
							<Form.Group as={Col} controlId="formFirstName">
								{/* <Form.Label>Όνομα</Form.Label> */}
								<Form.Control
									name="firstName"
									type="text"
									placeholder="Όνομα"
									required
									value={this.state.formData.firstName}
									onChange={this.handleFormChange}
								/>
							</Form.Group>
							<Form.Group as={Col} controlId="formLastName">
								{/* <Form.Label>Επίθετο</Form.Label> */}
								<Form.Control
									name="lastName"
									className="input is-medium"
									type="text"
									placeholder="Επίθετο"
									required
									value={this.state.formData.lastName}
									onChange={this.handleFormChange}
								/>
							</Form.Group>
						</Form.Row>
					)}
					<Form.Row>
						{this.props.formType !== 'Login' && (
							<Form.Group as={Col} controlId="formUsername">
								{/* <Form.Label>Όνομα χρήστη</Form.Label> */}
								<Form.Control
									name="username"
									type="text"
									placeholder="Όνομα χρήστη"
									required
									value={this.state.formData.username}
									onChange={this.handleFormChange}
								/>
							</Form.Group>
						)}
						<Form.Group as={Col} controlId="formEmail">
							{/* <Form.Label>Email</Form.Label> */}
							<Form.Control
								name="email"
								type="email"
								placeholder="your@email.com"
								required
								value={this.state.formData.email}
								onChange={this.handleFormChange}
							/>
						</Form.Group>
						<Form.Group as={Col} controlId="formPassword">
							{/* <Form.Label>Password</Form.Label> */}
							<Form.Control
								name="password"
								type="password"
								placeholder="Κωδικός"
								required
								value={this.state.formData.password}
								onChange={this.handleFormChange}
							/>
						</Form.Group>
					</Form.Row>
					{this.props.formType !== 'Login' && (
						<Form.Row>
							<Form.Group as={Col} controlId="formAddress">
								{/* <Form.Label>Οδός</Form.Label> */}
								<Form.Control
									placeholder="Οδός"
									name="streetName"
									type="text"
									required
									value={this.state.formData.streetName}
									onChange={this.handleFormChange}
								/>
							</Form.Group>
							<Form.Group as={Col} controlId="formAddressNumber">
								{/* <Form.Label>Αριθμός διεύθυνσης</Form.Label> */}
								<Form.Control
									placeholder="Αριθμός"
									name="streetNumber"
									type="text"
									required
									value={this.state.formData.streetNumber}
									onChange={this.handleFormChange}
								/>
							</Form.Group>
						</Form.Row>
					)}
					{this.props.formType !== 'Login' && (
						<Form.Row>
							<Form.Group as={Col} controlId="formCity">
								{/* <Form.Label>Πόλη</Form.Label> */}
								<Form.Control
									placeholder="Πόλη"
									name="city"
									type="text"
									required
									value={this.state.formData.city}
									onChange={this.handleFormChange}
								/>
							</Form.Group>
							<Form.Group as={Col} controlId="formZip">
								{/* <Form.Label>Τ.Κ.</Form.Label> */}
								<Form.Control
									placeholder="Τ.Κ."
									name="zipCode"
									type="text"
									required
									value={this.state.formData.zipCode}
									onChange={this.handleFormChange}
								/>
							</Form.Group>
						</Form.Row>
					)}
					{this.props.formType === 'GetStarted' && (
						<Form.Row>
							<Form.Group as={Col} controlId="formStore">
								{/* <Form.Label>Όνομα εταιρείας</Form.Label> */}
								<Form.Control
									placeholder="Όνομα εταιρείας"
									name="storeName"
									type="text"
									required
									value={this.state.formData.storeName}
									onChange={this.handleFormChange}
								/>
							</Form.Group>
							<Form.Group as={Col} controlId="FormStoreType">
								{/* <Form.Label>Είδος μαγαζιού</Form.Label> */}
								<Form.Control
									as="select"
									placeholder="Είδος προιόντων"
									name="storeType"
									required
									value={this.state.formData.storeType}
									onChange={this.handleFormChange}
								>
									<option value="">Είδος μαγαζιού</option>
									<option value="other">Άλλο</option>
									<option value="coffee_and_drinks">Cafe - Bar</option>
									<option value="restaurant">Εστιατόριο</option>
									<option value="quick_service_restaurant">Fast-food</option>
								</Form.Control>
							</Form.Group>
						</Form.Row>
					)}
					{this.props.formType === 'BecomeSupplier' && (
						<Form.Row>
							<Form.Group as={Col} controlId="formStore">
								{/* <Form.Label>Όνομα εταιρείας</Form.Label> */}
								<Form.Control
									placeholder="Όνομα εταιρείας"
									name="companyName"
									type="text"
									required
									value={this.state.formData.companyName}
									onChange={this.handleFormChange}
								/>
							</Form.Group>
							<Form.Group as={Col} controlId="ForCompanyType">
								{/* <Form.Label>Είδος προιόντων</Form.Label> */}
								<Form.Control
									as="select"
									placeholder="Είδος προιόντων"
									name="companyType"
									required
									value={this.state.formData.companyType}
									onChange={this.handleFormChange}
								>
									<option value="">Είδος προιόντων</option>
									<option value="meat_and_poultry">Κρεατικά</option>
									<option value="coffee_and_drinks">Καφές και ποτά</option>
									<option value="other">Άλλο</option>
								</Form.Control>
							</Form.Group>
						</Form.Row>
					)}
					{this.props.formType !== 'Login' && (
						<Button  variant="danger" type="submit" className="button btn-square" value="Submit" disabled={!this.state.valid}>
							Εγγραφή
						</Button>
					)}
					{this.props.formType === 'Login' && (
						<Button variant="success" type="submit" className="button btn-square" value="Submit" disabled={!this.state.valid}>
							Σύνδεση
						</Button>
					)}
				</form>
			</div>
		);
	}
}

export default Forms;
