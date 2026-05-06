#!/usr/bin/env python3
"""
加载环境变量脚本
从配置文件读取并导出为环境变量
使用方式: source scripts/load_env.sh 或 eval $(python scripts/load_env.py)
"""
import os
import sys
import json

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src'))

def load_env_from_config():
    """从配置文件加载环境变量"""
    config_files = [
        os.path.join(project_root, 'config/agent_config.json'),
        os.path.join(project_root, 'config/agent_config.json.example'),
    ]
    
    config_path = None
    for path in config_files:
        if os.path.exists(path):
            config_path = path
            break
    
    if not config_path:
        return {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        env_vars = {}
        
        # LLM配置
        llm = config.get('llm', {})
        if llm.get('api_key'):
            env_vars['LLM_API_KEY'] = llm['api_key']
        if llm.get('base_url'):
            env_vars['LLM_BASE_URL'] = llm['base_url']
        if llm.get('model'):
            env_vars['LLM_MODEL'] = llm['model']
        
        # 搜索配置
        search = config.get('search', {})
        if search.get('api_key'):
            env_vars['SEARCH_API_KEY'] = search['api_key']
        
        # 图片配置
        image = config.get('image', {})
        if image.get('api_key'):
            env_vars['IMAGE_API_KEY'] = image['api_key']
        
        # 微信配置
        wechat = config.get('wechat', {})
        if wechat.get('app_id'):
            env_vars['WECHAT_APP_ID'] = wechat['app_id']
        if wechat.get('app_secret'):
            env_vars['WECHAT_APP_SECRET'] = wechat['app_secret']
        
        return env_vars
    
    except Exception as e:
        print(f"# Error loading config: {e}", file=sys.stderr)
        return {}


if __name__ == "__main__":
    env_vars = load_env_from_config()
    
    for key, value in env_vars.items():
        # 转义特殊字符
        escaped_value = value.replace("'", "'\\''")
        print(f"export {key}='{escaped_value}'")
    
    print(f"# Loaded {len(env_vars)} environment variables", file=sys.stderr)
