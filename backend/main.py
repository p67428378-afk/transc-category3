from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pydantic import BaseModel

from backend.database import get_db, init_db, engine
from backend.models import Base, Transaction
from backend.etl.pipeline import run_etl_pipeline

app = FastAPI()

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()

class TransactionResponse(BaseModel):
    transaction_id: str
    date: datetime
    description: str
    amount: float
    raw_category: str | None
    final_category: str | None
    is_flagged_for_review: bool

    class Config:
        from_attributes = True

@app.post("/api/transactions/upload")
async def upload_transactions(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    contents = await file.read()
    csv_content = contents.decode("utf-8")

    try:
        num_processed = await run_etl_pipeline(csv_content, db)
        return {"message": f"Successfully processed {num_processed} transactions.", "filename": file.filename}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during ETL: {str(e)}")

@app.get("/api/reports/categorized", response_model=List[TransactionResponse])
async def get_categorized_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions
