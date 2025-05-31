import io
import math
import os
from io import BytesIO

import cv2
import numpy as np
from PIL import Image
from pydantic import BaseModel

from streamlit.runtime.uploaded_file_manager import UploadedFile
from config.MyPath import RESIZE_PATH

__all__ = [
    "analyze_image",
    "image_resize",
    "pdf_reduce_size",
    "image_resize_cv",
    "pdf_resize_cv"
]


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


def image_resize(image: UploadedFile = None, target_kb=400, quality=85, min_scale=0.1):
    """
    Pillow自动降低图片分辨率直到小于目标大小(默认400KB)
    :param image: 图片
    :param target_kb: 目标大小(KB)
    :param quality: 保存质量(1-100)
    :param min_scale: 最小缩放比例(防止缩得过小)
    """
    # 检查原始文件大小
    original_size = image.size / 1024  # 转换为KB

    if original_size <= target_kb:
        # 如果已经小于目标大小，直接复制
        print(f"图片已小于{target_kb}KB，无需调整。大小: {original_size:.2f}KB")
        return image

    print(f"原始图片大小: {original_size:.2f}KB，开始压缩...")

    with Image.open(image) as img:
        width, height = img.size
        scale = 1.0

        # 计算初始缩放比例估计(基于文件大小比例)
        initial_scale = math.sqrt(target_kb / original_size)
        scale = max(initial_scale * 0.9, min_scale)  # 稍微多降一点，留有余地

        last_valid_img = None
        last_valid_scale = 1.0

        while True:
            # 计算新尺寸
            new_width = int(width * scale)
            new_height = int(height * scale)

            # 缩放图像
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            if not os.path.exists(f"{RESIZE_PATH}"):
                os.makedirs(f"{RESIZE_PATH}")
            # 保存到临时文件检查大小
            temp_path = f"{RESIZE_PATH}temp_resized.jpg"
            resized_img.save(temp_path, quality=quality)
            current_size = os.path.getsize(temp_path) / 1024

            print(f"尝试缩放比例: {scale:.2f}, 生成大小: {current_size:.2f}KB")

            if current_size <= target_kb:
                last_valid_img = resized_img
                last_valid_scale = scale
                if scale >= 0.95:  # 接近原始比例时直接使用
                    break
                # 尝试更大一点的比例
                scale = min(scale * 1.05, 1.0)  # 增加5%看看
            else:
                if last_valid_img is not None:
                    break  # 已经找到合适的就退出
                # 继续降低比例
                scale *= 0.9  # 减少10%
                if scale < min_scale:
                    scale = min_scale
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    last_valid_img = resized_img
                    break

        # 保存最终结果
        if last_valid_img:
            # # 将 Image 对象转为 bytes
            # img_byte_arr = BytesIO()
            # last_valid_img.save(img_byte_arr, format="png")
            # bytes_data = img_byte_arr.getvalue()
            with open(temp_path, 'rb') as f:
                content = f.read()
            print("输出图片大小：", len(content))
            return content
        else:
            # raise Exception("无法将图片压缩到目标大小以下")
            print("无法将图片压缩到目标大小以下")
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format=img.format or 'JPEG')
            img_bytes = img_byte_arr.getvalue()
            return img_bytes

def pdf_reduce_size(input_path, target_kb=400, quality=85, min_scale=0.1):
    """
    Pillow自动降低图片分辨率直到小于目标大小(默认400KB)
    :param input_path: 输入图片路径
    :param target_kb: 目标大小(KB)
    :param quality: 保存质量(1-100)
    :param min_scale: 最小缩放比例(防止缩得过小)
    """
    # 检查原始文件大小
    original_size = os.path.getsize(input_path) / 1024  # 转换为KB

    if original_size <= target_kb:
        image = Image.open(input_path)
        bytes_data = io.BytesIO()
        image.save(bytes_data, format='PNG')  # 保存图像到BytesIO对象，格式可以是JPEG, PNG等
        bytes_data = bytes_data.getvalue()
        print(f"图片已小于{target_kb}KB，无需调整。大小: {original_size:.2f}KB")
        return bytes_data

    print(f"原始图片大小: {original_size:.2f}KB，开始压缩...")

    with Image.open(input_path) as img:
        width, height = img.size
        scale = 1.0

        # 计算初始缩放比例估计(基于文件大小比例)
        initial_scale = math.sqrt(target_kb / original_size)
        scale = max(initial_scale * 0.9, min_scale)  # 稍微多降一点，留有余地

        last_valid_img = None
        last_valid_scale = 1.0

        while True:
            # 计算新尺寸
            new_width = int(width * scale)
            new_height = int(height * scale)

            # 缩放图像
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 保存到临时文件检查大小
            temp_path = f"{RESIZE_PATH}temp_pdf_resized.jpg"
            resized_img.save(temp_path, quality=quality)
            current_size = os.path.getsize(temp_path) / 1024

            print(f"尝试缩放比例: {scale:.2f}, 生成大小: {current_size:.2f}KB")

            if current_size <= target_kb:
                last_valid_img = resized_img
                last_valid_scale = scale
                if scale >= 0.95:  # 接近原始比例时直接使用
                    break
                # 尝试更大一点的比例
                scale = min(scale * 1.05, 1.0)  # 增加5%看看
            else:
                if last_valid_img is not None:
                    break  # 已经找到合适的就退出
                # 继续降低比例
                scale *= 0.9  # 减少10%
                if scale < min_scale:
                    scale = min_scale
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    last_valid_img = resized_img
                    break

        # 保存最终结果
        if last_valid_img:
            # 将 Image 对象转为 bytes
            # img_byte_arr = BytesIO()
            # last_valid_img.save(img_byte_arr, format="png")
            # bytes_data = img_byte_arr.getvalue()
            with open(temp_path, 'rb') as f:
                content = f.read()
            print("返回的图片大小:", len(content))
            return content
            # return bytes_data
        else:
            print("无法将图片压缩到目标大小以下")
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format=img.format or 'JPEG')
            img_bytes = img_byte_arr.getvalue()
            return img_bytes


