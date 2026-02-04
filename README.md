# SmartMove Backend

This is the backend service for the SmartMove application, built with Flask.

## Table of Contents

-   [Features](#features)
-   [Setup](#setup)
    -   [Prerequisites](#prerequisites)
    -   [Local Installation](#local-installation)
    -   [Environment Variables](#environment-variables)
-   [Running the Application](#running-the-application)
-   [Database Migrations](#database-migrations)
-   [Testing](#testing)
-   [Celery Background Tasks](#celery-background-tasks)
-   [Deployment](#deployment)

## Features

(To be populated as features are implemented)

## Setup

### Prerequisites

-   Python 3.9+
-   pip (Python package installer)
-   (Optional) virtualenv or conda for virtual environments
-   PostgreSQL (recommended for production) or SQLite (for local development)
-   Redis (for Celery message broker)

### Local Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/smartmove-backend.git
    cd smartmove-backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables

Create a `.env` file in the root directory of the project, based on `.env.example`.

```ini
# .env file
SECRET_KEY='your_super_secret_key_here'
DATABASE_URL='sqlite:///app.db' # For local development with SQLite
# DATABASE_URL='postgresql://user:password@host:port/database' # For PostgreSQL
CELERY_BROKER_URL='redis://localhost:6379/0'
CELERY_RESULT_BACKEND='redis://localhost:6379/0'
# Add other environment variables as needed (e.g., API keys, email service credentials)
```

## Running the Application

For local development, you can run the Flask application directly:

```bash
python run.py
```

For production-like environments, use Gunicorn:

```bash
gunicorn --bind 0.0.0.0:${PORT:-8000} run:app
```
(Note: The gunicorn command here should be updated to reflect the `Dockerfile`'s CMD for consistency. The `wsgi:app` should likely be `run:app` based on the `Dockerfile` too.)

## Database Migrations

This project uses Flask-Migrate (Alembic) for database migrations.

To initialize a new migration:
```bash
flask db migrate -m "Initial migration"
```

To apply migrations:
```bash
flask db upgrade
```

To downgrade migrations:
```bash
flask db downgrade
```

## Testing

This project uses `pytest` for testing.

To run all tests:
```bash
pytest
```

## Celery Background Tasks

To run Celery workers for background tasks:

```bash
celery -A celery_app.celery_app worker --loglevel=info
```

## Deployment

Deployment is handled via Docker, with a `Dockerfile` configured for platforms like Railway. The `Dockerfile` handles database migrations automatically on startup.

---
**Note:** This `README.md` is a starting point and should be updated as the project evolves and specific features are implemented.
