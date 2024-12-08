import streamlit as st
# import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

# Cho 3 file csv nhu sau:

# San_pham.csv: chứa thông tin sản phẩm thuộc nhóm “Chăm sóc da mặt” như ma_san_pham, ten_san_pham, gia_ban, gia_goc, phan_loai, mo_ta, diem_trung_binh
# Khach_hang.csv: chứa thông tin khách hàng gồm ma_khach_hang,ho_ten
# Danh_gia.csv: chứa thông tin đánh giá của khách hàng cho sản phẩm gồm id, ma_khach_hang, noi_dung_binh_luan, ngay_binh_luan, gio_binh_luan, so_sao, ma_san_pham

#################### SET SIDEBAR, PAGE TITLE


st.set_page_config(page_title="Product Analysis", page_icon="🔍")
st.title("🔍 Phân tích sản phẩm:")

st.sidebar.success("Giáo Viên Hướng Dẫn: /n # KHUẤT THUỲ PHƯƠNG")
st.sidebar.success("Học Viên:/n # NGUYỄN CHẤN NAM /n # CHẾ THỊ ANH TUYỀN")
st.sidebar.success("Ngày báo cáo: /n # 16/12/2024")

################################ BIỂU ĐỒ TỔNG QUAN VỀ BÌNH LUẬN VÀ SẢN PHẨM

# "C:/Users/Windows 10/Documents/Zalo Received Files/GUI_project1_Copy/GUI_project1_Copy/"

san_pham = pd.read_csv('C:/Users/Windows 10/Documents/Zalo Received Files/GUI_project1_Copy/GUI_project1_Copy/San_pham.csv')
danh_gia= pd.read_csv('C:/Users/Windows 10/Documents/Zalo Received Files/GUI_project1_Copy/GUI_project1_Copy/Danh_gia.csv')
khach_hang= pd.read_csv('C:/Users/Windows 10/Documents/Zalo Received Files/GUI_project1_Copy/GUI_project1_Copy/Khach_hang.csv')

# Hàm phân loại dựa trên giá trị của cột 'so_sao'
def classify_rating(star_rating):
    if star_rating <= 4:
        return 'negative'
    elif star_rating == 5:
        return 'positive'

# Áp dụng hàm vào cột 'so_sao' để tạo cột mới 'phan_loai_danh_gia'
danh_gia['phan_loai_danh_gia'] = danh_gia['so_sao'].apply(classify_rating)


danhgia_sanpham = danh_gia.merge(san_pham,on="ma_san_pham", how='left')
df=danhgia_sanpham.copy()

#------------START_Hàm thống kế số lượng bình luận theo tháng-------------------------------
def analyze_month_statistics(df, selected_product):
    """Thống kê số lượng bình luận theo tháng và trực quan hóa trên biểu đồ."""
    st.write(f"**I. Số lượng bình luận theo tháng cho sản phẩm ID '{selected_product}':**")

    # Lọc dữ liệu cho sản phẩm cụ thể
    df = df[df['ma_san_pham'] == selected_product]

    # Convert 'ngay_binh_luan' to datetime if it's not already
    df['ngay_binh_luan'] = pd.to_datetime(df['ngay_binh_luan'], dayfirst=True)

    # Nhóm dữ liệu theo tháng
    df['month'] = df['ngay_binh_luan'].dt.to_period('M')  # Creates a Period index for month
    month_count = df.groupby('month').size().reset_index(name='count')

    # Sort by 'month' column in descending order
    month_count = month_count.sort_values(by='month', ascending=False)

    # Lấy tháng có số lượt bình luận nhiều nhất
    if not month_count.empty:
        max_count = month_count['count'].max()
        top_month_row = month_count[month_count['count'] == max_count].iloc[0]
        st.write(f"Tháng có số lượt đánh giá nhiều nhất: {top_month_row['month']} với {top_month_row['count']} đánh giá.")

        # Trực quan hóa bằng Matplotlib
        plt.figure(figsize=(15, 7))
        
        # Vẽ biểu đồ cột
        bars = plt.bar(month_count['month'].astype(str), month_count['count'])
        
        # Tiêu đề và nhãn
        plt.title(f'Số lượng bình luận theo tháng - Sản phẩm {selected_product}', fontsize=15)
        plt.xlabel('Tháng', fontsize=12)
        plt.ylabel('Số lượng bình luận', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Thêm số lượng comment lên từng cột
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height)}', 
                     ha='center', va='bottom', 
                     fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.write("Không có bình luận nào.")
