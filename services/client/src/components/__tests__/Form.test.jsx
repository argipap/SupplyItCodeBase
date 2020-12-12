/**
 * @jest-environment jest-environment-jsdom-sixteen
 **/

import React from "react";
import {screen, act, fireEvent, waitFor, cleanup} from "@testing-library/react";

import LoginForm from "../forms/LoginForm";
import RegisterForm from "../forms/RegisterForm";

// const props = {
//     handleLoginFormSubmit: jest.fn((email, password) => {
//         return Promise.resolve({email, password});
//     }),
//     isAuthenticated: jest.fn()
// };


const testData = [
    {
        formType: 'Login',
        title: 'Σύνδεση',
        formData: {
            email: 'test@email.com',
            password: '12345678'
        },
        loginUser: jest.fn(),
        handleLoginFormSubmit: jest.fn((email, password) => {
            return Promise.resolve({email, password});
        }),
        isAuthenticated: jest.fn()
    },
    {
        formType: 'GetStarted',
        title: 'GET STARTED',
        formData: {
            first_name: 'testName',
            last_name: 'testSurname',
            username: 'testUsername',
            email: 'test@email.com',
            password: '12345678',
            streetName: 'testStreet',
            streetNumber: '66',
            city: 'testCity',
            zipCode: '19009',
            storeName: 'testStore',
            storeType: 'Άλλο',

        },
        loginUser: jest.fn(),
        isAuthenticated: jest.fn(),
        handleRegisterFormSubmit: jest.fn(),
    },
    {
        formType: 'BecomeSupplier',
        title: 'BECOME A SUPPLIER',
        formData: {
            first_name: 'testName',
            last_name: 'testSurname',
            username: 'testUsername',
            email: 'test@email.com',
            password: '12345678',
            streetName: 'testStreet',
            streetNumber: '66',
            city: 'testCity',
            zipCode: '19009',
            companyName: 'testCompany',
            companyType: 'Άλλο'

        },
        loginUser: jest.fn(),
        isAuthenticated: jest.fn(),
        handleRegisterFormSubmit: jest.fn(),
    }
];


function renderWithComponent(props) {
    if (props.formType === 'Login') {
        renderWithRouter(<LoginForm {...props} />);
    } else {
        renderWithRouter(<RegisterForm {...props} />);
    }
}

function getSubmitMethod(props) {
    if (props.formType === 'Login') {
        return props.handleLoginFormSubmit;
    }
    else {
        return props.handleRegisterFormSubmit;
    }
}

function getEmailInput() {
    return screen.getByPlaceholderText("your@email.com");
}

function getPasswordInput() {
    return screen.getByPlaceholderText("Κωδικός");
}

function getSubmitButton() {
    return screen.getByRole("button");
}

function getFirstNameInput() {
    return screen.getByPlaceholderText("Όνομα");
}

function getLastNameInput() {
    return screen.getByPlaceholderText("Επίθετο");
}

function getUserNameInput() {
    return screen.getByPlaceholderText("Όνομα χρήστη");
}

function getStreetNameInput() {
    return screen.getByPlaceholderText("Οδός");
}

function getStreetNumberInput() {
    return screen.getByPlaceholderText("Αριθμός");
}

function getCityInput() {
    return screen.getByPlaceholderText("Πόλη");
}

function getZipCodeInput() {
    return screen.getByPlaceholderText("Τ.Κ.");
}

function getCompanyNameInput() {
    return screen.getByPlaceholderText("Όνομα εταιρείας");
}

function getCompanyTypeSelect() {
    return screen.getByPlaceholderText("Είδος προιόντων");
}

function getStoreNameInput() {
    return screen.getByPlaceholderText("Όνομα καταστήματος");
}

function getStoreTypeSelect() {
    return screen.getByPlaceholderText("Είδος προιόντων");
}

