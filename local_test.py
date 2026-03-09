"""
本地测试脚本
无需Vercel，直接本地运行
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from novel_spider.qimao import QimaoSpider
from tts.edge_tts import generate_sweet_voice
from video.maker import generate_simple_video

def main():
    print("=" * 50)
    print("🍬 甜宠小说转抖音视频 - 本地测试")
    print("=" * 50)
    
    # 1. 获取小说
    print("\n📚 第1步：获取热门甜宠小说...")
    spider = QimaoSpider()
    novels = spider.get_hot_novels('sweet')
    
    if not novels:
        print("❌ 获取小说失败")
        return
    
    print(f"✅ 获取到 {len(novels)} 本小说")
    for i, n in enumerate(novels[:3]):
        print(f"  {i+1}. {n['title']} - {n['author']}")
    
    # 选择第一本
    novel = novels[0]
    print(f"\n▶ 选中: {novel['title']}")
    
    # 2. 获取章节内容
    print("\n📖 第2步：获取章节内容...")
    content = spider.get_chapter_content(novel['id'], 0)
    if not content:
        print("❌ 获取内容失败")
        return
    
    # 取前500字
    text = content[:500]
    print(f"✅ 获取到内容 ({len(text)} 字)")
    print(f"   预览: {text[:100]}...")
    
    # 3. 生成语音
    print("\n🔊 第3步：生成语音...")
    audio_file = f"output/{novel['id']}_audio.mp3"
    if generate_sweet_voice(text, audio_file):
        print(f"✅ 语音已生成: {audio_file}")
    else:
        print("❌ 语音生成失败")
    
    # 4. 生成视频
    print("\n🎬 第4步：生成视频...")
    video_file = f"output/{novel['id']}_video.mp4"
    if generate_simple_video(text, video_file, 'sweet'):
        print(f"✅ 视频已生成: {video_file}")
    else:
        print("❌ 视频生成失败")
    
    print("\n" + "=" * 50)
    print("🎉 测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
