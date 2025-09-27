# FastAPI Microservices Template: MongoDB Full-Stack Edition with uv

This repository contains a comprehensive, production-ready template for building scalable, modern web applications using a microservices architecture. It is designed for financial services applications, adhering strictly to SOLID principles and leveraging a powerful, modern technology stack.

## Table of Contents
1. [High-Level Architecture](#high-level-architecture)
2. [Technology Stack](#technology-stack)
3. [Core Features and Microservices](#core-features-and-microservices)
4. [SOLID Principles Implementation](#solid-principles-implementation)
5. [Project Structure](#project-structure)
6. [Key Configurations & File Examples](#key-configurations--file-examples)
    - [uv & `pyproject.toml`](#uv--pyprojecttoml)
    - [FastAPI `main.py`](#fastapi-mainpy)
    - [Beanie Models `models.py`](#beanie-models-modelspy)
    - [Frontend `vite.config.ts`](#frontend-viteconfigts)
    - [Dockerfile with `uv`](#dockerfile-with-uv)
    - [`docker-compose.yml`](#docker-composeyml)
7. [Setup and Local Development](#setup-and-local-development)
8. [Testing Strategy](#testing-strategy)
9. [Scaling and Performance](#scaling-and-performance)

---

## 1. High-Level Architecture

The architecture is designed as a set of loosely coupled microservices communicating via a lightweight API Gateway. The frontend interacts with the gateway, which routes requests to the appropriate backend service. This design ensures that services can be developed, deployed, and scaled independently.

```mermaid
graph TD
    subgraph "Client-Side"
        A[Browser - React App]
    end

    subgraph "API Layer"
        B(API Gateway - FastAPI)
    end

    subgraph "Backend Microservices (uv Projects)"
        C(Auth & Authz Service)
        D(Account Mgmt Service)
        E(Transaction Service)
        F(Risk & Fraud Service - ML)
    end

    subgraph "Database"
        G[(MongoDB)]
    end

    subgraph "External Services"
      H{{Email Service - SendGrid/SMTP}}
    end

    A -- "HTTPS/REST" --> B
    B -- "Routes to" --> C
    B -- "Routes to" --> D
    B -- "Routes to" --> E
    B -- "Routes to" --> F

    C -- "Manages Users & JWT" --> G
    D -- "Manages Profiles" --> G
    E -- "Processes Transactions" --> G
    F -- "Analyzes Data" --> G
    C -- "Sends Password Reset" --> H

    linkStyle 0 stroke:#333,stroke-width:2px;
    linkStyle 1 stroke:#333,stroke-width:2px;
    linkStyle 2 stroke:#333,stroke-width:2px;
    linkStyle 3 stroke:#333,stroke-width:2px;
    linkStyle 4 stroke:#333,stroke-width:2px;
    linkStyle 5 stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;
    linkStyle 6 stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;
    linkStyle 7 stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;
    linkStyle 8 stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;
    linkStyle 9 stroke:#333,stroke-width:2px;

```

## 2. Technology Stack

- **Backend**: FastAPI, Python 3.11+, Uvicorn
- **Frontend**: React (Vite), TypeScript, Chakra UI
- **Database**: MongoDB with Beanie (Pydantic-based ODM)
- **Python Project Management**: `uv`
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest (backend), Playwright (E2E)
- **Authentication**: JWT, Passlib (for hashing)
- **Frontend Client**: Auto-generated via OpenAPI

## 3. Core Features and Microservices

- **Authentication & Authorization Service**: Manages JWT-based auth, password hashing (bcrypt), and email-based password recovery.
- **Account Management Service**: Handles user profiles, registration, and account settings.
- **Transaction Processing Service**: Securely processes financial transactions with async workflows.
- **Risk and Fraud Detection Service**: Integrates a `scikit-learn` model to detect anomalies in transactions.
- **API Gateway**: A lightweight FastAPI service to unify the microservices under a single entry point.

## 4. SOLID Principles Implementation

- **Single Responsibility Principle (SRP)**: Each microservice has a single, well-defined purpose (e.g., `auth-service` only handles authentication). Within a service, FastAPI routers separate concerns further (e.g., password reset logic is separate from token generation). `uv` enforces this by managing isolated `pyproject.toml` files for each service, preventing dependency bleed.
- **Open-Closed Principle (OCP)**: Services are open for extension but closed for modification. For example, the `risk-service` can support new ML models by implementing a common `FraudDetectionModel` abstract base class. FastAPI's dependency injection allows swapping implementations (e.g., different email services) without changing the core business logic.
- **Dependency Inversion Principle (DIP)**: High-level modules do not depend on low-level modules; both depend on abstractions. FastAPI's `Depends` system is a prime example. Instead of directly instantiating a database client, our endpoints depend on an abstract `get_db` function, which provides a session. This decouples our business logic from the database implementation and makes testing easier.

## 5. Project Structure

```
/
├── .github/
│   └── workflows/
│       └── ci.yml          # CI pipeline with uv caching
├── auth-service/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── core/
│   │       └── security.py # JWT and password hashing
│   ├── pyproject.toml      # Managed by uv
│   └── Dockerfile          # Optimized for uv
├── account-service/
│   ├── app/
│   │   └── main.py
│   ├── pyproject.toml
│   └── Dockerfile
├── transaction-service/
│   ├── app/
│   │   └── main.py
│   ├── pyproject.toml
│   └── Dockerfile
├── risk-service/
│   ├── app/
│   │   └── main.py
│   ├── pyproject.toml
│   └── Dockerfile
├── client/                   # Auto-generated frontend client
│   └── src/
│       └── index.ts
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
├── shared/                   # Shared library (optional, for monorepo setups)
│   ├── pyproject.toml
│   └── shared_lib/
│       ├── database.py       # Beanie initialization
│       └── models.py         # Shared Pydantic/Beanie models
├── docker-compose.yml
└── README.md
```

## 6. Key Configurations & File Examples

### uv & `pyproject.toml`
Each backend service has its own `pyproject.toml`, managed by `uv`.

**Example: `auth-service/pyproject.toml`**
```toml
[project]
name = "auth-service"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "pydantic",
    "pydantic-settings",
    "beanie",
    "motor",
    "passlib[bcrypt]",
    "python-jose[cryptography]",
    "sendgrid", # or your preferred email library
]

[project.optional-dependencies]
dev = [
    "pytest",
    "httpx",
]
```

### FastAPI `main.py`
A minimal entry point for a service.

**Example: `transaction-service/app/main.py` (Pseudocode)**
```python
from fastapi import FastAPI, Depends
from beanie import PydanticObjectId
from shared_lib.models import Transaction, User
from shared_lib.database import init_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/transactions/", response_model=Transaction)
async def create_transaction(transaction: Transaction, current_user: User = Depends(get_current_user)):
    # Dependency injection handles getting the logged-in user
    # Business logic for processing the transaction
    await transaction.insert()
    # Potentially notify risk-service via an async call
    return transaction
```

### Beanie Models `models.py`
Located in the `shared` library for reuse across services.

**Example: `shared/shared_lib/models.py`**
```python
from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(Document):
    email: EmailStr
    hashed_password: str
    is_active: bool = True

    class Settings:
        name = "users"

class Transaction(Document):
    amount: float
    description: str
    sender_id: str
    receiver_id: str

    class Settings:
        name = "transactions"
```

### Frontend `vite.config.ts`
Configuration for the React frontend build process.
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Required for Docker
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://api-gateway:8000', // Proxy to the API gateway
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
```

### Dockerfile with `uv`
A multi-stage Dockerfile for efficient, fast, and small production images.

**Example: `auth-service/Dockerfile`**
```Dockerfile
# 1. Builder stage: Install dependencies with uv
FROM python:3.11-slim as builder

# Install uv
RUN pip install uv

WORKDIR /app

# Copy only the dependency file and install
COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml

# 2. Final stage: Copy installed dependencies and source code
FROM python:3.11-slim

WORKDIR /app

# Copy virtual env from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source code
COPY ./app /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `docker-compose.yml`
Orchestrates the entire stack for local development.
```yaml
version: '3.8'

services:
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password

  auth-service:
    build: ./auth-service
    ports:
      - "8001:8000"
    environment:
      - DATABASE_URL=mongodb://admin:password@mongo:27017
      - SENDGRID_API_KEY=${SENDGRID_API_KEY}
    volumes:
      - ./auth-service/app:/app
    depends_on:
      - mongo

  # ... (other services: account, transaction, risk)

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev # Use a dev-specific Dockerfile for hot-reloading
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src # Mount source for hot-reloading
    depends_on:
      - auth-service # And other backend services

volumes:
  mongo_data:
```

## 7. Setup and Local Development

1. **Clone the repository.**
2. **Configure Environment Variables**: Create a `.env` file in the root and add secrets like `SENDGRID_API_KEY`. The `docker-compose.yml` can be configured to use it.
3. **Initialize Python Projects**: Navigate to each service directory (e.g., `auth-service/`) and run `uv init` followed by `uv sync` to create a virtual environment and install dependencies locally.
4. **Generate Frontend Client**:
   ```bash
   # Get the OpenAPI schema from the running gateway
   curl http://localhost:8000/openapi.json > openapi.json
   # Generate client
   npx @openapitools/openapi-generator-cli generate -i openapi.json -g typescript-axios -o ./client
   ```
5. **Run the Stack**:
   ```bash
   docker-compose up --build
   ```
   The frontend will be available at `http://localhost:3000` and the API gateway at `http://localhost:8000`.

## 8. Testing Strategy

- **Unit & Integration Tests (Pytest)**: Each microservice contains its own suite of tests. Use `pytest` and `httpx` for testing API endpoints. For database interactions, use `mongomock` to mock MongoDB. Run tests with `uv run pytest`.
- **End-to-End Tests (Playwright)**: A dedicated test suite in the root or `frontend` directory will use Playwright to simulate user flows across the entire application, from UI interactions in the React app to backend data validation.

## 9. Scaling and Performance

- **Horizontal Scaling**: The microservices architecture allows individual services to be scaled horizontally based on load. For instance, the `risk-service` can be scaled up during peak transaction times.
- **Database Scaling**: MongoDB supports sharding and replica sets for high availability and distributing load.
- **Optimized Builds**:
    - **Frontend**: Vite's production build (`npm run build`) creates highly optimized, static assets.
    - **Backend**: Multi-stage Dockerfiles with `uv` create lean container images for faster deployments. `uv`'s fast dependency resolution speeds up CI/CD pipelines.
- **Async Everywhere**: FastAPI and Beanie's async capabilities ensure non-blocking I/O, maximizing throughput.