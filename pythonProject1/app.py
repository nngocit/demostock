import streamlit as st
import openai
import pandas as pd
from vnstock3 import Vnstock
import os

# Lấy API Key từ biến môi trường
openai.api_key = os.getenv('OPENAI_API_KEY')

# Cấu hình Streamlit
st.set_page_config(page_title="Phân Tích Báo Cáo Kết Quả Kinh Doanh", layout="wide")

# Hiển thị tiêu đề ứng dụng
st.title("Phân Tích Báo Cáo Kết Quả Kinh Doanh Ngân Hàng")

# Kiểm tra xem API Key đã được thiết lập chưa
if openai.api_key:
    st.success("API Key đã được cấu hình thành công!")
else:
    st.error("API Key chưa được cấu hình. Vui lòng thiết lập API Key trong biến môi trường.")

# Hàm lấy Báo Cáo Kết Quả Kinh Doanh
def get_financial_report(symbol='ACB'):
    try:
        # Lấy báo cáo tài chính từ VNStock
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        income_df = stock.finance.income_statement(period='quarter', lang='vi')
        return income_df
    except Exception as e:
        st.error(f"Đã có lỗi khi lấy dữ liệu báo cáo tài chính: {str(e)}")
        return None

# Hàm tải lại dữ liệu
def reload_data():
    return get_financial_report()

# Hiển thị nút tải lại dữ liệu với biểu tượng F5
reload_button = st.button('🔄 Tải lại dữ liệu')

# Nếu người dùng nhấn nút tải lại, gọi lại hàm lấy dữ liệu
if reload_button:
    income_df = reload_data()
else:
    income_df = get_financial_report()

# Hiển thị dữ liệu báo cáo kết quả kinh doanh nếu có
if income_df is not None:
    st.subheader("Báo Cáo Kết Quả Kinh Doanh")
    st.dataframe(income_df)

    # Lấy dữ liệu từ DataFrame để phân tích
    report_data = income_df.to_string()

    # Tạo prompt phân tích
    prompt = f"""
    Dưới đây là Báo cáo Kết quả Kinh doanh của Ngân hàng ACB. 
    Phân tích tình hình doanh thu, lợi nhuận gộp, chi phí và lợi nhuận ròng trong các quý gần đây. 
    Dữ liệu chi tiết: 
    {report_data}
    """

    # Hiển thị nút gửi và xử lý yêu cầu gửi tới OpenAI khi nhấn nút
    if st.button('Gửi yêu cầu phân tích'):
        if openai.api_key:
            try:
                # Sử dụng mô hình gpt-3.5-turbo thay thế
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Mô hình thay thế
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                )
                # Hiển thị kết quả từ OpenAI
                st.subheader("Phân Tích Báo Cáo Kết Quả Kinh Doanh")
                st.write(response['choices'][0]['message']['content'].strip())
            except Exception as e:
                st.error(f"Đã có lỗi xảy ra khi yêu cầu OpenAI: {str(e)}")
        else:
            st.error("API Key chưa được cấu hình. Vui lòng thiết lập API Key trong biến môi trường.")
