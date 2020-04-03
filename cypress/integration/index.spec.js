describe('Index', () => {
    it('should display the page correctly if a user is not logged in', () => {
        cy
            .visit('/')
            .get('h1').contains('Όλοι οι αγαπημένοι προμηθευτές σας με ένα click!')
            .get('.navbar-collapse').click()
            .get('a.nav-link').contains('Status').should('not.be.visible')
            .get('a.nav-link').contains('Αρχική')
            .get('a.nav-link').contains('Δοκιμάστε')
            .get('a.nav-link').contains('Πως δουλεύει')
            .get('a.nav-link').contains('Γίνετε προμηθευτής')
            .get('a.btn-square').contains('Σύνδεση');
            // .get('.notification.is-success').should('not.be.visible');
    });
});
