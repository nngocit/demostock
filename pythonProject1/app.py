import streamlit as st
import google.generativeai as genai
import pandas as pd
from vnstock3 import Vnstock
import os

# Lấy API Key từ biến môi trường
genai.configure(api_key=os.getenv('OPENAI_API_KEY'))

# Cấu hình Streamlit
st.set_page_config(page_title="Phân Tích Báo Cáo Kết Quả Kinh Doanh", layout="wide")

# Hiển thị tiêu đề ứng dụng
st.title("Phân Tích Báo Cáo Kết Quả Kinh Doanh Ngân Hàng")

# Kiểm tra xem API Key đã được thiết lập chưa
if not os.getenv('OPENAI_API_KEY'):
    st.error("API Key chưa được cấu hình. Vui lòng thiết lập API Key trong biến môi trường.")

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

# Biến để kiểm tra dữ liệu đã tải hay chưa
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.income_df = None

# Hiển thị spinner chỉ khi dữ liệu chưa được tải
if not st.session_state.data_loaded:
    with st.spinner('Đang tải dữ liệu...'):
        # Kiểm tra và tải dữ liệu
        error_message = get_financial_report()

        if isinstance(error_message, pd.DataFrame):  # Nếu dữ liệu trả về hợp lệ
            st.session_state.income_df = error_message
            st.session_state.data_loaded = True
        else:  # Nếu có lỗi
            st.error(f"Đã có lỗi khi lấy dữ liệu báo cáo tài chính: {error_message}")

# Nếu dữ liệu đã được tải thành công
if st.session_state.data_loaded:
    st.subheader("Báo Cáo Kết Quả Kinh Doanh")
    st.dataframe(st.session_state.income_df)

    # Lấy dữ liệu từ DataFrame để phân tích
    report_data = st.session_state.income_df.to_string()

    # Tạo prompt phân tích
    prompt = f"""
    Dưới đây là Báo cáo Kết quả Kinh doanh của Ngân hàng ACB. 
    Phân tích tình hình doanh thu, lợi nhuận gộp, chi phí và lợi nhuận ròng trong các quý gần đây. 
    Dữ liệu chi tiết: 
    {report_data}
    """

    # Tạo nút "Gửi yêu cầu phân tích"
    if st.button('Gửi yêu cầu phân tích'):
        # Hiển thị spinner "AI đang phân tích"
        with st.spinner('AI đang phân tích...'):
            try:
                # Gửi yêu cầu phân tích tới Gemini AI
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)

                # Hiển thị kết quả từ Gemini AI
                st.subheader("Phân Tích Báo Cáo Kết Quả Kinh Doanh")
                st.write(response.text.strip())

                # Reset session state for analysis after response is received
                st.session_state.data_loaded = False
                st.session_state.income_df = None
            except Exception as e:
                st.error(f"Đã có lỗi xảy ra khi yêu cầu Gemini AI: {str(e)}")

# Nếu không có dữ liệu, hiển thị nút tải lại
if not st.session_state.data_loaded:
    if st.button('🔄 Tải lại dữ liệu'):
        st.session_state.income_df = get_financial_report()
        st.session_state.data_loaded = st.session_state.income_df is not None
        if st.session_state.data_loaded:
            st.success("Dữ liệu đã được tải lại thành công!")
        else:
            st.error("Không thể tải dữ liệu, vui lòng thử lại.")
