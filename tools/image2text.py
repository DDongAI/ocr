"""
 * @author: zkyuan
 * @date: 2025/4/10 14:27
 * @description: 将单张本地图片转为文本，输出为md格式
"""
import base64
import io

import requests
from PIL import Image

from config.entry import *
from tools.image import *
from config.constant import *

__all__ = ["image2md"]


def image2md(image_path: str, prompt: str) -> str:
    if image_path is None:
        return "图片为空"

    image = Image.open(image_path)

    # 检查上传的图片文件是否超过最大大小，如果没有超过，则读取文件内容并显示图片。
    bytes_data = None
    if image is not None:
        if analyze_image(image_path).size > MAX_FILE_SIZE:
            print("文件过大")
        else:
            # 使用BytesIO获取图像的二进制数据
            bytes_data = io.BytesIO()
            image.save(bytes_data, format='PNG')  # 保存图像到BytesIO对象，格式可以是JPEG, PNG等
            bytes_data = bytes_data.getvalue()
    else:
        print("文件为空")

    base_url = MY_QWEN_VL_URL

    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MY_QWEN_VL_API_KEY}"}
        # 如果上传了图片，则将图片转换为 Base64 编码，并构建包含文本和图片的请求负载。
        if bytes_data is not None:
            base64_image = base64.b64encode(bytes_data).decode("utf-8")
            payload = {
                # "model": "gpt-4o",
                "model": MY_QWEN_VL_MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": my_prompt_vl_Customize(prompt),
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
            }
        else:
            # 如果没有上传图片，则构建仅包含文本的请求负载。
            payload = {
                # "model": "gpt-4o",
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
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        response = requests.post(
            base_url + "/chat/completions", headers=headers, json=payload
        )
        # 检查状态码是否正常，不正常会触发异常
        response.raise_for_status()
        print(response.json())
        result = response.json()["choices"][0]["message"]["content"]
        print(result)
        return result
    except Exception as e:
        print(e)
