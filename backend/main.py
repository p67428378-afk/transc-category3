from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
import os

from .database import SessionLocal, engine, init_db, Transaction
from .etl_pipeline import process_csv

app = FastAPI()

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/transactions/upload")
async def upload_transactions(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        contents = await file.read()
        # For now, we'll save it to a temporary in-memory file or local disk
        # In a real scenario, this would go to Cloud Storage (e.g., GCS/S3)
        temp_file_path = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as f:
            f.write(contents)
        
        # Process the CSV using the ETL pipeline
        # Assuming a user_id for now, can be extracted from auth in future
        processed_count = process_csv(temp_file_path, user_id="test_user")
        
        # Clean up the temporary file
        os.remove(temp_file_path)

        return {"message": f"Successfully processed {processed_count} transactions.", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

@app.get("/api/reports/categorized")
async def get_categorized_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions

