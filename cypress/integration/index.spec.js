describe('Index', () => {
    it('should display the page correctly if a user is not logged in', () => {
        cy
            .visit('/')
            .get('h1').contains('ALL YOUR SUPPLIERS')
            .get('.navbar-burger').click()
            .get('a').contains('USER STATUS').should('not.be.visible')
            .get('a').contains('HOME')
            .get('a').contains('GET STARTED')
            .get('a').contains('HOW IT WORKS')
            .get('a').contains('BECOME A SUPPLIER')
            .get('a').contains('Sign In')
            .get('.notification.is-success').should('not.be.visible');
    });
});
