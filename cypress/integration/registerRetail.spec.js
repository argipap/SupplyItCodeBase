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
describe('Register', () => {
    it('should display the registration form', () => {
        cy
            .visit('/getStarted')
            .get('h2').contains('Συμπληρώστε την παρακάτω φόρμα για να εγγραφείτε')
            .get('form');
            // .get('button[disabled]');
            // .get('.validation-list')
            // .get('.validation-list > .error').first().contains(
            // 'Username must be greater than 3 characters.');
    });

    it('should allow a user to register', () => {
        //delete user first
        cy.request({url: `/users/email/${email}`, method: 'DELETE', failOnStatusCode: false});
        const inboxId = email.split('@')[0];
        //first empty inbox from old emails
        cy.emptyInbox(inboxId);

        // register user
        cy
            .visit('/getStarted')
            .get('input[name="first_name"]').type(firstName)
            .get('input[name="last_name"]').type(lastName)
            .get('input[name="username"]').type(username)
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('input[name="street_name"]').type(streetName)
            .get('input[name="street_number"]').type(streetNumber)
            .get('input[name="city"]').type(city)
            .get('input[name="zip_code"]').type(zipCode)
            .get('input[name="store_name"]').type(storeName)
            .get('select[name="store_type"]').select(storeType)
            .get('button[value="Submit"]').click()
            .wait(100);


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
        
    });

    it('should validate the password field', () => {
        cy
            .visit('/getStarted')
            .get('h2').contains('Συμπληρώστε την παρακάτω φόρμα για να εγγραφείτε')
            .get('form');
            // .get('button[disabled]');
            // .get('.validation-list > .error').contains(
            // 'Password must be greater than 7 characters.')
            // .get('input[name="password"]').type(password)
            // .get('.validation-list')
            // .get('.validation-list > .error').contains(
            // 'Password must be greater than 7 characters.').should('not.be.visible')
            // .get('.validation-list > .success').contains(
            // 'Password must be greater than 7 characters.');
        cy.get('.navbar-nav').click();
        cy.get('a.btn-square').contains('Σύνδεση').click();
        cy.get('a.nav-link').contains('Δοκιμάστε').click();
        // cy.get('.validation-list > .error').contains(
        //     'Password must be greater than 7 characters.')
    });

    it('should throw an error if the username is taken', () => {
        // register user with duplicate user name
        cy
            .visit('/getStarted')
            .get('input[name="first_name"]').type(firstName)
            .get('input[name="last_name"]').type(lastName)
            .get('input[name="username"]').type(`${username}unique`)
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('input[name="street_name"]').type(streetName)
            .get('input[name="street_number"]').type(streetNumber)
            .get('input[name="city"]').type(city)
            .get('input[name="zip_code"]').type(zipCode)
            .get('input[name="store_name"]').type(storeName)
            .get('select[name="store_type"]').select(storeType)
            .get('button[value="Submit"]').click();

        // assert user registration failed
        cy.contains('All Users').should('not.be.visible');
        cy.contains('Συμπληρώστε την παρακάτω φόρμα για να εγγραφείτε');
        cy.get('.navbar-collapse').click();
        cy.get('.navbar-nav').within(() => {
            cy
                .get('a.nav-link').contains('Status').should('not.be.visible')
                .get('a.btn-square').contains('Αποσύνδεση').should('not.be.visible')
                .get('a.btn-square').contains('Σύνδεση')
                .get('a.nav-link').contains('Δοκιμάστε')
                .get('a.nav-link').contains('Γίνετε προμηθευτής');
        })
            .wait(100);
        cy
            .get('.fade.toast').contains('That user already exists.');
    });

    it('should throw an error if the email is taken', () => {
        // register user with duplicate email
        cy
            .visit('/getStarted')
            .get('input[name="first_name"]').type(firstName)
            .get('input[name="last_name"]').type(lastName)
            .get('input[name="username"]').type(`${username}unique`)
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type(password)
            .get('input[name="street_name"]').type(streetName)
            .get('input[name="street_number"]').type(streetNumber)
            .get('input[name="city"]').type(city)
            .get('input[name="zip_code"]').type(zipCode)
            .get('input[name="store_name"]').type(storeName)
            .get('select[name="store_type"]').select(storeType)
            .get('button[value="Submit"]').click();

        // assert user registration failed
        cy.contains('All Users').should('not.be.visible');
        cy.contains('Δοκιμάστε');
        cy.get('.navbar-collapse').click();
        cy.get('.navbar-nav').within(() => {
            cy
                .get('a.nav-link').contains('Status').should('not.be.visible')
                .get('a.btn-square').contains('Αποσύνδεση').should('not.be.visible')
                .get('a.btn-square').contains('Σύνδεση')
                .get('a.nav-link').contains('Δοκιμάστε')
                .get('a.nav-link').contains('Γίνετε προμηθευτής');
        })
            .wait(100);
        cy
            .get('.fade.toast').contains('That user already exists.');
    });
});
