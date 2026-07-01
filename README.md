# FastAPI WeatherProxy 🌤️ 

![Angular](https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Cypress](https://img.shields.io/badge/Cypress-17202C?style=for-the-badge&logo=cypress&logoColor=white)
![Material Design](https://img.shields.io/badge/Material_Design-757575?style=for-the-badge&logo=material-design&logoColor=white)

A full-stack web application that allows users to search for cities and view current weather and 5-day forecasts. 

## Architecture
This project strictly follows a decoupled, API-driven architecture separated into two main environments:

### Frontend
- **Framework:** Angular (TypeScript)
- **UI Components:** Angular Material
- **Testing:** Cypress (E2E)
- **State Management:** Angular Signals & RxJS

### Backend
- **Framework:** FastAPI (Python)
- **Validation:** Pydantic
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL (Containerized)

## Repository Structure

The monorepo is divided into distinct domains to maintain a clean separation of concerns:

```text
📦 FastAPIWeatherProxy
 ┣ 📂 backend/               
 ┃ ┣ 📂 core/                # Configuration and settings
 ┃ ┣ 📂 database/            # SQLAlchemy setup and sessions
 ┃ ┣ 📂 models/              # DB Models
 ┃ ┣ 📂 routers/             # API Endpoints
 ┃ ┣ 📂 schemas/             # Pydantic validation models
 ┃ ┣ 📂 services/            # Business logic and external API calls
 ┃ ┗ 📜 main.py              # Application entry point
 ┣ 📂 frontend/              
 ┃ ┣ 📂 cypress/             # E2E Test suites
 ┃ ┗ 📂 src/                 # Angular components, services, and UI
 ┣ 📜 db.docker-compose.yml  # PostgreSQL database container configuration
 ┣ 📜 requirements.txt       # Python backend dependencies
 ┗ 📜 .env.example           # Environment variables template
````


## Getting Started

Because this is a decoupled architecture, the frontend and backend run as independent services. We have detailed setup instructions for each part of the stack.

Please select the environment you wish to configure:

### [Frontend Setup & Testing Guide](./frontend/README.md)

*Learn how to run the Angular development server and execute the Cypress E2E test suite.*

### [Backend Setup & Database Guide](./backend/README.md)

*Learn how to spin up the PostgreSQL database via Docker, set up your Python virtual environment, and run the FastAPI server.*

