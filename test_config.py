#!/usr/bin/env python3
"""
配置验证脚本
用于验证配置文件是否正确
"""
import os
import sys
import json

# 添加项目路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))


def validate_llm_config(llm: dict) -> list:
    """验证LLM配置"""
    errors = []
    if not llm.get('api_key'):
        errors.append("LLM API Key未配置")
    if not llm.get('base_url'):
        errors.append("LLM Base URL未配置")
    if not llm.get('model'):
        errors.append("LLM Model未配置")
    return errors


def validate_search_config(search: dict) -> list:
    """验证搜索配置"""
    errors = []
    if not search.get('api_key'):
        errors.append("搜索 API Key未配置")
    return errors


def validate_image_config(image: dict) -> list:
    """验证图片配置"""
    errors = []
    if not image.get('api_key'):
        errors.append("图片生成 API Key未配置")
    return errors


def validate_wechat_config(wechat: dict) -> list:
    """验证微信配置"""
    errors = []
    if not wechat.get('app_id'):
        errors.append("微信公众号 AppID未配置")
    if not wechat.get('app_secret'):
        errors.append("微信公众号 AppSecret未配置")
    return errors


def main():
    config_path = os.path.join(project_root, 'config', 'agent_config.json')
    
    print("🔍 微信公众号文章Agent配置验证")
    print("=" * 50)
    
    # 检查配置文件是否存在
    if not os.path.exists(config_path):
        example_path = os.path.join(project_root, 'config', 'agent_config.json.example')
        if os.path.exists(example_path):
            print(f"❌ 配置文件不存在")
            print(f"   请复制配置模板: cp {example_path} {config_path}")
            print(f"   然后编辑 {config_path} 填入您的API Key")
            return 1
        else:
            print(f"❌ 配置文件模板不存在")
            return 1
    
    # 加载配置
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        return 1
    
    all_errors = []
    
    # 验证各模块配置
    llm_errors = validate_llm_config(config.get('llm', {}))
    all_errors.extend([f"  - LLM: {e}" for e in llm_errors])
    
    search_errors = validate_search_config(config.get('search', {}))
    all_errors.extend([f"  - 搜索: {e}" for e in search_errors])
    
    image_errors = validate_image_config(config.get('image', {}))
    all_errors.extend([f"  - 图片: {e}" for e in image_errors])
    
    wechat_errors = validate_wechat_config(config.get('wechat', {}))
    all_errors.extend([f"  - 微信: {e}" for e in wechat_errors])
    
    # 输出结果
    if all_errors:
        print("⚠️  配置验证发现问题:")
        for err in all_errors:
            print(err)
        print()
        print("请编辑 config/agent_config.json 完善配置")
        return 1
    else:
        print("✅ 所有配置项已填写")
        print()
        print("配置摘要:")
        print(f"  LLM Provider: {config.get('llm', {}).get('provider', 'N/A')}")
        print(f"  LLM Model: {config.get('llm', {}).get('model', 'N/A')}")
        print(f"  Search Provider: {config.get('search', {}).get('provider', 'N/A')}")
        print(f"  Image Provider: {config.get('image', {}).get('provider', 'N/A')}")
        print(f"  WeChat AppID: {config.get('wechat', {}).get('app_id', 'N/A')}")
        print()
        print("🚀 配置验证通过！可以启动服务了")
        print("   运行: python src/main.py")
        return 0


if __name__ == '__main__':
    sys.exit(main())
