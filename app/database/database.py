import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

__all__ = ["get_db", "engine", "Base", "SessionLocal"]

# Load environment variables from .env file (for local development)
load_dotenv()

# Get RDS database details from environment variables set by Elastic Beanstalk
DB_HOST = os.getenv("RDS_HOSTNAME")
DB_PORT = os.getenv("RDS_PORT", "5432")
DB_NAME = os.getenv("RDS_DB_NAME")
DB_USER = os.getenv("RDS_USERNAME")
DB_PASSWORD = os.getenv("RDS_PASSWORD")

# Construct the database URL for SQLAlchemy using psycopg2
if DB_HOST and DB_NAME and DB_USER and DB_PASSWORD:
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    # Fallback to local DATABASE_URL for development
    DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine using psycopg2
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency to get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
