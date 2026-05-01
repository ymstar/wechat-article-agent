#!/bin/bash
# 加载环境变量脚本
# 使用方式: source scripts/load_env.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 检查配置文件
if [ ! -f "$PROJECT_ROOT/config/agent_config.json" ]; then
    echo "# Warning: config/agent_config.json not found"
    if [ -f "$PROJECT_ROOT/config/agent_config.json.example" ]; then
        echo "# Copy example config: cp config/agent_config.json.example config/agent_config.json"
    fi
    return 0 2>/dev/null || exit 0
fi

# 使用Python解析JSON
eval "$(python3 "$SCRIPT_DIR/load_env.py")"

echo "# Environment variables loaded from config"
