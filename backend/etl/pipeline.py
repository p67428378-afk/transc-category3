import pandas as pd
from io import StringIO
from datetime import datetime
from sqlalchemy.orm import Session
from backend.models import Transaction
from backend.llm_service import categorize_transaction

async def run_etl_pipeline(csv_file_content: str, db: Session):
    # 1. Extract (from CSV)
    df = pd.read_csv(StringIO(csv_file_content))

    # Basic validation
    required_columns = ['date', 'description', 'amount']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV is missing required columns. Expected: {required_columns}")

    # 2. Transform
    # Deduplication (simple example: based on description, amount, and date)
    df.drop_duplicates(subset=['date', 'description', 'amount'], inplace=True)

    # Standardize date format
    df['date'] = pd.to_datetime(df['date'])

    # Categorize transactions using LLM service
    # This will be an async operation, so we'll collect tasks
    categorization_tasks = []
    for _, row in df.iterrows():
        categorization_tasks.append(categorize_transaction(row['description']))
    
    categories = await asyncio.gather(*categorization_tasks)
    df['raw_category'] = categories
    df['final_category'] = categories # For now, raw and final are the same

    # Prepare for loading into DB
    transactions_to_load = []
    for _, row in df.iterrows():
        transactions_to_load.append(
            Transaction(
                date=row['date'],
                description=row['description'],
                amount=row['amount'],
                raw_category=row['raw_category'],
                final_category=row['final_category'],
                # user_id can be added here if available from context
            )
        )
    
    # 3. Load
    db.add_all(transactions_to_load)
    db.commit()

    return len(transactions_to_load)