#------------END_Hàm thống kế số lượng bình luận theo tháng-------------------------------

#------------START_Hàm thống kế số lượng bình luận theo giờ-------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def analyze_comments_by_hour(df, product_id):
    """Thống kê số lượng bình luận theo khung giờ trong ngày cho một sản phẩm."""
    
    # Chọn ra bình luận của sản phẩm cụ thể
    product_comments = df[df['ma_san_pham'] == product_id]
    
    # Chuyển đổi cột 'gio_binh_luan' sang kiểu datetime để lấy giờ
    product_comments['gio_binh_luan'] = product_comments['gio_binh_luan'].astype(str)
    product_comments['hour'] = pd.to_datetime(product_comments['gio_binh_luan'], format='%H:%M').dt.hour

    # Đếm số lượng bình luận theo giờ
    hourly_counts = product_comments.groupby('hour').size().reset_index(name='count')

    # Hiển thị bảng thống kê
    st.write(f"**II. Số lượng bình luận theo giờ cho sản phẩm ID '{product_id}':**")

    # Trực quan hóa bằng matplotlib
    plt.figure(figsize=(10, 5))
    bars = plt.bar(hourly_counts['hour'], hourly_counts['count'], color='skyblue')
    plt.xlabel('Khung giờ trong ngày')
    plt.ylabel('Số lượng bình luận')
    plt.title(f"Số lượng bình luận theo khung giờ cho sản phẩm ID {product_id}")
    plt.xticks(hourly_counts['hour'])  # Đảm bảo tất cả các giờ được hiển thị
    plt.grid(axis='y')

    # Thêm nhãn số liệu lên từng cột trong biểu đồ
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom')  # va='bottom' để đặt nhãn ở trên cột

    # Hiển thị đồ thị trong Streamlit
    st.pyplot(plt)

    # Để người dùng chọn khung giờ
    selected_hour = st.selectbox('Chọn khung giờ bạn muốn xem bình luận:', hourly_counts['hour'].unique())

    # Lấy bình luận trong khung giờ đã chọn
    comments_in_selected_hour = product_comments[product_comments['hour'] == selected_hour]
    
    if not comments_in_selected_hour.empty:
        st.write(f"**Chi tiết bình luận vào khung giờ {selected_hour}:**")
        st.dataframe(comments_in_selected_hour[['gio_binh_luan', 'noi_dung_binh_luan', 'so_sao']])  # Giả sử có các cột cụ thể

        # Thống kê số lượng bình luận theo đánh giá cho 5 loại đánh giá
        rating_counts = comments_in_selected_hour['so_sao'].value_counts().reindex(range(1, 6), fill_value=0).reset_index()
        rating_counts.columns = ['so_sao', 'count']

        # Hiển thị thống kê đánh giá
        st.write(f"**Thống kê bình luận theo đánh giá cho khung giờ {selected_hour}:**")
        
        # Tạo cột trong Streamlit để hiển thị bảng và biểu đồ ngang nhau
        col1, col2 = st.columns([1, 2])  # Cột 1 (bảng) 1 phần, cột 2 (biểu đồ) 2 phần

        # Hiển thị bảng thống kê trong cột 1
        with col1:
            st.dataframe(rating_counts)

        # Trực quan hóa thống kê đánh giá trong cột 2
        with col2:
            plt.figure(figsize=(5, 5))  # Điều chỉnh kích thước của biểu đồ
            plt.bar(rating_counts['so_sao'].astype(str), rating_counts['count'], color='green')
            plt.xlabel('Đánh giá')
            plt.ylabel('Số lượng bình luận')
            plt.title(f"Số lượng bình luận theo đánh giá vào khung giờ {selected_hour} cho sản phẩm ID {product_id}")
            plt.xticks(rating_counts['so_sao'].astype(str))  # Đảm bảo tất cả các đánh giá được hiển thị
            plt.grid(axis='y')
            st.pyplot(plt)

        # Để giữ cho chiều cao cột cân bằng, tạo một dòng trống bằng cách sử dụng `st.empty()`.
        st.empty()  # Giữ không gian cho chiều cao bằng nhau
    else:
        st.write(f"Không có bình luận nào vào khung giờ {selected_hour}.")
