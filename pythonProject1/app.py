import os
import streamlit as st

# Lấy giá trị OPENAI_API_KEY từ môi trường
openai_api_key = os.getenv("OPENAI_API_KEY")

# In ra giá trị của API Key
st.write(f"OPENAI_API_KEY: {openai_api_key}")

# Kiểm tra và hiển thị thông báo tương ứng
if openai_api_key is None:
    st.error("API Key chưa được cấu hình. Vui lòng thiết lập API Key trong biến môi trường.")
else:
    st.success("API Key đã được cấu hình thành công.")
