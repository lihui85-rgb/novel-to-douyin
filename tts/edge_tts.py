# 语音合成模块
import asyncio
import edge_tts
import os
import uuid

# 可用的中文语音
VOICES = {
    # 女声
    'xiaoxiao': 'zh-CN-XiaoxiaoNeural',      # 晓晓 - 温柔女声
    'xiaoyi': 'zh-CN-XiaoyiNeural',          # 晓伊 - 活泼女声
    'jenny': 'zh-CN-JennyNeural',            # Jenny - 成熟女声
    # 男声
    'yunxi': 'zh-CN-YunxiNeural',            # 云希 - 沉稳男声
    'yunyang': 'zh-CN-YunyangNeural',        # 云扬 - 青年男声
    'yongji': 'zh-CN-YongjiNeural',          # 永吉 - 成熟男声
}

# 甜宠推荐语音
SWEET_LOVE_VOICES = [
    'zh-CN-XiaoxiaoNeural',   # 晓晓
    'zh-CN-XiaoyiNeural',    # 晓伊
    'zh-CN-JennyNeural',      # Jenny
]

async def _generate_async(text, voice, output_file):
    """异步生成语音"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file

def generate_speech(text, voice='zh-CN-XiaoxiaoNeural', output_file='output/speech.mp3'):
    """
    生成语音文件
    
    Args:
        text: 要转换的文本
        voice: 语音名称 (默认: 晓晓)
        output_file: 输出文件路径
    
    Returns:
        bool: 是否成功
    """
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file) or 'output', exist_ok=True)
        
        # 验证语音
        if voice not in VOICES.values():
            voice = 'zh-CN-XiaoxiaoNeural'
        
        # 限制文本长度 (TTS API限制)
        max_length = 5000
        if len(text) > max_length:
            text = text[:max_length]
        
        # 异步执行
        asyncio.run(_generate_async(text, voice, output_file))
        
        print(f"✅ 语音已生成: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ 语音生成失败: {e}")
        return False

def generate_sweet_voice(text, output_file='output/speech.mp3'):
    """
    生成甜宠风格的语音（自动选择温柔女声）
    """
    import random
    voice = random.choice(SWEET_LOVE_VOICES)
    return generate_speech(text, voice, output_file)

def get_available_voices():
    """获取可用语音列表"""
    return VOICES

if __name__ == "__main__":
    # 测试
    test_text = "凌晨三点，京城市中心医院的VIP病房里。林晚桐睁开眼睛，入目是一片雪白的天花板。"
    generate_speech(test_text, "zh-CN-XiaoxiaoNeural", "output/test.mp3")
