#!/bin/bash
# 部署脚本 - 支持多种部署方式

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_header() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  $1${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
}

# 检查环境
check_env() {
    print_header "检查环境..."
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 未安装"
        exit 1
    fi
    print_success "Python 3 已安装"
    
    # 检查 Docker（可选）
    if command -v docker &> /dev/null; then
        print_success "Docker 已安装"
        DOCKER_AVAILABLE=true
    else
        print_warning "Docker 未安装，跳过 Docker 部署选项"
        DOCKER_AVAILABLE=false
    fi
    
    # 检查配置文件
    if [ ! -f "config/agent_llm_config.json" ]; then
        print_error "配置文件不存在: config/agent_llm_config.json"
        exit 1
    fi
    print_success "配置文件存在"
    
    # 检查 .env 文件
    if [ ! -f ".env" ]; then
        print_warning ".env 文件不存在，将从 .env.example 创建"
        cp .env.example .env
        print_warning "请编辑 .env 文件，填入真实的配置"
    else
        print_success ".env 文件存在"
    fi
}

# 安装依赖
install_deps() {
    print_header "安装依赖..."
    
    pip install -r requirements.txt
    print_success "基础依赖安装完成"
    
    if [ "$1" = "--with-mcp" ]; then
        pip install -r requirements-mcp.txt
        print_success "MCP 依赖安装完成"
    fi
}

# 启动本地服务
start_local() {
    print_header "启动本地服务..."
    
    check_env
    install_deps
    
    echo ""
    echo "🚀 启动 API 服务（端口 5000）..."
    echo "📚 API 文档: http://localhost:5000/docs"
    echo ""
    
    python3 src/main.py -m http -p 5000
}

# 启动 MCP Server
start_mcp() {
    print_header "启动 MCP Server..."
    
    check_env
    install_deps --with-mcp
    
    echo ""
    echo "🚀 启动 MCP Server..."
    echo "💡 使用方法："
    echo "   1. 在 Claude Desktop 配置 MCP"
    echo "   2. 工具名称: wechat-article-creator"
    echo ""
    
    python3 mcp_server.py
}

# Docker 部署
deploy_docker() {
    print_header "Docker 部署..."
    
    if [ "$DOCKER_AVAILABLE" != true ]; then
        print_error "Docker 不可用"
        exit 1
    fi
    
    check_env
    
    # 复制 .env 为 .env.production
    if [ ! -f ".env.production" ]; then
        cp .env .env.production
        print_warning "请编辑 .env.production 文件，配置生产环境变量"
    fi
    
    echo ""
    echo "🐳 构建 Docker 镜像..."
    docker-compose build
    
    echo ""
    echo "🚀 启动容器..."
    docker-compose up -d
    
    print_success "服务已启动"
    echo ""
    echo "📚 API 文档: http://localhost:5000/docs"
    echo "🔍 健康检查: http://localhost:5000/health"
    echo ""
    echo "查看日志:"
    echo "  docker-compose logs -f"
    echo ""
    echo "停止服务:"
    echo "  docker-compose down"
}

# MCP Docker 部署
deploy_mcp_docker() {
    print_header "MCP Docker 部署..."
    
    if [ "$DOCKER_AVAILABLE" != true ]; then
        print_error "Docker 不可用"
        exit 1
    fi
    
    check_env
    
    echo ""
    echo "🐳 构建 Docker 镜像..."
    docker-compose build
    
    echo ""
    echo "🚀 启动 MCP Server 容器..."
    docker-compose --profile mcp up -d
    
    print_success "MCP Server 已启动"
    echo ""
    echo "查看日志:"
    echo "  docker-compose -p mcp logs -f mcp-server"
    echo ""
}

# 测试服务
test_service() {
    print_header "测试服务..."
    
    # 等待服务启动
    sleep 2
    
    echo "🔍 健康检查..."
    response=$(curl -s http://localhost:5000/health)
    
    if echo "$response" | grep -q "ok"; then
        print_success "服务健康检查通过"
    else
        print_error "服务健康检查失败"
        echo "$response"
    fi
    
    echo ""
    echo "🧪 测试配置检查..."
    curl -s -X POST http://localhost:5000/run \
        -H "Content-Type: application/json" \
        -d '{"text": "你好"}' | jq -r '.messages[-1].content' | head -20
}

# 显示帮助
show_help() {
    cat << EOF
微信公众号智能体 - 部署脚本

用法: ./deploy.sh [选项]

选项:
  local           启动本地服务（端口 5000）
  mcp             启动 MCP Server（本地）
  docker          Docker 部署
  mcp-docker      MCP Docker 部署
  test            测试服务
  install         仅安装依赖
  help            显示帮助信息

示例:
  ./deploy.sh local          # 启动本地服务
  ./deploy.sh mcp            # 启动 MCP Server
  ./deploy.sh docker         # Docker 部署
  ./deploy.sh test           # 测试服务

环境变量:
  COZE_WORKLOAD_IDENTITY_API_KEY    # Coze API Key
  COZE_INTEGRATION_MODEL_BASE_URL   # 模型服务地址
  WECHAT_APP_ID                     # 微信公众号 AppID
  WECHAT_APP_SECRET                 # 微信公众号 AppSecret

文档:
  docs/PUBLISH_GUIDE.md  # 发布部署指南
  README.md             # 项目文档

EOF
}

# 主函数
main() {
    case "$1" in
        local)
            start_local
            ;;
        mcp)
            start_mcp
            ;;
        docker)
            deploy_docker
            ;;
        mcp-docker)
            deploy_mcp_docker
            ;;
        test)
            test_service
            ;;
        install)
            check_env
            install_deps
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "未知选项: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
