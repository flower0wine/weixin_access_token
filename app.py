from flask import Flask, jsonify, request
import requests
import logging

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_weixin_token(app_id: str, app_secret: str) -> str:
    """获取微信 access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    response = requests.get(url)
    data = response.json()
    
    if 'access_token' not in data:
        logger.error(f"Token acquisition failed: {data}")
        raise ValueError("Token acquisition failed")
    
    return data['access_token']

@app.route('/access_token', methods=['GET'])
def get_access_token():
    try:
        # 从请求参数获取凭证
        app_id = request.args.get('app_id')
        app_secret = request.args.get('app_secret')
        
        # 验证参数
        if not app_id or not app_secret:
            return jsonify({"error": "Internal server error"}), 500
        
        # 获取新 token
        token = get_weixin_token(app_id, app_secret)
        return jsonify({"access_token": token})
        
    except Exception as e:
        # 记录错误日志，但不返回具体错误信息
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 