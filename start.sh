#!/bin/bash
# 微信公众号文章Agent启动脚本

set -e

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# 加载环境变量
if [ -f "$PROJECT_ROOT/config/agent_config.json" ]; then
    echo "📁 配置文件已找到: config/agent_config.json"
elif [ -f "$PROJECT_ROOT/config/agent_config.json.example" ]; then
    echo "⚠️  未找到配置文件，正在复制示例..."
    cp "$PROJECT_ROOT/config/agent_config.json.example" "$PROJECT_ROOT/config/agent_config.json"
    echo "⚠️  请编辑 config/agent_config.json 配置您的API Key"
    echo "   然后重新运行此脚本"
    exit 1
else
    echo "❌ 未找到配置文件"
    exit 1
fi

# 检查Python依赖
if ! pip show langchain > /dev/null 2>&1; then
    echo "📦 正在安装依赖..."
    pip install -r requirements.txt
fi

# 解析参数
PORT=${1:-5000}
MODE=${2:-http}

case "$MODE" in
    http)
        echo "🚀 启动HTTP服务 (端口: $PORT)"
        python src/main.py -p "$PORT"
        ;;
    cli)
        echo "💻 CLI模式"
        if [ -z "$3" ]; then
            echo "❌ 请提供输入内容"
            echo "   用法: $0 5000 cli '请创作一篇关于AI的文章'"
            exit 1
        fi
        python src/main.py -m cli -i "$3"
        ;;
    mcp)
        echo "🔧 启动MCP Server"
        python mcp_server.py
        ;;
    *)
        echo "❌ 未知模式: $MODE"
        echo "   支持: http, cli, mcp"
        exit 1
        ;;
esac
