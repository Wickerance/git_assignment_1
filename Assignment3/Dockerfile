# 使用官方的 Python 3.10 基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 强制更新时间戳，以确保下一层的缓存被破坏
RUN echo $(date +%s) > /tmp/force_update.txt

# 复制应用代码
COPY ./app /app/

# 极端口罩式修复：强制在容器内部替换旧的相对导入 (全覆盖) 
# Dockerfile 中不允许使用 Markdown 的 --- 符号，已替换为 # 注释行

# 1. 修复 /app/services/student_service.py
RUN sed -i 's/from \.\.db import models/from db import models/g' /app/services/student_service.py
RUN sed -i 's/from \.\.db import schemas/from db import schemas/g' /app/services/student_service.py

# 2. 修复 /app/api/groups_router.py 
RUN sed -i 's/from \.\.db\.database import get_db/from db.database import get_db/g' /app/api/groups_router.py
RUN sed -i 's/from \.\.db import schemas/from db import schemas/g' /app/api/groups_router.py
RUN sed -i 's/from \.\.services import student_service/from services import student_service/g' /app/api/groups_router.py
RUN sed -i 's/from \.\.services import group_service/from services import group_service/g' /app/api/groups_router.py

# 3. 修复 /app/services/group_service.py
RUN sed -i 's/from \.\.db import models/from db import models/g' /app/services/group_service.py
RUN sed -i 's/from \.\.db import schemas/from db import schemas/g' /app/services/group_service.py


# 设置 Python 路径
ENV PYTHONPATH=/app

# 暴露 FastAPI 运行的端口
EXPOSE 8000

# 启动 Uvicorn 服务器
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]