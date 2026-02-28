"""
配图生成工具 - 为文章生成高质量的配图
"""
from langchain.tools import tool
from langchain.tools import ToolRuntime
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_dev_sdk import ImageGenerationClient


@tool
def generate_article_image(prompt: str, runtime: ToolRuntime = None) -> str:
    """
    为微信公众号文章生成配图。
    
    Args:
        prompt: 图片描述，应该包含主题、风格、色彩等要素
        runtime: 工具运行时上下文
    
    Returns:
        返回生成的图片URL，可直接用于微信公众号
    """
    ctx = runtime.context if runtime else new_context(method="generate")
    client = ImageGenerationClient(ctx=ctx)
    
    try:
        # 生成2K分辨率的图片
        response = client.generate(
            prompt=prompt,
            size="2K",
            watermark=False,  # 不添加水印，适合公众号使用
            response_format="url"
        )
        
        if response.success and response.image_urls:
            # 返回第一张图片的URL
            return response.image_urls[0]
        else:
            error_msg = "、".join(response.error_messages) if response.error_messages else "未知错误"
            return f"图片生成失败：{error_msg}"
    except Exception as e:
        return f"图片生成异常：{str(e)}"
