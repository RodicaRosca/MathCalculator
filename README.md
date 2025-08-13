# MathCalculator

## Solution Overview

MathCalculator is a modular, production-ready FastAPI microservice designed to provide secure mathematical computation services with a modern web interface, robust authentication, monitoring, and logging. The application is structured to be scalable, maintainable, and easily extensible for future features.

I chose **FastAPI** because it is a performant web framework for building APIs with Python. It provides OpenAPI documentation, supports asynchronous programming, and is easy to use for both small and large projects. FastAPI is ideal for scalable microservices like MathCalculator.

---

### Architecture & Components

- **FastAPI Backend**: The core of the application is built with FastAPI, providing high-performance RESTful endpoints for mathematical operations (factorial, Fibonacci, power, etc.), user authentication, and information retrieval.

- **Database Layer**: SQLAlchemy is used for ORM and database management, with models and schemas organized for clarity. User data and request logs are persisted for security and analytics.
  - *I chose SQLAlchemy because it is the most widely used Python ORM, supports multiple databases, and integrates seamlessly with FastAPI.*

- **Authentication**: Secure user registration and login are implemented using JWT tokens. Endpoints are protected, and user credentials are safely managed. The authentication logic is separated into dedicated controllers and services for clean code organization.
  - *I chose JWT because it is a stateless, secure, and scalable way to manage authentication in distributed systems.*

- **Frontend Integration**: Jinja2 templates are used to render dynamic HTML pages for user interaction, including login, signup, and math operation forms. The frontend controllers handle routing and rendering, providing a user-friendly interface.
  - *I chose Jinja2 because it is a flexible and powerful templating engine, well-supported in FastAPI and Python web projects.*

- **Monitoring & Observability**: Prometheus metrics are integrated using `prometheus_fastapi_instrumentator`, exposing application metrics for monitoring and alerting. Grafana is included for advanced visualization of metrics and dashboards. A `/health` endpoint is provided for health checks.
  - *I chose Prometheus and Grafana because they are industry standards for monitoring and visualization, easy to integrate with Docker and FastAPI, and provide real-time insights.*

- **Logging**: Kafka-based logging is included for distributed log management, enabling scalable and reliable log collection for auditing and debugging. Kafka can be monitored and visualized using external tools or integrated with Grafana dashboards.
  - *I chose Kafka because it is a robust, scalable solution for distributed logging and event streaming, suitable for microservices architectures.*

- **Testing**: Comprehensive unit and integration tests are provided using pytest and FastAPI's TestClient, covering authentication, endpoints, and mathematical logic. Redis dependencies are mocked in tests for reliability.
  - *I chose pytest because it is simple, powerful, and widely adopted for Python testing.*

- **Containerization**: The application includes a Dockerfile and docker-compose setup for easy deployment, including all dependencies (database, Kafka, Redis, Prometheus, Grafana, etc.).
  - *I chose Docker Compose for orchestrating multi-service environments, simplifying setup and deployment.*

---

### Key Features

- User registration and login with JWT authentication
- Secure, token-protected math endpoints (factorial, Fibonacci, power, etc.)
- Web frontend for interactive use
- Prometheus metrics and health checks for observability
- Grafana dashboards for real-time monitoring and visualization
- Kafka-based logging for distributed environments
- Modular codebase for easy maintenance and extension
- Full test coverage with mocked external dependencies

---

### Usage

#### 1. Prerequisites

- Docker and Docker Compose installed (recommended for easiest setup)
- Alternatively, Python 3.11+ and all dependencies from `requirements.txt`

#### 2. Running the Application

**With Docker Compose (recommended):**
```
docker-compose up --build
```
This will start the FastAPI app, database, Redis, Kafka, Prometheus, and Grafana. The backend will be available at `http://localhost:8000` by default.

- **Grafana**: [http://localhost:3000](http://localhost:3000) (default login: `admin` / `admin`)
- **Kafka**: Available for logging and monitoring. You can use tools like Kafdrop or external Kafka clients to inspect messages if needed.

**Without Docker (manual):**

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

#### 3. Accessing the Web Pages

- Open your browser and go to: [http://localhost:8000](http://localhost:8000)
- You will find pages for:
  - User login (`/login`)
  - User signup (`/signup`)
  - Math operations (e.g., `/factorial`, `/fibonacci`, `/pow`)
  - Home/index page (`/`)

#### 4. Using the API Endpoints

- You can use tools like curl, Postman, or the built-in OpenAPI docs at [http://localhost:8000/docs](http://localhost:8000/docs) to interact with the API.
- Example endpoints:
  - `POST /signup2` — Register a new user
  - `POST /token` — Obtain a JWT token
  - `GET /retrieve_info` — Retrieve user info (requires authentication)
  - `POST /factorial`, `/fibonacci`, `/pow` — Math operations

---

#### 5. Monitoring, Logging & Health

- **Prometheus metrics**: [http://localhost:8000/metrics](http://localhost:8000/metrics)
- **Prometheus UI**: [http://localhost:9090/query](http://localhost:9090/query)
- **Grafana dashboards**: [http://localhost:3000](http://localhost:3000) (default login: `admin` / `admin`). Pre-configured dashboards visualize Prometheus metrics and, optionally, Kafka statistics.
- **Kafka**: Running at the address specified in `docker-compose.yml`. Used for logging and can be monitored with external tools (e.g., Kafdrop, Grafana plugins).
  - View Kafka logs in terminal:
    ```
    docker-compose exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic apilogs --from-beginning
    ```
- **Health check**: [http://localhost:8000/health](http://localhost:8000/health)
- **Redis CLI**:
  ```
  docker-compose exec redis redis-cli
  # Then run: keys *
  ```

---

#### 6. Running Tests

- Run all tests with:
  ```
  pytest
  ```

---

This architecture ensures MathCalculator is robust, secure, and ready for both development and

![Diagram 1](docs/diagram.png)
