#!/bin/bash
# start.sh

# 在 Alpine 基础镜像中，为了使用 pg_isready，我们需要安装 postgresql-client。
# 但是您的基础镜像是 python:3.11-slim-buster，我们先使用 Python 自己的重试逻辑。

# 确保 PostgreSQL 启动并创建表
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

# 启动 Uvicorn 服务器
echo "Starting Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000