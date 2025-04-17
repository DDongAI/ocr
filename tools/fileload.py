import streamlit as st

__all__ = ["generate_download_md_button"]


def generate_download_md_button(data, file_name: str = "example.md", mime: str = "text/markdown"):
    """
    封装下载按钮逻辑，确保数据有效性和异常处理。

    参数：\n
    : data: 要下载的数据，必须是字符串或字节流。\n
    : file_name: 下载文件的名称，默认为 "example.md"。\n
    : mime: 文件的 MIME 类型，默认为 "text/markdown"。\n
    """
    try:
        # 确保数据是字符串或字节流
        if not isinstance(data, (str, bytes)):
            raise ValueError("数据必须是字符串或字节流")

        # 创建下载按钮
        st.download_button(
            label=f"下载 {file_name}",
            data=data,
            file_name=file_name,
            # mime=mime,
            type="secondary",
            icon="📂",
        )
    except Exception as e:
        # 捕获异常并提示用户
        st.error(f"下载失败: {e}")
