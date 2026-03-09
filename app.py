"""
甜宠小说转抖音视频 - Vercel API入口
"""
import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# 延迟导入，避免 Vercel 启动时报错
def get_spider():
    from novel_spider.qimao import QimaoSpider
    return QimaoSpider()

def get_tts():
    from tts.edge_tts import generate_speech
    return generate_speech

def get_video():
    from video.maker import generate_video
    return generate_video

@app.route('/')
def index():
    return jsonify({
        "status": "ok",
        "message": "🍬 甜宠小说转抖音视频 API",
        "endpoints": {
            "/crawl": "获取小说列表",
            "/chapter": "获取章节内容",
            "/auto": "全自动生成"
        }
    })

@app.route('/crawl', methods=['GET'])
def crawl_novel():
    """获取热门甜宠小说列表"""
    source = request.args.get('source', 'qimao')
    category = request.args.get('category', 'sweet')
    
    try:
        spider = get_spider()
        novels = spider.get_hot_novels(category=category)
        return jsonify({"success": True, "data": novels})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/chapter', methods=['GET'])
def get_chapter():
    """获取指定小说章节内容"""
    novel_id = request.args.get('novel_id')
    chapter_index = int(request.args.get('index', 0))
    
    if not novel_id:
        return jsonify({"success": False, "error": "需要novel_id参数"})
    
    try:
        spider = get_spider()
        content = spider.get_chapter_content(novel_id, chapter_index)
        return jsonify({"success": True, "content": content})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/auto', methods=['GET'])
def auto_generate():
    """全自动：抓小说 -> 生成语音"""
    import random
    
    try:
        # 1. 获取热门小说
        spider = get_spider()
        novels = spider.get_hot_novels(category='sweet')
        
        if not novels:
            return jsonify({"success": False, "error": "获取小说失败"})
        
        # 随机选一本
        novel = random.choice(novels)
        novel_id = novel['id']
        
        # 2. 获取第一章内容
        content = spider.get_chapter_content(novel_id, 0)
        if not content:
            return jsonify({"success": False, "error": "获取章节内容失败"})
        
        # 3. 取前300字返回（Vercel免费版有60秒限制）
        text = content[:300]
        
        return jsonify({
            "success": True,
            "novel": novel,
            "text": text,
            "message": "语音和视频生成需要在本地环境运行"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Vercel serverless handler
def handler(request):
    return app(request.environ, app.start_response)
