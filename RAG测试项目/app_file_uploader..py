import streamlit as st
from knowledge_base import KnowledgeBaseService
import time


st.title("知识库更新服务")

uploaded_file = st.file_uploader(
    "上传txt文件",
    type=["txt"],
    accept_multiple_files=False,
)


if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


if uploaded_file is not None:
    
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024  # 转换为KB
    

    st.subheader(f"文件名：{file_name}")
    st.write(f"文件类型: {file_type} | 文件大小: {file_size:.2f} KB")

    text = uploaded_file.getvalue().decode("utf-8")

    with st.spinner("正在上传文件..."):
        time.sleep(1)  # 模拟上传过程

    result = st.session_state["service"].upload_by_str(text,file_name)
    st.write(result)