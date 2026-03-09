"""
项目配置
"""

# 小说源配置
NOVEL_SOURCE = {
    'qimao': {
        'name': '七猫小说',
        'api': 'https://www.qimao.com/api/v2',
    },
    'qidian': {
        'name': '起点中文网',
        'api': 'https://www.qidian.com',
    }
}

# 默认配置
DEFAULT_CONFIG = {
    'novel_source': 'qimao',      # 小说源
    'category': 'sweet',            # 分类: sweet/cute/romantic
    'voice': 'zh-CN-XiaoxiaoNeural',  # 默认语音
    'video_style': 'sweet',         # 视频风格
    'text_length': 500,            # 每次生成字数
    'output_dir': 'output',        # 输出目录
}

# 分类配置
CATEGORY_CONFIG = {
    'sweet': {
        'name': '甜宠',
        'voice': 'zh-CN-XiaoxiaoNeural',
        'style': 'sweet',
        'keywords': ['甜', '宠', '总裁', '娇妻', '豪门']
    },
    'urban': {
        'name': '都市',
        'voice': 'zh-CN-YunxiNeural',
        'style': 'romantic',
        'keywords': ['都市', '逆袭', '重生', '战神']
    },
    'fantasy': {
        'name': '玄幻',
        'voice': 'zh-CN-YunyangNeural',
        'style': 'romantic',
        'keywords': ['玄幻', '修仙', '系统', '穿越']
    },
    'apocalypse': {
        'name': '末日',
        'voice': 'zh-CN-YongjiNeural',
        'style': 'cute',
        'keywords': ['末日', '进化', '变异', '丧尸']
    },
    'boss': {
        'name': '霸总',
        'voice': 'zh-CN-JennyNeural',
        'style': 'sweet',
        'keywords': ['霸总', '总裁', '契约', '闪婚']
    }
}

def get_config(key, default=None):
    """获取配置"""
    return DEFAULT_CONFIG.get(key, default)

def get_category_config(category):
    """获取分类配置"""
    return CATEGORY_CONFIG.get(category, CATEGORY_CONFIG['sweet'])
