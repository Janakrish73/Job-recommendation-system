#Database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/job_recommender"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      
    pool_recycle=300,        
    echo=False                
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency — yields a database session, closes it after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
