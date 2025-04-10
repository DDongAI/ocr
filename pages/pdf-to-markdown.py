"""
 * @author: zkyuan
 * @date: 2025/4/8 10:53
 * @description: 使用大模型做ocr识别
"""

import base64  # base64 用于处理 Base64 编码
import os
import re
from time import sleep

import fitz
import streamlit as st
from PIL import Image

from config.MyPath import *
from config.entry import *
from config.constant import *
from tools.image2text import image2md


# 这段代码定义了一个名为 vision_page 的函数，并设置了页面标题和描述，解释了 GPT-4o 的功能及其当前的限制。
def pdf_to_markdown_page():
    st.title("pdf识别助手")
    st.caption(
        "这个页面的功能没你想象的那么好。\n"
    )

    if "base_url" not in st.session_state:
        st.session_state['base_url'] = MY_QWEN_VL_URL

    if "api_key" not in st.session_state:
        st.session_state['api_key'] = MY_QWEN_VL_API_KEY
    # 初始化参数
    api_key = (
        st.session_state.api_key
        if "api_key" in st.session_state and st.session_state.api_key != ""
        else None
    )
    if api_key is None:
        st.error("Please enter your API key in the home.")
        st.stop()

    if "base_url" in st.session_state:
        base_url = st.session_state.base_url
    else:
        base_url = "https://api.openai.com/v1"

    # 创建一个文件上传器
    upload_pdf = st.file_uploader(
        label="提示：把文件拖到这里，或者点击上传按钮，一次只支持一个文件",
        type="pdf",
        label_visibility="visible",
        accept_multiple_files=False,
        help="只支持pdf格式",
    )

    if upload_pdf is None:
        st.error("文件未上传，请选择文件上传！")
        st.stop()

    # 处理用户输入的提示信息 prompt 和上传的图片
    if prompt := st.chat_input():
        # 如果用户输入了提示信息，则显示用户消息。
        st.chat_message("user").write(prompt)
        with st.chat_message('assistant'):
            with st.spinner('Thinking...'):
                try:
                    # 将上传的文件转为二进制数据
                    pdf_data = upload_pdf.getvalue()

                    # 用 fitz 打开二进制流
                    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

                    # 示例：获取页数
                    print(f"PDF总页数: {len(pdf_document)}")
                    # print(f"PDF页面：{pdf_document.page_count}")

                    result = ""

                    for page_number in range(pdf_document.page_count):
                        page = pdf_document.load_page(page_number)

                        pix = page.get_pixmap(dpi=300)

                        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

                        if not os.path.exists(f'{TEMP_PATH}'):
                            os.makedirs(f'{TEMP_PATH}')
                            print("创建临时文件夹成功")
                        image_file_name = f"{TEMP_PATH}page_{page_number + 1}.png"

                        print(img)
                        print("图片保存")
                        print(image_file_name)

                        img.save(image_file_name)

                        print("保存成功")
                        if not os.path.exists(image_file_name):
                            print("文件路径错误！")
                            st.error("文件路径错误！")

                        print("图片识别接口")
                        # 调用图片识别接口
                        image_md = image2md(image_file_name, " ")
                        image_md = re.sub(r"```markdown", "", image_md)
                        image_md = re.sub(r"```(?=$|\n)", "", image_md)
                        result += image_md

                    # 关闭文档（重要！）
                    pdf_document.close()
                    sleep(1)

                    result = "```markdown\n" + result + "\n```"
                    st.markdown(result)
                except Exception as e:
                    st.error(e)
                    st.stop()



if __name__ == "__main__":
    pdf_to_markdown_page()
