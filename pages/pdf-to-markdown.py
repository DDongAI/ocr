"""
 * @author: zkyuan
 * @date: 2025/4/8 10:53
 * @description: 识别pdf的信息
"""

import os
import re
import time

import fitz
import streamlit as st
from PIL import Image

from config.MyPath import *
from tools.image2text import image2md


def pdf_to_markdown_page():
    st.title("🤖 pdf识别助手")
    st.caption(
        "这个页面的功能没你想象的那么好。\n"
    )
    # 创建一个文件上传器
    upload_pdf = st.file_uploader(
        label="提示：把文件拖到这里，或者点击上传按钮，一次只支持上传一个文件",
        type="pdf",
        label_visibility="visible",
        accept_multiple_files=False,
        help="只支持pdf格式",
    )

    if upload_pdf is None:
        st.error("文件未上传，请选择文件上传！")
        st.stop()

    # 设置进度条的初始文本
    progress_text = "操作进行中，请稍候。"
    # 创建一个进度条对象
    my_bar = st.progress(0, text=progress_text)

    # 处理用户输入的提示信息 prompt 和上传的图片
    if prompt := st.chat_input():
        # 如果用户输入了提示信息，则显示用户消息。
        st.chat_message("user").write(prompt)
        with st.chat_message('assistant'):
            with st.spinner('你可能会等很久~~~Thinking...'):
                try:
                    # 将上传的文件转为二进制数据
                    pdf_data = upload_pdf.getvalue()

                    # 用 fitz 打开二进制流
                    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

                    # 示例：获取页数
                    print(f"PDF总页数: {len(pdf_document)}")
                    # st.write(f"PDF总页数: {len(pdf_document)}")
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

                        print(f"第{str(page_number + 1)}图片信息：{img}")
                        print("开始图片保存")
                        print(f"图片保存路径：{image_file_name}")

                        img.save(image_file_name)

                        print("图片保存成功")
                        if not os.path.exists(image_file_name):
                            print("临时文件路径错误！")
                            st.error("临时文件路径错误！")

                        print(f"开始调用图片识别接口处理第{page_number + 1}页")
                        # 调用图片识别接口
                        image_md = image2md(image_file_name, " ")
                        image_md = re.sub(r"```markdown", "", image_md)
                        image_md = re.sub(r"```(?=$|\n)", "", image_md)
                        result += image_md

                        # st.write("第" + str(page_number + 1) + "页处理完成")
                        progress_text = f"PDF总页数: {len(pdf_document)}，第{str(page_number + 1)}页处理完成！"
                        percent_complete = round((page_number + 1)/len(pdf_document), 2)
                        my_bar.progress(percent_complete, text=progress_text)

                    # 关闭文档
                    pdf_document.close()

                    # 删掉临时文件
                    if os.path.exists(f'{TEMP_PATH}'):
                        try:
                            # 遍历文件夹中的所有文件
                            for file_name in os.listdir(TEMP_PATH):
                                file_path = os.path.join(TEMP_PATH, file_name)

                                # 确保是文件而不是子文件夹
                                if os.path.isfile(file_path):
                                    os.remove(file_path)  # 删除文件
                                    print(f"Deleted: {file_path}")
                        except Exception as e:
                            print(f"An error occurred: {e}")

                    result = "```markdown\n" + result + "\n```"
                    st.markdown(result)
                except Exception as e:
                    st.error(e)
                    st.stop()


if __name__ == "__main__":
    pdf_to_markdown_page()
