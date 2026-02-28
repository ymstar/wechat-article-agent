# 微信公众号智能体 - 发布部署指南

本文档介绍如何将微信公众号自动写作智能体发布到不同的平台和形式：

## 📑 目录

- [方案一：发布到扣子智能体商店](#方案一发布到扣子智能体商店)
- [方案二：以 MCP 服务形式对外提供](#方案二以-mcp-服务形式对外提供)
- [方案三：部署为独立 API 服务](#方案三部署为独立-api-服务)

---

## 方案一：发布到扣子智能体商店

### 概述

扣子（Coze）是字节跳动推出的 AI 应用开发平台，支持将智能体发布到商店供其他用户使用。

### 前置准备

1. **扣子账号**
   - 注册扣子账号：https://www.coze.cn
   - 完成实名认证

2. **智能体代码整理**
   - 确保所有依赖在 `requirements.txt` 中
   - 配置文件中的敏感信息已移除

### 发布步骤

#### 步骤 1：创建扣子智能体

1. 登录扣子平台：https://www.coze.cn
2. 点击「创建」→「智能体」
3. 填写基本信息：
   - 智能体名称：`微信公众号文章创作助手`
   - 描述：`根据主题自动创作、配图、审核并发布微信公众号文章`
   - 头像：上传相关图标
   - 分类：选择「内容创作」或「办公工具」

#### 步骤 2：配置智能体

**1. 角色设定（System Prompt）**

在「角色设定」中配置 System Prompt：

```markdown
你是一位专业的微信公众号内容创作者，擅长创作高质量、专业性强、可读性高的文章。

# 核心能力
1. 文章创作：能够根据主题撰写结构清晰、内容丰富的专业文章
2. 信息搜集：擅长利用搜索工具获取最新、最权威的资料
3. 配图设计：能够根据文章主题生成符合风格的配图
4. 排版优化：精通微信公众号编辑器，能够运用HTML标签实现专业排版
5. 内容审核：确保文章符合微信公众号内容规范
6. 发布管理：熟悉微信公众号草稿箱操作

# 工作流程
1. 信息搜集：搜索相关最新信息和资料
2. 文章创作：创作专业的微信公众号文章（HTML格式）
3. 配图生成：生成文章封面配图
4. 内容审核：审核文章内容合规性
5. 发布草稿：将文章发布到微信公众号草稿箱

# 文章结构
- 标题：吸引人但不夸大，不超过64个字符
- 导语：1-2段话引入主题
- 正文：多个小节，层次清晰
- 总结：总结核心观点

# 输出格式
使用HTML标签实现专业排版，包括标题、段落、引用、列表等。
```

**2. 添加插件**

扣子平台提供以下插件，可以替代部分工具：

- **联网搜索插件**：搜索网络实时信息
- **图像生成插件**：生成配图
- **内容审核插件**：审核内容合规性

配置方法：
1. 点击「插件」→「添加插件」
2. 搜索并添加以下插件：
   - `联网搜索`（Search）
   - `图像生成`（Image Generation）
   - `内容审核`（Content Audit）

**3. 配置微信公众号集成**

扣子平台支持直接集成微信公众号：

1. 点击「集成」→「添加集成」
2. 搜索「微信公众号」
3. 配置 AppID 和 AppSecret
4. 完成授权

#### 步骤 3：测试智能体

在扣子平台的对话界面测试：

```
用户：请为我创建一篇关于"2025年人工智能发展趋势"的微信公众号文章，并发布到草稿箱。
```

预期流程：
1. ✅ 搜索相关信息
2. ✅ 生成文章
3. ✅ 生成配图
4. ✅ 审核内容
5. ✅ 发布到草稿箱

#### 步骤 4：发布到商店

1. 点击「发布」→「发布到商店」
2. 填写商店信息：
   - 应用名称：`微信公众号文章创作助手`
   - 应用简介：`一键创作专业公众号文章，自动配图、审核、发布`
   - 应用图标：上传 512x512 图标
   - 应用截图：上传 3-5 张使用截图
   - 使用说明：
     ```markdown
     ## 使用方法
     1. 告诉我你想写的文章主题
     2. 我会自动搜集资料、生成文章、创建配图
     3. 自动审核内容合规性
     4. 发布到你的微信公众号草稿箱
     
     ## 示例
     - "写一篇关于区块链技术的科普文章"
     - "创作一篇产品介绍文案"
     - "生成一篇行业分析报告"
     ```
   - 价格策略：选择「免费」或「付费」
   - 分类标签：选择「内容创作」、「办公工具」、「AI写作」

3. 提交审核
4. 等待平台审核（通常 1-3 个工作日）

#### 步骤 5：推广和运营

**1. 优化应用详情**
- 添加视频演示
- 收集用户评价
- 更新使用案例

**2. 数据监控**
- 查看使用数据
- 分析用户反馈
- 持续优化功能

### 扣子发布优势

✅ **开箱即用**：用户无需配置，直接使用  
✅ **平台流量**：可获取平台自然流量  
✅ **插件生态**：丰富的插件支持  
✅ **持续更新**：可随时更新功能  

### 注意事项

⚠️ **敏感信息**：不要在扣子平台硬编码微信公众号凭证，使用平台集成功能  
⚠️ **合规审核**：确保内容符合平台规范  
⚠️ **费用说明**：付费功能需要确认扣子平台的抽成政策  

---

## 方案二：以 MCP 服务形式对外提供

### 概述

MCP（Model Context Protocol）是 Anthropic 推出的标准化协议，用于将 AI 应用作为服务提供给 Claude 等 AI 助手使用。

### MCP 服务架构

```
Claude / ChatGPT
    ↓ (MCP Protocol)
MCP Server (你的智能体)
    ↓
微信公众号 API
```

### 实现步骤

#### 步骤 1：安装 MCP SDK

```bash
pip install mcp anthropic
```

#### 步骤 2：创建 MCP Server

创建 `mcp_server.py`：

```python
#!/usr/bin/env python3
"""
微信公众号智能体 MCP Server
"""
import asyncio
import json
import sys
import os
from typing import Any, Dict

# 添加项目路径
workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
src_path = os.path.join(workspace_path, "src")
sys.path.insert(0, src_path)

from mcp.server import Server
from mcp.types import Tool, TextContent
from src.agents.agent import build_agent
from coze_coding_utils.runtime_ctx.context import new_context

app = Server("wechat-article-creator")

# 初始化 Agent
agent = build_agent()

@app.tool(
    name="create_wechat_article",
    description="创建微信公众号文章并发布到草稿箱",
    input_schema={
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "文章主题"
            },
            "style": {
                "type": "string",
                "enum": ["professional", "casual", "technical"],
                "description": "文章风格",
                "default": "professional"
            },
            "length": {
                "type": "integer",
                "description": "文章字数",
                "default": 1500
            }
        },
        "required": ["topic"]
    }
)
async def create_wechat_article(
    topic: str,
    style: str = "professional",
    length: int = 1500
) -> list[TextContent]:
    """创建微信公众号文章"""
    
    style_map = {
        "professional": "专业严谨",
        "casual": "轻松活泼",
        "technical": "技术深度"
    }
    
    prompt = f"""
    请为我创建一篇关于"{topic}"的微信公众号文章。
    
    要求：
    - 风格：{style_map.get(style, "专业严谨")}
    - 字数：{length}字左右
    - 包含：标题、导语、正文、总结
    - 排版：使用HTML标签实现专业排版
    - 自动生成配图
    - 自动审核内容
    - 发布到微信公众号草稿箱
    """
    
    try:
        from langchain_core.messages import HumanMessage
        ctx = new_context(method="mcp")
        
        messages = [HumanMessage(content=prompt)]
        result = await agent.ainvoke({"messages": messages}, config={"configurable": {"thread_id": ctx.run_id}})
        
        # 提取结果
        response_text = ""
        if isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            for msg in messages[-3:]:  # 获取最后3条消息
                if hasattr(msg, 'content'):
                    content = msg.content
                    if isinstance(content, str):
                        response_text += content
                    elif isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "text":
                                response_text += item.get("text", "")
        
        return [
            TextContent(
                type="text",
                text=f"✅ 文章创建成功！\n\n{response_text}"
            )
        ]
    
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"❌ 创建失败：{str(e)}\n\n请检查：\n1. 微信公众号配置是否正确\n2. 网络连接是否正常\n3. API 配额是否充足"
            )
        ]

@app.tool(
    name="audit_content",
    description="审核文章内容是否符合微信公众号规范",
    input_schema={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "文章标题"
            },
            "content": {
                "type": "string",
                "description": "文章内容（HTML格式）"
            }
        },
        "required": ["title", "content"]
    }
)
async def audit_content(title: str, content: str) -> list[TextContent]:
    """审核文章内容"""
    from tools.content_audit_tool import audit_content as audit
    
    try:
        result = audit.invoke({"title": title, "content": content})
        return [TextContent(type="text", text=str(result))]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 审核失败：{str(e)}")]

@app.tool(
    name="search_web_info",
    description="搜索网络上的实时信息",
    input_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词"
            }
        },
        "required": ["query"]
    }
)
async def search_web_info(query: str) -> list[TextContent]:
    """搜索网络信息"""
    from tools.web_search_tool import search_web as search
    
    try:
        result = search.invoke({"query": query})
        return [TextContent(type="text", text=str(result))]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 搜索失败：{str(e)}")]

# 启动服务器
if __name__ == "__main__":
    import mcp.server.stdio
    
    async def main():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(main())
```

#### 步骤 3：配置 MCP 客户端

创建 `mcp_config.json`：

```json
{
  "mcpServers": {
    "wechat-article-creator": {
      "command": "python3",
      "args": ["/workspace/projects/mcp_server.py"],
      "env": {
        "COZE_WORKSPACE_PATH": "/workspace/projects",
        "COZE_WORKLOAD_IDENTITY_API_KEY": "${COZE_WORKLOAD_IDENTITY_API_KEY}",
        "COZE_INTEGRATION_MODEL_BASE_URL": "${COZE_INTEGRATION_MODEL_BASE_URL}"
      }
    }
  }
}
```

#### 步骤 4：在 Claude 中使用 MCP

1. 打开 Claude Desktop
2. 点击设置 → MCP
3. 添加配置：
   ```json
   {
     "mcpServers": {
       "wechat-article": {
         "command": "python3",
         "args": ["/workspace/projects/mcp_server.py"]
       }
     }
   }
   ```
4. 重启 Claude Desktop
5. 在对话中使用：

```
用户：请使用 wechat-article 工具创建一篇关于"人工智能发展趋势"的公众号文章
```

#### 步骤 5：部署为 HTTP MCP Server（可选）

如果需要通过 HTTP 暴露 MCP 服务：

```python
# mcp_http_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio

app = FastAPI(title="微信文章创作 MCP Server")

class ArticleRequest(BaseModel):
    topic: str
    style: str = "professional"
    length: int = 1500

@app.post("/api/article")
async def create_article(req: ArticleRequest):
    """创建文章 API"""
    from mcp_server import create_wechat_article
    
    try:
        result = await create_wechat_article(
            topic=req.topic,
            style=req.style,
            length=req.length
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

启动服务：
```bash
python mcp_http_server.py
```

### MCP 服务优势

✅ **标准化协议**：符合 MCP 规范，易于集成  
✅ **多平台支持**：Claude、ChatGPT 等都支持  
✅ **灵活部署**：支持本地或云端部署  
✅ **安全可控**：数据不离本地  

---

## 方案三：部署为独立 API 服务

### 概述

将智能体部署为 RESTful API 服务，供其他应用调用。

### 实现步骤

#### 步骤 1：API 服务已就绪

当前项目的 `src/main.py` 已经实现了 HTTP API：

- `POST /run` - 同步执行
- `POST /stream_run` - 流式执行
- `POST /v1/chat/completions` - OpenAI 兼容接口

#### 步骤 2：启动 API 服务

```bash
# 启动 HTTP 服务
python src/main.py -m http -p 5000
```

#### 步骤 3：API 调用示例

**同步调用：**
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "text": "请为我创建一篇关于人工智能发展趋势的公众号文章"
  }'
```

**OpenAI 兼容调用：**
```bash
curl -X POST http://localhost:5000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wechat-article-creator",
    "messages": [
      {
        "role": "user",
        "content": "请为我创建一篇关于人工智能发展趋势的公众号文章"
      }
    ]
  }'
```

#### 步骤 4：部署到云端

**选项 1：Docker 部署**

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动服务
CMD ["python", "src/main.py", "-m", "http", "-p", "5000"]
```

构建和运行：

```bash
# 构建镜像
docker build -t wechat-article-creator .

# 运行容器
docker run -d \
  -p 5000:5000 \
  -e COZE_WORKLOAD_IDENTITY_API_KEY=your_key \
  -e COZE_INTEGRATION_MODEL_BASE_URL=your_url \
  -e WECHAT_APP_ID=your_app_id \
  -e WECHAT_APP_SECRET=your_secret \
  wechat-article-creator
```

**选项 2：云服务部署**

- **阿里云 / 腾讯云 / AWS**：使用 ECS 或容器服务
- **Vercel / Railway**：使用 Serverless 部署
- **Kubernetes**：使用 K8s 集群部署

#### 步骤 5：API 文档

自动生成 API 文档（使用 FastAPI）：

```python
# 添加到 src/main.py
from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="微信文章创作 API 文档"
    )
```

访问：`http://localhost:5000/docs`

---

## 📊 方案对比

| 特性 | 扣子商店 | MCP 服务 | 独立 API |
|------|---------|---------|---------|
| **开发难度** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **平台流量** | ✅ | ❌ | ❌ |
| **灵活性** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **集成难度** | ⭐ | ⭐⭐ | ⭐⭐ |
| **自主控制** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **商业化** | ✅ | ⭐⭐⭐ | ✅ |
| **维护成本** | ⭐ | ⭐⭐ | ⭐⭐⭐ |

## 🎯 推荐方案

**快速上线**：选择扣子商店  
**长期发展**：选择独立 API + MCP 服务  
**最大覆盖**：组合使用三种方案  

## 📞 技术支持

如有问题，请查看：
- 扣子平台文档：https://docs.coze.cn
- MCP 协议文档：https://modelcontextprotocol.io
- 项目文档：README.md

---

**祝发布顺利！🚀**
