# 初始化目录
if [ "$COZE_PROJECT_ENV" = "DEV" ]; then
  if [ ! -d "${COZE_WORKSPACE_PATH}/assets" ]; then
    mkdir -p "${COZE_WORKSPACE_PATH}/assets"
  fi
fi

# 安装Python三方包依赖
pip install -r requirements.txt
