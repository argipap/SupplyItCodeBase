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



describe('Sign In', () => {
    it('should display the sign in form', () => {
        cy
            .visit('/login')
            .get('h1').contains('Sign In')
            .get('form')
            .get('input[disabled]')
            .get('.validation-list')
            .get('.validation-list > .error').first().contains(
            'Email is required.');
    });

    it('should allow a user to sign in', () => {
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

        // log a user out
        cy.get('.navbar-burger').click();
        cy.contains('Log Out').click();

        // log a user in
        cy
            .get('a').contains('Sign In').click()
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('input[type="submit"]').click()
            .wait(100);

        // assert user is redirected to '/'
        // assert '/' is displayed properly
        cy.contains('All Users');
        cy
            .get('table')
            .find('tbody > tr').last()
            .find('td').contains(username);
        cy.get('.notification.is-success').contains('Welcome!');
        cy.get('.navbar-burger').click();
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('USER STATUS')
                .get('.navbar-item').contains('Log Out')
                .get('.navbar-item').contains('Sign In').should('not.be.visible')
                .get('.navbar-item').contains('GET STARTED').should('not.be.visible')
                .get('.navbar-item').contains('HOW IT WORKS');
        });


        // log a user out
        cy.get('.navbar-burger').click();
        cy.get('a').contains('Log Out').click();

        // assert '/logout' is displayed properly
        cy.get('p').contains('You are now logged out');
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('USER STATUS').should('not.be.visible')
                .get('.navbar-item').contains('Log Out').should('not.be.visible')
                .get('.navbar-item').contains('Sign In')
                .get('.navbar-item').contains('GET STARTED')
                .get('.navbar-item').contains('HOW IT WORKS');
        });
    });

    it('should throw an error if the credentials are incorrect', () => {
        // attempt to log in
        cy
            .visit('/login')
            .get('input[name="email"]').type('incorrect@email.com')
            .get('input[name="password"]').type(password)
            .get('input[type="submit"]').click();

        // assert user login failed
        cy.contains('All Users').should('not.be.visible');
        cy.contains('Sign In');
        cy.get('.navbar-burger').click();
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('USER STATUS').should('not.be.visible')
                .get('.navbar-item').contains('Log Out').should('not.be.visible')
                .get('.navbar-item').contains('Sign In')
                .get('.navbar-item').contains('GET STARTED')
                .get('.navbar-item').contains('HOW IT WORKS')
        });
        cy
            .get('.notification.is-success').should('not.be.visible')
            .get('.notification.is-danger').contains('Email or password is invalid');

        // attempt to log in
        cy
            .get('a').contains('Sign In').click()
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type('incorrectpassword')
            .get('input[type="submit"]').click()
            .wait(100);

        // assert user login failed
        cy.contains('All Users').should('not.be.visible');
        cy.contains('Sign In');
        cy.get('.navbar-burger').click();
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('USER STATUS').should('not.be.visible')
                .get('.navbar-item').contains('Log Out').should('not.be.visible')
                .get('.navbar-item').contains('Sign In')
                .get('.navbar-item').contains('GET STARTED')
                .get('.navbar-item').contains('HOW IT WORKS')
        });
        cy
            .get('.notification.is-success').should('not.be.visible')
            .get('.notification.is-danger').contains('Email or password is invalid');
    });
});
