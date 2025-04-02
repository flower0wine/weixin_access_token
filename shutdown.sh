#!/bin/bash

# 确保脚本在正确的目录下执行
cd "$(dirname "$0")"

# 检查 PID 文件
if [ ! -f "weixin.pid" ]; then
    echo "找不到 PID 文件，服务可能没有运行"
    exit 1
fi

# 读取 PID
pid=$(cat weixin.pid)

# 检查进程是否存在
if ! ps -p $pid > /dev/null; then
    echo "进程不存在，可能已经停止"
    rm weixin.pid
    exit 1
fi

# 停止服务
echo "正在停止服务 (PID: $pid)..."
kill $pid

# 等待进程结束
count=0
while ps -p $pid > /dev/null; do
    sleep 1
    count=$((count + 1))
    if [ $count -gt 10 ]; then
        echo "服务没有及时响应，强制终止..."
        kill -9 $pid
        break
    fi
done

# 删除 PID 文件
rm weixin.pid
echo "服务已停止" 