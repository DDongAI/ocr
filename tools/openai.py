"""
 * @author: zkyuan
 * @date: 2025/4/17 14:21
 * @description: 模型调用
"""

import requests

from config.constant import MAX_TOKENS
from config.entry import *

__all__ = [
    "openai_call",
    "openai_call_with_image",
]


def openai_call(prompt: str,) -> str:
    """
    调用llm
    :param prompt: 提示词
    :return: 结果
    """
    base_url = MY_QWEN_VL_URL
    if base_url.endswith('/'):
        base_url = base_url[:-1]

    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MY_QWEN_VL_API_KEY}"}
        payload = {
            "model": MY_QWEN_VL_MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "max_tokens": MAX_TOKENS,
        }
        # 发送请求到 OpenAI API
        response = requests.post(
            base_url + "/chat/completions", headers=headers, json=payload
        )
        # 检查状态码是否正常，不正常会触发异常
        response.raise_for_status()
        print(response.json())
        result = response.json()["choices"][0]["message"]["content"]
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenAI API: {e}")
        return "Error calling OpenAI API"


def openai_call_with_image(prompt: str, base64_image: str, choices: int = 1) -> str:
    """
    调用VLM图片识别
    :param prompt: 提示词
    :param base64_image: 图片字节码
    :param choices: 选择模型，1为图片转md，2为图片转txt
    :return: 识别结果
    """
    base_url = MY_QWEN_VL_URL
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    if choices == 1:
        # 图片转md
        system_prompt = my_prompt_vl_customize(prompt)
    elif choices == 2:
        # 图片转txt
        system_prompt = my_prompt_vl_text2text(prompt)
    else:
        return "choices参数错误，请检查配置"

    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MY_QWEN_VL_API_KEY}"}
        payload = {
            "model": MY_QWEN_VL_MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": system_prompt
                        },
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": MY_PROMPT_VL_USER,
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                },
            ],
            "max_tokens": MAX_TOKENS,
            # "temperature": 0.2,
        }
        # 发送请求到 OpenAI API
        response = requests.post(
            base_url + "/chat/completions", headers=headers, json=payload, timeout=180
        )
        # 检查状态码是否正常，不正常会触发异常
        response.raise_for_status()
        print(response.json())
        result = response.json()["choices"][0]["message"]["content"]
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenAI API: {e}")
        return "Error calling OpenAI API"
