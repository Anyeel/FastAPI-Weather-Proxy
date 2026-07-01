# Frontend: Weather API Dashboard

This is the client-facing application for the Weather Proxy system. It provides a real-time, reactive interface for monitoring current weather conditions and 5-day forecasts across multiple cities simultaneously.

## Tech Stack

- **Framework:** Angular 19
- **State Management:** Angular Signals & RxJS
- **UI Library:** Angular Material
- **Styling:** Sass (SCSS)
- **E2E Testing:** Cypress

---

## Architecture

This project enforces a strict separation of concerns to maintain scalability:

- **`core/`**: The brain of the app. Contains global services (`WeatherService`, `CityService`), data models, and the main header components.
- **`features/`**: The visual business logic. Contains the routable views, specifically the `CurrentWeather` (Material Cards) and `Forecast` (Material Table) components.
- **`environments/`**: Configuration files managing API endpoints (connecting to the local Python FastAPI server).

---

## Getting Started

### 1. Prerequisites
Ensure you have [Node.js](https://nodejs.org/) installed.

### 2. Environment Configuration
By default, the application looks for the Python backend at `http://127.0.0.1:8000`. 
You can also update the `apiUrl` for production in: `src/environments/environment.ts`

### 3. Installation & Local Server
Navigate into the `frontend` directory and install the dependencies:

```bash
npm install
````

Start the local development server:

```bash
ng serve
```

Once the server is running, open your browser and navigate to **[http://localhost:4200/](https://www.google.com/search?q=http://localhost:4200/)**. The application will automatically reload if you change any of the source files.

-----

## End-to-End Testing (Cypress)

We have implemented a rigorous suite of 5 Critical Flow tests using Cypress to guarantee application stability. These tests cover initial UI state, multi-city search logic, routing data verification, and global API error resilience.

**To run the tests in the interactive Cypress UI:**

```bash
npx cypress open
```

*(Select "E2E Testing" -\> Choose your browser -\> Click a test file to watch it run).*

**To run the tests headlessly (ideal for CI/CD):**

```bash
npx cypress run
```

-----

## Building for Production

To compile the project for production, run:

```bash
ng build
```

This will optimize your application for performance and speed, storing the build artifacts in the `dist/` directory, ready to be deployed to a static hosting service (like Nginx, Vercel, or AWS S3).
