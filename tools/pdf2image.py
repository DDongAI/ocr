"""
 * @author: zkyuan
 * @date: 2025/4/10 10:00
 * @description: 将pdf转为图片
"""

import os
import re
from time import sleep

import fitz  # pip install pymupdf
from PIL import Image

from config.MyPath import *

__all__ = ["pdf2image"]

# 批量处理
def getfilename(file_path):
    """去除文件的后缀前缀"""
    text = re.sub('\.[^\.]+$', '', file_path)
    text = re.sub(r'[\s\S]+[\\/](?=[^\\/]+$)', "", text)
    text = re.sub(r"\\", "", text)
    return text


def pdf2image(pdf_file_path: str):
    """将pdf按页码切成单个图片，"""

    pdf_document = fitz.open(pdf_file_path)

    fname = getfilename(pdf_file_path)

    for page_number in range(pdf_document.page_count):

        page = pdf_document.load_page(page_number)

        pix = page.get_pixmap(dpi=300)

        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        image_file_name = f"{IMAGE_PDF}{fname}_page_{page_number + 1}.png"

        img.save(image_file_name)

    pdf_document.close()
    sleep(1)


def pdf_2_image(dicpath):
    """文件夹里的pdf文件循环处理"""
    file_names = os.listdir(dicpath)

    for filename in file_names:
        pdf2image(dicpath + '\\' + filename)


if __name__ == '__main__':
    pdf_2_image(PDF_PATH)
