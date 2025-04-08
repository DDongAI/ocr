"""
 * @author: zkyuan
 * @date: 2025/4/8 16:44
 * @description: 常量
"""
from enum import Enum

from pydantic import BaseModel

__all__ = ["MyModel", "MyPrompt"]
class MyModel(Enum):
    """模型的api-key和url"""
    # 千问图像识别的的模型名
    MY_QWEN_VL_MODEL_NAME = "Qwen2_5-VL-7B"
    # 千问图像识别的的模型api-key
    MY_QWEN_VL_API_KEY = "token-abc123"
    # 千问图像识别的的模型url
    MY_QWEN_VL_URL = "http://175.6.13.6:50008/v1"

class MyPrompt(Enum):
    """提示词"""
    MY_PROMPT_VL_SYSTEM = (
    """
    # 你是一个图像识别助手，请根据用户给定的图片和要求进行识别。
    # 识别图片中的表格、文字、图形、流程图等内容，为了使信息更完整准确，输出时可以适当调整文本的形式。
    # 输出的格式为md文档格式
    """
    )


