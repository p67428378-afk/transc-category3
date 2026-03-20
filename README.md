# Automated Transaction Categorization System

This repository contains the code for an automated transaction categorization system, as described in Jira issue [SCRUM-65](https://bfsi-na-ai-engineering.atlassian.net/browse/SCRUM-65).

## Features

- Upload and categorize bank transaction data using an LLM-based engine.
- View spending trends and categorized data through a frontend dashboard.
- Backend API for managing transaction data.
- ETL pipeline for data cleaning, deduplication, and storage.

## Getting Started (Backend)

To run the backend application, follow these steps:

### Prerequisites

*   Docker and Docker Compose installed.

### Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/p67428378-afk/transc-category3.git
    cd transc-category3
    ```

2.  **Create a `.env` file:**

    Create a `.env` file in the `backend/` directory based on `backend/.env.example`:

    ```bash
    cp backend/.env.example backend/.env
    ```

    Edit `backend/.env` and configure your PostgreSQL database connection string. For local development with Docker Compose, the default in `.env.example` should work.

    ```ini
    DATABASE_URL="postgresql://user:password@db:5432/transactions_db"
    ```

3.  **Build and run with Docker Compose:**

    From the root of the repository, run:

    ```bash
    docker-compose -f docker-compose.yml up --build
    ```

    This will:

    *   Build the Docker image for the backend API.
    *   Start a PostgreSQL database container.
    *   Run the FastAPI application.

    The API will be accessible at `http://localhost:8000`.

### API Endpoints

*   **POST /api/transactions/upload**
    *   Upload a CSV file containing transaction data.
    *   Example using `curl`:
        ```bash
        curl -X POST -H "Content-Type: multipart/form-data" -F "file=@/path/to/your/transactions.csv" http://localhost:8000/api/transactions/upload
        ```

*   **GET /api/reports/categorized**
    *   Retrieve all categorized transactions.
    *   Example using `curl`:
        ```bash
        curl http://localhost:8000/api/reports/categorized
        ```

## Project Structure

```
.
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── .env.example
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── etl_pipeline.py
│   ├── llm_service.py
│   └── requirements.txt
└── docker-compose.yml
```
