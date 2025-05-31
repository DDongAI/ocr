"""
 * @author: zkyuan
 * @date: 2025/4/10 14:27
 * @description: 将单张本地图片转为文本，输出为md格式
"""
import base64
import io

from PIL import Image
import streamlit as st

from tools.image import *
from config.constant import *

from tools.image import pdf_reduce_size

from tools.openai import openai_call_with_image

__all__ = [
    "image2md",
    "image2txt",
]


def image2md(image_path: str, prompt: str) -> str:
    """
    图片转md
    :param image_path: 图片路径
    :param prompt: 提示词
    :return: 图片内容
    """
    if image_path is None:
        return "图片为空"

    image = Image.open(image_path)

    # 检查上传的图片文件是否超过最大大小，如果没有超过，则读取文件内容并显示图片。
    bytes_data = None
    if image is not None:
        if analyze_image(image_path).size > MAX_FILE_SIZE:
            print("文件过大")
            st.error("pdf中每页内容过多，请重新上传")
            st.stop()
        else:
            # 使用BytesIO获取图像的二进制数据
            # bytes_data = io.BytesIO()
            # image.save(bytes_data, format='PNG')  # 保存图像到BytesIO对象，格式可以是JPEG, PNG等
            # bytes_data = bytes_data.getvalue()
            # bytes_data = pdf_reduce_size(image_path, target_kb=350, quality=85, min_scale=0.1)
            bytes_data = pdf_resize_cv(image_path, target_kb=350, quality=85, min_scale=0.1)
    else:
        print("文件为空")

    if bytes_data is not None:
        base64_image = base64.b64encode(bytes_data).decode("utf-8")
        result = openai_call_with_image(prompt, base64_image, 1)
        print(result)
        return result
    else:
        print("图片读取错误！")
        return "图片读取错误！"


def image2txt(image_path: str, prompt: str) -> str:
    """
    图片转txt
    :param image_path: 图片路径
    :param prompt: 提示词
    :return: 图片内容
    """
    if image_path is None:
        return "图片为空"

    image = Image.open(image_path)

    # 检查上传的图片文件是否超过最大大小，如果没有超过，则读取文件内容并显示图片。
    bytes_data = None
    if image is not None:
        if analyze_image(image_path).size > MAX_FILE_SIZE:
            print("文件过大")
            st.error("pdf中每页内容过多，请重新上传")
            st.stop()
        else:
            # 使用BytesIO获取图像的二进制数据
            bytes_data = io.BytesIO()
            image.save(bytes_data, format='PNG')  # 保存图像到BytesIO对象，格式可以是JPEG, PNG等
            bytes_data = bytes_data.getvalue()
    else:
        print("文件为空")

    if bytes_data is not None:
        base64_image = base64.b64encode(bytes_data).decode("utf-8")
        result = openai_call_with_image(prompt, base64_image, 2)
        print(result)
        return result
    else:
        print("图片读取错误！")
        return "图片读取错误！"


