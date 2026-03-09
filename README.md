# 🍬 甜宠小说转抖音视频

> 自动抓取热门甜宠小说 → 生成语音 → 生成视频

## 📁 项目结构

```
sweet-love-story/
├── app.py                 # Vercel API 入口
├── config.py              # 配置文件
├── vercel.json            # Vercel 配置
├── requirements.txt       # Python 依赖
├── local_test.py         # 本地测试脚本
├── novel_spider/         # 小说爬虫
│   └── qimao.py          # 七猫小说爬虫
├── tts/                  # 语音合成
│   └── edge_tts.py      # Edge TTS
├── video/                # 视频生成
│   └── maker.py          # MoviePy
└── output/               # 输出目录
    └── (生成的文件)
```

## 🚀 快速开始

### 本地测试

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/sweet-love-story.git
cd sweet-love-story

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行测试
python local_test.py
```

### 部署到 Vercel

```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 登录
vercel login

# 3. 部署
vercel deploy
```

或者：
1. 把代码推送到 GitHub
2. 在 Vercel 后台 Import Git Repository
3. 配置环境变量（可选）
4. Deploy!

## 📡 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 查看API状态 |
| `/crawl` | GET | 获取热门小说列表 |
| `/chapter` | GET | 获取章节内容 |
| `/tts` | POST | 生成语音 |
| `/video` | POST | 生成视频 |
| `/auto` | GET | 全自动生成 |

### 调用示例

```bash
# 获取热门小说
curl "https://your-app.vercel.app/crawl?category=sweet"

# 全自动生成
curl "https://your-app.vercel.app/auto"
```

## ⚙️ 配置

在 Vercel 后台设置环境变量：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `NOVEL_SOURCE` | qimao | 小说源 |
| `VOICE_NAME` | zh-CN-XiaoxiaoNeural | 语音 |
| `VIDEO_STYLE` | sweet | 视频风格 |

## 🎨 可选语音

| 语音 | 说明 |
|------|------|
| zh-CN-XiaoxiaoNeural | 晓晓（温柔女声）|
| zh-CN-XiaoyiNeural | 晓伊（活泼女声）|
| zh-CN-JennyNeural | Jenny（成熟女声）|
| zh-CN-YunxiNeural | 云希（沉稳男声）|

## ⚠️ 注意事项

1. **版权**: 请使用免费公版或已授权的小说内容
2. **API限制**: Edge TTS 免费，MoviePy 需要本地渲染
3. **视频生成**: Vercel 免费版有60秒超时，建议生成短视频

## 📞 支持

有问题？请提交 Issue 或联系作者。
