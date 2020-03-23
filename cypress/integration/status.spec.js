const randomstring = require('randomstring');

const username = randomstring.generate();
// const email = '26edbe8f-5b62-4620-b617-0cad9e4a725e@mailslurp.com';
const email = '79a7f01e-cd8e-4071-8b40-5fd016d311de@mailslurp.com';
const password = '12345678';
const firstName = 'Argi';
const lastName = 'Pap';
const streetName = 'Aigaiou';
const streetNumber = '46';
const city = 'Rafina';
const zipCode = '190 09';
const storeName = 'Argi Shop';
const storeType = 'other';

let emailBody;
describe('Status', () => {
    it('should not display user info if a user is not logged in', () => {
        cy
            .visit('/status')
            .get('p').contains('You must be logged in to view this.')
            .get('a').contains('Status').should('not.be.visible')
            .get('a').contains('Αποσύνδεση').should('not.be.visible')
            .get('a').contains('Δοκιμάστε')
            .get('a').contains('Γίνετε προμηθευτής')
            .get('a').contains('Σύνδεση');
    });

    it('should display user info if a user is logged in', () => {
        //delete user first
        cy.request({url: `/users/email/${email}`, method: 'DELETE', failOnStatusCode: false});
        const inboxId = email.split('@')[0];
        //first empty inbox from old emails
        cy.emptyInbox(inboxId);

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
            .get('button[value="Submit"]').click()
            .wait(100);

        cy.get('.fade.toast').contains('Επιβεβαίωση email');

        //then get last email
        cy.waitForLatestEmail(inboxId).then((registrationEmail) => {
            var el = document.createElement('html');
            emailBody = registrationEmail.body;
            el.innerHTML = emailBody;
            let res = el.getElementsByTagName('a')[0].href;
            cy.request(res);
        });

        cy.visit('/login')
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('button[value="Submit"]').click()
            .wait(500);

        // assert '/status' is displayed properly
        cy.visit('/status');
        cy.get('.navbar-nav').click();
        cy.contains('Status').click();
        cy.get('.list-group-item > strong').contains('User ID:')
            .get('.list-group-item > strong').contains('Email:')
            .get('.list-group-item').contains(email)
            .get('.list-group-item > strong').contains('Username:')
            .get('.list-group-item').contains(username)
            .get('.list-group-item > strong').contains('Confirmed:')
            .get('.list-group-item').contains('true')
            .get('.list-group-item > strong').contains('Admin:')
            .get('.list-group-item').contains('false')
            .get('.list-group-item > strong').contains('User type')
            .get('.list-group-item').contains('retail')
            .get('a.nav-link').contains('Status')
            .get('a.btn-square').contains('Αποσύνδεση')
            .get('a.nav-link').contains('Δοκιμάστε').should('not.be.visible')
            .get('a.btn-square').contains('Σύνδεση').should('not.be.visible');
    });
});
