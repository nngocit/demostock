import streamlit as st
import google.generativeai as genai
from vnstock3 import Vnstock
import os
import pandas as pd
# Lấy API Key từ biến môi trường
genai.configure(api_key=os.getenv('OPENAI_API_KEY'))

# Hàm lấy Báo Cáo Kết Quả Kinh Doanh
def get_financial_report(symbol='ACB'):
    try:
        # Lấy báo cáo tài chính từ VNStock
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        income_df = stock.finance.income_statement(period='quarter', lang='vi')

        # Kiểm tra nếu không có dữ liệu trả về
        if income_df.empty:
            raise ValueError("Dữ liệu báo cáo tài chính trống.")

        return income_df
    except Exception as e:
        return str(e)

# Cấu hình Streamlit
st.set_page_config(page_title="Phân Tích Báo Cáo Kết Quả Kinh Doanh", layout="wide")
st.title("Phân Tích Báo Cáo Kết Quả Kinh Doanh Ngân Hàng")

# Kiểm tra và tải dữ liệu
with st.spinner('Đang tải dữ liệu...'):
    income_df = get_financial_report()

if isinstance(income_df, pd.DataFrame):
    st.subheader("Báo Cáo Kết Quả Kinh Doanh")
    st.dataframe(income_df)

    # Tạo prompt phân tích và gửi yêu cầu đến Gemini AI với timeout
    prompt = f"Dưới đây là Báo cáo Kết quả Kinh doanh của Ngân hàng ACB. Phân tích tình hình doanh thu, lợi nhuận gộp, chi phí và lợi nhuận ròng trong các quý gần đây. Dữ liệu chi tiết: {income_df.to_string()}"

    # Gửi yêu cầu phân tích và nhận phản hồi
    if st.button('Gửi yêu cầu phân tích'):
        with st.spinner('Đang phân tích...'):
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.write(response.text)
else:
    st.error("Không thể tải dữ liệu, vui lòng thử lại.")
