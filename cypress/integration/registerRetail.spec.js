const randomstring = require('randomstring');

const username = randomstring.generate();
const email = `${username}@test.com`;
const password = '12345678';
const firstName = 'Argi';
const lastName = 'Pap';
const streetName = 'Aigaiou';
const streetNumber = '46';
const city = 'Rafina';
const zipCode = '190 09';
const storeName = 'Argi Shop';
const storeType = 'cafeBar';


describe('Register', () => {
    it('should display the registration form', () => {
        cy
            .visit('/getStarted')
            .get('h1').contains('LET\'S GET STARTED')
            .get('form')
            .get('input[disabled]')
            .get('.validation-list')
            .get('.validation-list > .error').first().contains(
            'Username must be greater than 3 characters.');
    });

    it('should allow a user to register', () => {
        // register user
        cy
            .visit('/getStarted')
            .get('input[name="firstName"]').type(firstName)
            .get('input[name="lastName"]').type(lastName)
            .get('input[name="username"]').type(username)
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('input[name="streetName"]').type(streetName)
            .get('input[name="streetNumber"]').type(streetNumber)
            .get('input[name="city"]').type(city)
            .get('input[name="zipCode"]').type(zipCode)
            .get('input[name="storeName"]').type(storeName)
            .get('select[name="storeType"]').select(storeType)
            .get('input[type="submit"]').click();

        // assert user is redirected to '/'
        // assert '/' is displayed properly
        cy.contains('All Users');
        cy.contains(username);
        cy.get('.navbar-burger').click();
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('USER STATUS')
                .get('.navbar-item').contains('Log Out')
                .get('.navbar-item').contains('Sign In').should('not.be.visible')
                .get('.navbar-item').contains('GET STARTED').should('not.be.visible')
                .get('.navbar-item').contains('BECOME A SUPPLIER').should('not.be.visible');
        });
    });

    it('should validate the password field', () => {
        cy
            .visit('/getStarted')
            .get('h1').contains('LET\'S GET STARTED')
            .get('form')
            .get('input[disabled]')
            .get('.validation-list > .error').contains(
            'Password must be greater than 7 characters.')
            .get('input[name="password"]').type(password)
            .get('.validation-list')
            .get('.validation-list > .error').contains(
            'Password must be greater than 7 characters.').should('not.be.visible')
            .get('.validation-list > .success').contains(
            'Password must be greater than 7 characters.');
        cy.get('.navbar-burger').click();
        cy.get('.navbar-item').contains('Sign In').click();
        cy.get('.navbar-item').contains('GET STARTED').click();
        cy.get('.validation-list > .error').contains(
            'Password must be greater than 7 characters.')
    });

    it('should throw an error if the username is taken', () => {
        // register user with duplicate user name
        cy
            .visit('/getStarted')
            .get('input[name="firstName"]').type(firstName)
            .get('input[name="lastName"]').type(lastName)
            .get('input[name="username"]').type(`${username}unique`)
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('input[name="streetName"]').type(streetName)
            .get('input[name="streetNumber"]').type(streetNumber)
            .get('input[name="city"]').type(city)
            .get('input[name="zipCode"]').type(zipCode)
            .get('input[name="storeName"]').type(storeName)
            .get('select[name="storeType"]').select(storeType)
            .get('input[type="submit"]').click();

        // assert user registration failed
        cy.contains('All Users').should('not.be.visible');
        cy.contains('LET\'S GET STARTED');
        cy.get('.navbar-burger').click();
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('USER STATUS').should('not.be.visible')
                .get('.navbar-item').contains('Log Out').should('not.be.visible')
                .get('.navbar-item').contains('Sign In')
                .get('.navbar-item').contains('GET STARTED')
                .get('.navbar-item').contains('BECOME A SUPPLIER');
        });
        cy
            .get('.notification.is-success').should('not.be.visible')
            .get('.notification.is-danger').contains('That user already exists.');
    });

    it('should throw an error if the email is taken', () => {
        // register user with duplicate email
        cy
            .visit('/getStarted')
            .visit('/getStarted')
            .get('input[name="firstName"]').type(firstName)
            .get('input[name="lastName"]').type(lastName)
            .get('input[name="username"]').type(`${username}unique`)
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('input[name="streetName"]').type(streetName)
            .get('input[name="streetNumber"]').type(streetNumber)
            .get('input[name="city"]').type(city)
            .get('input[name="zipCode"]').type(zipCode)
            .get('input[name="storeName"]').type(storeName)
            .get('select[name="storeType"]').select(storeType)
            .get('input[type="submit"]').click();

        // assert user registration failed
        cy.contains('All Users').should('not.be.visible');
        cy.contains('GET STARTED');
        cy.get('.navbar-burger').click();
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('USER STATUS').should('not.be.visible')
                .get('.navbar-item').contains('Log Out').should('not.be.visible')
                .get('.navbar-item').contains('Sign In')
                .get('.navbar-item').contains('GET STARTED')
                .get('.navbar-item').contains('BECOME A SUPPLIER');
        });
        cy
            .get('.notification.is-success').should('not.be.visible')
            .get('.notification.is-danger').contains('That user already exists.');
    });
});
