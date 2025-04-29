import streamlit as st
from dotenv import load_dotenv

from tools.pages import pages_set


def home():
    pages_set("首页", "resource/d.png")
    st.title("🏠数据清洗工具")
    st.caption("如果你在使用过程中遇到问题，请不要着急，因为这是正常现象")

    st.markdown(
            """
            ### 1 🤖 图片转MD格式  \n
            将图片内容转为markdown格式文档 \n
            你可以简单的描述一下图片是有什么内容，或者什么都不要描述 \n
            例如：\n
             - 📝 eg1：表格、图表、流程图、思维导图 \n
             - 📝 eg2：表格、图画 \n
            
            ### 2 🤖 复杂PDF转MD格式 \n
            将pdf里的内容转化为markdown格式文档 \n
             - ⚠️ 有些pdf是由ppt、海报、流程图等转化而来，这导致pdf整页都是图片，这个模块是为了处理这种情况\n
             - 📢 建议你不要输入任何内容的提示词，因为pdf的内容太多，若是描述的不准确可能会起反作用 \n
             - 📢 建议你敲空格回车就好了 \n
            
            ### 3 🤖 文本式PDF转txt格式 \n
            将pdf里的内容转化为txt格式文档 \n
             - ⚠️ 有些纯文字的pdf文档上的文字无法用鼠标选择，原因是pdf每页都是一张图片，文字都是在图片上，这个模块是为了更好的处理这种情况\n
             - 📢 建议你敲空格回车就好了 \n
            
            ### end 💬 说明
             - 📩 使用过程中遇到问题请与管理员取得联系\n
             --- 
            """
        )


if __name__ == "__main__":
    load_dotenv(dotenv_path=r"config/.env", override=True)
    home()
