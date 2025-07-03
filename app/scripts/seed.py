# run_seed.py

import argparse
from app.db.seeder import seed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run database seeder")
    parser.add_argument('--env', type=str, default="dev", help='Environment name')

    args = parser.parse_args()
    print(f"Running seeder in {args.env} environment...")
    seed()
