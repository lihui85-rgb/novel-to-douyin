"""
甜宠小说转抖音视频 - Vercel API入口
"""
import os
import json
from flask import Flask, request, jsonify
from novel_spider.qimao import QimaoSpider
from tts.edge_tts import generate_speech
from video.maker import generate_video

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "ok",
        "message": "甜宠小说转抖音视频 API",
        "endpoints": {
            "/crawl": "获取小说章节",
            "/tts": "生成语音",
            "/video": "生成视频",
            "/auto": "全自动生成"
        }
    })

@app.route('/crawl', methods=['GET'])
def crawl_novel():
    """获取热门甜宠小说列表"""
    source = request.args.get('source', 'qimao')
    category = request.args.get('category', 'sweet')  # sweet:甜宠
    
    spider = QimaoSpider()
    novels = spider.get_hot_novels(category=category)
    
    return jsonify({
        "success": True,
        "data": novels
    })

@app.route('/chapter', methods=['GET'])
def get_chapter():
    """获取指定小说章节内容"""
    novel_id = request.args.get('novel_id')
    chapter_index = int(request.args.get('index', 0))
    
    if not novel_id:
        return jsonify({"success": False, "error": "需要novel_id参数"})
    
    spider = QimaoSpider()
    content = spider.get_chapter_content(novel_id, chapter_index)
    
    return jsonify({
        "success": True,
        "content": content
    })

@app.route('/tts', methods=['POST'])
def text_to_speech():
    """生成语音"""
    data = request.get_json()
    text = data.get('text', '')
    voice = data.get('voice', 'zh-CN-XiaoxiaoNeural')
    output_file = data.get('output', 'output/speech.mp3')
    
    if not text:
        return jsonify({"success": False, "error": "需要text参数"})
    
    result = generate_speech(text, voice, output_file)
    
    return jsonify({
        "success": result,
        "file": output_file
    })

@app.route('/video', methods=['POST'])
def make_video():
    """生成视频"""
    data = request.get_json()
    audio_file = data.get('audio', 'output/speech.mp3')
    text = data.get('text', '')
    output_file = data.get('output', 'output/video.mp4')
    style = data.get('style', 'sweet')
    
    result = generate_video(audio_file, text, output_file, style)
    
    return jsonify({
        "success": result,
        "file": output_file
    })

@app.route('/auto', methods=['GET'])
def auto_generate():
    """全自动：抓小说 -> 生成语音 -> 生成视频"""
    import random
    
    # 1. 获取热门小说
    spider = QimaoSpider()
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
    
    # 3. 生成语音 (取前500字，避免太长)
    text = content[:500]
    audio_file = f"output/audio_{novel_id}.mp3"
    generate_speech(text, "zh-CN-XiaoxiaoNeural", audio_file)
    
    # 4. 生成视频
    video_file = f"output/video_{novel_id}.mp4"
    generate_video(audio_file, text, video_file, "sweet")
    
    return jsonify({
        "success": True,
        "novel": novel,
        "video": video_file,
        "preview_text": text[:100] + "..."
    })

# Vercel serverless handler
def handler(request):
    return app(request)
