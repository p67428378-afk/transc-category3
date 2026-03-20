import pandas as pd
from sqlalchemy.orm import Session
from database.models import Transaction
from llm.categorizer import categorize_transaction

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop rows with any missing values
    df.dropna(inplace=True)
    # Convert 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])
    # Ensure 'amount' is numeric
    df['amount'] = pd.to_numeric(df['amount'])
    return df

def deduplicate_data(df: pd.DataFrame) -> pd.DataFrame:
    # Deduplicate based on a combination of transaction_id, date, description, amount
    df.drop_duplicates(subset=['transaction_id', 'date', 'description', 'amount'], inplace=True)
    return df

def categorize_data(df: pd.DataFrame) -> pd.DataFrame:
    df['category'] = df['description'].apply(categorize_transaction)
    return df

def load_data(df: pd.DataFrame, db: Session):
    for index, row in df.iterrows():
        transaction = Transaction(
            transaction_id=row['transaction_id'],
            date=row['date'],
            description=row['description'],
            amount=row['amount'],
            category=row['category']
        )
        db.add(transaction)
    db.commit()

def run_etl_pipeline(file_content: bytes, db: Session):
    # Assuming file_content is a CSV
    from io import BytesIO
    df = pd.read_csv(BytesIO(file_content))

    df = clean_data(df)
    df = deduplicate_data(df)
    df = categorize_data(df)
    load_data(df, db)
