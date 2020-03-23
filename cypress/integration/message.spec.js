const randomstring = require('randomstring');

const username = randomstring.generate();
const email = '26edbe8f-5b62-4620-b617-0cad9e4a725e@mailslurp.com';
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
describe('Message', () => {
    it(`should display flash messages correctly`, () => {
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
            .get('button[value="Submit"]').click();

        // assert flash messages are removed when user clicks the 'x'
        cy
            .get('.fade.toast').contains('Επιβεβαίωση email')
            .get('.close').click()
            .get('.fade.toast').should('not.be.visible');

        //then get last email
        cy.waitForLatestEmail(inboxId).then((registrationEmail) => {
            var el = document.createElement('html');
            emailBody = registrationEmail.body;
            el.innerHTML = emailBody;
            let res = el.getElementsByTagName('a')[0].href;
            cy.request(res);
        });

        // then login
        cy.visit('/login')
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('button[value="Submit"]').click();

        // log a user out
        cy.get('.navbar-collapse').click();
        cy.contains('Αποσύνδεση').click();

        // attempt to log in with wrong email
        cy
            .visit('/login')
            .get('input[name="email"]').type('incorrect@email.com')
            .get('input[name="password"]').type(password)
            .get('button[value="Submit"]').click()
            .wait(100);

        // assert correct message is flashed
        cy
            .get('.fade.toast').contains('Email or password is invalid');

        // attempt to login with the correct email
        cy
            .get('input[name="email"]').clear().type(email)
            .get('input[name="password"]').clear().type(password)
            .get('button[value="Submit"]').click()
            .wait(100);

        // assert flash message is removed when a new message is flashed
        cy
            .get('.toast-header').contains('Καλώς Ήλθατε!');

        // log a user out
        cy.get('.navbar-collapse').click();
        cy.contains('Αποσύνδεση').click();

        // log a user in
        cy
            .contains('Σύνδεση').click()
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('button[value="Submit"]').click()
            .wait(100);

        // assert flash message is removed after three seconds
        cy
            .get('.toast-header').contains('Καλώς Ήλθατε!')
            .wait(5000)
            .get('.fade.toast').should('not.be.visible');
    });
});