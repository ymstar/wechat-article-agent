# 贡献指南

感谢你考虑为微信公众号自动写作发布智能体项目做出贡献！我们欢迎任何形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复或功能改进
- 🤝 帮助其他用户解决问题

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交 Pull Request](#提交-pull-request)
- [问题报告](#问题报告)

## 🤝 行为准则

本项目采用贡献者契约（Contributor Covenant）作为行为准则。请阅读 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) 了解详情。

简而言之：
- 尊重不同观点和经验
- 优雅地接受建设性批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

## 🚀 如何贡献

### 报告 Bug

在报告 Bug 之前，请先：

1. 🔍 搜索现有的 [Issues](https://github.com/[your-username]/[your-repo]/issues)，确认问题未被报告
2. 创建新的 Issue，使用 Bug Report 模板
3. 提供详细信息：
   - 问题描述
   - 复现步骤
   - 预期行为
   - 实际行为
   - 环境信息（操作系统、Python 版本等）
   - 相关日志或截图

### 提出新功能

1. 🔍 搜索现有的 [Issues](https://github.com/[your-username]/[your-repo]/issues) 和 [Pull Requests](https://github.com/[your-username]/[your-repo]/pulls)
2. 创建新的 Feature Request Issue，详细描述你的想法
3. 说明这个功能的价值和预期用法
4. 等待维护者讨论和反馈

### 提交代码

#### 前置准备

1. **Fork 项目**
   ```bash
   # 在 GitHub 上点击 "Fork" 按钮
   ```

2. **克隆你的 Fork**
   ```bash
   git clone https://github.com/[your-username]/[your-repo].git
   cd [your-repo]
   ```

3. **添加上游仓库**
   ```bash
   git remote add upstream https://github.com/[original-username]/[your-repo].git
   ```

4. **创建虚拟环境**
   ```bash
   # 使用 venv
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows

   # 使用 conda
   conda create -n wechat-agent python=3.8
   conda activate wechat-agent
   ```

5. **安装依赖**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-mcp.txt  # 如果需要 MCP 支持
   ```

## 🔄 开发流程

### 1. 创建分支

为每个功能或修复创建一个新分支：

```bash
# 从 main 分支创建新分支
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/bug-description
```

**分支命名规范：**
- `feature/` - 新功能
- `fix/` - Bug 修复
- `docs/` - 文档更新
- `refactor/` - 代码重构
- `test/` - 测试相关
- `chore/` - 构建或工具链相关

### 2. 进行开发

- 遵循项目代码规范（见下方）
- 添加必要的测试
- 更新相关文档

### 3. 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 或使用项目提供的测试脚本
python src/main.py --test
```

### 4. 提交代码

```bash
# 添加修改的文件
git add .

# 提交（遵循提交信息规范）
git commit -m "feat: 添加新功能描述"

# 或提交到暂存区
git commit -m "fix: 修复某Bug"
```

**提交信息规范：**

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type（类型）：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建或工具链相关
- `ci`: CI/CD 相关

**示例：**
```
feat(agent): 添加多语言支持功能

- 支持英文、日文文章生成
- 添加语言检测工具
- 更新文档说明多语言用法

Closes #123
```

### 5. 同步上游代码

```bash
# 获取上游最新代码
git fetch upstream

# 合并上游 main 分支到你的分支
git merge upstream/main

# 解决冲突（如果有）
```

### 6. 推送到你的 Fork

```bash
git push origin feature/your-feature-name
```

## 📐 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- 使用类型提示（Type Hints）
- 添加 docstring 说明函数和类的用途
- 最大行长度：120 字符
- 使用 4 空格缩进

**示例：**
```python
from typing import Optional, List
from langchain.tools import tool

@tool
def example_tool(input_param: str, optional_param: Optional[int] = None) -> str:
    """
    示例工具函数。
    
    Args:
        input_param: 输入参数说明
        optional_param: 可选参数说明
        
    Returns:
        str: 返回值说明
        
    Example:
        >>> result = example_tool("test")
        >>> print(result)
    """
    # 实现代码
    return "result"
```

### 文档规范

- 使用 Markdown 格式
- 提供清晰的使用示例
- 说明参数和返回值
- 添加适当的截图或图表

### 测试规范

- 为新功能编写单元测试
- 测试覆盖率应 > 80%
- 使用清晰的测试名称
- 添加必要的测试数据

**示例：**
```python
import pytest
from src.tools.web_search_tool import search_web

def test_search_web_basic():
    """测试基本的网络搜索功能"""
    result = search_web("人工智能")
    assert result is not None
    assert len(result) > 0
```

## 📤 提交 Pull Request

### PR 检查清单

在提交 PR 之前，请确保：

- [ ] 代码通过所有测试
- [ ] 代码符合项目风格规范
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] Commit 信息清晰明确
- [ ] PR 描述清晰说明了变更内容
- [ ] 没有引入新的警告或错误

### PR 描述模板

```markdown
## 变更类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 重构
- [ ] 文档更新
- [ ] 其他

## 变更描述
简要描述你的变更内容和目的。

## 测试情况
说明你如何测试了这些变更。

## 相关 Issue
Closes #123

## 截图（如果有）
如有 UI 变更，请提供截图。
```

### 提交 PR

1. 访问你的 Fork 页面
2. 点击 "Compare & pull request"
3. 填写 PR 描述
4. 等待代码审查

### 代码审查

- 维护者会审查你的代码
- 可能会要求你进行修改
- 请及时回应反馈意见

## 🐛 问题报告

### 报告前检查

- [ ] 搜索现有 Issues
- [ ] 确认是 Bug 而不是使用问题
- [ ] 提供最小复现示例
- [ ] 包含完整的错误堆栈

### Issue 模板

使用项目提供的 Issue 模板创建问题报告。

## 📝 文档贡献

文档是项目的重要组成部分！你可以：

- 修正拼写和语法错误
- 添加缺失的示例
- 改进现有文档的清晰度
- 添加新的教程或指南

文档贡献同样遵循上述开发流程。

## 🎯 贡献者指南

### 首次贡献

如果你是第一次贡献，建议：

1. 从简单的 Bug 修复或文档改进开始
2. 查看 "good first issue" 标签的 Issues
3. 在开始开发前先在 Issue 中讨论你的方案
4. 逐步熟悉项目架构和代码规范

### 贡献者权益

- 你的名字会出现在贡献者列表中
- 可以参与项目决策讨论
- 有机会成为项目维护者

## 📚 相关资源

- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Pull Request 最佳实践](https://github.blog/2015-01-21-how-to-write-the-perfect-pull-request/)

## 🙋 获取帮助

如果你在贡献过程中遇到问题：

- 在 Issue 中提问
- 在讨论区发起讨论
- 联系项目维护者

---

再次感谢你的贡献！🎉
