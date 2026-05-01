"""
联网搜索工具 - 用于获取实时信息，保证文章的时效性
支持多种搜索provider: tavily, serper, serpapi
"""
from typing import Optional
from langchain.tools import tool
from langchain.tools import ToolRuntime

from src.config import get_config


class SearchProvider:
    """搜索Provider基类"""
    
    def search(self, query: str, count: int = 10) -> str:
        """执行搜索并返回格式化结果"""
        raise NotImplementedError


class TavilySearch(SearchProvider):
    """Tavily搜索"""
    
    def __init__(self, api_key: str, search_depth: str = "advanced"):
        self.api_key = api_key
        self.search_depth = search_depth
    
    def search(self, query: str, count: int = 10) -> str:
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=self.api_key)
            
            # Tavily搜索
            response = client.search(
                query=query,
                max_results=count,
                search_depth=self.search_depth,
                include_answer=True,
                include_raw_content=False,
                include_images=False,
            )
            
            result_lines = []
            
            # 添加AI摘要
            if response.get("answer"):
                result_lines.append(f"【AI摘要】\n{response['answer']}\n")
            
            # 添加搜索结果
            results = response.get("results", [])
            if results:
                result_lines.append(f"【搜索结果】\n")
                for i, item in enumerate(results, 1):
                    title = item.get("title", "无标题")
                    url = item.get("url", "")
                    content = item.get("content", "")
                    score = item.get("score", 0)
                    
                    result_lines.append(f"{i}. 标题：{title}")
                    result_lines.append(f"   摘要：{content[:200]}..." if len(content) > 200 else f"   摘要：{content}")
                    result_lines.append(f"   相关度：{score:.2f}")
                    result_lines.append(f"   链接：{url}")
                    result_lines.append("")
            else:
                result_lines.append("未找到相关搜索结果")
            
            return "\n".join(result_lines)
            
        except ImportError:
            return "搜索失败：Tavily SDK未安装，请运行: pip install tavily-python"
        except Exception as e:
            return f"搜索失败：{str(e)}"


class SerperSearch(SearchProvider):
    """Serper搜索 (Google Serper API)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def search(self, query: str, count: int = 10) -> str:
        try:
            import requests
            
            url = "https://google.serper.dev/search"
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            payload = {
                'q': query,
                'num': count
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            result_lines = []
            
            # 添加搜索结果
            results = data.get("organic", [])
            if results:
                result_lines.append(f"【搜索结果】\n")
                for i, item in enumerate(results, 1):
                    title = item.get("title", "无标题")
                    link = item.get("link", "")
                    snippet = item.get("snippet", "")
                    
                    result_lines.append(f"{i}. 标题：{title}")
                    result_lines.append(f"   摘要：{snippet}")
                    result_lines.append(f"   链接：{link}")
                    result_lines.append("")
            else:
                result_lines.append("未找到相关搜索结果")
            
            return "\n".join(result_lines)
            
        except ImportError:
            return "搜索失败：requests库未安装"
        except Exception as e:
            return f"搜索失败：{str(e)}"


class SerpAPISearch(SearchProvider):
    """SerpAPI搜索"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def search(self, query: str, count: int = 10) -> str:
        try:
            from serpapi import GoogleSearch
            
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": count,
                "engine": "google"
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            result_lines = []
            
            # 添加搜索结果
            organic = results.get("organic_results", [])
            if organic:
                result_lines.append(f"【搜索结果】\n")
                for i, item in enumerate(organic, 1):
                    title = item.get("title", "无标题")
                    link = item.get("link", "")
                    snippet = item.get("snippet", "")
                    
                    result_lines.append(f"{i}. 标题：{title}")
                    result_lines.append(f"   摘要：{snippet}")
                    result_lines.append(f"   链接：{link}")
                    result_lines.append("")
            else:
                result_lines.append("未找到相关搜索结果")
            
            return "\n".join(result_lines)
            
        except ImportError:
            return "搜索失败：SerpAPI SDK未安装，请运行: pip install google-search-results"
        except Exception as e:
            return f"搜索失败：{str(e)}"


def get_search_provider() -> Optional[SearchProvider]:
    """根据配置获取搜索provider"""
    config = get_config()
    search_cfg = config.search
    
    if not search_cfg.api_key:
        return None
    
    provider = search_cfg.provider.lower()
    
    if provider == "tavily":
        return TavilySearch(
            api_key=search_cfg.api_key,
            search_depth=search_cfg.search_depth
        )
    elif provider == "serper":
        return SerperSearch(api_key=search_cfg.api_key)
    elif provider == "serpapi":
        return SerpAPISearch(api_key=search_cfg.api_key)
    else:
        # 默认使用Tavily
        return TavilySearch(
            api_key=search_cfg.api_key,
            search_depth=search_cfg.search_depth
        )


@tool
def search_web(query: str, runtime: ToolRuntime = None) -> str:
    """
    搜索网络上的实时信息，用于获取最新的资料、新闻、趋势等数据。
    
    Args:
        query: 搜索关键词，描述需要查询的主题
        runtime: 工具运行时上下文
    
    Returns:
        返回搜索结果的摘要信息，包括标题、摘要、来源等
    """
    provider = get_search_provider()
    
    if provider is None:
        return "搜索失败：未配置搜索API Key，请在config/agent_config.json中配置search.api_key"
    
    return provider.search(query=query, count=10)
