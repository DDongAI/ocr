import os

import numpy as np
from PIL import Image
from pydantic import BaseModel

__all__ = ["analyze_image"]


class ImageSize(BaseModel):
    memory: int = 0
    pixel: int = 0
    size: int = 0


def analyze_image(image_path) -> ImageSize:
    """获取图片的大小"""
    # 打开图片
    image = Image.open(image_path)

    # 1. 获取分辨率
    width, height = image.size

    # print(f"分辨率: {width}x{height} 像素")

    # 2. 获取内存占用
    image_np = np.array(image)
    # print(f"实际内存占用: {image_np.nbytes} Bytes")

    # 3. 获取文件大小
    file_size = os.path.getsize(image_path)
    # print(f"文件大小: {file_size} Bytes")

    return ImageSize(memory=image_np.nbytes, pixel=width * height, size=file_size)
