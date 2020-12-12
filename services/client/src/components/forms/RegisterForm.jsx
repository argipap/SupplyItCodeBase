import React from "react";
import PropTypes from "prop-types";
import {Formik} from "formik";
import {Redirect} from "react-router-dom";

import "./FormErrors.css";
import {Button, Col, Form, InputGroup} from "react-bootstrap";
import registerFormValidationRules from "./RegisterFormValidations"
import Error from "./FormErrors";
import ConfirmationPending from "../ConfirmationPending";


const RegisterForm = props => {
    if (props.isAuthenticated()) {
        return <Redirect to="/users"/>;
    }
    if (props.email_confirmation === 'pending') {
        return (
            <ConfirmationPending createMessage={props.createMessage}/>
        );
    }
    return (
        <div className={"Register"}>
            <hr/>
            <br/>
            <Formik
                initialValues={{
                    username: "",
                    email: "",
                    password: "",
                    first_name: "",
                    last_name: "",
                    street_name: "",
                    street_number: "",
                    city: "",
                    zip_code: "",
                    store_name: "",
                    store_type: "",
                    company_name: "",
                    company_type: "",
                    formType: props.formType
                }}
                validationSchema={registerFormValidationRules}
                onSubmit={(values, {setSubmitting, resetForm}) => {
                    delete values.formType;
                    if (props.formType === "GetStarted") {
                        delete values.company_name;
                        delete values.company_type;
                    } else if (props.formType === "BecomeSupplier") {
                        delete values.store_name;
                        delete values.store_type;
                    }
                    props.handleRegisterFormSubmit(values);
                    resetForm();
                    setSubmitting(false);
                    window.scrollTo(0, 0);
                }}

            >
                {props => {
                    const {
                        values,
                        touched,
                        errors,
                        isSubmitting,
                        handleChange,
                        handleBlur,
                        handleSubmit,
                    } = props;

                    return (
                        <Form onSubmit={handleSubmit}>
                            <Form.Row>
                                <Form.Group as={Col} controlId="formfirst_name" role="formGroup">
                                    <InputGroup>
                                        <InputGroup.Prepend>
                                            <InputGroup.Text>
                                                <i className="fas fa-user"/>
                                            </InputGroup.Text>
                                        </InputGroup.Prepend>
                                        <Form.Control
                                            className={
                                                errors.first_name && touched.first_name ? "input error" : "input"
                                            }
                                            name="first_name"
                                            type="text"
                                            placeholder="Όνομα"
                                            value={values.first_name}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                    </InputGroup>
                                    <Error touched={touched.first_name} message={errors.first_name}/>
                                </Form.Group>
                                <Form.Group as={Col} controlId="formlast_name" role="formGroup">
                                    <InputGroup>
                                        <InputGroup.Prepend>
                                            <InputGroup.Text>
                                                <i className="fas fa-user-plus"/>
                                            </InputGroup.Text>
                                        </InputGroup.Prepend>
                                        <Form.Control
                                            className={
                                                errors.last_name && touched.last_name ? "input error " : "input"
                                            }
                                            name="last_name"
                                            type="text"
                                            placeholder="Επίθετο"
                                            value={values.last_name}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                    </InputGroup>
                                    <Error touched={touched.last_name} message={errors.last_name}/>
                                </Form.Group>
                            </Form.Row>
                            <Form.Row>
                                <Form.Group as={Col} controlId="formUsername" role="formGroup">
                                    <InputGroup>
                                        <InputGroup.Prepend>
                                            <InputGroup.Text>
                                                <i className="fas fa-user-secret"/>
                                            </InputGroup.Text>
                                        </InputGroup.Prepend>
                                        <Form.Control
                                            className={
                                                errors.username && touched.username ? "input error " : "input"
                                            }
                                            name="username"
                                            type="text"
                                            placeholder="Όνομα χρήστη"
                                            value={values.username}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                    </InputGroup>
                                    <Error touched={touched.username} message={errors.username}/>
                                </Form.Group>
                                <Form.Group as={Col} controlId="formEmail" role="formGroup">
                                    <InputGroup>
                                        <InputGroup.Prepend>
                                            <InputGroup.Text>
                                                <i className="fas fa-envelope"/>
                                            </InputGroup.Text>
                                        </InputGroup.Prepend>
                                        <Form.Control
                                            className={
                                                errors.email && touched.email ? "input error" : "input"
                                            }
                                            name="email"
                                            type="email"
                                            placeholder="your@email.com"
                                            value={values.email}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                    </InputGroup>
                                    <Error touched={touched.email} message={errors.email}/>
                                </Form.Group>
                                <Form.Group as={Col} controlId="formPassword" role="formGroup">
                                    <InputGroup>
                                        <InputGroup.Prepend>
                                            <InputGroup.Text>
                                                <i className="fas fa-key"/>
                                            </InputGroup.Text>
                                        </InputGroup.Prepend>
                                        <Form.Control
                                            className={
                                                errors.password && touched.password ? "input error" : "input"
                                            }
                                            name="password"
                                            type="password"
                                            placeholder="Κωδικός"
                                            value={values.password}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                    </InputGroup>
                                    <Error touched={touched.password} message={errors.password}/>
                                </Form.Group>
                            </Form.Row>
                            <Form.Row>
                                <Form.Group as={Col} controlId="formAddress" role="formGroup">
                                    <InputGroup>
                                        <InputGroup.Prepend>
                                            <InputGroup.Text>
                                                <i className="fas fa-home"/>
                                            </InputGroup.Text>
                                        </InputGroup.Prepend>
                                        <Form.Control
                                            className={
                                                errors.street_name && touched.street_name ? "input error" : "input"
                                            }
                                            placeholder="Οδός"
                                            name="street_name"
                                            type="text"
                                            value={values.street_name}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                    </InputGroup>
                                    <Error touched={touched.street_name} message={errors.street_name}/>
                                </Form.Group>
                                <Form.Group as={Col} controlId="formAddressNumber" role="formGroup">
                                    <InputGroup>
                                        <InputGroup.Prepend>
                                            <InputGroup.Text>
                                                <i className="fas fa-map-marker-alt"/>
                                            </InputGroup.Text>
                                        </InputGroup.Prepend>
                                        <Form.Control
                                            className={
                                                errors.street_number && touched.street_number ? "input error" : "input"
                                            }
                                            placeholder="Αριθμός"
                                            name="street_number"
                                            type="text"
                                            value={values.street_number}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                    </InputGroup>
                                    <Error touched={touched.street_number} message={errors.street_number}/>
                                </Form.Group>
                            </Form.Row>
                            <Form.Row>
                                <Form.Group as={Col} controlId="formCity" role="formGroup">
                                    <InputGroup>
                                        <InputGroup.Prepend>
                                            <InputGroup.Text>
                                                <i className="fas fa-building"/>
                                            </InputGroup.Text>
                                        </InputGroup.Prepend>
                                        <Form.Control
                                            className={
                                                errors.city && touched.city ? "input error" : "input"
                                            }
                                            placeholder="Πόλη"
                                            name="city"
                                            type="text"
                                            value={values.city}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                    </InputGroup>
                                    <Error touched={touched.city} message={errors.city}/>
                                </Form.Group>
                                <Form.Group as={Col} controlId="formZip" role="formGroup">
                                    <InputGroup>
                                        <InputGroup.Prepend>
                                            <InputGroup.Text>
                                                <i className="fas fa-archive"/>
                                            </InputGroup.Text>
                                        </InputGroup.Prepend>
                                        <Form.Control
                                            className={
                                                errors.zip_code && touched.zip_code ? "input error" : "input"
                                            }
                                            placeholder="Τ.Κ."
                                            name="zip_code"
                                            type="text"
                                            value={values.zip_code}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                    </InputGroup>
                                    <Error touched={touched.zip_code} message={errors.zip_code}/>
                                </Form.Group>
                            </Form.Row>
                            {values.formType === "GetStarted" && (
                                <Form.Row>
                                    <Form.Group as={Col} controlId="formStore" role="formGroup">
                                        <InputGroup>
                                            <InputGroup.Prepend>
                                                <InputGroup.Text>
                                                    <i className="fas fa-warehouse"/>
                                                </InputGroup.Text>
                                            </InputGroup.Prepend>
                                            <Form.Control
                                                className={
                                                    errors.store_name && touched.store_name ? "input error" : "input"
                                                }
                                                placeholder="Όνομα καταστήματος"
                                                name="store_name"
                                                type="text"
                                                value={values.store_name}
                                                onChange={handleChange}
                                                onBlur={handleBlur}
                                            />
                                        </InputGroup>
                                        <Error touched={touched.store_name} message={errors.store_name}/>
                                    </Form.Group>
                                    <Form.Group as={Col} controlId="formstore_type" role="formGroup">
                                        <Form.Control
                                            className={
                                                errors.store_type && touched.store_type ? "input error" : "input"
                                            }
                                            as="select"
                                            placeholder="Είδος προιόντων"
                                            name="store_type"
                                            value={values.store_type}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        >
                                            <option value="">Είδος καταστήματος</option>
                                            <option value="other">Άλλο</option>
                                            <option value="coffee_and_drinks">Cafe - Bar</option>
                                            <option value="restaurant">Εστιατόριο</option>
                                            <option value="quick_service_restaurant">Fast-food</option>
                                        </Form.Control>
                                        <Error touched={touched.store_type} message={errors.store_type}/>
                                    </Form.Group>
                                </Form.Row>
                            )}
                            {values.formType === 'BecomeSupplier' && (
                                <Form.Row>
                                    <Form.Group as={Col} controlId="formCompany" role="formGroup">
                                        <Form.Control
                                            className={
                                                errors.company_name && touched.company_name ? "input error" : "input"
                                            }
                                            placeholder="Όνομα εταιρείας"
                                            name="company_name"
                                            type="text"
                                            value={values.company_name}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                        <Error touched={touched.company_name} message={errors.company_name}/>
                                    </Form.Group>
                                    <Form.Group as={Col} controlId="Formcompany_type" role="formGroup">
                                        <Form.Control
                                            className={
                                                errors.company_type && touched.company_type ? "input error" : "input"
                                            }
                                            as="select"
                                            placeholder="Είδος προιόντων"
                                            name="company_type"
                                            value={values.company_type}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        >
                                            <option value="">Είδος προιόντων</option>
                                            <option value="meat_and_poultry">Κρεατικά</option>
                                            <option value="coffee_and_drinks">Καφές και ποτά</option>
                                            <option value="other">Άλλο</option>
                                        </Form.Control>
                                        <Error touched={touched.company_type} message={errors.company_type}/>
                                    </Form.Group>
                                </Form.Row>
                            )}
                            <Button variant="danger" type="submit" className="button btn-square" value="Submit"
                                    disabled={isSubmitting}>
                                Εγγραφή
                            </Button>
                        </Form>
                    )
                        ;
                }}
            </Formik>
        </div>
    );
};

RegisterForm.propTypes = {
    handleRegisterFormSubmit: PropTypes.func.isRequired,
    isAuthenticated: PropTypes.func.isRequired
};


export default RegisterForm;