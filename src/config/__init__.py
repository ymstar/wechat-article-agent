#!/usr/bin/env python3
"""
配置管理模块
统一管理所有配置项，支持从配置文件、环境变量、默认值三层优先级
"""
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class LLMConfig:
    """LLM配置"""
    provider: str = "openai"
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 4000
    timeout: int = 120
    thinking: str = "disabled"  # 部分模型支持: "enabled" 或 "disabled"


@dataclass
class SearchConfig:
    """搜索配置"""
    provider: str = "tavily"  # 支持: tavily, serper, serpapi
    api_key: str = ""
    search_depth: str = "advanced"  # basic, advanced


@dataclass
class ImageConfig:
    """图片生成配置"""
    provider: str = "openai"  # 支持: openai (DALL-E), stabilityai
    api_key: str = ""
    model: str = "dall-e-3"  # dall-e-3, dall-e-2, stable-diffusion-xl
    size: str = "1024x1024"
    quality: str = "standard"  # standard, hd


@dataclass
class WechatConfig:
    """微信公众号配置"""
    app_id: str = ""
    app_secret: str = ""


@dataclass
class AuditConfig:
    """审核配置"""
    enable_llm_audit: bool = True
    sensitive_words_path: str = "config/sensitive_words.txt"


@dataclass
class AgentConfig:
    """Agent完整配置"""
    llm: LLMConfig = field(default_factory=LLMConfig)
    search: SearchConfig = field(default_factory=SearchConfig)
    image: ImageConfig = field(default_factory=ImageConfig)
    wechat: WechatConfig = field(default_factory=WechatConfig)
    audit: AuditConfig = field(default_factory=AuditConfig)
    
    # 系统配置
    max_messages: int = 40  # 最大保留消息数
    system_prompt: str = ""  # 系统提示词


