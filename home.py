import streamlit as st
from dotenv import load_dotenv


def home():
    st.title("🏠数据清洗工具")
    st.caption("如果你在使用过程中遇到问题，请不要着急，因为这是正常现象")

    st.markdown(
            """
            ### 1 🤖 image-to-markdown  \n
            将图片内容转为markdown格式文档 \n
            你可以简单的描述一下图片是有什么内容，或者什么都不要描述 \n
            例如：\n
             - 📝 eg1：表格、图表、流程图、思维导图 \n
             - 📝 eg2：表格、图画 \n
             
            ### 2 🤖 pdf-to-markdown \n
            将pdf里的内容转化为markdown格式文档 \n
             - 📢 建议你不要输入任何内容的提示词，因为pdf的内容太多，我怕你把握不住 \n
             - 📢 建议你敲空格回车就好了 \n
            
            ### end 💬 说明
            ⚠️ 如果你在使用过程中遇到报错，请不要着急，因为这是正常现象。\n
            ⚠️ 如果你发现识别的效果不够好，请不要着急，因为这是正常现象。\n
            ⚠️ 如果你觉得这个工具还可以继续优化，那对不起，做不到。\n
             --- 
            ❌ 大bug改不了、小bug不用改。\n
            ❌ 我劝你不要没事找事！\n
             --- 
            """
        )


if __name__ == "__main__":
    load_dotenv(dotenv_path=r"config/.env", override=True)
    home()
