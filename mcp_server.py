#!/usr/bin/env python3
"""
微信公众号智能体 MCP Server
支持通过 MCP 协议为 Claude 等 AI 助手提供服务
去掉扣子依赖
"""
import asyncio
import json
import sys
import os
from typing import Any, Dict

# 添加项目路径
src_path = os.path.join(os.path.dirname(__file__), "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    print("⚠️  MCP SDK 未安装，请运行: pip install mcp")
    MCP_AVAILABLE = False
    sys.exit(1)

# 导入项目模块
try:
    from src.agents.agent import build_agent
    from src.config import get_config, validate_config
    PROJECT_AVAILABLE = True
except Exception as e:
    print(f"⚠️  项目模块导入失败: {e}")
    PROJECT_AVAILABLE = False


# 创建 MCP Server
app = Server("wechat-article-creator")

# 初始化 Agent
agent = None
if PROJECT_AVAILABLE:
    try:
        # 验证配置
        valid, errors = validate_config()
        if valid:
            agent = build_agent()
            print("✅ Agent 初始化成功")
        else:
            print("⚠️  Agent 初始化失败 - 配置验证失败:")
            for err in errors:
                print(f"  - {err}")
    except Exception as e:
        print(f"⚠️  Agent 初始化失败: {e}")
        agent = None


@app.tool(
    name="create_wechat_article",
    description="创建微信公众号文章并发布到草稿箱。自动完成：信息搜集、文章创作、配图生成、内容审核、发布草稿。",
    input_schema={
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "文章主题，例如：人工智能发展趋势、区块链技术应用等"
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
                "default": 1500,
                "minimum": 500,
                "maximum": 5000
            },
            "auto_publish": {
                "type": "boolean",
                "description": "是否自动发布到草稿箱",
                "default": False
            }
        },
        "required": ["topic"]
    }
)
async def create_wechat_article(
    topic: str,
    style: str = "professional",
    length: int = 1500,
    auto_publish: bool = False
) -> list[TextContent]:
    """
    创建微信公众号文章
    
    参数：
        topic: 文章主题（必填）
        style: 文章风格（可选，默认 professional）
        length: 文章字数（可选，默认 1500）
        auto_publish: 是否自动发布（可选，默认 False）
    """
    
    if not PROJECT_AVAILABLE or not agent:
        return [TextContent(
            type="text",
            text="❌ Agent 未初始化，请检查配置"
        )]
    
    style_map = {
        "professional": "专业严谨",
        "casual": "轻松活泼",
        "technical": "技术深度"
    }
    
    publish_note = "并发布到微信公众号草稿箱" if auto_publish else ""
    
    prompt = f"""
请为我创建一篇关于"{topic}"的微信公众号文章{publish_note}。

要求：
- 风格：{style_map.get(style, "专业严谨")}
- 字数：{length}字左右
- 包含：标题、导语、正文（多个小节）、总结
- 排版：使用HTML标签实现专业排版（标题、段落、引用、列表等）
- 内容：基于最新搜索结果，引用权威来源
{'执行流程：创作 → 生成配图 → 内容审核 → 发布草稿' if auto_publish else '仅生成文章和配图，不发布'}

请严格按照工作流程执行，每完成一步都要汇报进度。
"""
    
    try:
        from langchain_core.messages import HumanMessage
        import uuid
        
        messages = [HumanMessage(content=prompt)]
        thread_id = str(uuid.uuid4())
        
        result = await agent.ainvoke(
            {"messages": messages},
            config={"configurable": {"thread_id": thread_id}}
        )
        
        # 提取结果
        response_text = ""
        if isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            # 获取最后 5 条消息（包含工具调用结果）
            for msg in messages[-5:]:
                if hasattr(msg, 'content'):
                    content = msg.content
                    if isinstance(content, str):
                        response_text += content + "\n"
                    elif isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "text":
                                response_text += item.get("text", "") + "\n"
        
        return [
            TextContent(
                type="text",
                text=f"✅ 文章创建成功！\n\n{response_text.strip()}"
            )
        ]
    
    except Exception as e:
        error_msg = f"❌ 创建失败：{str(e)}"
        
        # 提供排查建议
        suggestions = "\n\n请检查以下事项："
        suggestions += "\n1. 微信公众号配置是否正确（app_id 和 app_secret）"
        suggestions += "\n2. 网络连接是否正常"
        suggestions += "\n3. API 配额是否充足"
        suggestions += "\n4. 配置文件 config/agent_config.json 是否正确"
        
        return [TextContent(type="text", text=error_msg + suggestions)]


