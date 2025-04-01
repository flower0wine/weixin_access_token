from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

app = Flask(__name__)

class TokenManager:
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expires_at = None

    def ensure_access_token(self) -> str:
        """确保获取有效的access_token"""
        if self.access_token and self.token_expires_at and self.token_expires_at > datetime.now() + timedelta(minutes=1):
            return self.access_token

        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        response = requests.get(url)
        data = response.json()
        
        if 'access_token' not in data:
            raise ValueError(f"获取access_token失败: {data}")
        
        self.access_token = data['access_token']
        self.token_expires_at = datetime.now() + timedelta(seconds=data['expires_in'])
        return self.access_token

# 从环境变量获取配置
app_id = os.getenv('WEIXIN_APP_ID')
app_secret = os.getenv('WEIXIN_APP_SECRET')

if not app_id or not app_secret:
    raise ValueError("请在 .env 文件中设置 WEIXIN_APP_ID 和 WEIXIN_APP_SECRET")

token_manager = TokenManager(app_id, app_secret)

@app.route('/access_token', methods=['GET'])
def get_access_token():
    try:
        token = token_manager.ensure_access_token()
        return jsonify({"access_token": token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 