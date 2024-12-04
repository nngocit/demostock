import streamlit as st
import openai
import pandas as pd
from vnstock3 import Vnstock

# Khởi tạo API Key OpenAI
openai.api_key = "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"  # Thay thế bằng API key thực của bạn

# Cấu hình Streamlit
st.set_page_config(page_title="Phân Tích Báo Cáo Kết Quả Kinh Doanh", layout="wide")

# Khởi tạo tiêu đề ứng dụng
st.title("Phân Tích Báo Cáo Kết Quả Kinh Doanh Ngân Hàng")

# Hàm lấy Báo Cáo Kết Quả Kinh Doanh
def get_financial_report(symbol='ACB'):
    # Lấy báo cáo tài chính từ VNStock
    stock = Vnstock().stock(symbol=symbol, source='VCI')
    income_df = stock.finance.income_statement(period='quarter', lang='vi')
    return income_df

# Hiển thị Báo Cáo Kết Quả Kinh Doanh
income_df = get_financial_report()

# Hiển thị dữ liệu báo cáo kết quả kinh doanh
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

# Nút gửi yêu cầu phân tích
if st.button('Gửi yêu cầu phân tích'):
    try:
        # Gửi yêu cầu phân tích đến OpenAI API (Sử dụng GPT-4)
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # Sử dụng mô hình GPT-3.5 nếu không có quyền truy cập GPT-4
            prompt=prompt,
            max_tokens=500,  # Giới hạn số token trong phản hồi
            temperature=0.7,  # Kiểm soát tính sáng tạo của câu trả lời
            top_p=1.0  # Cách chọn từ (tùy chọn)
        )

        # Hiển thị kết quả phân tích
        st.success("Phân tích hoàn tất!")
        st.write("### Kết Quả Phân Tích Từ OpenAI")
        st.write(response['choices'][0]['text'].strip())

    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")