#------------END_Hàm thống kế số lượng bình luận theo giờ-------------------------------

#------------START_Hàm thống kế số lượng bình luận theo loại sao-------------------------------
def plot_star_ratings(danh_gia, user_input_int):
    # Chuyển đổi user_input_int sang kiểu int nếu cần
    user_input_int = str(user_input_int)
    
    # Thống kê số lượng đánh giá theo từng sao
    star_ratings_count = danh_gia[danh_gia['ma_san_pham'] == user_input_int]['so_sao'].value_counts().sort_index()
    
    # Đảm bảo có đủ các mức sao từ 1 đến 5
    full_star_ratings = pd.Series([0] * 5, index=range(1, 6))
    full_star_ratings.update(star_ratings_count)
    
    # Hiển thị thông tin trên Streamlit
    st.write(f"**III. Số lượng đánh giá theo từng sao của sản phẩm ID '{user_input_int}':**")

    # Tạo biểu đồ dạng cột với matplotlib
    fig, ax = plt.subplots()
    ax.bar(full_star_ratings.index, full_star_ratings.values, color='skyblue')
    ax.set_title('Số lượng đánh giá theo từng sao')
    ax.set_xlabel('Sao')
    ax.set_ylabel('Số lượng đánh giá')
    ax.set_xticks(range(1, 6))

    # Thêm nhãn cho các cột
    for i, v in enumerate(full_star_ratings.values, start=1):
        ax.text(i, v, str(v), ha='center', va='bottom')

    # Trực quan hóa biểu đồ trong Streamlit
    st.pyplot(fig)

    st.write("Chi tiết đánh giá")
    # Tạo tabs để hiển thị bình luận theo mức sao
    tabs = st.tabs([f"{star} Sao" for star in range(1, 6)])
    
    for star, tab in zip(range(1, 6), tabs):
        with tab:
            # Lọc bình luận theo sao
            comments_df = danh_gia[(danh_gia['ma_san_pham'] == user_input_int) & (danh_gia['so_sao'] == star)]
            # Hiển thị bình luận dưới dạng bảng
            st.write(f"Bình luận {star} Sao:")
            st.dataframe(comments_df[['noi_dung_binh_luan']],hide_index=True,width=1000)

#------------END_Hàm thống kế số lượng bình luận theo loại sao-------------------------------

#------------START_Hàm vẽ wordcloud bình luận theo sản phẩm-------------------------------
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

