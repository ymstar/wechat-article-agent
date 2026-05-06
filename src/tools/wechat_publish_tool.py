"""
微信公众号草稿发布工具 - 将文章发布到微信公众号草稿箱
"""
import requests
import json
import base64
import os
import time
from typing import Any, Dict, List
from langchain.tools import tool
from langchain.tools import ToolRuntime

from src.config import get_config

# 全局变量缓存 access_token 和过期时间
_access_token_cache = None
_token_expire_time = 0


def load_wechat_config() -> tuple:
    """加载微信公众号配置"""
    config = get_config()
    wechat_cfg = config.wechat
    
    app_id = wechat_cfg.app_id
    app_secret = wechat_cfg.app_secret
    
    if not app_id or not app_secret:
        raise ValueError(
            "微信公众号配置未完成！请在 config/agent_config.json 中配置 app_id 和 app_secret。\n"
            "配置示例：\n"
            "{\n"
            "  \"wechat\": {\n"
            "    \"app_id\": \"your_app_id\",\n"
            "    \"app_secret\": \"your_app_secret\"\n"
            "  }\n"
            "}"
        )
    
    return app_id, app_secret


def get_access_token() -> str:
    """
    获取微信公众号 access_token（使用缓存机制）
    
    Returns:
        access_token 字符串
    """
    global _access_token_cache, _token_expire_time
    
    # 检查缓存是否有效（access_token 有效期为 7200 秒）
    current_time = time.time()
    if _access_token_cache and current_time < _token_expire_time:
        return _access_token_cache
    
    # 缓存失效，重新获取
    app_id, app_secret = load_wechat_config()
    
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "access_token" not in data:
            raise Exception(f"获取 access_token 失败: {data}")
        
        _access_token_cache = data["access_token"]
        # 提前5分钟过期，避免临界问题
        _token_expire_time = current_time + data.get("expires_in", 7200) - 300
        
        return _access_token_cache
    
    except Exception as e:
        raise Exception(f"获取 access_token 异常: {e}")


def _is_base64(s: str) -> bool:
    """检查字符串是否为base64编码"""
    t = s.strip().replace("\n", "")
    try:
        base64.b64decode(t, validate=True)
        return True
    except Exception:
        return False


def _prepare_media_files(image: Any) -> tuple:
    """准备图片文件上传"""
    files = None
    f_to_close = None
    
    if isinstance(image, bytes):
        files = {"media": ("image.jpg", image)}
    elif isinstance(image, str):
        if image.startswith("http://") or image.startswith("https://"):
            resp = requests.get(image, timeout=30)
            resp.raise_for_status()
            files = {"media": ("image.jpg", resp.content)}
        elif image.startswith("data:"):
            b64 = image.split(",", 1)[1] if "," in image else ""
            data = base64.b64decode(b64)
            files = {"media": ("image.jpg", data)}
        elif _is_base64(image):
            data = base64.b64decode(image.strip().replace("\n", ""), validate=True)
            files = {"media": ("image.jpg", data)}
        else:
            if not os.path.isfile(image):
                raise FileNotFoundError(image)
            f_to_close = open(image, "rb")
            files = {"media": f_to_close}
    elif hasattr(image, "read"):
        name = getattr(image, "name", "image")
        files = {"media": (os.path.basename(name), image)}
    else:
        raise ValueError("不支持的图片参数类型")
    
    return files, f_to_close


