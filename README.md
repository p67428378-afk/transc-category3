# Automated Transaction Categorization System

This project implements an Automated Transaction Categorization System as described in Jira issue [SCRUM-65](https://bfsi-na-ai-engineering.atlassian.net/browse/SCRUM-65) and its High-Level Design (HLD) document.

## Project Structure

- `backend/`: Contains the FastAPI application, database models, ETL pipeline, and mock LLM service.
- `frontend/`: (Placeholder) Will contain the web dashboard.

## Getting Started

### Prerequisites

- Docker (recommended) or Python 3.9+
- `pip`

### Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/p67428378-afk/transc-category3.git
    cd transc-category3
    git checkout SCRUM-65
    ```

2.  **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    Create a `.env` file in the project root based on `.env.example`.

    ```ini
    # .env
    DATABASE_URL="postgresql://user:password@localhost:5432/transactions_db"
    ```

### Running the Application

1.  **Start the PostgreSQL database (e.g., using Docker):**

    ```bash
    docker run --name transaction-db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=transactions_db -p 5432:5432 -d postgres:13
    ```

2.  **Run database migrations (if any) and create tables:**

    (This step will be added once Alembic is integrated or a simple table creation script is available.)

3.  **Start the FastAPI backend:**

    ```bash
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
    ```

    The API will be available at `http://localhost:8000`.

## API Endpoints

- `POST /api/transactions/upload`: Upload a CSV file for categorization.
- `GET /api/reports/categorized`: Retrieve categorized transaction data.

## Running Tests

```bash
pytest
```
