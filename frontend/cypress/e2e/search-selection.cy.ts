describe('Weather Proxy Dashboard - E2E Functional Tests', () => {

  beforeEach(() => {
    cy.visit('/');
  });

  /**
   * Initial View State
   * Ensures the application boots with the correct UI constraints.
   * - Validates presence of the Header and Search Input.
   * - Verifies that navigation buttons are disabled until data is present.
   */
  it('Should initialize with a search bar and disabled navigation buttons', () => {
    cy.get('app-header').should('be.visible');

    cy.get('input[placeholder*="Type a city name"]').should('be.visible');

    cy.contains('button', 'Current Weather').should('be.disabled');
    cy.contains('button', 'Forecast').should('be.disabled');
  });

  /**
   * Multi-City Selection
   * Validates the integration between the Search Input, Material Autocomplete,
   * and the Global City Selection state (Chips).
   * - Searches for three specific cities: Granada, Madrid, and Amsterdam.
   * - Confirms each is added to the selection grid.
   * - Verifies that navigation is enabled once cities are selected.
   */
  it('Should search and add Granada, Madrid, and Amsterdam', () => {
    const cities = ['Granada', 'Madrid', 'Amsterdam'];

    cities.forEach(city => {
      // We use delay to mimic real typing speed so the backend can react
      cy.get('input[placeholder*="Type a city name"]').type(city, { delay: 100 });

      cy.get('mat-option').first().should('be.visible').click();

      cy.get('mat-chip-row').should('contain', city);

      cy.get('input[placeholder*="Type a city name"]').should('have.value', '');
    });

    // Do we have 3 chips?
    cy.get('mat-chip-row').should('have.length', 3);

    // Are the buttons now active?
    cy.contains('button', 'Current Weather').should('not.be.disabled');
    cy.contains('button', 'Forecast').should('not.be.disabled');
  });

});
