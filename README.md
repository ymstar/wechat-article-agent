<div align="center">

# 微信公众号自动写作发布智能体

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-1.0-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-1.0-orange.svg)

**基于 LangChain 和 LangGraph 的智能内容创作平台，支持自定义LLM配置**

[快速开始](#-快速开始) • [功能特性](#-功能特性) • [配置指南](#-配置指南) • [部署指南](#-部署指南) • [API文档](#-api文档)

</div>

---

## 📖 项目简介

一个基于 LangChain 和 LangGraph 的微信公众号内容创作智能体，能够根据指定主题自动搜集资料、生成专业文章、创建配图、审核内容并发布到微信公众号草稿箱。

**本版本完全去除扣子(Coze)依赖，支持用户配置自己的API Key运行。**

### ✨ 核心价值

- 🚀 **高效创作**：全自动文章生成，从选题到发布一站式完成
- 🎨 **智能配图**：AI 生成高质量封面图，提升文章视觉效果
- ✅ **合规审核**：内置内容审核机制，确保符合微信平台规范
- 🌐 **实时搜索**：基于最新网络信息，保证文章时效性
- 📱 **专业排版**：自动生成适合移动端阅读的 HTML 排版
- 🔧 **通用LLM**：支持 OpenAI/Claude/DeepSeek 等任意 OpenAI 兼容 API

---

## 🌟 功能特性

### 核心功能

- 🔍 **实时信息搜集**：基于 Tavily/Serper 搜索获取最新、最权威的资料
- ✍️ **智能文章创作**：自动生成结构清晰、内容丰富的专业文章
- 🖼️ **智能配图生成**：支持 DALL-E 3 / Stable Diffusion 等
- ✅ **智能内容审核**：根据微信公众号规范自动审核内容合规性
- 📤 **自动发布草稿**：一键发布到微信公众号草稿箱

### LLM 支持

| 提供商 | 模型 | 状态 |
|--------|------|------|
| OpenAI | GPT-4o, GPT-4, GPT-3.5 | ✅ 支持 |
| Anthropic | Claude 3.5, Claude 3 | ✅ 支持 |
| DeepSeek | DeepSeek V3, DeepSeek Coder | ✅ 支持 |
| 火山引擎 | Doubao, Seed 系列 | ✅ 支持 |
| 其他 | 任意 OpenAI 兼容 API | ✅ 支持 |

### 搜索支持

| 提供商 | 免费额度 | 状态 |
|--------|----------|------|
| Tavily | 1000次/月 | ✅ 推荐 |
| Serper | 2500次/月 | ✅ 支持 |
| SerpAPI | 100次/月 | ✅ 支持 |

### 配图支持

| 提供商 | 模型 | 状态 |
|--------|------|------|
| OpenAI DALL-E | DALL-E 3, DALL-E 2 | ✅ 支持 |
| Stability AI | Stable Diffusion XL | ⚙️ 可选 |

---

## 📋 环境要求

### 系统要求

- Python 3.8 或更高版本
- Linux/macOS/Windows 操作系统

### 依赖安装

```bash
pip install -r requirements.txt
```

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/ymstar/wechat-article-agent.git
cd wechat-article-agent
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

```bash
# 复制配置模板
cp config/agent_config.json.example config/agent_config.json

# 编辑配置文件
vim config/agent_config.json
```

详细配置说明请查看 [配置指南](#-配置指南)

### 4. 运行服务

```bash
# HTTP服务模式 (默认端口5000)
python src/main.py

# 或指定端口
python src/main.py -p 8080

# CLI模式
python src/main.py -m cli -i "请创作一篇关于AI发展趋势的文章"
```

### 5. 访问 API

```
API文档: http://localhost:5000/docs
```

---

## 📝 配置指南

### 完整配置示例

```json
{
    "llm": {
        "provider": "openai",
        "api_key": "sk-your-api-key",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 4000,
        "timeout": 120
    },
    "search": {
        "provider": "tavily",
        "api_key": "tvly-your-tavily-api-key",
        "search_depth": "advanced"
    },
    "image": {
        "provider": "openai",
        "api_key": "sk-your-api-key",
        "model": "dall-e-3",
        "size": "1024x1024",
        "quality": "standard"
    },
    "wechat": {
        "app_id": "wx-your-app-id",
        "app_secret": "your-app-secret"
    },
    "audit": {
        "enable_llm_audit": true,
        "sensitive_words_path": "config/sensitive_words.txt"
    }
}
```

### 配置项说明

#### LLM 配置 (`llm`)

| 参数 | 说明 | 示例 |
|------|------|------|
| `provider` | LLM 提供商 | `openai`, `anthropic`, `deepseek` |
| `api_key` | API Key | `sk-xxx` |
| `base_url` | API 地址 | `https://api.openai.com/v1` |
| `model` | 模型名称 | `gpt-4o`, `claude-3-5-sonnet` |
| `temperature` | 温度参数 | `0.7` |
| `max_tokens` | 最大 token 数 | `4000` |

#### 搜索配置 (`search`)

| 参数 | 说明 | 示例 |
|------|------|------|
| `provider` | 搜索提供商 | `tavily`, `serper`, `serpapi` |
| `api_key` | API Key | `tvly-xxx` |

#### 图片配置 (`image`)

| 参数 | 说明 | 示例 |
|------|------|------|
| `provider` | 图片提供商 | `openai`, `stabilityai` |
| `api_key` | API Key | `sk-xxx` |
| `model` | 模型 | `dall-e-3` |
| `size` | 图片尺寸 | `1024x1024` |

#### 微信公众号配置 (`wechat`)

| 参数 | 说明 | 获取方式 |
|------|------|----------|
| `app_id` | 应用ID | 公众平台 -> 设置 -> 基本配置 |
| `app_secret` | 应用密钥 | 公众平台 -> 设置 -> 基本配置 |

### 获取 API Key

#### OpenAI API Key

1. 访问 https://platform.openai.com/api-keys
2. 创建新的 API Key
3. 充值或选择付费套餐

#### Tavily API Key

1. 访问 https://tavily.com
2. 注册并获取免费 API Key
3. 免费额度：1000次/月

#### 微信公众号凭证

1. 登录 https://mp.weixin.qq.com
2. 进入「设置与开发」→「基本配置」
3. 记录 AppID 和 AppSecret

### 环境变量优先级

配置优先级：`环境变量` > `config/agent_config.json` > `默认值`

支持的的环境变量：

```bash
export LLM_API_KEY="sk-xxx"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="gpt-4o"
export SEARCH_API_KEY="tvly-xxx"
export IMAGE_API_KEY="sk-xxx"
export WECHAT_APP_ID="wx-xxx"
export WECHAT_APP_SECRET="xxx"
```

---

## 🏗️ 技术架构

### 技术栈

| 技术 | 说明 |
|------|------|
| **LangChain** | LLM 应用开发框架 |
| **LangGraph** | Agent 编排框架 |
| **FastAPI** | HTTP API 框架 |
| **Tavily** | 实时搜索服务 |

### 项目结构

```
wechat-article-agent/
├── src/
│   ├── main.py                    # 主入口
│   ├── config/                    # 配置管理
│   │   └── __init__.py            # 配置加载器
│   ├── agents/
│   │   └── agent.py               # Agent 核心逻辑
│   └── tools/
│       ├── web_search_tool.py     # 联网搜索工具
│       ├── image_generation_tool.py # 配图生成工具
│       ├── content_audit_tool.py  # 内容审核工具
│       └── wechat_publish_tool.py # 微信发布工具
├── config/
│   ├── agent_config.json.example  # 配置模板
│   └── sensitive_words.txt        # 敏感词库
├── scripts/
│   └── load_env.sh                # 环境变量加载脚本
├── requirements.txt               # Python 依赖
├── mcp_server.py                  # MCP Server
└── README.md                      # 项目文档
```

### 工作流程

```
用户输入主题
    ↓
1. 搜索网络信息 (Tavily/Serper)
    ↓
2. 生成专业文章 (LLM)
    ↓
3. 生成封面配图 (DALL-E/Stability)
    ↓
4. 审核文章内容 (LLM + 敏感词)
    ↓
5. 发布到草稿箱 (微信API)
```

---

## 📖 API 文档

### HTTP API

#### 运行 Agent

```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"text": "请创作一篇关于AI发展趋势的文章"}'
```

响应：
```json
{
  "status": "success",
  "result": {...},
  "thread_id": "xxx"
}
```

#### 流式运行

```bash
curl -X POST http://localhost:5000/stream_run \
  -H "Content-Type: application/json" \
  -d '{"text": "请创作一篇关于AI的文章"}'
```

#### 健康检查

```bash
curl http://localhost:5000/health
```

### Python SDK

```python
from src.agents.agent import build_agent
from langchain_core.messages import HumanMessage

# 构建 Agent
agent = build_agent()

# 运行
result = await agent.ainvoke({
    "messages": [HumanMessage(content="请创作一篇关于AI的文章")]
})

print(result)
```

---

## 🐳 Docker 部署

### 构建镜像

```bash
docker build -t wechat-article-agent .
```

### 运行容器

```bash
docker run -d \
  --name wechat-agent \
  -p 5000:5000 \
  -v $(pwd)/config:/app/config \
  -e LLM_API_KEY=sk-xxx \
  -e SEARCH_API_KEY=tvly-xxx \
  -e IMAGE_API_KEY=sk-xxx \
  -e WECHAT_APP_ID=wx-xxx \
  -e WECHAT_APP_SECRET=xxx \
  wechat-article-agent
```

### Docker Compose

```yaml
version: '3.8'
services:
  wechat-agent:
    image: wechat-article-agent
    ports:
      - "5000:5000"
    volumes:
      - ./config:/app/config
    environment:
      - LLM_API_KEY=sk-xxx
      - SEARCH_API_KEY=tvly-xxx
      - IMAGE_API_KEY=sk-xxx
      - WECHAT_APP_ID=wx-xxx
      - WECHAT_APP_SECRET=xxx
```

---

## 🤝 MCP Server

支持通过 MCP 协议为 Claude 等 AI 助手提供服务。

### 安装 MCP 依赖

```bash
pip install -r requirements-mcp.txt
```

### 启动 MCP Server

```bash
python mcp_server.py
```

### Claude Desktop 配置

```json
{
  "mcpServers": {
    "wechat-article": {
      "command": "python3",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

---

## 🔧 常见问题

### Q: 配置文件路径在哪里？

默认路径：`config/agent_config.json`

可通过环境变量指定：
```bash
export CONFIG_PATH=/path/to/config.json
```

### Q: 如何使用 Claude？

```json
{
  "llm": {
    "provider": "anthropic",
    "api_key": "sk-ant-xxx",
    "base_url": "https://api.anthropic.com/v1",
    "model": "claude-3-5-sonnet-20241022"
  }
}
```

### Q: 如何使用 DeepSeek？

```json
{
  "llm": {
    "provider": "deepseek",
    "api_key": "sk-xxx",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat"
  }
}
```

### Q: 搜索失败怎么办？

1. 检查 `search.api_key` 是否配置
2. 确认 API Key 是否有效
3. 查看日志获取详细错误信息

---

## 📜 开源协议

本项目采用 [Apache License 2.0](LICENSE) 开源协议。

---

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - LLM 应用开发框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent 编排框架
- [Tavily](https://tavily.com) - 实时搜索服务

---

<div align="center">

**Made with ❤️**

</div>
