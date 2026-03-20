from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.database import Transaction
import pytest
import io
from decimal import Decimal

def test_upload_transactions_success(client: TestClient, db_session: Session):
    csv_content = """
date,description,amount
2023-01-01,Starbucks Coffee,5.50
2023-01-02,Monthly Rent,1200.00
2023-01-03,Electricity Bill,75.25
"""
    files = {"file": ("transactions.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    response = client.post("/api/transactions/upload", files=files)
    assert response.status_code == 200
    assert response.json()["message"].startswith("Successfully processed")
    assert response.json()["filename"] == "transactions.csv"

    transactions = db_session.query(Transaction).order_by(Transaction.date).all()
    assert len(transactions) == 3

    assert transactions[0].description == "Starbucks Coffee"
    assert float(transactions[0].amount) == 5.50
    assert transactions[0].final_category == "Food"

    assert transactions[1].description == "Monthly Rent"
    assert float(transactions[1].amount) == 1200.00
    assert transactions[1].final_category == "Rent"

    assert transactions[2].description == "Electricity Bill"
    assert float(transactions[2].amount) == 75.25
    assert transactions[2].final_category == "Utilities"

def test_upload_transactions_invalid_file_type(client: TestClient):
    files = {"file": ("document.txt", io.BytesIO(b"some text"), "text/plain")}
    response = client.post("/api/transactions/upload", files=files)
    assert response.status_code == 400
    assert response.json() == {"detail": "Only CSV files are allowed"}

def test_get_categorized_transactions(client: TestClient, db_session: Session):
    # First, upload some transactions to ensure data exists
    csv_content = """
date,description,amount
2023-01-01,Starbucks Coffee,5.50
2023-01-02,Monthly Rent,1200.00
"""
    files = {"file": ("transactions_for_get.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    client.post("/api/transactions/upload", files=files)

    response = client.get("/api/reports/categorized")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Verify structure and some content
    assert "description" in data[0]
    assert "amount" in data[0]
    assert "final_category" in data[0]
    assert data[0]["description"] == "Starbucks Coffee"
    assert float(data[0]["amount"]) == 5.50
    assert data[0]["final_category"] == "Food"

    assert data[1]["description"] == "Monthly Rent"
    assert float(data[1]["amount"]) == 1200.00
    assert data[1]["final_category"] == "Rent"

def test_get_categorized_transactions_empty(client: TestClient, db_session: Session):
    # Ensure no transactions are in the DB before this test
    response = client.get("/api/reports/categorized")
    assert response.status_code == 200
    assert response.json() == []
