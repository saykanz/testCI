# 1️⃣ 使用官方 Playwright 镜像（已包含浏览器）
FROM mcr.microsoft.com/playwright/python:v1.57.0-noble

# 2️⃣ 设置工作目录（容器内部）
WORKDIR /app

# 3️⃣ 复制项目文件到容器
COPY . .

# 4️⃣ 安装 Python 依赖
RUN pip install -r requirements.txt

# 5️⃣ 运行测试（容器启动时执行）
CMD ["pytest", "-s", "-v"]