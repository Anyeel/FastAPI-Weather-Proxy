# FastAPI Weather Proxy Backend

A asynchronous proxy API for OpenWeatherMap built with **FastAPI** and **PostgreSQL**.

This project acts as an intermediary layer between the frontend client and the external weather provider. It maps
official city IDs, fetches live weather data, and caches the results in a local database to drastically minimize
unnecessary external API calls and reduce latency.

---

## Features

- **Asynchronous:** Built with FastAPI and `httpx` for non-blocking, concurrent API requests.
- **Smart Caching*:* Validates requests against a local PostgreSQL database. If a city ID is missing, the system
  automatically fetches, registers, and caches it.
- **Optimized:** Implements a Singleton pattern (Lazy Initialization) for the HTTP client to reuse connections.
- **Robust Error Handling:** Centralized exception handling gracefully maps external network or provider errors into
  standard FastAPI HTTP responses.
- **Tested:** Comprehensive test suite using `pytest` to ensure reliability without consuming from the real
  OpenWeatherMap API.

---

## Configuration & Setup

This project uses environment variables to manage API keys and database connections.

### 1. Prerequisites

- Python 3.10+
- Docker and Docker Compose (to run the database)
- An API Key from [OpenWeatherMap](https://openweathermap.org/api)

### 2. Environment Variables

Create a `.env` file at the **root** of the repo and fill in your specific values:

| Variable                    | Description                         | Example / Default                                        |
|:----------------------------|:------------------------------------|:---------------------------------------------------------|
| **OPENWEATHERMAP_API_KEY**  | Your private API key                | `abcdef123456...`                                        |
| **OPENWEATHERMAP_BASE_URL** | The base endpoint                   | `https://api.openweathermap.org/data/2.5`                |
| **DATABASE_URL**            | Async DB connection string          | `postgresql+asyncpg://root:pass@localhost:5432/postgres` |
| **PGSQL_VOLUME**            | Local folder path for persistent DB | `~/pgsql`                                                |
| **PGSQL_PORT_MAPPING**      | Docker port mapping                 | `5432:5432`                                              |
| **PGSQL_ADMIN_PASS**        | Super admin password for SQL server | `your_secure_password`                                   |

> **Note:** Never commit your `.env` file to version control. It is already included in `.gitignore`.

---

## Infrastructure (Database)

The project requires PostgreSQL 18. We manage this via Docker to ensure a consistent development environment.

### Spin up the Database

From the **root** folder of the project, start the container:

```bash
docker compose -f db.docker-compose.yml up -d
```

*(To stop the database later, run: `docker compose -f db.docker-compose.yml stop`)*

---

## Running the Application

Once the database is running, set up your Python environment and start the server.
*(Note: Steps 1 & 2 are usually already satisfied automatically if you are opening the project in PyCharm).*

1. **Navigate to the root directory and create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

2. **Activate the environment:**
   ```bash
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI server:**
   ```bash
   # Run this from the root folder so it finds the backend module
   uvicorn backend.main:app --reload
   ```

Navigate to **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** in your browser to explore the interactive API
documentation.

---

## Usage Guide & Endpoints

This API strictly uses official OpenWeatherMap City IDs. You can search for a city on
the [OpenWeatherMap website](https://openweathermap.org/find) to find its ID (e.g.,
`https://openweathermap.org/city/3117735` -> ID is `3117735`).

### Core Endpoints

- **Current Weather (Single):** `GET /weather/{city_id}`
- **Current Weather (Batch):** `GET /weather/?cities={id_1},{id_2}`
- **5-Day Forecast (Batch):** `GET /forecast/?cities={id_1},{id_2}`

---

## Database Operations

You can interact directly with the PostgreSQL container to verify data persistence and cache status.

**Check registered cities:**

```bash
docker exec -it pgsql psql -U root -d postgres -c "SELECT * FROM cities;"
```

**Verify the weather cache and timestamps:**

```bash
docker exec -it pgsql psql -U root -d postgres -c "SELECT * FROM weather_information;"
```

**Wipe the database and start fresh (Deletes the volume):**

```bash
docker compose -f db.docker-compose.yml down -v
```

---

## Testing

The test suite ensures application integrity by mocking external HTTP requests and database sessions. To run the tests:

```bash
# Ensure your virtual environment is activated
python -m pytest
```
