import streamlit as st
from gemini_ai.gemini import GeminiAI
from vnstock3 import Vnstock

# Tiêu đề ứng dụng
st.title("Phân Tích Báo Cáo Tài Chính Ngân Hàng ACB")

# Khởi tạo đối tượng GeminiAI với API key mặc định
gemini = GeminiAI(api_key='AIzaSyCFVp1vJ53OkxxC_FzALVuujuC8NzwOBsc')
gemini.config(temp=0.7, top_p=0.9)

# Sử dụng Session State để lưu trữ dữ liệu báo cáo tài chính
if "income_df" not in st.session_state:
    st.session_state.income_df = None

# Mặc định luôn tải Báo Cáo Kết Quả Kinh Doanh khi ứng dụng chạy
if st.session_state.income_df is None:
    try:
        stock = Vnstock().stock(symbol='ACB', source='VCI')
        st.session_state.income_df = stock.finance.income_statement(period='quarter', lang='vi')
        st.success("Dữ liệu Báo Cáo Kết Quả Kinh Doanh đã được tải thành công!")
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")

# Hiển thị báo cáo tài chính nếu đã tải thành công
if st.session_state.income_df is not None:
    st.write("### Báo Cáo Kết Quả Kinh Doanh (Income Statement)")
    st.dataframe(st.session_state.income_df)

# Nút "Gửi Yêu Cầu Phân Tích"
if st.session_state.income_df is not None and st.button("Gửi Yêu Cầu Phân Tích"):
    try:
        # Tạo prompt phân tích
        prompt = f"""
        Dưới đây là Báo cáo Kết quả Kinh doanh của Ngân hàng ACB. 
        Phân tích tình hình doanh thu, lợi nhuận gộp, chi phí và lợi nhuận ròng trong các quý gần đây. 
        Dữ liệu chi tiết: 
        {st.session_state.income_df.to_string()}
        """

        # Gửi yêu cầu phân tích đến Gemini AI
        with st.spinner("Đang phân tích dữ liệu..."):
            response = gemini.generate(prompt)

        # Hiển thị kết quả phân tích
        st.success("Phân tích hoàn tất!")
        st.write("### Kết Quả Phân Tích Từ Gemini AI")
        st.write(response)
    except Exception as e:
        st.error(f"Lỗi khi phân tích dữ liệu: {e}")
