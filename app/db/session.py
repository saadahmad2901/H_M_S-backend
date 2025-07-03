from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core import settings


print(settings.DATABASE_URL)
engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
