import pandas as pd
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal, Transaction
from backend.llm.categorizer import categorize_transaction
from datetime import datetime
import uuid

def process_csv(file_path: str, user_id: str = None):
    df = pd.read_csv(file_path)

    # Data Cleaning and Deduplication
    # Assuming 'transaction_id' is unique, if not, generate one
    if 'transaction_id' not in df.columns:
        df['transaction_id'] = [str(uuid.uuid4()) for _ in range(len(df))]
    else:
        df.drop_duplicates(subset=['transaction_id'], inplace=True)

    # Standardize date format
    df['date'] = pd.to_datetime(df['date'])

    # Categorization using LLM Service
    df['raw_category'] = df['description'].apply(categorize_transaction)
    df['final_category'] = df['raw_category'] # For now, final is same as raw
    df['is_flagged_for_review'] = False # LLM service can set this if ambiguity is detected

    # Add user_id if provided
    if user_id:
        df['user_id'] = user_id
    else:
        df['user_id'] = 'default_user'

    # Prepare for database insertion
    transactions_to_db = []
    for index, row in df.iterrows():
        transaction = Transaction(
            transaction_id=row['transaction_id'],
            user_id=row['user_id'],
            date=row['date'],
            description=row['description'],
            amount=row['amount'],
            raw_category=row['raw_category'],
            final_category=row['final_category'],
            is_flagged_for_review=row['is_flagged_for_review'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        transactions_to_db.append(transaction)
    
    db: Session = SessionLocal()
    try:
        db.bulk_save_objects(transactions_to_db)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    return len(transactions_to_db)
