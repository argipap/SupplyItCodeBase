const {MailSlurp} = require('mailslurp-client');
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
describe('Sign In', () => {
    it('should display the sign in form', () => {
        cy
            .visit('/login')
            .get('h1').contains('Σύνδεση')
            .get('form')
            .get('button[disabled]');
        
        // .get('.validation-list')
        // .get('.validation-list > .error').first().contains(
        // 'Email is required.');
    });

    it('should allow a user to sign in', () => {
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


        //
        // });


        cy.visit('/login')
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('button[value="Submit"]').click();

        // log a user out
        cy.get('.navbar-collapse').click();
        cy.contains('Αποσύνδεση').click();

        // log a user in
        cy
            .get('a').contains('Σύνδεση').click()
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('button[value="Submit"]').click()
            .wait(100);

        // assert user is redirected to '/'
        // assert '/' is displayed properly
        cy.contains('Χρήστες');
        cy
            .get('table')
            .find('tbody > tr').last()
            .find('td').contains(username);
        cy.get('.fade.toast').contains('Καλώς Ήλθατε!');
        cy.get('.navbar-collapse').click();
        cy.get('.ml-auto.navbar-nav').within(() => {
            cy
                .get('.nav-link').contains('Status')
                .get('a.btn-square').contains('Αποσύνδεση')
                .get('a.btn-square').contains('Σύνδεση').should('not.be.visible')
                .get('.nav-link').contains('Δοκιμάστε').should('not.be.visible')
                .get('.nav-link').contains('Πως δουλεύει');
        });


        // log a user out
        cy.get('a.btn-square').click()
            .wait(100);

        // assert '/logout' is displayed properly
        cy.get('.fade.toast').contains('Εις το επανιδείν!');
        cy.get('.ml-auto.navbar-nav').within(() => {
            cy
                .get('.nav-link').contains('Status').should('not.be.visible')
                .get('a.btn-square').contains('Αποσύνδεση').should('not.be.visible')
                .get('a.btn-square').contains('Σύνδεση')
                .get('.nav-link').contains('Δοκιμάστε')
                .get('.nav-link').contains('Πως δουλεύει');
        });
    });

    it('should throw an error if the credentials are incorrect', () => {
        // attempt to log in
        cy
            .visit('/login')
            .get('input[name="email"]').type('incorrect@email.com')
            .get('input[name="password"]').type(password)
            .get('button[value="Submit"]').click();

        // assert user login failed
        cy.contains('Χρήστες').should('not.be.visible');
        cy.contains('Σύνδεση');
        cy.get('.navbar-collapse').click();
        cy.get('.ml-auto.navbar-nav').within(() => {
            cy
                .get('.nav-link').contains('Status').should('not.be.visible')
                .get('a.btn-square').contains('Αποσύνδεση').should('not.be.visible')
                .get('a.btn-square').contains('Σύνδεση')
                .get('.nav-link').contains('Δοκιμάστε')
                .get('.nav-link').contains('Πως δουλεύει')
        })
            .wait(100);
        cy
            // .get('.notification.is-success').should('not.be.visible')
            .get('.fade.toast').contains('Email or password is invalid');

        // attempt to log in
        cy
            .get('a').contains('Σύνδεση').click()
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type('incorrectpassword')
            .get('button[value="Submit"]').click()
            .wait(100);

        // assert user login failed
        cy.contains('Χρήστες').should('not.be.visible');
        cy.get('.navbar-collapse').click();
        cy.get('.ml-auto.navbar-nav').within(() => {
            cy
                .get('.nav-link').contains('Status').should('not.be.visible')
                .get('a.btn-square').contains('Αποσύνδεση').should('not.be.visible')
                .get('a.btn-square').contains('Σύνδεση')
                .get('.nav-link').contains('Δοκιμάστε')
                .get('.nav-link').contains('Πως δουλεύει')
        })
            .wait(100);
        cy
            // .get('.notification.is-success').should('not.be.visible')
            .get('.fade.toast').contains('Email or password is invalid');
    });
});