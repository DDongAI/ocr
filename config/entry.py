"""
 * @author: zkyuan
 * @date: 2025/4/8 16:44
 * @description: 模型的配置
"""

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
MY_QWEN_VL_MODEL_NAME = "Qwen2_5-VL-7B"
# 千问图像识别的的模型api-key
MY_QWEN_VL_API_KEY = "token-abc123"
# 千问图像识别的的模型url
MY_QWEN_VL_URL = "http://175.6.13.6:50008/v1"

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

