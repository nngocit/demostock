import streamlit as st
import openai
import pandas as pd
from vnstock3 import Vnstock
import os
import time

# Lấy API Key từ biến môi trường
openai.api_key = os.getenv('OPENAI_API_KEY')

# Cấu hình Streamlit
st.set_page_config(page_title="Phân Tích Báo Cáo Kết Quả Kinh Doanh", layout="wide")

# Hiển thị tiêu đề ứng dụng
st.title("Phân Tích Báo Cáo Kết Quả Kinh Doanh Ngân Hàng")

# Kiểm tra xem API Key đã được thiết lập chưa
api_key_status = st.empty()  # Tạo chỗ trống cho thông báo

if openai.api_key:
    # Hiển thị thông báo khi API Key thành công
    api_key_status.success("Cấu hình thành công!")
    time.sleep(3)  # Chờ 3 giây trước khi tắt thông báo
    api_key_status.empty()  # Tắt thông báo
else:
    api_key_status.error("API Key chưa được cấu hình. Vui lòng thiết lập API Key trong biến môi trường.")

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

# Biến để kiểm tra dữ liệu đã tải hay chưa
data_loaded = False
income_df = None

# Hiển thị thông báo đang tải dữ liệu khi hàm đang thực hiện
with st.spinner('Đang tải dữ liệu...'):
    # Kiểm tra và tải dữ liệu
    income_df = get_financial_report()
    data_loaded = income_df is not None

# Nếu dữ liệu đã được tải thành công
if data_loaded:
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
else:
    # Nếu không có dữ liệu, hiển thị nút tải lại
    if st.button('🔄 Tải lại dữ liệu', disabled=data_loaded):
        income_df = reload_data()
        data_loaded = income_df is not None
        if data_loaded:
            st.success("Dữ liệu đã được tải lại thành công!")
        else:
            st.error("Không thể tải dữ liệu, vui lòng thử lại.")
