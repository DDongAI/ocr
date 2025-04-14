"""
 * @author: zkyuan
 * @date: 2025/4/8 16:44
 * @description: 模型的配置
"""
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=r".env", override=True)

__all__ = [
    "MY_QWEN_VL_MODEL_NAME",
    "MY_QWEN_VL_API_KEY",
    "MY_QWEN_VL_URL",
    "MY_PROMPT_VL_SYSTEM",
    "MY_PROMPT_VL_USER",
    "my_prompt_vl_Customize",
]


"""模型的api-key和url"""
# 千问图像识别的的模型名
MY_QWEN_VL_MODEL_NAME = os.getenv("MY_QWEN_VL_MODEL_NAME")
# 千问图像识别的的模型api-key
MY_QWEN_VL_API_KEY = os.getenv("MY_QWEN_VL_API_KEY")
# 千问图像识别的的模型url
MY_QWEN_VL_URL = os.getenv("MY_QWEN_VL_URL")

"""提示词"""
MY_PROMPT_VL_SYSTEM = """
# 你是一个图像识别助手，请根据用户给定的图片和要求进行识别。
## 识别图片中的内容
### 内容包括表格、文字、图形、流程图等内容；
### 若没有表格、图形、流程图等，则输出为文本即可，不需要过多的格式化；
### 识别要求信息完整准确、文本逻辑清晰，不要丢失重要信息；
## 输出的格式为Markdown文档格式,格式如下：
```markdown
    识别的具体内容
```
"""

# MY_PROMPT_VL_SYSTEM = """
# # 你是一个图像识别助手，请根据用户给定的图片和要求进行识别。
# ## 识别图片中内容
# ## 输出的格式为Markdown文档格式,格式如下：
# ```markdown
#     识别的具体内容
# ```
# """

MY_PROMPT_VL_USER = """
请根据图片中的内容，生成一份格式为Markdown格式的文档
"""


def my_prompt_vl_Customize(prompt: str) -> str:
    """输入需要识别的内容"""
    return f"""
    # 角色定义
    你是一名专业的图像识别助手，专门负责分析用户提供的图片，并依据用户的具体需求提取信息。
    
    ## 任务描述
    ### 图像内容识别
    - **目标**：识别并提取图片中的所有相关信息。
    - **内容包括但不限于**：
      - 文字（包括艺术字、印刷体和手写体）
      - 特定主题元素（如：{prompt}）
      - 表格、图形、流程图等（如果存在）
      
    - **优先级**：
      - 若图片中包含表格、图形或流程图，请特别指出并尽可能详细地描述这些元素的内容。
      - 如果没有上述复杂结构，专注于识别图片中的文本信息即可，无需进行额外的格式化处理。
    
    ### 识别标准
    - 确保提取的信息完整且精确，保持文本逻辑清晰，避免丢失任何关键细节。
    
    ## 输出指南
    ### 标题层级使用规则
    - 使用以下Markdown语法来创建标题层级：
      - `##` 一级标题
      - `###` 二级标题
      - `####` 三级标题
      - `#####` 四级标题
    
    ### 输出格式要求
    - 所有输出应遵循Markdown文档格式，示例如下：
    ```markdown
    识别的具体内容
    ```
    请按照以上指导原则进行操作，确保所提供的信息既全面又准确，以满足用户的特定需求。
    """

def my_prompt_vl_Customize_2(prompt: str) -> str:
    """输入需要识别的内容"""
    return f"""
    # 角色
     - 你是一个图像识别助手，请根据用户给定的图片和要求进行识别
    ## 识别图片中的内容
    ### 内容包括文字、{prompt}等内容；
    ### 若没有表格、图形、流程图等，则识别图中的文本即可，不需要过多的格式化处理；
    ### 识别要求信息完整准确、文本逻辑清晰，不要丢失重要信息；
    ## 输出格式
    ### 各级标题
     - ## 一级标题
     - ### 二级标题
     - #### 三级标题
     - ##### 四级标题
    ### 输出的格式
     - 输出的格式为Markdown文档格式,格式如下：
    ```markdown
        识别的具体内容
    ```
    """
