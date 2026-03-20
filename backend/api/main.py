from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import SessionLocal, engine, Base, get_db
from database.models import Transaction
from etl.pipeline import run_etl_pipeline
from pydantic import BaseModel

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

class TransactionResponse(BaseModel):
    id: int
    transaction_id: str
    date: str
    description: str
    amount: float
    category: str

    class Config:
        from_attributes = True

@app.post("/api/transactions/upload")
async def upload_transactions(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    try:
        contents = await file.read()
        run_etl_pipeline(contents, db)
        return {"message": "Transactions uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

@app.get("/api/reports/categorized", response_model=List[TransactionResponse])
async def get_categorized_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions
