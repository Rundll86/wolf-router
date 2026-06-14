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
        "base_url": "https://ai.onyxaxis.org/api/chat/completions",
        "api_key_env": "FS_ONLYAXIS",
        "model": "claude-opus-4.8",
    },
    ModelName.GPT: {
        "base_url": "https://ai.onyxaxis.org/api/chat/completions",
        "api_key_env": "FS_ONLYAXIS",
        "model": "gpt-5.5-s",
    },
    ModelName.DOUBAO: {
        "base_url": "https://ai.onyxaxis.org/api/chat/completions",
        "api_key_env": "FS_ONLYAXIS",
        "model": "glm-4.5v",
    },
    ModelName.GEMINI: {
        "base_url": "https://ai.onyxaxis.org/api/chat/completions",
        "api_key_env": "FS_ONLYAXIS",
        "model": "gemini-3.1-pro-preview",
    },
    ModelName.QWEN: {
        "base_url": "https://ai.onyxaxis.org/api/chat/completions",
        "api_key_env": "FS_ONLYAXIS",
        "model": "qwen3-32b-fast",
    },
    ModelName.GLM: {
        "base_url": "https://ai.onyxaxis.org/api/chat/completions",
        "api_key_env": "FS_ONLYAXIS",
        "model": "glm-4.5v",
    },
}

ROUTER_LLM_CONFIG = {
    "base_url": "https://ai.onyxaxis.org/api/chat/completions",
    "api_key_env": "FS_ONLYAXIS",
    "model": "glm-4.5v",
}


def get_api_key(env_name: str) -> Optional[str]:
    return os.environ.get(env_name)


def get_model_base_url(model_name: ModelName) -> str:
    return MODEL_CONFIG[model_name]["base_url"]


def get_model_api_key(model_name: ModelName) -> Optional[str]:
    return get_api_key(MODEL_CONFIG[model_name]["api_key_env"])
