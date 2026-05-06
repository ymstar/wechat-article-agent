#!/usr/bin/env python3
"""
微信公众号文章Agent - 主入口
去掉扣子依赖，使用标准 FastAPI + LangGraph
"""
import argparse
import asyncio
import json
import logging
import sys
import os
from typing import Any, Dict, AsyncGenerator

# 添加 src 目录到 Python 路径
src_path = os.path.dirname(os.path.abspath(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from langgraph.graph import StateGraph, END

from src.config import get_config, validate_config
from src.agents.agent import build_agent, AgentState


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LangChainJSONEncoder(json.JSONEncoder):
    """自定义 JSON 编码器，用于处理 LangChain 消息对象"""

    def default(self, obj):
        if hasattr(obj, '__dict__'):
            try:
                return {
                    'type': obj.__class__.__name__,
                    **{k: self._convert_value(v) for k, v in obj.__dict__.items() if not k.startswith('_')}
                }
            except Exception:
                return str(obj)
        
        if isinstance(obj, dict):
            return {k: self._convert_value(v) for k, v in obj.items()}
        
        if isinstance(obj, (list, tuple)):
            return [self._convert_value(item) for item in obj]
        
        return super().default(obj)
    
    def _convert_value(self, value):
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, dict):
            return {k: self._convert_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return [self._convert_value(item) for item in value]
        elif hasattr(value, '__dict__'):
            return str(value)
        else:
            return str(value)


# 超时配置常量
TIMEOUT_SECONDS = 900  # 15分钟


class AgentService:
    """Agent服务类"""
    
    def __init__(self):
        self._agent = None
        self._graph = None
    
    def _get_agent(self):
        """获取Agent实例（懒加载）"""
        if self._agent is None:
            self._agent = build_agent()
        return self._agent
    
    async def run(self, payload: Dict[str, Any], thread_id: str = "default") -> Dict[str, Any]:
        """
        同步运行Agent
        
        Args:
            payload: 输入参数
            thread_id: 会话ID
        
        Returns:
            运行结果
        """
        agent = self._get_agent()
        
        try:
            # 构建输入
            messages = []
            if "text" in payload:
                from langchain_core.messages import HumanMessage
                messages = [HumanMessage(content=payload["text"])]
            elif "messages" in payload:
                messages = payload["messages"]
            
            # 执行
            result = await agent.ainvoke(
                {"messages": messages},
                config={"configurable": {"thread_id": thread_id}}
            )
            
            return {"status": "success", "result": result}
        
        except asyncio.TimeoutError:
            return {"status": "timeout", "message": f"执行超时（超过{TIMEOUT_SECONDS}秒）"}
        except Exception as e:
            logger.error(f"Agent执行错误: {str(e)}", exc_info=True)
            return {"status": "error", "message": str(e)}
    
    async def stream_run(self, payload: Dict[str, Any], thread_id: str = "default") -> AsyncGenerator[str, None]:
        """
        流式运行Agent
        
        Args:
            payload: 输入参数
            thread_id: 会话ID
        
        Yields:
            SSE格式的事件流
        """
        agent = self._get_agent()
        
        try:
            # 构建输入
            messages = []
            if "text" in payload:
                from langchain_core.messages import HumanMessage
                messages = [HumanMessage(content=payload["text"])]
            elif "messages" in payload:
                messages = payload["messages"]
            
            # 流式执行
            async for chunk in agent.astream(
                {"messages": messages},
                config={"configurable": {"thread_id": thread_id}}
            ):
                yield f"data: {json.dumps(chunk, ensure_ascii=False, default=str)}\n\n"
        
        except Exception as e:
            logger.error(f"Agent流式执行错误: {str(e)}", exc_info=True)
            yield f"data: {json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"


# 创建服务实例
service = AgentService()

# 创建FastAPI应用
app = FastAPI(
    title="微信公众号文章Agent",
    description="基于LangGraph的微信公众号文章自动创作Agent",
    version="2.0.0"
)


@app.post("/run")
async def http_run(request: Request) -> Dict[str, Any]:
    """
    同步运行Agent
    
    请求体:
    {
        "text": "请创作一篇关于人工智能的文章"
    }
    或
    {
        "messages": [{"role": "user", "content": "..."}]
    }
    """
    try:
        payload = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    
    # 生成会话ID
    import uuid
    thread_id = payload.get("thread_id", str(uuid.uuid4()))
    
    logger.info(f"Received request: thread_id={thread_id}, payload={payload}")
    
    try:
        result = await asyncio.wait_for(
            service.run(payload, thread_id),
            timeout=float(TIMEOUT_SECONDS)
        )
        result["thread_id"] = thread_id
        return result
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail=f"Execution timeout (exceeded {TIMEOUT_SECONDS} seconds)"
        )


@app.post("/stream_run")
async def http_stream_run(request: Request):
    """
    流式运行Agent (SSE格式)
    
    请求体同/run
    """
    try:
        payload = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    
    # 生成会话ID
    import uuid
    thread_id = payload.get("thread_id", str(uuid.uuid4()))
    
    logger.info(f"Received stream request: thread_id={thread_id}")
    
    return StreamingResponse(
        service.stream_run(payload, thread_id),
        media_type="text/event-stream"
    )


@app.get("/health")
async def health_check():
    """健康检查"""
    # 验证配置
    valid, errors = validate_config()
    
    return {
        "status": "ok" if valid else "degraded",
        "service": "wechat-article-agent",
        "version": "2.0.0",
        "config_valid": valid,
        "config_errors": errors
    }


@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "wechat-article-agent",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="微信公众号文章Agent服务")
    parser.add_argument("-m", "--mode", type=str, default="http", 
                       choices=["http", "cli"],
                       help="运行模式: http(API服务) 或 cli(命令行)")
    parser.add_argument("-p", "--port", type=int, default=5000, help="HTTP服务端口")
    parser.add_argument("-i", "--input", type=str, default="", help="CLI模式输入")
    return parser.parse_args()


async def run_cli(input_text: str):
    """命令行模式运行"""
    from langchain_core.messages import HumanMessage
    
    logger.info(f"CLI mode: input={input_text}")
    
    result = await service.run({"text": input_text})
    
    print(json.dumps(result, ensure_ascii=False, indent=2, cls=LangChainJSONEncoder))


def main():
    """主入口"""
    args = parse_args()
    
    # 验证配置
    valid, errors = validate_config()
    if not valid:
        print("⚠️  配置验证失败:")
        for err in errors:
            print(f"  - {err}")
        print("\n请创建 config/agent_config.json 配置文件")
    
    if args.mode == "http":
        # HTTP服务模式
        print(f"🚀 启动HTTP服务，端口: {args.port}")
        print(f"📚 API文档: http://localhost:{args.port}/docs")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=args.port,
            log_level="info"
        )
    else:
        # CLI模式
        if not args.input:
            print("请提供输入内容: python src/main.py -m cli -i '请创作一篇关于AI的文章'")
            sys.exit(1)
        
        asyncio.run(run_cli(args.input))


if __name__ == "__main__":
    main()
