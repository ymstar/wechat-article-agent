"""
内容审核工具 - 根据微信公众号内容规范审核文章内容
"""
import re
import os
from typing import Dict, List, Any, Optional
from langchain.tools import tool
from langchain.tools import ToolRuntime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from src.config import get_config

# 微信公众号违规内容分类
VIOLATION_CATEGORIES = {
    "政治敏感": [
        "涉政、涉台、涉藏、涉疆等敏感政治话题",
        "传播颠覆国家政权的信息",
        "煽动民族仇恨、民族歧视"
    ],
    "违法信息": [
        "色情、淫秽内容",
        "赌博、毒品相关信息",
        "暴力、恐怖、血腥内容",
        "诈骗、传销、非法集资",
        "教唆犯罪、传授犯罪方法"
    ],
    "虚假宣传": [
        "夸大宣传、虚假广告",
        "误导性信息、谣言",
        "伪科学、虚假健康信息",
        "夸大产品效果、虚假承诺"
    ],
    "侵权内容": [
        "抄袭、盗版内容",
        "侵犯他人隐私",
        "侵犯知识产权",
        "未经授权使用他人作品"
    ],
    "低俗内容": [
        "低俗、庸俗内容",
        "性暗示、性挑逗内容",
        "低级趣味内容"
    ],
    "恶意营销": [
        "诱导分享、诱导关注",
        "违规营销推广",
        "诱导点击、诱导下载",
        "违规广告"
    ],
    "敏感词": [
        "使用违法违规词汇",
        "使用敏感词汇",
        "使用违规术语"
    ]
}


