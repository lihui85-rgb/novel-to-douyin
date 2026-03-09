"""
甜宠小说转抖音视频 - Vercel API入口
"""
from flask import Flask, jsonify, request
import random

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
    category = request.args.get('category', 'sweet')
    try:
        from novel_spider.qimao import QimaoSpider
        spider = QimaoSpider()
        novels = spider.get_hot_novels(category=category)
        return jsonify({"success": True, "data": novels})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/chapter')
def get_chapter():
    novel_id = request.args.get('novel_id')
    chapter_index = int(request.args.get('index', 0))
    if not novel_id:
        return jsonify({"success": False, "error": "需要novel_id参数"})
    try:
        from novel_spider.qimao import QimaoSpider
        spider = QimaoSpider()
        content = spider.get_chapter_content(novel_id, chapter_index)
        return jsonify({"success": True, "content": content})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/auto')
def auto_generate():
    try:
        from novel_spider.qimao import QimaoSpider
        spider = QimaoSpider()
        novels = spider.get_hot_novels(category='sweet')
        if not novels:
            return jsonify({"success": False, "error": "获取小说失败"})
        novel = random.choice(novels)
        content = spider.get_chapter_content(novel['id'], 0)
        if not content:
            return jsonify({"success": False, "error": "获取章节内容失败"})
        text = content[:300]
        return jsonify({
            "success": True,
            "novel": novel,
            "text": text,
            "note": "语音视频生成需本地运行"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Vercel serverless function
def handler(request):
    return app(request.environ, app.start_response)
