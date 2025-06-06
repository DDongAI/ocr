"""
 * @author: zkyuan
 * @date: 2025/4/8 10:53
 * @description: 使用大模型做ocr识别
"""

import base64  # base64 用于处理 Base64 编码
import re
from io import BytesIO

import requests  # requests 用于发送 HTTP 请求
import streamlit as st

from config.constant import *
from config.entry import *
from tools.fileload import generate_download_md_button
from tools.pages import pages_set
from tools.image import image_resize, image_resize_cv


def image_to_markdown_page():
    pages_set("图片转md", r"resource\d.png")
    st.title("🤖 图片识别助手")
    st.caption(
        "这个页面的功能没你想象的那么好。\n"
    )
    base_url = MY_QWEN_VL_URL
    # 创建一个文件上传器，允许用户上传图片文件，并设置最大文件大小为 5MB。
    upload_images = st.file_uploader(
        label="提示：把文件拖到这里，或者点击上传按钮，一次只支持一张图片；且不要上传超过5M的图片。",
        type=IMAGE_TYPE,
        label_visibility="visible",
        accept_multiple_files=False,
        help=f"只支持{IMAGE_TYPE}格式",
    )

    # 创建一个数字输入框，让用户输入最大 tokens 数量，默认值为 300。
    max_tokens = st.number_input("Max tokens(如果图片内容过多，可以适当调大；如果图片内容少，可以适当调小)", min_value=1,
                                 value=500, step=1)

    # 检查上传的图片文件是否超过最大大小，如果没有超过，则读取文件内容并显示图片。
    bytes_data = None
    if upload_images is not None:
        if upload_images.size > MAX_FILE_SIZE:
            st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
            st.stop()
        else:
            # image = Image.open(upload_images)
            bytes_data = upload_images.getvalue()
            st.image(bytes_data, caption=upload_images.name, width=200)

    if "image2md" not in st.session_state:
        st.session_state.image2md = {}

    # 初始化状态
    if "result" not in st.session_state.image2md:
        st.session_state.image2md["result"] = ""
    if "prompt" not in st.session_state.image2md:
        st.session_state.image2md["prompt"] = ""
    # 处理用户输入的提示信息 prompt 和上传的图片
    if prompt := st.chat_input("描述图中有哪些内容"):
        st.session_state.image2md["prompt"] = prompt
        # 如果用户输入了提示信息，则显示用户消息。
        st.chat_message("user").write(st.session_state.image2md["prompt"])
        # 图片压缩
        if len(bytes_data) > 400000:
            # bytes_data = image_resize(upload_images, 400)
            bytes_data = image_resize_cv(upload_images, 400)
        with st.chat_message('assistant'):
            with st.spinner('Thinking...'):
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
                                            "text": my_prompt_vl_customize(st.session_state.image2md["prompt"]),
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
                            "max_tokens": max_tokens,
                            # "temperature": 0.2,
                        }
                    else:
                        # 如果没有上传图片，则构建仅包含文本的请求负载。
                        payload = {
                            # "model": "gpt-4o",
                            "model": MY_QWEN_VL_MODEL_NAME,
                            "messages": [
                                {
                                    "role": "user",
                                    "content": st.session_state.image2md["prompt"],
                                },
                            ],
                            "max_tokens": max_tokens,
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
                    result = re.sub(r"```markdown", "", result)
                    result = re.sub(r"```(?=$|\n)", "", result)
                    st.session_state.image2md["result"] = result
                    st.markdown("```markdown\n" + st.session_state.image2md["result"] + "\n```")
                except Exception as e:
                    st.error(e)
                    st.stop()
    else:
        st.chat_message("user").write(st.session_state.image2md["prompt"])
        with st.chat_message('assistant'):
            st.markdown("```markdown\n" + st.session_state.image2md["result"] + "\n```")
    generate_download_md_button(st.session_state.image2md["result"], "result.md", "text/markdown")


if __name__ == "__main__":
    image_to_markdown_page()
