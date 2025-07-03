# Step 1: Initialize Alembic (only once)
alembic init alembic

# Step 2: Generate a new migration from model changes
alembic revision --autogenerate -m "Initial migration"

# Step 3: Apply migrations to the database
alembic upgrade head

# Step 4: Seed data if already have not done
python -m app.scripts.seed