class ConfigManager:
    """
    配置管理器
    
    配置优先级: 配置文件 > 环境变量 > 默认值
    """
    
    # 配置文件路径
    CONFIG_FILE = "config/agent_config.json"
    CONFIG_EXAMPLE = "config/agent_config.json.example"
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config_file()
        self._config: Optional[AgentConfig] = None
    
    def _find_config_file(self) -> str:
        """查找配置文件，按优先级尝试多个位置"""
        possible_paths = [
            self.CONFIG_FILE,
            os.path.join(os.path.dirname(__file__), "..", "..", self.CONFIG_FILE),
            os.path.expanduser(f"~/.wechat-article-agent/{self.CONFIG_FILE}"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
        
        # 返回第一个路径作为默认（即使不存在）
        return os.path.abspath(possible_paths[0])
    
    def load(self) -> AgentConfig:
        """加载配置"""
        if self._config is not None:
            return self._config
        
        # 1. 尝试从文件加载
        config_dict = self._load_from_file()
        
        # 2. 合并环境变量（环境变量优先级更高）
        config_dict = self._merge_env_vars(config_dict)
        
        # 3. 解析配置
        self._config = self._parse_config(config_dict)
        return self._config
    
    def _load_from_file(self) -> Dict[str, Any]:
        """从配置文件加载"""
        if not os.path.exists(self.config_path):
            return {}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠️  配置文件解析失败: {e}")
            return {}
    
    def _merge_env_vars(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """合并环境变量"""
        # LLM配置
        if "llm" not in config_dict:
            config_dict["llm"] = {}
        
        env_mappings = {
            # LLM配置
            "LLM_PROVIDER": ("llm", "provider"),
            "LLM_API_KEY": ("llm", "api_key"),
            "LLM_BASE_URL": ("llm", "base_url"),
            "LLM_MODEL": ("llm", "model"),
            "LLM_TEMPERATURE": ("llm", "temperature"),
            "LLM_MAX_TOKENS": ("llm", "max_tokens"),
            
            # 搜索配置
            "SEARCH_PROVIDER": ("search", "provider"),
            "SEARCH_API_KEY": ("search", "api_key"),
            
            # 图片配置
            "IMAGE_PROVIDER": ("image", "provider"),
            "IMAGE_API_KEY": ("image", "api_key"),
            "IMAGE_MODEL": ("image", "model"),
            
            # 微信配置
            "WECHAT_APP_ID": ("wechat", "app_id"),
            "WECHAT_APP_SECRET": ("wechat", "app_secret"),
        }
        
        for env_key, (section, key) in env_mappings.items():
            value = os.getenv(env_key)
            if value:
                if section not in config_dict:
                    config_dict[section] = {}
                
                # 类型转换
                if key in ("temperature",):
                    try:
                        value = float(value)
                    except ValueError:
                        value = None
                elif key in ("max_tokens",):
                    try:
                        value = int(value)
                    except ValueError:
                        value = None
                
                if value is not None:
                    config_dict[section][key] = value
        
        return config_dict
    
    def _parse_config(self, config_dict: Dict[str, Any]) -> AgentConfig:
        """解析配置字典"""
        # LLM配置
        llm_cfg = config_dict.get("llm", {})
        llm = LLMConfig(
            provider=llm_cfg.get("provider", "openai"),
            api_key=llm_cfg.get("api_key", ""),
            base_url=llm_cfg.get("base_url", "https://api.openai.com/v1"),
            model=llm_cfg.get("model", "gpt-4o"),
            temperature=float(llm_cfg.get("temperature", 0.7)),
            max_tokens=int(llm_cfg.get("max_tokens", 4000)),
            timeout=int(llm_cfg.get("timeout", 120)),
            thinking=str(llm_cfg.get("thinking", "disabled")),
        )
        
        # 搜索配置
        search_cfg = config_dict.get("search", {})
        search = SearchConfig(
            provider=search_cfg.get("provider", "tavily"),
            api_key=search_cfg.get("api_key", ""),
            search_depth=search_cfg.get("search_depth", "advanced"),
        )
        
        # 图片配置
        image_cfg = config_dict.get("image", {})
        image = ImageConfig(
            provider=image_cfg.get("provider", "openai"),
            api_key=image_cfg.get("api_key", ""),
            model=image_cfg.get("model", "dall-e-3"),
            size=image_cfg.get("size", "1024x1024"),
            quality=image_cfg.get("quality", "standard"),
        )
        
        # 微信配置
        wechat_cfg = config_dict.get("wechat", {})
        wechat = WechatConfig(
            app_id=wechat_cfg.get("app_id", ""),
            app_secret=wechat_cfg.get("app_secret", ""),
        )
        
        # 审核配置
        audit_cfg = config_dict.get("audit", {})
        audit = AuditConfig(
            enable_llm_audit=audit_cfg.get("enable_llm_audit", True),
            sensitive_words_path=audit_cfg.get("sensitive_words_path", "config/sensitive_words.txt"),
        )
        
        # 系统提示词
        system_prompt = config_dict.get("system_prompt", "")
        
        return AgentConfig(
            llm=llm,
            search=search,
            image=image,
            wechat=wechat,
            audit=audit,
            max_messages=config_dict.get("max_messages", 40),
            system_prompt=system_prompt,
        )
    
    @property
    def config(self) -> AgentConfig:
        """获取配置（懒加载）"""
        if self._config is None:
            return self.load()
        return self._config
    
    def reload(self):
        """重新加载配置"""
        self._config = None
        return self.load()
    
    def validate(self) -> tuple[bool, list[str]]:
        """
        验证配置完整性
        
        注意：现在支持"单API Key启动"，只需要配置 llm.api_key 即可运行
        其他功能（搜索、配图、发布）都是可选的
        
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        warnings = []
        config = self.config
        
        # 检查LLM配置（这是必须的）
        if not config.llm.api_key:
            errors.append("LLM API Key 未配置 (llm.api_key) - 必须配置才能运行")
        
        # 以下是可选配置的提示（不再是错误）
        if not config.search.api_key:
            warnings.append("搜索 API Key 未配置 - 搜索功能已禁用，将使用内置知识创作")
        
        if not config.image.api_key:
            warnings.append("图片生成 API Key 未配置 - 配图功能已禁用，文章将不包含封面图")
        
        if not config.wechat.app_id or not config.wechat.app_secret:
            warnings.append("微信公众号配置未完成 - 发布功能已禁用，需手动复制文章到公众号后台")
        
        return len(errors) == 0, errors + warnings


# 全局配置实例
_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_path: Optional[str] = None) -> ConfigManager:
    """获取全局配置管理器"""
    global _config_manager
    if _config_manager is None or config_path is not None:
        _config_manager = ConfigManager(config_path)
    return _config_manager


def get_config() -> AgentConfig:
    """获取当前配置"""
    return get_config_manager().config


def validate_config() -> tuple[bool, list[str]]:
    """验证配置完整性"""
    return get_config_manager().validate()