def image_resize_cv(upload_file, target_kb=400, quality=85, min_scale=0.1):
    """
    使用OpenCV降低图片分辨率至目标大小以下
    :param upload_file: PIL Image对象
    :param target_kb: 目标大小(KB)
    :param quality: 保存质量(1-100)
    :param min_scale: 最小缩放比例
    :return: 处理后的PIL Image对象
    """
    img = Image.open(upload_file)
    # 将PIL图像转换为OpenCV格式
    opencv_image = np.array(img)
    # 转换颜色空间(RGB->BGR)
    if len(opencv_image.shape) == 3 and opencv_image.shape[2] == 3:
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)

    # 检查原始大小
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    # 确保图像是 uint8 类型，并且是 2D/3D 数组
    if not isinstance(opencv_image, np.ndarray):
        raise ValueError("输入图像必须是 NumPy 数组")

    if opencv_image.dtype != np.uint8:
        opencv_image = opencv_image.astype(np.uint8)

    # 如果是带透明通道的图像 (4通道)，则移除 alpha 通道
    if len(opencv_image.shape) == 3 and opencv_image.shape[2] == 4:
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGRA2BGR)

    # 再次确认 shape 是否有效
    if len(opencv_image.shape) not in [2, 3]:
        raise ValueError("图像维度不合法，请确保是灰度图或三通道彩色图")
    _, buffer = cv2.imencode('.jpg', opencv_image, encode_param)
    original_size_kb = len(buffer) / 1024

    if original_size_kb <= target_kb:
        print(f"图片已小于{target_kb}KB，无需调整。大小: {original_size_kb:.2f}KB")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format or 'JPEG')
        img_bytes = img_byte_arr.getvalue()
        return img_bytes

    print(f"原始图片大小: {original_size_kb:.2f}KB，开始压缩...")

    height, width = opencv_image.shape[:2]
    scale = 1.0
    last_valid_img = None
    last_valid_scale = 1.0

    # progress_bar = st.progress(0)
    # status_text = st.empty()

    # 计算初始缩放比例
    initial_scale = math.sqrt(target_kb / original_size_kb)
    scale = max(initial_scale * 0.9, min_scale)

    max_attempts = 10
    attempts = 0

    while attempts < max_attempts:
        attempts += 1
        progress = attempts / max_attempts
        # progress_bar.progress(min(progress, 1.0))

        # 计算新尺寸
        new_width = int(width * scale)
        new_height = int(height * scale)

        # 缩放图像(使用INTER_AREA插值-最适合缩小)
        resized_img = cv2.resize(
            opencv_image,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

        # 检查大小
        _, buffer = cv2.imencode('.jpg', resized_img, encode_param)
        current_size_kb = len(buffer) / 1024

        # status_text.text(f"尝试 {attempts}/{max_attempts}: 比例 {scale:.2f}, 大小 {current_size_kb:.2f}KB")

        if current_size_kb <= target_kb:
            last_valid_img = resized_img
            last_valid_scale = scale
            if scale >= 0.95:
                break
            scale = min(scale * 1.05, 1.0)
        else:
            if last_valid_img is not None:
                break
            scale *= 0.9
            if scale < min_scale:
                scale = min_scale
                new_width = int(width * scale)
                new_height = int(height * scale)
                resized_img = cv2.resize(
                    opencv_image,
                    (new_width, new_height),
                    interpolation=cv2.INTER_AREA
                )
                last_valid_img = resized_img
                break

    # progress_bar.empty()
    # status_text.empty()

    if last_valid_img is not None:
        # 转换回PIL格式
        if len(last_valid_img.shape) == 3 and last_valid_img.shape[2] == 3:
            last_valid_img = cv2.cvtColor(last_valid_img, cv2.COLOR_BGR2RGB)
        processed_img = Image.fromarray(last_valid_img)

        # 计算最终大小
        img_byte_arr = io.BytesIO()
        processed_img.save(img_byte_arr, format='JPEG', quality=quality)
        final_size_kb = len(img_byte_arr.getvalue()) / 1024

        print(f"压缩完成! 最终大小: {final_size_kb:.2f}KB, 缩放比例: {last_valid_scale:.2f}")

        return img_byte_arr.getvalue()
    else:
        print("无法将图片压缩到目标大小以下")
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format=img.format or 'JPEG')
        img_bytes = img_byte_arr.getvalue()
        return img_bytes


