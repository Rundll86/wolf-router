import json
from typing import Generator

import requests
from config import MODEL_CONFIG, ModelName, get_model_api_key


def stream_openai(model_name: ModelName, user_input: str) -> Generator[str, None, None]:
    """使用 OpenAI 兼容接口流式调用任意模型。"""
    api_key = get_model_api_key(model_name)
    if not api_key:
        yield "错误：未配置 API Key"
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": MODEL_CONFIG[model_name]["model"],
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 4096,
        "stream": True,
    }

    try:
        response = requests.post(
            MODEL_CONFIG[model_name]["base_url"],
            headers=headers,
            json=payload,
            stream=True,
            timeout=120,
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue
            line_str = line.decode("utf-8")
            if not line_str.startswith("data: "):
                continue
            data_str = line_str[6:]
            if data_str == "[DONE]":
                break
            try:
                data = json.loads(data_str)
                choices = data.get("choices", [])
                if not choices:
                    continue
                delta = choices[0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    yield content
            except json.JSONDecodeError:
                continue
    except requests.exceptions.RequestException as e:
        yield f"错误：{str(e)}"


def stream_model_response(
    model_name: ModelName, user_input: str
) -> Generator[str, None, None]:
    """统一的模型响应入口，所有模型均走 OpenAI 兼容接口。"""
    yield from stream_openai(model_name, user_input)
