MathCalculator is a microservice designed to provide mathematical services with a web interface. The appplication provides authentication, monitoring, caching, containerization and logging. The core of the application is build with FastAPI and has RESTful endpoints for each mathematical operation and authentication.

QLAlchemy is used for ORM and database management, with models and schemas organized for clarity. User data and request logs are persisted for security and analytics.

Secure user registration and login are implemented using JWT tokens. Endpoints are protected, and user credentials are safely managed. The authentication logic is separated into controllers and services for a clean organization.

Jinja2 templates are used to render dynamic HTML pages for user interaction, including login, signup, and math operation forms. The frontend controllers handle routing and rendering, providing a user-friendly interface.

Prometheus metrics are integrated using `prometheus_fastapi_instrumentator`, exposing application metrics for monitoring and alerting. Grafana is included for advanced visualization of metrics and dashboards. A `/health` endpoint is provided for health checks.

Kafka logging is included for log management. 

Unit and integration tests are provided using pytest and covers authentication, endpoints, and mathematical logic. Redis dependencies are mocked in tests for reliability.

The application includes a Dockerfile and docker-compose setup for easy deployment, including all dependencies (database, Kafka, Redis, Prometheus, Grafana, etc.).


# Key Features

- User registration and login with JWT authentication
- Secure, token-protected math endpoints (factorial, Fibonacci, power)
- Web frontend for interactive use
- Prometheus metrics and health checks for observability
- Grafana dashboards for real-time monitoring and visualization
- Kafka-based logging for distributed environments
- Modular codebase for easy maintenance and extension
- Full test coverage with mocked external dependencies


# Prerequisites

- Docker and Docker Compose installed (recommended for easiest setup)
- Alternatively, Python 3.11+ and all dependencies from `requirements.txt`

# Running the Application

# Docker

```
docker-compose up --build
```

This will start the FastAPI app, database, Redis, Kafka, Prometheus, and Grafana. The backend will be available at `http://localhost:8000`.


# Grafana

Will be available at [http://localhost:3000] (default login: `admin` / `admin`).
Kafka will be running and available for logging and monitoring. You can use tools like Kafdrop or external Kafka clients to inspect messages if needed.

# Without Docker

1. Set required environment variables (e.g., `SECRET_KEY`).
2. Start any required services (e.g., Redis, Kafka, database) as described in the project documentation or docker-compose file.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   uvicorn app:app --reload
   ```

# Accessing the Web Pages

- Open your browser and go to: [http://localhost:8000]
- Pages:
  - User login (`/login`)
  - User signup (`/signup`)
  - Math operations (e.g., `/factorial`, `/fibonacci`, `/pow`)
  - Home/index page (`/`)

# Using the API Endpoints

- [http://localhost:8000/docs] 
- Endpoints:
  - `POST /signup2` — Register a new user
  - `POST /token` — Obtain a JWT token
  - `GET /retrieve_info` — Retrieve user info (requires authentication)
  - `POST /factorial`, `/fibonacci`, `/pow` — Math operations


# Monitoring, Logging & Health

- Prometheus metrics: [http://localhost:8000/metrics]

- Grafana dashboards: [http://localhost:3000] (default login: `admin` / `admin`)

- Kafka: docker-compose exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic apilogs --from-beginning

- Health check: [http://localhost:8000/health]

- Redis: docker exec -it redis redis-cli
keys * (for all cached items)
keys factorial:* (for caching a certain type)


# Running Tests

- Run all tests with:
  ```
  pytest
  ```

This architecture ensures MathCalculator is robust, secure, and ready for both development and production environments.