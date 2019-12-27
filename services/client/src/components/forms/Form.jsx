import React, {Component} from 'react';
import axios from 'axios';
import {Redirect} from 'react-router-dom';
import {loginFormRules, registerFormRules} from "./form-rules";
import FormErrors from "./FormErrors";

class Form extends Component {
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
            registerFormRules: registerFormRules,
            loginFormRules: loginFormRules,
            valid: false
        };
        this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
        this.handleFormChange = this.handleFormChange.bind(this);
    };

    componentDidMount() {
        this.clearForm();
        this.resetRules();
    };


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
    };

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
            self.setState({registerFormRules: formRules});
            if (self.allTrue()) self.setState({valid: true});
        }
        // validate login form
        if (self.props.formType === 'Login') {
            const formRules = self.state.loginFormRules;
            if (formData.email.length > 0) formRules[0].valid = true;
            if (formData.password.length > 0) formRules[1].valid = true;
            self.setState({loginFormRules: formRules});
            if (self.allTrue()) self.setState({valid: true});
        }
    };

    allTrue() {
        let formRules = loginFormRules;
        if (this.props.formType === 'GetStarted' || this.props.formType === 'BecomeSupplier') {
            formRules = registerFormRules;
        }
        for (const rule of formRules) {
            if (!rule.valid) return false;
        }
        return true;
    };

    resetRules() {
        const registerFormRules = this.state.registerFormRules;
        for (const rule of registerFormRules) {
            rule.valid = false;
        }
        this.setState({registerFormRules: registerFormRules});
        const loginFormRules = this.state.loginFormRules;
        for (const rule of loginFormRules) {
            rule.valid = false;
        }
        this.setState({loginFormRules: loginFormRules});
        this.setState({valid: false});
    };

    validateEmail(email) {
        // eslint-disable-next-line
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    };

    handleFormChange(event) {
        const obj = this.state.formData;
        obj[event.target.name] = event.target.value;
        this.setState(obj);
        this.validateForm();
    };

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
        axios.post(url, data)
            .then((res) => {
                this.clearForm();
                this.props.loginUser(res.data.auth_token);
            })
            .catch((err) => {
                this.props.createMessage(err.response.data.message, 'danger');
            });
    };

    render() {
        if (this.props.isAuthenticated) {
            return <Redirect to='/users'/>;
        }
        let formRules = this.state.loginFormRules;
        if (this.props.formType === 'GetStarted' || this.props.formType === 'BecomeSupplier') {
            formRules = this.state.registerFormRules;
        }
        return (
            <div className={this.props.formType === "Login" ? "column is-three-fifths" : ""}>
                <FormErrors
                    formType={this.props.formType}
                    formRules={formRules}
                />
                {this.props.formType === 'Login' &&
                <h1 className="title is-2">Sign In</h1>
                }
                <hr/>
                {(this.props.formType !== 'GetStarted' && this.props.formType !== 'BecomeSupplier') &&
                <br/>
                }
                <form onSubmit={(event) => this.handleUserFormSubmit(event)}>
                    {(this.props.formType !== 'Login') &&
                    <div className="field is-grouped">
                        <p className="control is-expanded">
                            <input
                                name="firstName"
                                className="input is-medium"
                                type="text"
                                placeholder="First name"
                                required
                                value={this.state.formData.firstName}
                                onChange={this.handleFormChange}
                            />
                        </p>
                        <p className="control is-expanded">
                            <input
                                name="lastName"
                                className="input is-medium"
                                type="text"
                                placeholder="Last name"
                                required
                                value={this.state.formData.lastName}
                                onChange={this.handleFormChange}
                            />
                        </p>
                    </div>
                    }
                    {(this.props.formType !== 'Login') &&
                    <div className="field">
                        <input
                            name="username"
                            className="input is-medium"
                            type="text"
                            placeholder="Enter a username"
                            required
                            value={this.state.formData.username}
                            onChange={this.handleFormChange}
                        />
                    </div>
                    }
                    <div className="field">
                        <input
                            name="email"
                            className="input is-medium"
                            type="email"
                            placeholder="your@email.com"
                            required
                            value={this.state.formData.email}
                            onChange={this.handleFormChange}
                        />
                    </div>
                    <div className="field">
                        <input
                            name="password"
                            className="input is-medium"
                            type="password"
                            placeholder="Enter a password"
                            required
                            value={this.state.formData.password}
                            onChange={this.handleFormChange}
                        />
                    </div>
                    {(this.props.formType !== 'Login') &&
                    <div className="field is-grouped">
                        <p className="control is-expanded">
                            <input
                                name="streetName"
                                className="input is-medium"
                                type="text"
                                placeholder="street name"
                                required
                                value={this.state.formData.streetName}
                                onChange={this.handleFormChange}
                            />
                        </p>
                        <p className="control is-expanded">
                            <input
                                name="streetNumber"
                                className="input is-medium"
                                type="text"
                                placeholder="street number"
                                required
                                value={this.state.formData.streetNumber}
                                onChange={this.handleFormChange}
                            />
                        </p>
                    </div>
                    }
                    {(this.props.formType !== 'Login') &&
                    <div className="field is-grouped">
                        <p className="control is-expanded">
                            <input
                                name="city"
                                className="input is-medium"
                                type="text"
                                placeholder="city"
                                required
                                value={this.state.formData.city}
                                onChange={this.handleFormChange}
                            />
                        </p>
                        <p className="control is-expanded">
                            <input
                                name="zipCode"
                                className="input is-medium"
                                type="text"
                                placeholder="zip code"
                                required
                                value={this.state.formData.zipCode}
                                onChange={this.handleFormChange}
                            />
                        </p>
                    </div>
                    }
                    {(this.props.formType === 'GetStarted') &&
                    <div className="field">
                        <input
                            name="storeName"
                            className="input is-medium"
                            type="text"
                            placeholder="Store name"
                            required
                            value={this.state.formData.storeName}
                            onChange={this.handleFormChange}
                        />
                    </div>
                    }
                    {(this.props.formType === 'GetStarted') &&
                    <div className="field select">
                        <select
                            name="storeType"
                            className="input is-medium"
                            required
                            value={this.state.formData.storeType}
                            onChange={this.handleFormChange}>
                            <option value="other">other</option>
                            <option value="cafeBar">cafe-Bar</option>
                            <option value="restaurant">restaurant</option>
                            <option value="quick_service_restaurant">quick service restaurant</option>
                        </select>
                    </div>
                    }
                    {(this.props.formType === 'BecomeSupplier') &&
                    <div className="field">
                        <input
                            name="companyName"
                            className="input is-medium"
                            type="text"
                            placeholder="Company name"
                            required
                            value={this.state.formData.companyName}
                            onChange={this.handleFormChange}
                        />
                    </div>
                    }
                    {(this.props.formType === 'BecomeSupplier') &&
                    <div className="field select">
                        <select
                            name="companyType"
                            className="input is-medium"
                            required
                            value={this.state.formData.companyType}
                            onChange={this.handleFormChange}>
                            <option value="other">other</option>
                            <option value="meat_and_poultry">meat & poultry</option>
                            <option value="coffee_and_drinks">coffe & drinks</option>
                        </select>
                    </div>
                    }
                    <input
                        type="submit"
                        className="button is-primary is-medium is-fullwidth"
                        value="Submit"
                        disabled={!this.state.valid}
                    />
                </form>
            </div>
        )
    };
}

export default Form;