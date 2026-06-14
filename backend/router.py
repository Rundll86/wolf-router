import json
import re
from typing import Optional

import requests
from config import ROUTER_LLM_CONFIG, ModelName, get_api_key
from prompts import ROUTER_SYSTEM_PROMPT, ROUTER_USER_PROMPT_TEMPLATE


class RouteResult:
    def __init__(self, model: ModelName, reason: str):
        self.model = model
        self.reason = reason


def parse_router_response(response_text: str) -> Optional[RouteResult]:
    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if match:
        json_str = match.group(0)
        data = json.loads(json_str)

        if "model" in data and "reason" in data:
            model_name = data["model"].strip().lower()
            if ModelName.has_value(model_name):
                return RouteResult(model=ModelName(model_name), reason=data["reason"])
    return None


def call_router_llm(user_input: str) -> Optional[RouteResult]:
    api_key = get_api_key(ROUTER_LLM_CONFIG["api_key_env"])
    if not api_key:
        return None

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    messages = [
        {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": ROUTER_USER_PROMPT_TEMPLATE.format(user_input=user_input),
        },
    ]

    payload = {
        "model": ROUTER_LLM_CONFIG["model"],
        "messages": messages,
    }

    response = requests.post(
        ROUTER_LLM_CONFIG["base_url"], headers=headers, json=payload, timeout=30
    )
    response.raise_for_status()

    result = response.json()
    if result.get("choices"):
        content = result["choices"][0]["message"]["content"]
        return parse_router_response(content)