def load_sensitive_words() -> List[str]:
    """从配置文件加载敏感词"""
    config = get_config()
    words_path = config.audit.sensitive_words_path
    
    # 支持绝对路径和相对路径
    if not os.path.isabs(words_path):
        # 相对路径，相对于项目根目录
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        words_path = os.path.join(base_dir, words_path)
    
    if not os.path.exists(words_path):
        # 返回默认敏感词
        return _get_default_sensitive_words()
    
    try:
        with open(words_path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return words
    except Exception:
        return _get_default_sensitive_words()


def _get_default_sensitive_words() -> List[str]:
    """获取默认敏感词列表"""
    return [
        # 政治敏感词
        "颠覆", "暴动", "游行示威", "独立", "分裂",
        # 违法词汇
        "赌博", "博彩", "毒品", "冰毒", "海洛因", "枪支", "炸弹",
        # 低俗词汇
        "色情", "淫秽", "裸聊", "一夜情",
        # 虚假宣传词汇
        "包治百病", "根治", "100%有效", "神医", "祖传秘方",
        # 营销违规词
        "点击领取", "转发有奖", "分享赚佣金", "扫码领红包"
    ]


def check_sensitive_words(text: str) -> List[str]:
    """
    检查文本中的敏感词
    
    Args:
        text: 要检查的文本
    
    Returns:
        发现的敏感词列表
    """
    sensitive_words = load_sensitive_words()
    found_words = []
    text_lower = text.lower()
    
    for word in sensitive_words:
        if word.lower() in text_lower:
            found_words.append(word)
    
    return found_words


def check_title_compliance(title: str) -> Dict[str, Any]:
    """
    检查标题合规性
    
    Args:
        title: 文章标题
    
    Returns:
        包含检查结果的字典
    """
    issues = []
    
    # 检查标题长度（不超过64个字符）
    if len(title) > 64:
        issues.append("标题长度超过64个字符")
    
    # 检查是否含有敏感词
    sensitive_words = check_sensitive_words(title)
    if sensitive_words:
        issues.append(f"标题包含敏感词: {', '.join(sensitive_words)}")
    
    # 检查夸大宣传词
    exaggeration_words = ["震惊", "必看", "绝密", "曝光", "内幕", "重磅"]
    for word in exaggeration_words:
        if word in title:
            issues.append(f"标题可能含有夸大宣传词汇: {word}")
    
    return {
        "compliant": len(issues) == 0,
        "issues": issues
    }


def get_llm_client() -> Optional[ChatOpenAI]:
    """获取LLM客户端"""
    config = get_config()
    llm_cfg = config.llm
    
    if not llm_cfg.api_key:
        return None
    
    try:
        llm = ChatOpenAI(
            model=llm_cfg.model,
            api_key=llm_cfg.api_key,
            base_url=llm_cfg.base_url,
            temperature=0.1,
            max_tokens=1000,
            timeout=llm_cfg.timeout,
        )
        return llm
    except Exception:
        return None


def audit_content_with_llm(title: str, content: str) -> Dict[str, Any]:
    """
    使用 LLM 进行智能内容审核
    
    Args:
        title: 文章标题
        content: 文章正文内容
    
    Returns:
        审核结果字典
    """
    llm = get_llm_client()
    
    if llm is None:
        return {
            "pass": True,
            "violations": [],
            "suggestions": [],
            "note": "LLM未配置，跳过智能审核"
        }
    
    system_prompt = """你是一位专业的内容审核专家，负责审核微信公众号文章内容是否符合平台规范。

你的任务是审核给定的文章标题和正文，判断是否包含违规内容。

违规内容分类：
1. 政治敏感：涉政、涉台、涉藏、涉疆等敏感话题
2. 违法信息：色情、淫秽、赌博、毒品、暴力恐怖、诈骗传销等
3. 虚假宣传：夸大宣传、虚假广告、误导性信息、谣言
4. 侵权内容：抄袭、盗版、侵犯隐私、侵犯知识产权
5. 低俗内容：低俗、庸俗、性暗示等
6. 恶意营销：诱导分享、诱导关注、违规营销
7. 敏感词：使用违法违规词汇、敏感词汇

请严格按照以下JSON格式返回审核结果：
{
    "pass": true/false,
    "violations": [
        {
            "category": "违规类别",
            "reason": "具体违规原因",
            "location": "违规内容位置（标题/正文）"
        }
    ],
    "suggestions": ["修改建议1", "修改建议2"]
}

如果没有违规内容，violations 应为空数组。"""

    # 移除 HTML 标签，提取纯文本
    text_only = re.sub(r'<[^>]+>', '', content)
    
    user_message = f"""请审核以下文章内容：

标题：{title}

正文内容：
{text_only[:2000]}

请判断内容是否合规，并按照指定格式返回审核结果。"""

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        
        response = llm.invoke(messages)
        response_text = response.content
        
        if isinstance(response_text, list):
            response_text = " ".join([str(item) for item in response_text])
        
        # 提取 JSON 部分
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            result = json.loads(json_match.group())
            return result
        else:
            # 如果无法解析 JSON，返回默认通过结果
            return {
                "pass": True,
                "violations": [],
                "suggestions": []
            }
    
    except Exception as e:
        # 如果 LLM 审核失败，返回保守结果
        return {
            "pass": False,
            "violations": [
                {
                    "category": "审核系统错误",
                    "reason": f"内容审核失败: {str(e)}",
                    "location": "系统"
                }
            ],
            "suggestions": ["请稍后重试"]
        }


@tool
def audit_content(title: str, content: str, runtime: ToolRuntime = None) -> str:
    """
    审核文章内容是否符合微信公众号内容规范。
    
    Args:
        title: 文章标题
        content: 文章正文内容（HTML格式）
        runtime: 工具运行时上下文
    
    Returns:
        返回审核结果，包含通过/不通过状态及详细信息
    """
    try:
        # 步骤1: 检查标题合规性
        title_check = check_title_compliance(title)
        
        # 步骤2: 检查敏感词
        text_content = re.sub(r'<[^>]+>', '', content)
        sensitive_words = check_sensitive_words(text_content)
        
        # 步骤3: 使用 LLM 进行智能审核
        config = get_config()
        if config.audit.enable_llm_audit:
            llm_result = audit_content_with_llm(title, content)
        else:
            llm_result = {
                "pass": True,
                "violations": [],
                "suggestions": [],
                "note": "LLM审核已禁用"
            }
        
        # 汇总审核结果
        all_issues = []
        
        # 标题问题
        if not title_check["compliant"]:
            all_issues.extend([f"标题问题: {issue}" for issue in title_check["issues"]])
        
        # 敏感词问题
        if sensitive_words:
            all_issues.append(f"正文包含敏感词: {', '.join(sensitive_words)}")
        
        # LLM 审核问题
        if not llm_result["pass"]:
            for violation in llm_result.get("violations", []):
                all_issues.append(
                    f"{violation['category']}: {violation['reason']} (位置: {violation.get('location', '未知')})"
                )
        
        # 生成审核报告
        if len(all_issues) == 0:
            report = """✅ 内容审核通过

审核详情：
- 标题：合规
- 正文：合规
- 敏感词：未发现
- 智能审核：通过

文章内容符合微信公众号内容规范，可以发布。"""
            
            if llm_result.get("note"):
                report += f"\n\n备注：{llm_result['note']}"
            
            return report
        else:
            issue_list = "\n".join([f"  ❌ {issue}" for issue in all_issues])
            
            suggestions = ""
            if llm_result.get("suggestions"):
                suggestions = "\n修改建议：\n" + "\n".join([f"  • {s}" for s in llm_result["suggestions"]])
            
            return f"""❌ 内容审核不通过

发现以下问题：
{issue_list}

{suggestions}

请根据以上问题修改文章内容，修改后重新审核。只有审核通过后才能发布到微信公众号。"""
    
    except Exception as e:
        return f"❌ 内容审核失败：{str(e)}"
