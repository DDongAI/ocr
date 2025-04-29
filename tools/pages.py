import streamlit as st


def pages_set(page_title: str, page_icon: str = "resource/d.png"):
    st.set_page_config(
        page_title=page_title,  # 浏览器标签页标题
        page_icon=page_icon,  # 可选：设置图标（Emoji 或本地图片路径）
        layout="wide",  # 可选：设置页面布局（wide 或 centered）
    )

    # 自定义导航菜单
    # 隐藏默认的 pages 导航
    hide_default_nav = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """
    st.markdown(hide_default_nav, unsafe_allow_html=True)
    # 在侧边栏添加自定义导航按钮
    with st.sidebar:
        st.page_link("home.py", label="首页", icon="🏠")
        st.page_link("pages/image-to-markdown.py", label="图片转MD格式", icon="📈")
        st.page_link("pages/pdf-to-markdown.py", label="复杂PDF转MD格式", icon="📈")
        st.page_link("pages/text_pdf_to_text.py", label="文本式PDF转txt格式", icon="📈")

