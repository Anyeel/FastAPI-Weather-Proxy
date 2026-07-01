describe('Global Error Handling', () => {

  beforeEach(() => {
    cy.visit('/');
  });

  /**
   * API Failure
   * Validates the application's ability to handle a 500 Internal Server Error.
   * - Intercepts the outgoing search request and forces a mock 500 response.
   * - Triggers a search action.
   * - Verifies that the global error banner/component becomes visible with the error message.
   */
  it('should display a global error message when the backend returns a 500 status', () => {
    cy.intercept('GET', '**/weather/search*', {
      statusCode: 500,
      body: { detail: 'Simulated Backend Crash' }
    }).as('searchError');

    cy.get('input[placeholder*="Type a city name"]').type('Stormwind');

    cy.wait('@searchError');

    cy.contains('Simulated Backend Crash').should('be.visible');
  });

});
