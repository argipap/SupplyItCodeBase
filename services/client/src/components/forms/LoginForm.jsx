import React from "react";
import PropTypes from "prop-types";
import {Formik} from "formik";
import * as Yup from "yup";
import {Redirect} from "react-router-dom";

import "./FormErrors.css";
import {Button, Col, Form} from "react-bootstrap";


const LoginForm = props => {
    if (props.isAuthenticated()) {
        return <Redirect to="/users"/>;
    }
    return (
        <div className="Login">
            <h1>Σύνδεση</h1>
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
                validationSchema={Yup.object().shape({
                    email: Yup.string()
                        .email("Enter a valid email.")
                        .required("Email is required."),
                    password: Yup.string()
                        .required("Password is required.")
                })}
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
                        <form onSubmit={handleSubmit}>
                            <Form.Row>
                                <Form.Group as={Col} controlId="formEmail">
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
                                        <div className="input-feedback">{errors.email}</div>
                                    )}
                                </Form.Group>
                                <Form.Group as={Col} controlId="formPassword">
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
                                    {errors.password && touched.password && (
                                        <div className="input-feedback">{errors.password}</div>
                                    )}
                                </Form.Group>
                            </Form.Row>
                            <Button variant="success" type="submit" className="button btn-square" value="Submit"
                                    disabled={isSubmitting}>
                                Σύνδεση
                            </Button>
                        </form>
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
