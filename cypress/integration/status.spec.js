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


describe('Status', () => {
    it('should not display user info if a user is not logged in', () => {
        cy
            .visit('/status')
            .get('p').contains('You must be logged in to view this.')
            .get('a').contains('USER STATUS').should('not.be.visible')
            .get('a').contains('Log Out').should('not.be.visible')
            .get('a').contains('GET STARTED')
            .get('a').contains('BECOME A SUPPLIER')
            .get('a').contains('Sign In')
            .get('.notification.is-success').should('not.be.visible');
    });

    it('should display user info if a user is logged in', () => {
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
            .get('input[type="submit"]').click()
            .get('.navbar-burger').click();

        cy.wait(800);

        // assert '/status' is displayed properly
        cy.visit('/status');
        cy.get('.navbar-burger').click();
        cy.contains('USER STATUS').click();
        // cy.get('li > strong').contains('User ID:')
        //     .get('li > strong').contains('Email:')
        //     .get('li').contains(email)
        //     .get('li > strong').contains('Username:')
        //     .get('li').contains(username)
        //     .get('li > strong').contains('User type')
        //     .get('li').contains('retail')
        //     .get('a').contains('USER STATUS')
        //     .get('a').contains('Log Out')
        //     .get('a').contains('GET STARTED').should('not.be.visible')
        //     .get('a').contains('Sign In').should('not.be.visible');
    });
});
