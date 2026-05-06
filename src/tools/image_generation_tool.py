"""
配图生成工具 - 为文章生成高质量的配图
支持多种provider: openai (DALL-E), stabilityai
"""
from typing import Optional
import base64
import os
from langchain.tools import tool
from langchain.tools import ToolRuntime

from src.config import get_config


class ImageProvider:
    """图片生成Provider基类"""
    
    def generate(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        """生成图片并返回URL或base64"""
        raise NotImplementedError


class OpenAIImage(ImageProvider):
    """OpenAI DALL-E图片生成"""
    
    def __init__(self, api_key: str, model: str = "dall-e-3"):
        self.api_key = api_key
        self.model = model
    
    def generate(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            # DALL-E 3 支持 1024x1024, 1024x1792, 1792x1024
            # DALL-E 2 支持 256x256, 512x512, 1024x1024
            if self.model == "dall-e-3":
                if size not in ["1024x1024", "1024x1792", "1792x1024"]:
                    size = "1024x1024"
            else:
                if size not in ["256x256", "512x512", "1024x1024"]:
                    size = "1024x1024"
            
            response = client.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
                response_format="url"
            )
            
            if response.data and response.data[0].url:
                return response.data[0].url
            else:
                return "图片生成失败：未获取到图片URL"
                
        except ImportError:
            return "图片生成失败：OpenAI SDK未安装，请运行: pip install openai"
        except Exception as e:
            return f"图片生成失败：{str(e)}"


class StabilityAIImage(ImageProvider):
    """Stability AI图片生成"""
    
    def __init__(self, api_key: str, model: str = "stable-diffusion-xl-1024-v1-0"):
        self.api_key = api_key
        self.model = model
    
    def generate(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        try:
            import stability_sdk.client
            import stability_sdk.api as stability
            
            # 设置API key
            stability.api.key = self.api_key
            
            # 解析尺寸
            width, height = map(int, size.split("x"))
            
            # 调用API
            answer = stability.Generation.generate(
                prompt=stability.TextPrompt(
                    text=prompt,
                    weight=1.0
                ),
                steps=30,
                seed=42,
                cfg_scale=7.0,
                width=width,
                height=height,
                samples=1,
                model=stability.GenerationModel(self.model),
            )
            
            # 处理结果
            for resp in answer:
                if resp.HasField("artifact"):
                    artifact = resp.artifact
                    if artifact.type == stability.Artifact.IMAGE:
                        # 保存到临时文件
                        img_data = artifact.binary
                        
                        # 尝试上传到临时图床或返回base64
                        import tempfile
                        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                            f.write(img_data)
                            temp_path = f.name
                        
                        # 这里返回本地路径，实际使用时可上传到图床
                        return f"data:image/png;base64,{base64.b64encode(img_data).decode()}"
            
            return "图片生成失败：未获取到图片数据"
                
        except ImportError:
            return "图片生成失败：Stability AI SDK未安装，请运行: pip install stability-sdk"
        except Exception as e:
            return f"图片生成失败：{str(e)}"


class DummyImageProvider(ImageProvider):
    """占位图片生成器（用于测试）"""
    
    def generate(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        return f"[占位图片] prompt: {prompt[:50]}... size: {size}"


def get_image_provider() -> Optional[ImageProvider]:
    """根据配置获取图片生成provider"""
    config = get_config()
    image_cfg = config.image
    
    if not image_cfg.api_key:
        return None
    
    provider = image_cfg.provider.lower()
    
    if provider == "openai":
        return OpenAIImage(
            api_key=image_cfg.api_key,
            model=image_cfg.model
        )
    elif provider == "stabilityai":
        return StabilityAIImage(
            api_key=image_cfg.api_key,
            model="stable-diffusion-xl-1024-v1-0"
        )
    elif provider == "dummy":
        return DummyImageProvider()
    else:
        # 默认使用OpenAI
        return OpenAIImage(
            api_key=image_cfg.api_key,
            model=image_cfg.model
        )


@tool
def generate_article_image(prompt: str, runtime: ToolRuntime = None) -> str:
    """
    为微信公众号文章生成配图。
    
    Args:
        prompt: 图片描述，应该包含主题、风格、色彩等要素
        runtime: 工具运行时上下文
    
    Returns:
        返回生成的图片URL或base64编码，可直接用于微信公众号
    """
    provider = get_image_provider()
    
    if provider is None:
        return "【提示】未配置图片生成API Key，配图功能已禁用。文章可以不包含配图，或建议用户配置 image.api_key 启用配图生成。"
    
    config = get_config()
    
    return provider.generate(
        prompt=prompt,
        size=config.image.size,
        quality=config.image.quality
    )
