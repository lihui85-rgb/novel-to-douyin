# 七猫小说爬虫
import requests
from bs4 import BeautifulSoup
import json
import random

class QimaoSpider:
    """七猫小说爬虫"""
    
    BASE_URL = "https://www.qimao.com"
    API_URL = "https://www.qimao.com/api/v2"
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.qimao.com"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_hot_novels(self, category='sweet', limit=10):
        """
        获取热门小说列表
        
        category: sweet(甜宠), urban(玄幻), apocalypse(都市), fantasy(末日)
        """
        # 七猫小说分类ID
        category_map = {
            'sweet': '237',      # 甜宠
            'urban': '230',       # 都市
            'fantasy': '231',     # 玄幻
            'apocalypse': '235',  # 末日
            'boss': '238',       # 霸总
        }
        
        channel_id = category_map.get(category, '237')
        
        # 热门小说API
        url = f"{self.API_URL}/novel/hot"
        params = {
            "channel_id": channel_id,
            "page": 1,
            "limit": limit
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            novels = []
            for item in data.get('data', []):
                novels.append({
                    'id': str(item.get('novel_id')),
                    'title': item.get('novel_name'),
                    'author': item.get('author_name'),
                    'cover': item.get('cover'),
                    'desc': item.get('description', '')[:100],
                    'words': item.get('word_count', 0),
                    'likes': item.get('like_count', 0)
                })
            
            return novels
            
        except Exception as e:
            print(f"获取小说列表失败: {e}")
            return self._get_mock_novels()
    
    def get_chapter_content(self, novel_id, chapter_index=0):
        """获取章节内容"""
        # 获取章节目录
        catalog_url = f"{self.API_URL}/novel/{novel_id}/chapters"
        
        try:
            response = self.session.get(catalog_url, timeout=10)
            data = response.json()
            
            chapters = data.get('data', [])
            if not chapters:
                return None
            
            # 获取指定章节
            if chapter_index >= len(chapters):
                chapter_index = 0
            
            chapter = chapters[chapter_index]
            chapter_id = chapter.get('id')
            
            # 获取章节内容
            content_url = f"{self.API_URL}/chapter/{chapter_id}/content"
            content_response = self.session.get(content_url, timeout=10)
            content_data = content_response.json()
            
            content = content_data.get('data', {}).get('content', '')
            return self._clean_content(content)
            
        except Exception as e:
            print(f"获取章节内容失败: {e}")
            return self._get_mock_content()
    
    def _clean_content(self, content):
        """清理内容"""
        # 移除多余空白
        lines = content.split('\n')
        cleaned = []
        for line in lines:
            line = line.strip()
            if line:
                cleaned.append(line)
        return '\n'.join(cleaned)
    
    def _get_mock_novels(self):
        """模拟数据 - 当API失败时使用"""
        return [
            {
                'id': '123456',
                'title': '甜婚蜜爱：总裁别太猛',
                'author': '糖小豆',
                'cover': '',
                'desc': '一场精心设计的阴谋，让她被迫嫁给传闻中的恶魔总裁...',
                'words': 520000,
                'likes': 12888
            },
            {
                'id': '123457',
                'title': '隐婚甜妻：总裁轻点宠',
                author: '顾南城',
                'cover': '',
                'desc': '隐婚三年，她才知道自己是替身...',
                'words': 480000,
                'likes': 9876
            },
            {
                'id': '123458',
                'title': '重生甜妻：墨少轻轻宠',
                'author': '白茶',
                'cover': '',
                'desc': '重生回到十八岁，她决定远离渣渣，抱住金主大腿...',
                'words': 550000,
                'likes': 15632
            }
        ]
    
    def _get_mock_content(self):
        """模拟章节内容"""
        return """凌晨三点，京城市中心医院的VIP病房里。

林晚桐睁开眼睛，入目是一片雪白的天花板。

"醒了？"低沉磁性的男声在耳边响起。

她转头，看到一个穿着黑色西装的男人坐在病床边，五官深邃立体，眉眼如刀裁般锋利，此刻正用一种审视的目光看着她。

"你是谁？"林晚桐的声音有些沙哑。

"你的丈夫。"男人站起身，居高临下地看着她，"或者应该说，是你的未婚夫。"

林晚桐愣住了。

她记得自己明明已经死了，在那个雨夜里，被继母和未婚夫联手推下了楼。

可是现在......

"怎么？摔了一跤，把脑子摔坏了？"男人冷笑一声，"林晚桐，别装了，老爷子还在等我们的好消息。"

"""

if __name__ == "__main__":
    spider = QimaoSpider()
    novels = spider.get_hot_novels('sweet')
    print(f"获取到 {len(novels)} 本小说")
    for n in novels[:3]:
        print(f"- {n['title']} by {n['author']}")