@app.tool(
    name="audit_wechat_content",
    description="审核文章内容是否符合微信公众号内容规范。检查：政治敏感、违法信息、虚假宣传、侵权内容、低俗内容、恶意营销、敏感词。",
    input_schema={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "文章标题"
            },
            "content": {
                "type": "string",
                "description": "文章内容（支持HTML格式）"
            }
        },
        "required": ["title", "content"]
    }
)
async def audit_wechat_content(title: str, content: str) -> list[TextContent]:
    """
    审核文章内容
    
    参数：
        title: 文章标题
        content: 文章内容（HTML格式）
    """
    
    try:
        from src.tools.content_audit_tool import audit_content
        result = audit_content.invoke({"title": title, "content": content})
        return [TextContent(type="text", text=str(result))]
    except Exception as e:
        return [TextContent(
            type="text", 
            text=f"❌ 审核失败：{str(e)}\n\n请确保内容格式正确"
        )]


@app.tool(
    name="search_web_for_article",
    description="搜索网络上的实时信息，用于文章创作。返回最新的、权威的资料。",
    input_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词，建议包含主题核心词汇"
            }
        },
        "required": ["query"]
    }
)
async def search_web_for_article(query: str) -> list[TextContent]:
    """
    搜索网络信息
    
    参数：
        query: 搜索关键词
    """
    
    try:
        from src.tools.web_search_tool import search_web
        result = search_web.invoke({"query": query})
        return [TextContent(type="text", text=str(result))]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 搜索失败：{str(e)}\n\n请检查网络连接"
        )]


@app.tool(
    name="get_wechat_config_status",
    description="检查微信公众号配置状态，验证 app_id 和 app_secret 是否配置正确。",
    input_schema={
        "type": "object",
        "properties": {}
    }
)
async def get_wechat_config_status() -> list[TextContent]:
    """
    检查微信公众号配置状态
    """
    
    try:
        config = get_config()
        wechat_cfg = config.wechat
        
        app_id = wechat_cfg.app_id
        app_secret = wechat_cfg.app_secret
        
        if not app_id or not app_secret:
            return [TextContent(
                type="text",
                text="❌ 微信公众号配置不完整\n\n请在 config/agent_config.json 中配置：\n{\n  \"wechat\": {\n    \"app_id\": \"your_app_id\",\n    \"app_secret\": \"your_app_secret\"\n  }\n}"
            )]
        
        # 隐藏 app_secret 的部分信息
        masked_secret = app_secret[:8] + "****" + app_secret[-4:] if len(app_secret) > 12 else "****"
        
        return [TextContent(
            type="text",
            text=f"✅ 微信公众号配置正常\n\nAppID: {app_id}\nAppSecret: {masked_secret}"
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 检查配置失败：{str(e)}"
        )]


# 启动服务器
if __name__ == "__main__":
    import mcp.server.stdio
    
    print("🚀 启动微信公众号智能体 MCP Server...")
    print("📚 可用工具：")
    print("  1. create_wechat_article - 创建文章")
    print("  2. audit_wechat_content - 审核内容")
    print("  3. search_web_for_article - 搜索信息")
    print("  4. get_wechat_config_status - 检查配置")
    print("\n💡 使用方法：")
    print("  在 Claude Desktop 中配置 MCP 服务器，然后在对话中调用工具")
    print()
    
    async def main():
        try:
            async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
                await app.run(
                    read_stream,
                    write_stream,
                    app.create_initialization_options()
                )
        except KeyboardInterrupt:
            print("\n\n👋 MCP Server 已停止")
        except Exception as e:
            print(f"\n❌ MCP Server 运行失败: {e}")
            raise
    
    asyncio.run(main())
