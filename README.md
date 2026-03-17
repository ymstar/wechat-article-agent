<div align="center">

# 微信公众号自动写作发布智能体

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-1.0.3-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-1.0.2-orange.svg)
![GitHub stars](https://img.shields.io/github/stars/ymstar/wechat-article-agent?style=social)
![GitHub forks](https://img.shields.io/github/forks/ymstar/wechat-article-agent?style=social)

[![codecov](https://codecov.io/gh/ymstar/wechat-article-agent/branch/main/graph/badge.svg)](https://codecov.io/gh/[your-username]/[your-repo])

**基于 LangChain 和 LangGraph 的智能内容创作平台**

[快速开始](#-快速开始) • [功能特性](#-功能特性) • [部署指南](#-部署指南) • [文档](#-文档) • [贡献](#-贡献)

</div>

---

## 📖 项目简介

一个基于 LangChain 和 LangGraph 的微信公众号内容创作智能体，能够根据指定主题自动搜集资料、生成专业文章、创建配图、审核内容并发布到微信公众号草稿箱。

### ✨ 核心价值

- 🚀 **高效创作**：全自动文章生成，从选题到发布一站式完成
- 🎨 **智能配图**：AI 生成高质量封面图，提升文章视觉效果
- ✅ **合规审核**：内置内容审核机制，确保符合微信平台规范
- 🌐 **实时搜索**：基于最新网络信息，保证文章时效性
- 📱 **专业排版**：自动生成适合移动端阅读的 HTML 排版

---

## 🌟 功能特性

### 核心功能

- 🔍 **实时信息搜集**：基于网络搜索获取最新、最权威的资料
- ✍️ **智能文章创作**：自动生成结构清晰、内容丰富的专业文章
- 🖼️ **智能配图生成**：根据文章主题自动生成高质量封面图
- ✅ **智能内容审核**：根据微信公众号规范自动审核内容合规性
- 📤 **自动发布草稿**：一键发布到微信公众号草稿箱，支持草稿管理

### 文章特点

- ✅ **专业性**：结构清晰，观点有理有据
- ✅ **实时性**：基于最新搜索结果，引用权威来源
- ✅ **可读性**：语言通俗易懂，适合手机阅读
- ✅ **原创性**：在现有资料基础上加入独立分析
- ✅ **排版美观**：使用专业的微信公众号 HTML 排版
- ✅ **合规安全**：通过内容审核，确保符合平台规范

### 内容审核能力

- 🔍 **7大违规类型检测**：政治敏感、违法信息、虚假宣传、侵权内容、低俗内容、恶意营销、敏感词
- 🤖 **LLM 智能审核**：使用大模型深度分析文章内容
- 📋 **详细审核报告**：提供违规类型、具体原因和修改建议
- 🛡️ **自动过滤敏感词**：内置敏感词库，实时检测违规词汇

---

## 🏗️ 技术架构

### 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| **LLM 模型** | Doubao Seed 2.0 Pro | 强大推理能力 |
| **图像生成** | 豆包生图大模型 | 2K 分辨率 |
| **搜索引擎** | Coze Web Search | 实时信息 |
| **内容审核** | Doubao Seed 2.0 Pro + 敏感词检测 | 双重审核机制 |
| **框架** | LangChain 1.0 + LangGraph 1.0 | Agent 框架 |
| **开发语言** | Python 3.8+ | 主要开发语言 |

### 核心组件

```
src/
├── agents/
│   └── agent.py                  # Agent 核心逻辑
├── tools/
│   ├── web_search_tool.py        # 联网搜索工具
│   ├── image_generation_tool.py  # 配图生成工具
│   ├── content_audit_tool.py     # 内容审核工具
│   └── wechat_publish_tool.py    # 微信发布工具
└── storage/                      # 存储与记忆管理
```

### 工作流程

```
用户输入主题
    ↓
1. 搜索网络信息 (search_web)
    ↓
2. 生成专业文章 (LLM)
    ↓
3. 生成封面配图 (generate_article_image)
    ↓
4. 审核文章内容 (audit_content)
    ↓
5. 用户确认
    ↓
6. 发布到草稿箱 (publish_to_wechat)
```

---

## 📋 环境要求

### 系统要求

- Python 3.8 或更高版本
- Linux/macOS/Windows 操作系统

### 依赖包

所有依赖已包含在 `requirements.txt` 中：

```bash
pip install -r requirements.txt
```

主要依赖包括：

- `langchain>=1.0.0`
- `langgraph>=1.0.0`
- `coze-coding-dev-sdk>=0.5.9`
- `requests>=2.32.0`

---

## 🚀 快速开始

### 方式一：本地运行

#### 1. 克隆项目

```bash
git clone https://github.com/[your-username]/[your-repo].git
cd [your-repo]
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置微信公众号

##### 3.1 获取微信公众号凭证

1. 登录微信公众平台：https://mp.weixin.qq.com
2. 进入「设置与开发」→「基本配置」
3. 记录以下信息：
   - **开发者ID (AppID)**：类似 `wx1234567890abcdef`
   - **开发者密码 (AppSecret)**：点击「重置」或「查看」获取

##### 3.2 配置项目

```bash
# 复制示例配置文件
cp config/agent_llm_config.json.example config/agent_llm_config.json

# 编辑配置文件
vim config/agent_llm_config.json
```

填入你的微信公众号信息：

```json
{
    "wechat": {
        "app_id": "YOUR_WECHAT_APP_ID",
        "app_secret": "YOUR_WECHAT_APP_SECRET"
    }
}
```

⚠️ **重要提示**：
- `config/agent_llm_config.json` 已在 `.gitignore` 中，不会被提交到 Git
- 请妥善保管你的 AppSecret，不要泄露

#### 4. 运行项目

```bash
# 方式 1：直接运行
python src/main.py

# 方式 2：使用部署脚本
./deploy.sh local

# 方式 3：HTTP 服务模式
python src/main.py --mode http
```

### 方式二：Docker 部署

```bash
# 1. 构建镜像
docker build -t wechat-article-agent .

# 2. 运行容器
docker run -d \
  --name wechat-agent \
  -p 5000:5000 \
  -e COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key \
  -e COZE_INTEGRATION_MODEL_BASE_URL=https://api.example.com/v1 \
  -e WECHAT_APP_ID=your_app_id \
  -e WECHAT_APP_SECRET=your_app_secret \
  wechat-article-agent

# 3. 访问服务
open http://localhost:5000/docs
```

### 方式三：MCP Server

```bash
# 1. 安装 MCP 依赖
pip install -r requirements-mcp.txt

# 2. 启动 MCP Server
python mcp_server.py

# 3. 在 Claude Desktop 配置
# 设置 → Developer → Edit Configurations:
{
  "mcpServers": {
    "wechat-article": {
      "command": "python3",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

详细部署指南请查看：[发布部署指南](docs/PUBLISH_GUIDE.md)

---

## 📖 使用示例

### 本地调用

```python
from src.agents.agent import build_agent

# 构建 Agent
agent = build_agent()

# 运行对话
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "请帮我创作一篇关于'人工智能发展趋势'的公众号文章"}
    ]
})

print(result)
```

### HTTP API 调用

```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "text": "请帮我创作一篇关于'人工智能发展趋势'的公众号文章"
  }'
```

### Claude MCP

在 Claude 中直接使用：

```
用户：请使用 wechat-article 工具创建一篇关于"人工智能发展趋势"的公众号文章

Claude：好的，我将为您创建文章...

[自动调用 MCP 工具]

✅ 文章创建成功！
```

---

## 📚 文档

| 文档 | 描述 |
|------|------|
| [README.md](README.md) | 项目说明和快速开始 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献指南 |
| [CHANGELOG.md](CHANGELOG.md) | 变更日志 |
| [SECURITY.md](SECURITY.md) | 安全政策 |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | 行为准则 |
| [docs/PUBLISH_GUIDE.md](docs/PUBLISH_GUIDE.md) | 发布部署指南 |

---

## 🤝 贡献

我们欢迎任何形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与贡献。

### 快速贡献流程

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 添加某个功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

详细步骤请参考：[贡献指南](CONTRIBUTING.md)

---

## 📜 开源协议

本项目采用 [Apache License 2.0](LICENSE) 开源协议。

```
Copyright 2025 [Your Name or Organization]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## 🙏 致谢

感谢以下开源项目：

- [LangChain](https://github.com/langchain-ai/langchain) - 强大的 LLM 应用开发框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent 编排框架
- [Doubao](https://www.doubao.com/) - 强大的 AI 模型服务

---

## 📞 联系方式

- **项目地址**：[https://github.com/[your-username]/[your-repo]](https://github.com/ymstar/wechat-article-agen)
- **问题反馈**：[Issues](https://github.com/ymstar/wechat-article-agent/issues)
- **讨论交流**：[Discussions](https://github.com/ymstar/wechat-article-agent/discussions)

---

## 🌟 Star History

如果这个项目对你有帮助，请给我们一个 Star ⭐️

[![Star History Chart](https://api.star-history.com/svg?repos=ymstar/wechat-article-agent&type=Date)](https://star-history.com/#ymstar/wechat-article-agent&Date)

---

<div align="center">

**Made with ❤️ by ymstar**

[⬆ 回到顶部](#微信公众号自动写作发布智能体)

</div>
