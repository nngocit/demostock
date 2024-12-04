import streamlit as st
import os

# Kiểm tra giá trị của OPENAI_API_KEY
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    st.error("API Key chưa được cấu hình. Vui lòng thiết lập API Key trong biến môi trường.")
else:
    st.success("API Key đã được cấu hình thành công.")
