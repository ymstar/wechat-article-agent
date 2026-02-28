"""
联网搜索工具 - 用于获取实时信息，保证文章的时效性
"""
from langchain.tools import tool
from langchain.tools import ToolRuntime
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_dev_sdk import SearchClient


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
    ctx = runtime.context if runtime else new_context(method="search.web")
    client = SearchClient(ctx=ctx)
    
    try:
        # 执行网络搜索，获取10条结果，包含AI摘要
        response = client.web_search_with_summary(query=query, count=10)
        
        result_lines = []
        
        # 添加AI摘要
        if response.summary:
            result_lines.append(f"【AI摘要】\n{response.summary}\n")
        
        # 添加搜索结果
        if response.web_items:
            result_lines.append(f"【搜索结果】\n")
            for i, item in enumerate(response.web_items, 1):
                result_lines.append(f"{i}. 标题：{item.title}")
                result_lines.append(f"   来源：{item.site_name}")
                result_lines.append(f"   摘要：{item.snippet}")
                if item.auth_info_des:
                    result_lines.append(f"   权威度：{item.auth_info_des}")
                result_lines.append(f"   链接：{item.url}")
                result_lines.append("")
        else:
            result_lines.append("未找到相关搜索结果")
        
        return "\n".join(result_lines)
    except Exception as e:
        return f"搜索失败：{str(e)}"
