"""
 * @author: zkyuan
 * @date: 2025/4/10 14:31
 * @description: 常量配置
"""

__all__ = [
    "MAX_FILE_SIZE",
    "MAX_TOKENS",
    "IMAGE_TYPE",
]
# 单个图片的最大大小为5MB
MAX_FILE_SIZE: int = 5 * 1024 * 1024

MAX_TOKENS: int = 1200

IMAGE_TYPE = ["png", "jpg", "jpeg"]
