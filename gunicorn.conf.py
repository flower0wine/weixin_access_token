import multiprocessing
import os

# 确保日志目录存在
if not os.path.exists('logs'):
    os.makedirs('logs')

# 基本配置
bind = "0.0.0.0:5000"  # 绑定地址和端口
workers = multiprocessing.cpu_count() * 2 + 1  # 工作进程数
worker_class = "sync"  # 工作模式

# 进程名称
proc_name = "weixin_token"

# 工作模式配置
worker_connections = 1000    # 最大并发连接数
timeout = 30                 # 请求超时时间
keepalive = 2               # 连接保持时间
max_requests = 2000         # 每个工作进程处理的最大请求数
max_requests_jitter = 200   # 随机重启抖动值

# 日志配置
accesslog = "logs/access.log"    # 访问日志放在当前目录下的 logs 文件夹
errorlog = "logs/error.log"      # 错误日志放在当前目录下的 logs 文件夹
loglevel = "info"
access_log_format = '%({x-real-ip}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190 