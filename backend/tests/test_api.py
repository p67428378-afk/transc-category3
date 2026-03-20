from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.models import Transaction
from datetime import datetime
import io

# Assuming 'client' and 'db_session' fixtures are available from conftest.py

def test_upload_transactions_success(client: TestClient, db_session: Session):
    csv_content = "date,description,amount\n2023-01-01,Starbucks Coffee,5.50\n2023-01-02,Monthly Rent Payment,1200.00"
    
    response = client.post(
        "/api/transactions/upload",
        files={"file": ("transactions.csv", csv_content, "text/csv")}
    )
    assert response.status_code == 200
    assert "Successfully processed 2 transactions." in response.json()["message"]
    
    transactions = db_session.query(Transaction).all()
    assert len(transactions) == 2
    assert transactions[0].description == "Starbucks Coffee"
    assert transactions[0].final_category == "Food"
    assert transactions[1].description == "Monthly Rent Payment"
    assert transactions[1].final_category == "Rent"

def test_upload_transactions_invalid_file_type(client: TestClient):
    response = client.post(
        "/api/transactions/upload",
        files={"file": ("transactions.txt", "not a csv", "text/plain")}
    )
    assert response.status_code == 400
    assert "Only CSV files are allowed" in response.json()["detail"]

def test_upload_transactions_malformed_csv(client: TestClient):
    csv_content = "date,description\n2023-01-01,Starbucks Coffee"
    response = client.post(
        "/api/transactions/upload",
        files={"file": ("transactions.csv", csv_content, "text/csv")}
    )
    assert response.status_code == 400
    assert "CSV is missing required columns. Expected: ['date', 'description', 'amount']" in response.json()["detail"]

def test_get_categorized_transactions_empty(client: TestClient):
    response = client.get("/api/reports/categorized")
    assert response.status_code == 200
    assert response.json() == []

def test_get_categorized_transactions_with_data(client: TestClient, db_session: Session):
    # Manually add a transaction to the database
    transaction = Transaction(
        date=datetime(2023, 1, 1),
        description="Test Transaction",
        amount=10.00,
        raw_category="Miscellaneous",
        final_category="Miscellaneous"
    )
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    response = client.get("/api/reports/categorized")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["description"] == "Test Transaction"
    assert data[0]["amount"] == 10.00
    assert data[0]["final_category"] == "Miscellaneous"