def plot_product_comments_wordcloud(df, product_id, stopwords=None):
    """Vẽ Word Cloud cho bình luận của sản phẩm cụ thể với các tab riêng biệt cho từ tích cực và tiêu cực."""
    # Lọc bình luận của sản phẩm cụ thể
    product_comments = df[df['ma_san_pham'] == product_id]['noi_dung_binh_luan']

    # Chuyển đổi bình luận thành chuỗi, loại bỏ NaN
    product_comments = product_comments.dropna()  # Bỏ NaN

    # Đảm bảo mỗi phần tử đều là kiểu str
    product_comments = product_comments.astype(str).tolist()

    # Kết hợp các bình luận thành một chuỗi
    all_comments_text = " ".join(product_comments)

    # Lấy các từ tích cực và tiêu cực từ file
    try:
        with open("C:/Users/Windows 10/Documents/Zalo Received Files/GUI_project1_Copy/GUI_project1_Copy/positive_words_VN.txt", 'r', encoding='utf-8') as f:
            positive_words = f.read().splitlines()
        
        with open("C:/Users/Windows 10/Documents/Zalo Received Files/GUI_project1_Copy/GUI_project1_Copy/negative_words_VN.txt", 'r', encoding='utf-8') as f:
            negative_words = f.read().splitlines()
        
        # Lấy stopwords nếu có
        if stopwords is None:
            stopwords = set()  # Khởi tạo với tập rỗng nếu không có stopwords
        
        with open("C:/Users/Windows 10/Documents/Zalo Received Files/GUI_project1_Copy/GUI_project1_Copy/vietnamese-stopwords.txt", 'r', encoding='utf-8') as f:
            stopwords.update(f.read().splitlines())
    
    except FileNotFoundError as e:
        st.error(f"Không tìm thấy file: {e.filename}. Hãy kiểm tra đường dẫn!")
        return

    # Tạo tabs cho wordcloud
    tabs = st.tabs(["Từ Tích Cực", "Từ Tiêu Cực"])

    # Tạo hàm để vẽ Word Cloud từ chuỗi văn bản
    def create_wordcloud(text):
        # Kiểm tra nếu văn bản không rỗng
        if text:
            wordcloud = WordCloud(width=800, height=400, 
                                  background_color='white', 
                                  stopwords=stopwords).generate(text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)
        else:
            st.write("Không có dữ liệu để hiển thị Word Cloud.")

    # Tạo Word Cloud cho từ tích cực trong tab Từ Tích Cực
    with tabs[0]:
        st.subheader("Word Cloud cho Từ Tích Cực")
        positive_text = " ".join([word for word in all_comments_text.split() 
                                   if word in positive_words and word not in stopwords])
        create_wordcloud(positive_text)

    # Tạo Word Cloud cho từ tiêu cực trong tab Từ Tiêu Cực
    with tabs[1]:
        st.subheader("Word Cloud cho Từ Tiêu Cực")
        negative_text = " ".join([word for word in all_comments_text.split() 
                                   if word in negative_words and word not in stopwords])
        create_wordcloud(negative_text)

#------------END_Hàm vẽ wordcloud bình luận theo sản phẩm-------------------------------

# Tạo giao diện tìm kiếm sản phẩm
st.title("Tìm Kiếm Sản Phẩm")

# Convert relevant columns to string, handling possible None values
df['ma_san_pham'] = df['ma_san_pham'].astype(str)
df['ten_san_pham'] = df['ten_san_pham'].astype(str)
danh_gia['ma_san_pham'] = danh_gia['ma_san_pham'].astype(str)

# Tạo hai tab: "Theo sản phẩm" và "Theo thương hiệu"
tabs = st.tabs(["Theo sản phẩm", "Theo thương hiệu"])

# Tab 1: Theo sản phẩm
with tabs[0]:
    filtered_df = df

    # Remove duplicates based on 'ma_san_pham'
    filtered_df = filtered_df.drop_duplicates(subset='ma_san_pham')

    # Display the filtered products in a dropdown
    if not filtered_df.empty:
        # Create a list of products with their codes for selection
        product_list = filtered_df.apply(lambda x: f"{x['ten_san_pham']} (Code: {x['ma_san_pham']})", axis=1).tolist()
        selected_product = st.selectbox("Vui lòng nhập tên sản phẩm, mã sản phẩm hoặc chọn 1 sản phẩm:", product_list)
        
        # Extract the selected code from the product string
        selected_code = selected_product.split(" (Code: ")[-1].rstrip(")")
        st.write("Bạn đã chọn:", selected_product)
        st.write("Mã sản phẩm:", selected_code)

        # Call the functions to analyze data based on the selected product
        analyze_month_statistics(danh_gia, selected_code)
        analyze_comments_by_hour(danh_gia, selected_code)
        plot_star_ratings(danh_gia, selected_code)
        plot_product_comments_wordcloud(danh_gia, selected_code)

    else:
        st.write("Không tìm hấy sản phẩm.")