describe("When not authenticated", () => {
    testData.forEach((props) => {
        it(`${props.formType} Form renders properly`, () => {
            renderWithComponent(props);
            if (props.formType === 'Login') {
                expect(screen.getByTitle("Login")).toHaveClass("title");
            }
            const formGroups = screen.getAllByRole("formGroup");
            expect(formGroups.length).toBe(Object.keys(props.formData).length);
        });

        it(`${props.formType} renders with default props`, () => {
            renderWithComponent(props);
            const emailInput = getEmailInput();
            const passwordInput = getPasswordInput();
            const submitButton = getSubmitButton();
            expect(emailInput).toHaveAttribute("type", "email");
            expect(emailInput).not.toHaveValue();
            expect(passwordInput).toHaveAttribute("type", "password");
            expect(passwordInput).not.toHaveValue();
            expect(submitButton).toHaveValue("Submit");

        });

        it(`${props.formType} Form should not be submitted in case of empty or invalid input data`, () => {
            renderWithComponent(props);
            act(() => {
                const submitButton = getSubmitButton(props);
                fireEvent.click(submitButton);
            });
            waitFor(() => {
                expect(props.handleLoginFormSubmit).toBeCalled();
                expect(props.handleLoginFormSubmit).toHaveBeenCalledTimes(0);
            });
        });


        it(`${props.formType} Form submits the form properly`, async () => {
            renderWithComponent(props);
            const emailInput = getEmailInput();
            const passwordInput = getPasswordInput();
            const submitButton = getSubmitButton();
            expect(getSubmitMethod(props)).toHaveBeenCalledTimes(0);
            act(() => {
                if (props.formType !== 'Login') {
                    const firstNameInput = getFirstNameInput();
                    fireEvent.change(firstNameInput, {target: {value: props.formData.first_name}});
                    const lastNameInput = getLastNameInput();
                    fireEvent.change(lastNameInput, {target: {value: props.formData.last_name}});
                    const userNameInput = getUserNameInput();
                    fireEvent.change(userNameInput, {target: {value: props.formData.username}});
                    const cityInput = getCityInput();
                    fireEvent.change(cityInput, {target: {value: props.formData.city}});
                    const zipCodeInput = getZipCodeInput();
                    fireEvent.change(zipCodeInput, {target: {value: props.formData.zipCode}});
                    const streetNameInput = getStreetNameInput();
                    fireEvent.change(streetNameInput, {target: {value: props.formData.streetName}});
                    const streetNumberInput = getStreetNumberInput();
                    fireEvent.change(streetNumberInput, {target: {value: props.formData.streetNumber}});
                }
                if (props.formType === 'BecomeSupplier') {
                    const companyNameInput = getCompanyNameInput();
                    fireEvent.change(companyNameInput, {target: {value: props.formData.companyName}});
                    const companyTypeSelect = getCompanyTypeSelect();
                    fireEvent.change(companyTypeSelect, {target: {value: props.formData.companyType}});
                }
                if (props.formType === 'GetStarted') {
                    const storeNameInput = getStoreNameInput();
                    fireEvent.change(storeNameInput, {target: {value: props.formData.storeName}});
                    const storeTypeSelect = getStoreTypeSelect();
                    fireEvent.change(storeTypeSelect, {target: {value: props.formData.storeType}});
                }
                fireEvent.change(emailInput, {target: {value: props.formData.email}});
                fireEvent.change(passwordInput, {target: {value: props.formData.password}});
                fireEvent.click(submitButton);
            });
            waitFor(() => {
                expect(getSubmitMethod(props)).toBeCalled();
                expect(getSubmitMethod(props)).toHaveBeenCalledTimes(1);
            });
        });

        it(`${props.formType} Form renders a snapshot properly`, () => {
            if (props.formType === 'Login') {
                const {asFragment} = renderWithRouter(<LoginForm {...props} />);
                expect(asFragment()).toMatchSnapshot();
            } else {
                const {asFragment} = renderWithRouter(<RegisterForm {...props} />);
                expect(asFragment()).toMatchSnapshot();
            }
        });
    });
});


