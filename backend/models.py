import json
import requests
import re
from typing import Optional, Generator, Dict, Any

from config import ModelName, MODEL_CONFIG, get_model_api_key, get_model_base_url

def stream_claude(model_name: ModelName, user_input: str) -> Generator[str, None, None]:
    api_key = get_model_api_key(model_name)
    if not api_key:
        yield "错误：未配置 API Key"
        return

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": MODEL_CONFIG[model_name]["model"],
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 4096,
        "stream": True
    }

    try:
        response = requests.post(
            MODEL_CONFIG[model_name]["base_url"],
            headers=headers,
            json=payload,
            stream=True,
            timeout=120
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    if data_str == '[DONE]':
                        break
                    try:
                        data = json.loads(data_str)
                        if 'delta' in data and 'text' in data['delta']:
                            yield data['delta']['text']
                    except json.JSONDecodeError:
                        continue
    except requests.exceptions.RequestException as e:
        yield f"错误：{str(e)}"

def stream_gpt(model_name: ModelName, user_input: str) -> Generator[str, None, None]:
    api_key = get_model_api_key(model_name)
    if not api_key:
        yield "错误：未配置 API Key"
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": MODEL_CONFIG[model_name]["model"],
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 4096,
        "stream": True
    }

    try:
        response = requests.post(
            MODEL_CONFIG[model_name]["base_url"],
            headers=headers,
            json=payload,
            stream=True,
            timeout=120
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    if data_str == '[DONE]':
                        break
                    try:
                        data = json.loads(data_str)
                        if 'choices' in data and len(data['choices']) > 0:
                            delta = data['choices'][0].get('delta', {})
                            if 'content' in delta:
                                yield delta['content']
                    except json.JSONDecodeError:
                        continue
    except requests.exceptions.RequestException as e:
        yield f"错误：{str(e)}"

def stream_doubao(model_name: ModelName, user_input: str) -> Generator[str, None, None]:
    api_key = get_model_api_key(model_name)
    if not api_key:
        yield "错误：未配置 API Key"
        return

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_CONFIG[model_name]["model"],
        "messages": [{"role": "user", "content": user_input}],
        "stream": True,
        "apiKey": api_key
    }

    try:
        response = requests.post(
            MODEL_CONFIG[model_name]["base_url"],
            headers=headers,
            json=payload,
            stream=True,
            timeout=120
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    try:
                        data = json.loads(data_str)
                        if 'result' in data:
                            yield data['result']
                        if data.get('is_end', False):
                            break
                    except json.JSONDecodeError:
                        continue
    except requests.exceptions.RequestException as e:
        yield f"错误：{str(e)}"

def stream_gemini(model_name: ModelName, user_input: str) -> Generator[str, None, None]:
    api_key = get_model_api_key(model_name)
    if not api_key:
        yield "错误：未配置 API Key"
        return

    params = {
        "key": api_key
    }

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "parts": [{
                "text": user_input
            }]
        }],
        "stream": True
    }

    try:
        response = requests.post(
            MODEL_CONFIG[model_name]["base_url"],
            headers=headers,
            params=params,
            json=payload,
            stream=True,
            timeout=120
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    try:
                        data = json.loads(data_str)
                        if 'candidates' in data and len(data['candidates']) > 0:
                            content = data['candidates'][0].get('content', {})
                            parts = content.get('parts', [])
                            if parts:
                                yield parts[0].get('text', '')
                    except json.JSONDecodeError:
                        continue
    except requests.exceptions.RequestException as e:
        yield f"错误：{str(e)}"

def stream_qwen(model_name: ModelName, user_input: str) -> Generator[str, None, None]:
    api_key = get_model_api_key(model_name)
    if not api_key:
        yield "错误：未配置 API Key"
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": MODEL_CONFIG[model_name]["model"],
        "input": user_input,
        "stream": True
    }

    try:
        response = requests.post(
            MODEL_CONFIG[model_name]["base_url"],
            headers=headers,
            json=payload,
            stream=True,
            timeout=120
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    try:
                        data = json.loads(data_str)
                        if 'output' in data:
                            yield data['output']['text']
                        if data.get('finish_reason') == 'stop':
                            break
                    except json.JSONDecodeError:
                        continue
    except requests.exceptions.RequestException as e:
        yield f"错误：{str(e)}"

def stream_glm(model_name: ModelName, user_input: str) -> Generator[str, None, None]:
    api_key = get_model_api_key(model_name)
    if not api_key:
        yield "错误：未配置 API Key"
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": MODEL_CONFIG[model_name]["model"],
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 4096,
        "stream": True
    }

    try:
        response = requests.post(
            MODEL_CONFIG[model_name]["base_url"],
            headers=headers,
            json=payload,
            stream=True,
            timeout=120
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    if data_str == '[DONE]':
                        break
                    try:
                        data = json.loads(data_str)
                        if 'choices' in data and len(data['choices']) > 0:
                            delta = data['choices'][0].get('delta', {})
                            if 'content' in delta:
                                yield delta['content']
                    except json.JSONDecodeError:
                        continue
    except requests.exceptions.RequestException as e:
        yield f"错误：{str(e)}"

MODEL_STREAM_FUNCTIONS = {
    ModelName.CLAUDE: stream_claude,
    ModelName.GPT: stream_gpt,
    ModelName.DOUBAO: stream_doubao,
    ModelName.GEMINI: stream_gemini,
    ModelName.QWEN: stream_qwen,
    ModelName.GLM: stream_glm
}

def stream_model_response(model_name: ModelName, user_input: str) -> Generator[str, None, None]:
    stream_func = MODEL_STREAM_FUNCTIONS.get(model_name)
    if stream_func:
        yield from stream_func(model_name, user_input)
    else:
        yield f"错误：不支持的模型 {model_name.value}"