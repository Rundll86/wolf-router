import os
from enum import Enum
from typing import Dict, Optional

class ModelName(Enum):
    CLAUDE = "claude"
    GPT = "gpt"
    DOUBAO = "doubao"
    GEMINI = "gemini"
    QWEN = "qwen"
    GLM = "glm"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_

MODEL_CONFIG: Dict[ModelName, Dict[str, str]] = {
    ModelName.CLAUDE: {
        "base_url": "https://api.anthropic.com/v1/messages",
        "api_key_env": "CLAUDE_API_KEY",
        "model": "claude-3-sonnet-20240229"
    },
    ModelName.GPT: {
        "base_url": "https://api.openai.com/v1/chat/completions",
        "api_key_env": "OPENAI_API_KEY",
        "model": "gpt-4o"
    },
    ModelName.DOUBAO: {
        "base_url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions",
        "api_key_env": "DOUBAO_API_KEY",
        "model": "ernie-4.0-turbo"
    },
    ModelName.GEMINI: {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        "api_key_env": "GEMINI_API_KEY",
        "model": "gemini-1.5-flash"
    },
    ModelName.QWEN: {
        "base_url": "https://dashscope.aliyuncs.com/api/text-generation/v1",
        "api_key_env": "QWEN_API_KEY",
        "model": "qwen-plus"
    },
    ModelName.GLM: {
        "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "api_key_env": "GLM_API_KEY",
        "model": "glm-4"
    }
}

ROUTER_LLM_CONFIG = {
    "base_url": "https://api.openai.com/v1/chat/completions",
    "api_key_env": "ROUTER_API_KEY",
    "model": "gpt-4o-mini"
}

def get_api_key(env_name: str) -> Optional[str]:
    return os.environ.get(env_name)

def get_model_base_url(model_name: ModelName) -> str:
    return MODEL_CONFIG[model_name]["base_url"]

def get_model_api_key(model_name: ModelName) -> Optional[str]:
    return get_api_key(MODEL_CONFIG[model_name]["api_key_env"])