def upload_permanent_image(image: Any) -> Dict[str, Any]:
    """
    上传永久图片素材
    
    Args:
        image: 图片URL、base64或文件路径
    
    Returns:
        包含media_id和url的字典
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    files, f_to_close = _prepare_media_files(image)
    
    try:
        r = requests.post(url, files=files, timeout=30)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        raise Exception(f"上传永久图片异常: {e}")
    finally:
        if f_to_close:
            try:
                f_to_close.close()
            except Exception:
                pass
    
    if data.get("errcode", 0) != 0:
        raise Exception(f"上传永久图片失败: {data}")
    
    return {"media_id": data.get("media_id"), "url": data.get("url")}


def upload_news_image(image: Any) -> str:
    """
    上传图文消息内的图片
    
    Args:
        image: 图片URL、base64或文件路径
    
    Returns:
        图片URL
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    files, f_to_close = _prepare_media_files(image)
    
    try:
        r = requests.post(url, files=files, timeout=30)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        raise Exception(f"上传图文消息图片异常: {e}")
    finally:
        if f_to_close:
            try:
                f_to_close.close()
            except Exception:
                pass
    
    if data.get("errcode", 0) != 0:
        raise Exception(f"上传图文消息图片失败: {data}")
    
    u = data.get("url")
    if not u:
        raise Exception(f"上传图文消息图片失败: {data}")
    
    return u


def add_draft(articles: List[Dict[str, Any]]) -> str:
    """
    新增草稿
    
    Args:
        articles: 文章列表
    
    Returns:
        草稿media_id
    """
    if not articles:
        raise ValueError("articles不能为空")
    
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    
    try:
        json_data = json.dumps({"articles": articles}, ensure_ascii=False).encode("utf-8")
        r = requests.post(url, data=json_data, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        raise Exception(f"新增草稿异常: {e}")
    
    if data.get("errcode", 0) != 0:
        raise Exception(f"新增草稿失败: {data}")
    
    media_id = data.get("media_id")
    if not media_id:
        raise Exception(f"新增草稿失败: {data}")
    
    return media_id


@tool
def publish_to_wechat(
    title: str,
    content: str,
    cover_image_url: str,
    runtime: ToolRuntime = None
) -> str:
    """
    将文章发布到微信公众号草稿箱。
    
    注意：内容中的图片URL必须先通过upload_news_image处理，否则会被过滤。
    
    Args:
        title: 文章标题
        content: 文章正文内容（HTML格式，支持微信编辑器标签）
        cover_image_url: 封面图片URL
        runtime: 工具运行时上下文
    
    Returns:
        返回草稿的media_id，表示成功发布到草稿箱
    """
    # 首先检查微信公众号配置是否完整
    config = get_config()
    wechat_cfg = config.wechat
    if not wechat_cfg.app_id or not wechat_cfg.app_secret:
        return "【提示】未配置微信公众号API，发布功能已禁用。文章内容已生成完成，请手动复制到公众号后台发布。"
    
    try:
        # 步骤1: 上传封面图片到微信素材库，获取thumb_media_id
        cover_result = upload_permanent_image(cover_image_url)
        thumb_media_id = cover_result["media_id"]
        
        # 步骤2: 处理文章内容中的图片
        # 查找所有<img>标签，将图片URL替换为微信URL
        processed_content = content
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        img_matches = re.findall(img_pattern, content)
        
        for img_url in img_matches:
            # 跳过已经是微信CDN的图片
            if "mmbiz.qpic.cn" in img_url:
                continue
            try:
                wechat_img_url = upload_news_image(img_url)
                processed_content = processed_content.replace(img_url, wechat_img_url)
            except Exception as e:
                # 如果单个图片上传失败，继续处理其他图片
                print(f"图片上传失败（跳过）: {img_url}, 错误: {str(e)}")
        
        # 步骤3: 构建文章对象
        article = {
            "title": title,
            "author": "",  # 可选
            "digest": "",  # 可选，会自动抓取前54个字
            "content": processed_content,
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 0,  # 不打开评论
            "only_fans_can_comment": 0,  # 所有人可评论
            "article_type": "news"
        }
        
        # 步骤4: 创建草稿
        media_id = add_draft([article])
        
        return f"成功发布到微信草稿箱，草稿ID: {media_id}"
    
    except ValueError as e:
        # 配置错误
        return f"配置错误：{str(e)}"
    except Exception as e:
        return f"发布失败：{str(e)}"
