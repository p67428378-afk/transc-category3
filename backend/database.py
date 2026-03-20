from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Base for models
Base = declarative_base()

# Default to PostgreSQL, but allow overriding for tests
DEFAULT_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/transactions_db")

# Global engine and SessionLocal, can be overridden for testing
_engine = None
_SessionLocal = None

def get_engine(database_url: str = None):
    global _engine
    if database_url:
        return create_engine(database_url, connect_args={"check_same_thread": False})
    if _engine is None:
        _engine = create_engine(DEFAULT_DATABASE_URL)
    return _engine

def get_session_local(database_url: str = None):
    global _SessionLocal
    if database_url:
        test_engine = get_engine(database_url)
        return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal

def get_db():
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()

def init_db(database_url: str = None):
    # Ensure models are imported before creating tables
    from backend.models import Base as AppBase
    AppBase.metadata.create_all(bind=get_engine(database_url))