def pdf_resize_cv(input_path, target_kb=400, quality=85, min_scale=0.1):
    """
    使用OpenCV降低图片分辨率至目标大小以下
    :param input_path: PIL Image对象
    :param target_kb: 目标大小(KB)
    :param quality: 保存质量(1-100)
    :param min_scale: 最小缩放比例
    :return: 处理后的PIL Image对象
    """
    img = Image.open(input_path)
    # 将PIL图像转换为OpenCV格式
    opencv_image = np.array(img)
    # 转换颜色空间(RGB->BGR)
    if len(opencv_image.shape) == 3 and opencv_image.shape[2] == 3:
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)

    # 检查原始大小
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    # 确保图像是 uint8 类型，并且是 2D/3D 数组
    if not isinstance(opencv_image, np.ndarray):
        raise ValueError("输入图像必须是 NumPy 数组")

    if opencv_image.dtype != np.uint8:
        opencv_image = opencv_image.astype(np.uint8)

    # 如果是带透明通道的图像 (4通道)，则移除 alpha 通道
    if len(opencv_image.shape) == 3 and opencv_image.shape[2] == 4:
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGRA2BGR)

    # 再次确认 shape 是否有效
    if len(opencv_image.shape) not in [2, 3]:
        raise ValueError("图像维度不合法，请确保是灰度图或三通道彩色图")
    _, buffer = cv2.imencode('.jpg', opencv_image, encode_param)
    original_size_kb = len(buffer) / 1024

    if original_size_kb <= target_kb:
        print(f"图片已小于{target_kb}KB，无需调整。大小: {original_size_kb:.2f}KB")
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format=img.format or 'JPEG')
        img_bytes = img_byte_arr.getvalue()
        return img_bytes

    print(f"原始图片大小: {original_size_kb:.2f}KB，开始压缩...")

    height, width = opencv_image.shape[:2]
    scale = 1.0
    last_valid_img = None
    last_valid_scale = 1.0

    # progress_bar = st.progress(0)
    # status_text = st.empty()

    # 计算初始缩放比例
    initial_scale = math.sqrt(target_kb / original_size_kb)
    scale = max(initial_scale * 0.9, min_scale)

    max_attempts = 10
    attempts = 0

    while attempts < max_attempts:
        attempts += 1
        # progress = attempts / max_attempts
        # progress_bar.progress(min(progress, 1.0))

        # 计算新尺寸
        new_width = int(width * scale)
        new_height = int(height * scale)

        # 缩放图像(使用INTER_AREA插值-最适合缩小)
        resized_img = cv2.resize(
            opencv_image,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

        # 检查大小
        _, buffer = cv2.imencode('.jpg', resized_img, encode_param)
        current_size_kb = len(buffer) / 1024

        # status_text.text(f"尝试 {attempts}/{max_attempts}: 比例 {scale:.2f}, 大小 {current_size_kb:.2f}KB")

        if current_size_kb <= target_kb:
            last_valid_img = resized_img
            last_valid_scale = scale
            if scale >= 0.95:
                break
            scale = min(scale * 1.05, 1.0)
        else:
            if last_valid_img is not None:
                break
            scale *= 0.9
            if scale < min_scale:
                scale = min_scale
                new_width = int(width * scale)
                new_height = int(height * scale)
                resized_img = cv2.resize(
                    opencv_image,
                    (new_width, new_height),
                    interpolation=cv2.INTER_AREA
                )
                last_valid_img = resized_img
                break

    # progress_bar.empty()
    # status_text.empty()

    if last_valid_img is not None:
        # 转换回PIL格式
        if len(last_valid_img.shape) == 3 and last_valid_img.shape[2] == 3:
            last_valid_img = cv2.cvtColor(last_valid_img, cv2.COLOR_BGR2RGB)
        processed_img = Image.fromarray(last_valid_img)

        # 计算最终大小
        img_byte_arr = io.BytesIO()
        processed_img.save(img_byte_arr, format='JPEG', quality=quality)
        final_size_kb = len(img_byte_arr.getvalue()) / 1024

        print(f"压缩完成! 最终大小: {final_size_kb:.2f}KB, 缩放比例: {last_valid_scale:.2f}")

        return img_byte_arr.getvalue()
    else:
        print("无法将图片压缩到目标大小以下")
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format=img.format or 'JPEG')
        img_bytes = img_byte_arr.getvalue()
        return img_bytes
