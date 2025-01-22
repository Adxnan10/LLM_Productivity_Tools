from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.env_setup import postgres_url

engine = create_engine(postgres_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
