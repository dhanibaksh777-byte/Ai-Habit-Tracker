from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os 


load_dotenv()

database_url = os.getenv("database_url")
if not database_url:
    raise RuntimeError("there is no api key in .env file")
engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db 

    finally:
        db.close()

