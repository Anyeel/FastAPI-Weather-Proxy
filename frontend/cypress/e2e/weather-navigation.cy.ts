describe('Weather Navigation - Current Weather Flow', () => {

  beforeEach(() => {
    cy.visit('/');
  });

  /**
   * Weather
   * Verifies that selecting a city and navigating to 'Current'
   * correctly displays the weather information card.
   */
  it('Should navigate to Current Weather and display the city card', () => {
    cy.get('input[placeholder*="Type a city name"]').type('Granada');
    cy.get('mat-option').contains('Granada').should('be.visible').click();

    cy.contains('button', 'Current Weather').click();

    cy.url().should('include', '/current');
    cy.url().should('include', 'cities=');

    cy.get('mat-card').should('be.visible');

    cy.get('mat-card-title').should('contain', 'Granada');

    cy.get('mat-card-content').should('not.be.empty');
  });

  /**
   * Forecast
   * Validates the end-to-end flow from city selection to the 5-day forecast.
   * - Searches for and selects 'Amsterdam'.
   * - Triggers routing to the /forecast endpoint.
   * - Verifies the presence of the Material Table.
   * - Confirms that data rows are populated.
   */
  it('Should navigate to Forecast and display the Material Table with data', () => {
    cy.get('input[placeholder*="Type a city name"]').type('Amsterdam');
    cy.get('mat-option').contains('Amsterdam').should('be.visible').click();

    cy.contains('button', 'Forecast').click();

    cy.url().should('include', '/forecast?cities=');

    cy.get('table').should('be.visible');

    cy.get('tbody tr').should('have.length.greaterThan', 0);
  });
});
