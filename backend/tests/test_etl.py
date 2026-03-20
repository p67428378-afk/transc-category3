import pytest
from sqlalchemy.orm import Session
from backend.etl.pipeline import run_etl_pipeline
from backend.models import Transaction
from datetime import datetime
import asyncio
from decimal import Decimal

@pytest.mark.asyncio
async def test_run_etl_pipeline_success(db_session: Session):
    csv_content = "date,description,amount\n2023-01-01,Starbucks Coffee,5.50\n2023-01-02,Monthly Rent Payment,1200.00\n2023-01-03,Electricity Bill,75.20"
    
    num_processed = await run_etl_pipeline(csv_content, db_session)
    assert num_processed == 3
    
    transactions = db_session.query(Transaction).all()
    assert len(transactions) == 3
    
    starbucks = next(t for t in transactions if "Starbucks" in t.description)
    assert starbucks.final_category == "Food"
    assert starbucks.amount == Decimal("5.50")
    
    rent = next(t for t in transactions if "Rent" in t.description)
    assert rent.final_category == "Rent"
    assert rent.amount == Decimal("1200.00")

    electricity = next(t for t in transactions if "Electricity" in t.description)
    assert electricity.final_category == "Utilities"
    assert electricity.amount == Decimal("75.20")

@pytest.mark.asyncio
async def test_run_etl_pipeline_deduplication(db_session: Session):
    csv_content = "date,description,amount\n2023-01-01,Starbucks Coffee,5.50\n2023-01-01,Starbucks Coffee,5.50\n2023-01-02,Monthly Rent Payment,1200.00"
    
    num_processed = await run_etl_pipeline(csv_content, db_session)
    assert num_processed == 2  # One duplicate should be removed
    
    transactions = db_session.query(Transaction).all()
    assert len(transactions) == 2

@pytest.mark.asyncio
async def test_run_etl_pipeline_malformed_csv(db_session: Session):
    csv_content = "date,description\n2023-01-01,Starbucks Coffee"
    with pytest.raises(ValueError, match="CSV is missing required columns. Expected: \['date', 'description', 'amount'\]"):
        await run_etl_pipeline(csv_content, db_session)

@pytest.mark.asyncio
async def test_run_etl_pipeline_date_format(db_session: Session):
    csv_content = "date,description,amount\n01/01/2023,Starbucks Coffee,5.50"
    num_processed = await run_etl_pipeline(csv_content, db_session)
    assert num_processed == 1
    transaction = db_session.query(Transaction).first()
    assert transaction.date == datetime(2023, 1, 1)
