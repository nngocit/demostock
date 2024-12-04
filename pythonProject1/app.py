import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Tiêu đề ứng dụng
st.title("Demo Thuyet Trinh")

# Phần tương tác với người dùng
st.sidebar.header("Tùy chọn")
num_data = st.sidebar.slider("Chọn số lượng dữ liệu", 10, 100, 50)
show_chart = st.sidebar.checkbox("Hiển thị biểu đồ", value=True)

# Tạo dữ liệu ngẫu nhiên
data = {
    "X": np.linspace(1, num_data, num_data),
    "Y": np.random.randint(1, 100, num_data)
}
df = pd.DataFrame(data)

# Hiển thị dữ liệu dạng bảng
st.write("### Dữ liệu ngẫu nhiên")
st.write(df)

# Hiển thị biểu đồ nếu được chọn
if show_chart:
    st.write("### Biểu đồ Dữ Liệu")
    fig, ax = plt.subplots()
    ax.plot(df["X"], df["Y"], marker="o", linestyle="-", color="blue")
    ax.set_title("Biểu đồ đường của dữ liệu")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    st.pyplot(fig)

# Tải dữ liệu xuống
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Tải xuống dữ liệu CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv"
)
