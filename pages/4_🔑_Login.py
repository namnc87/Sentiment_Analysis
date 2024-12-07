import streamlit as st
import pandas as pd

# Đọc dữ liệu sản phẩm và đánh giá
san_pham = pd.read_csv('San_pham.csv', index_col='ma_san_pham')
danh_gia = pd.read_csv('Danh_gia.csv', index_col=0)
khach_hang = pd.read_csv("Khach_hang.csv")

# Hàm phân loại dựa trên giá trị của cột 'so_sao'
def classify_rating(star_rating):
    if star_rating <= 4:
        return 'negative'
    elif star_rating == 5:
        return 'positive'

# Áp dụng hàm vào cột 'so_sao' để tạo cột mới 'phan_loai_danh_gia'
danh_gia['phan_loai_danh_gia'] = danh_gia['so_sao'].apply(classify_rating)

# Kết hợp dữ liệu đánh giá và sản phẩm
danhgia_sanpham = danh_gia.merge(san_pham, on="ma_san_pham", how='left')
danhgia_sanpham = danhgia_sanpham.merge(khach_hang, on='ma_khach_hang', how='left')
df_reviews = danhgia_sanpham[['ma_khach_hang','ho_ten', 'ma_san_pham', 'ten_san_pham', 'gia_ban',
                              'ngay_binh_luan', 'gio_binh_luan', 'noi_dung_binh_luan',
                              'phan_loai_danh_gia', 'so_sao']]

# Đọc dữ liệu từ file Khach_hang.csv
def load_users(df):
    df.columns = df.columns.str.strip()
    df["ma_khach_hang"] = df["ma_khach_hang"].astype(str).str.strip()
    df["mat_khau"] = df["mat_khau"].astype(str).str.strip()
    return df

# Hiển thị thông tin đánh giá của khách hàng
def display_customer_reviews(maKH, df_reviews):
    filtered_reviews = df_reviews[df_reviews['ma_khach_hang'] == maKH]
    filtered_reviews=filtered_reviews[['ngay_binh_luan', 'gio_binh_luan','ma_san_pham', 'ten_san_pham', 'gia_ban',
                               'noi_dung_binh_luan','phan_loai_danh_gia', 'so_sao' ]]
    filtered_reviews['ngay_binh_luan'] = pd.to_datetime(filtered_reviews['ngay_binh_luan'], errors='coerce')  # Đảm bảo 'ngay_binh_luan' có kiểu dữ liệu ngày tháng
    filtered_reviews = filtered_reviews.sort_values(by='ngay_binh_luan', ascending=False)  # Sắp xếp giảm dần theo ngày
    if not filtered_reviews.empty:
        # st.write("Thông tin đánh giá của khách hàng:")
        st.dataframe(filtered_reviews)
    else:
        st.warning("Khách hàng này chưa có đánh giá sản phẩm nào.")

# Giao diện Streamlit
def main():
    st.subheader("Hệ thống đăng nhập và tra cứu khách hàng")

    # Tải thông tin người dùng
    df_users = load_users(khach_hang)
    VALID_USERS = df_users.set_index("ma_khach_hang")["mat_khau"].to_dict()

    # Khởi tạo trạng thái phiên
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["ho_ten"] = ""

    # Nếu chưa đăng nhập
    if not st.session_state["logged_in"]:
        st.header("Đăng nhập")
        username = st.text_input("👤 Tên đăng nhập (Mã khách hàng):").strip()
        password = st.text_input("🔑 Mật khẩu (Gợi ý: password123):", type="password").strip()
        login_button = st.button("Đăng nhập")

        if login_button:
            # Kiểm tra thông tin đăng nhập
            if username in VALID_USERS and VALID_USERS[username] == password:
                # Lấy thông tin tên khách hàng (ho_ten)
                ho_ten = df_users[df_users["ma_khach_hang"] == username]["ho_ten"].values[0]
                # Cập nhật session state với thông tin khách hàng
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["ho_ten"] = ho_ten
                st.success("Đăng nhập thành công!")
                st.rerun()  # Làm mới trang để vào trạng thái đăng nhập
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu!")
    else:
        # Nếu đã đăng nhập
        st.success(f"Xin chào khách hàng có mã số: {st.session_state['username']}, Họ tên: {st.session_state['ho_ten']}")

        # Hiển thị lịch sử đánh giá sản phẩm của khách hàng
        st.markdown("#### Lịch sử đánh giá sản phẩm")
        maKH = int(st.session_state["username"])  # Chuyển mã khách hàng về kiểu số nguyên
        display_customer_reviews(maKH, df_reviews)

        # Nút Logout
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.session_state["ho_ten"] = ""
            st.rerun()  # Làm mới giao diện để quay lại màn hình đăng nhập

if __name__ == "__main__":
    main()