# Tab 2: Theo thương hiệu
with tabs[1]:
    # Đọc file brand_lst.csv
    brand_df = pd.read_csv('C:/Users/Windows 10/Documents/Zalo Received Files/GUI_project1_Copy/GUI_project1_Copy/Brand_lst.csv')
    brands = brand_df['thuong_hieu'].tolist()  # Giả sử cột tên thương hiệu là 'thuong_hieu'

    # Dropdown cho lựa chọn thương hiệu
    selected_brand = st.selectbox("Vui lòng nhập hoặc chọn 1 thương hiệu:", brands)

    if selected_brand:
        # Lọc DataFrame sản phẩm theo thương hiệu đã chọn
        filtered_brand_df = df[df['ten_san_pham'].str.contains(selected_brand, case=False) |
                                df['mo_ta'].str.contains(selected_brand, case=False, na=False)]

        # Remove duplicates based on 'ma_san_pham'
        filtered_brand_df = filtered_brand_df.drop_duplicates(subset='ma_san_pham')

        # Nếu có sản phẩm sau khi lọc
        if not filtered_brand_df.empty:
            # Tạo danh sách sản phẩm để hiển thị
            product_list_brands = filtered_brand_df.apply(lambda x: f"{x['ten_san_pham']} (Code: {x['ma_san_pham']})", axis=1).tolist()

            # In ra tổng số lượng sản phẩm của thương hiệu chọn
            product_count = filtered_brand_df.shape[0]
            st.write(f"Có {product_count} sản phẩm của thương hiệu {selected_brand}.")

            # Trực quan hóa số lượng đánh giá dựa trên số sao
            rating_counts = filtered_brand_df[['ma_san_pham', 'ten_san_pham']].copy()
            
            # Đảm bảo kiểu dữ liệu của 'ma_san_pham' là str
            rating_counts['ma_san_pham'] = rating_counts['ma_san_pham'].astype(str)

            # Tính số lượng đánh giá cho từng sản phẩm dựa vào số sao
            rating_summary = danh_gia.groupby('ma_san_pham')['so_sao'].value_counts().unstack(fill_value=0)
            rating_summary['tong_danh_gia'] = rating_summary.sum(axis=1)

            # Thêm thông tin số lượng đánh giá vào rating_counts
            rating_counts = rating_counts.merge(rating_summary[['tong_danh_gia']], on='ma_san_pham', how='left')

            # Trực quan hóa số lượng đánh giá
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 5))
            bars = plt.barh(rating_counts['ten_san_pham'], rating_counts['tong_danh_gia'], color='skyblue')

            # Thêm tổng số lượng đánh giá lên trên mỗi thanh
            for bar in bars:
                plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, 
                        f'{int(bar.get_width())}', va='center')
            plt.xlabel('Số lượng đánh giá')
            plt.title(f'Số lượng đánh giá theo sản phẩm của thương hiệu {selected_brand}')
            plt.tight_layout()
            st.pyplot(plt)

            # Gọi chức năng phân tích cho từng sản phẩm nếu cần
            selected_product_brand = st.selectbox("Chọn sản phẩm để phân tích:", product_list_brands)
            selected_code_brand = selected_product_brand.split(" (Code: ")[-1].rstrip(")")

            st.write("Bạn đã chọn sản phẩm:", selected_product_brand)
            st.write("Mã sản phẩm:", selected_code_brand)

            # Chuyển đổi selected_code_brand về kiểu dữ liệu phù hợp (nếu cần)
            selected_code_brand = str(selected_code_brand)  # Đảm bảo mã sản phẩm là kiểu str

            # Gọi các hàm phân tích dựa trên mã sản phẩm đã chọn
            st.write("Thống kê số lượng bình luận:")
            tabs = st.tabs(["Tháng","Giờ","Đánh giá"])
            with tabs[0]:
                analyze_month_statistics(danh_gia, selected_code_brand)
            with tabs[1]:
                analyze_comments_by_hour(danh_gia, selected_code_brand)
            with tabs[2]:
                plot_star_ratings(danh_gia, selected_code_brand)
                plot_product_comments_wordcloud(danh_gia, selected_code)


        else:
            st.write("Không tìm thấy sản phẩm cho thương hiệu này.")