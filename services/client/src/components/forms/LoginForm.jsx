import React from "react";
import PropTypes from "prop-types";
import {Formik} from "formik";
import {Redirect} from "react-router-dom";
import loginFormValidationRules from "./LoginFormValidations"
import "./FormErrors.css";
import {Button, Col, Form, InputGroup} from "react-bootstrap";
import Error from "./FormErrors";


const LoginForm = props => {
    if (props.isAuthenticated()) {
        return <Redirect to="/users"/>;
    }
    return (
        <div className="Login">
            <h1 className="title is-1" title="Login">Σύνδεση</h1>
            <hr/>
            <Formik
                initialValues={{
                    email: "",
                    password: ""
                }}
                onSubmit={(values, {setSubmitting, resetForm}) => {
                    props.handleLoginFormSubmit(values);
                    resetForm();
                    setSubmitting(false);
                }}
                validationSchema={loginFormValidationRules}
            >
                {props => {
                    const {
                        values,
                        touched,
                        errors,
                        isSubmitting,
                        handleChange,
                        handleBlur,
                        handleSubmit
                    } = props;

                    return (
                        <Form onSubmit={handleSubmit}>
                            <Form.Row>
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
                                        {errors.email && touched.email && (
                                            <InputGroup.Append>
                                                <InputGroup.Text>
                                                    <i className="fas fa-exclamation-triangle"/>
                                                </InputGroup.Text>
                                            </InputGroup.Append>
                                        )
                                        }
                                        {!errors.email && touched.email &&
                                        (
                                            <InputGroup.Append>
                                                <InputGroup.Text>
                                                    <i className="fas fa-check"/>
                                                </InputGroup.Text>
                                            </InputGroup.Append>
                                        )
                                        }
                                    </InputGroup>
                                    <Error touched={touched.email} message={errors.email}/>
                                </Form.Group>
                                <Form.Group as={Col} controlId="formPassword" role="formGroup">
                                    <InputGroup>
                                        <InputGroup.Prepend>
                                            <InputGroup.Text>
                                                <i className="fas fa-lock"/>
                                            </InputGroup.Text>
                                        </InputGroup.Prepend>
                                        <Form.Control
                                            className={
                                                errors.password && touched.password
                                                    ? "input error"
                                                    : "input"
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
                            <Button variant="success" type="submit" className="button btn-square" value="Submit"
                                    disabled={isSubmitting}>
                                Σύνδεση
                            </Button>
                        </Form>
                    );
                }}
            </Formik>
        </div>
    );
};


LoginForm.propTypes = {
    isAuthenticated: PropTypes.func.isRequired,
    handleLoginFormSubmit: PropTypes.func.isRequired,
};

export default LoginForm;
