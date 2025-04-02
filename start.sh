#!/bin/bash

# 确保脚本在正确的目录下执行
cd "$(dirname "$0")"

# 确保日志目录存在
mkdir -p logs

# 检查是否已经在运行
if [ -f "weixin.pid" ]; then
    pid=$(cat weixin.pid)
    if ps -p $pid > /dev/null; then
        echo "服务已经在运行中 (PID: $pid)"
        exit 1
    else
        rm weixin.pid
    fi
fi

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 后台启动服务
echo "正在启动服务..."
nohup gunicorn -c gunicorn.conf.py app:app > logs/nohup.log 2>&1 &

# 保存 PID
echo $! > weixin.pid
echo "服务已启动 (PID: $!)" 