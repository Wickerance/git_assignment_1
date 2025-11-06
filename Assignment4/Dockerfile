FROM python:3.11-slim-buster

# 目标工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目代码到容器的 /app 目录
# 这一步会创建 /app/app 目录，包含您的 Python 文件
COPY . .

# 暴露 FastAPI 运行的端口
EXPOSE 8000

# 保持 CMD 留空，让 docker-compose 控制