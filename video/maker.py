# 视频生成模块
import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap

# 视频配置
VIDEO_CONFIG = {
    'width': 1080,
    'height': 1920,  # 抖音竖屏
    'fps': 30,
    'duration_per_page': 3,  # 每页展示秒数
}

# 甜宠风格配色
STYLE_COLORS = {
    'sweet': {
        'bg': '#FFE4EC',  # 粉色背景
        'text': '#FF6B9D',  # 粉色文字
        'title': '#FF4081',  # 标题红色
        'accent': '#FFB6C1',  # 浅粉色装饰
    },
    'cute': {
        'bg': '#E8F5E9',  # 浅绿背景
        'text': '#4CAF50',  # 绿色文字
        'title': '#2E7D32',  # 深绿标题
        'accent': '#C8E6C9',  # 浅绿装饰
    },
    'romantic': {
        'bg': '#FFF3E0',  # 橙色背景
        'text': '#FF9800',  # 橙色文字
        'title': '#E65100',  # 深橙标题
        'accent': '#FFE0B2',  # 浅橙装饰
    }
}

def create_text_image(text, width, height, style='sweet'):
    """生成文字图片"""
    colors = STYLE_COLORS.get(style, STYLE_COLORS['sweet'])
    
    # 创建背景
    img = Image.new('RGB', (width, height), colors['bg'])
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体（Windows）
    try:
        font_size = 40
        font = ImageFont.truetype("msyh.ttc", font_size)  # 微软雅黑
        title_font = ImageFont.truetype("msyh.ttc", 60)
    except:
        font = ImageFont.load_default()
        title_font = font
    
    # 文字换行
    wrapper = textwrap.TextWrapper(width=20)
    wrapped_text = wrapper.wrap(text)
    
    # 绘制文字
    y_offset = height // 2 - len(wrapped_text) * 30
    for line in wrapped_text:
        # 计算文字宽度（近似）
        text_width = len(line) * font_size // 2
        x = (width - text_width) // 2
        draw.text((x, y_offset), line, fill=colors['text'], font=font)
        y_offset += font_size + 10
    
    return img

def create_title_card(title, author, width, height, style='sweet'):
    """生成标题卡片"""
    colors = STYLE_COLORS.get(style, STYLE_COLORS['sweet'])
    
    img = Image.new('RGB', (width, height), colors['bg'])
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        title_font = ImageFont.truetype("msyh.ttc", 72)
        author_font = ImageFont.truetype("msyh.ttc", 36)
    except:
        title_font = ImageFont.load_default()
        author_font = title_font
    
    # 标题
    title_width = len(title) * 72 // 2
    title_x = (width - title_width) // 2
    draw.text((title_x, height//3), title, fill=colors['title'], font=title_font)
    
    # 作者
    author_text = f"作者：{author}"
    author_width = len(author_text) * 36 // 2
    author_x = (width - author_width) // 2
    draw.text((author_x, height//3 + 100), author_text, fill=colors['text'], font=author_font)
    
    return img

def generate_video(audio_file, text, output_file='output/video.mp4', style='sweet'):
    """
    生成视频
    
    Args:
        audio_file: 语音文件路径
        text: 字幕文本
        output_file: 输出视频路径
        style: 风格 (sweet/cute/romantic)
    
    Returns:
        bool: 是否成功
    """
    try:
        # 确保输出目录
        os.makedirs(os.path.dirname(output_file) or 'output', exist_ok=True)
        
        width = VIDEO_CONFIG['width']
        height = VIDEO_CONFIG['height']
        
        # 1. 加载音频获取时长
        if os.path.exists(audio_file):
            audio = AudioFileClip(audio_file)
            total_duration = audio.duration
        else:
            # 如果没有音频，使用默认时长
            total_duration = 10
            audio = None
        
        # 2. 创建文字图片
        text_img = create_text_image(text, width, height, style)
        text_path = 'output/temp_text.png'
        text_img.save(text_path)
        
        # 3. 创建视频clip
        text_clip = ImageClip(text_path).set_duration(total_duration)
        
        # 4. 添加背景
        bg_color = STYLE_COLORS.get(style, STYLE_COLORS['sweet'])['bg']
        bg_clip = ColorClip(size=(width, height), color=bg_color).set_duration(total_duration)
        
        # 5. 合成视频
        video = CompositeVideoClip([bg_clip, text_clip])
        
        # 6. 添加音频
        if audio:
            video = video.set_audio(audio)
        
        # 7. 导出
        video.write_videofile(output_file, fps=VIDEO_CONFIG['fps'], codec='libx264')
        
        # 清理临时文件
        if os.path.exists(text_path):
            os.remove(text_path)
        
        print(f"✅ 视频已生成: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ 视频生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_simple_video(text, output_file='output/video.mp4', style='sweet'):
    """
    简单版：无需音频，只生成文字动画视频
    """
    try:
        os.makedirs(os.path.dirname(output_file) or 'output', exist_ok=True)
        
        width = VIDEO_CONFIG['width']
        height = VIDEO_CONFIG['height']
        colors = STYLE_COLORS.get(style, STYLE_COLORS['sweet'])
        
        # 创建背景
        bg = ColorClip(size=(width, height), color=colors['bg'], duration=5)
        
        # 创建文字clip
        txt_clip = TextClip(
            text,
            fontsize=40,
            color=colors['text'],
            font='Microsoft-YaHei',
            size=(width-100, None),
            method='caption'
        ).set_duration(5).set_position('center')
        
        # 合成
        video = CompositeVideoClip([bg, txt_clip])
        video.write_videofile(output_file, fps=24, codec='libx264')
        
        return True
    except Exception as e:
        print(f"❌ 简单视频生成失败: {e}")
        return False

if __name__ == "__main__":
    # 测试
    test_text = "一场精心设计的阴谋，让她被迫嫁给传闻中的恶魔总裁..."
    generate_simple_video(test_text, "output/test_video.mp4")
