"""
甜宠小说转抖音视频 - Vercel API入口（简化版）
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "ok",
        "message": "甜宠小说转抖音视频 API",
        "endpoints": {
            "/crawl": "获取小说列表",
            "/chapter": "获取章节内容", 
            "/auto": "全自动生成"
        }
    })

@app.route('/crawl')
def crawl_novel():
    return jsonify({
        "success": True, 
        "data": [
            {"id": "1", "title": "甜婚蜜爱", "author": "糖小豆"},
            {"id": "2", "title": "隐婚甜妻", "author": "顾南城"},
            {"id": "3", "title": "重生甜妻", "author": "白茶"}
        ]
    })

@app.route('/chapter')
def get_chapter():
    return jsonify({
        "success": True,
        "content": "这是测试章节内容..."
    })

@app.route('/auto')
def auto_generate():
    return jsonify({
        "success": True,
        "novel": {"id": "1", "title": "甜婚蜜爱", "author": "糖小豆"},
        "text": "凌晨三点，京城市中心医院的VIP病房里...",
        "note": "完整版需要本地运行"
    })

def handler(request):
    return app(request.environ, app.start_response)
