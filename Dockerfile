# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制 Python 服务器文件到容器中
COPY server.py .

# 复制 statics 到容器中
COPY statics .

# 暴露端口
EXPOSE 8000

# 启动服务器
CMD ["python", "server.py"]
