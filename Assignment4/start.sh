#!/bin/bash
# start.sh

# We are using python:3.11-slim-buster.
# Use Python's retry logic to wait for the database.

echo "Waiting for PostgreSQL database to be ready and creating tables..."
python -c '
import asyncio
import sys
import time
from app.database import init_db

MAX_RETRIES = 10
WAIT_SECONDS = 3

async def create_tables_with_retry():
    for i in range(MAX_RETRIES):
        try:
            print(f"Database initialization attempt {i+1}/{MAX_RETRIES}...")
            await init_db()
            print("Database tables created successfully!")
            return
        except Exception as e:
            if i < MAX_RETRIES - 1:
                print(f"Connection failed: {e}. Retrying in {WAIT_SECONDS} seconds...", file=sys.stderr)
                await asyncio.sleep(WAIT_SECONDS)
            else:
                print(f"Failed to initialize database after {MAX_RETRIES} attempts.", file=sys.stderr)
                sys.exit(1)

if __name__ == "__main__":
    asyncio.run(create_tables_with_retry())
'

# Start Uvicorn server
echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000