import os
import json
from pathlib import Path
from sqlalchemy.orm import Session

from app import models
from app.db.session import get_db

DATA_DIR = Path(__file__).parent / "../data"


def get_model_by_name(name):
    """Return SQLAlchemy model class by table name."""
    return getattr(models, name, None)


def seed():
    """Seed database tables from JSON files in the data folder."""
    db = next(get_db())
    print("Starting database seeding...")

    for file in DATA_DIR.glob("*.json"):
        table_name = file.stem.capitalize()
        model = get_model_by_name(table_name)
        if not model:
            print(f"Model for table '{table_name}' not found. Skipping.")
            continue

        with open(file, "r", encoding="utf-8") as f:
            records = json.load(f)
            if not isinstance(records, list):
                print(f"Data in {file.name} is not a list. Skipping.")
                continue

            for record in records:
                obj = model(**record)
                db.add(obj)
        print(f"Seeded data for table '{table_name}' from '{file.name}'.")

    db.commit()
    print("Seeding completed.")
