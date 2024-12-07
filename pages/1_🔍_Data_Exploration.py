import streamlit as st
# import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter



#################### SET SIDEBAR, PAGE TITLE


st.set_page_config(page_title="Data Exploration", page_icon="🔍")
st.title("🔍 Inside the Data:")

st.sidebar.success("Giáo Viên Hướng Dẫn: \n # KHUẤT THUỲ PHƯƠNG")
st.sidebar.success("Học Viên:\n # NGUYỄN CHẤN NAM \n # CHẾ THỊ ANH TUYỀN")
st.sidebar.success("Ngày báo cáo: \n # 16/12/2024")

################################ BIỂU ĐỒ TỔNG QUAN VỀ BÌNH LUẬN VÀ SẢN PHẨM

san_pham = pd.read_csv('San_pham.csv', index_col='ma_san_pham')
danh_gia= pd.read_csv('Danh_gia.csv', index_col=0)
khach_hang= pd.read_csv('Khach_hang.csv', index_col='ma_khach_hang')

# Hàm phân loại dựa trên giá trị của cột 'so_sao'
def classify_rating(star_rating):
    if star_rating <= 4:
        return 'negative'
    elif star_rating == 5:
        return 'positive'

# Áp dụng hàm vào cột 'so_sao' để tạo cột mới 'phan_loai_danh_gia'
danh_gia['phan_loai_danh_gia'] = danh_gia['so_sao'].apply(classify_rating)


danhgia_sanpham = danh_gia.merge(san_pham,on="ma_san_pham", how='left')
df=danhgia_sanpham[['ma_khach_hang','ma_san_pham','ngay_binh_luan','gio_binh_luan','noi_dung_binh_luan','phan_loai_danh_gia','so_sao','ten_san_pham','gia_ban']]

# Đánh dấu cột có bình luận
df['co_binh_luan'] = df['noi_dung_binh_luan'].notnull() & df['noi_dung_binh_luan'].str.strip().astype(bool)

# Tính số lượng bình luận tích cực, tiêu cực và không có bình luận
# Đếm số lượng sản phẩm duy nhất
total_products = san_pham.index.nunique()
total_products_eval = df['ma_san_pham'].nunique()
total_eval= df['so_sao'].count()
total_comments = df['noi_dung_binh_luan'].count()
positive_count = df[(df['phan_loai_danh_gia'] == 'positive') & (df['co_binh_luan'])].shape[0]
negative_count = df[(df['phan_loai_danh_gia'] == 'negative') & (df['co_binh_luan'])].shape[0]
no_comment_count = df[~df['co_binh_luan']].shape[0]

# Dữ liệu cho biểu đồ
categories = ['Tích cực', 'Tiêu cực', 'Không có bình luận']
values = [positive_count, negative_count, no_comment_count]
colors = sns.color_palette("pastel", len(categories))

# # Hiển thị thông tin 
st.subheader("1. Tổng quan về đánh giá và sản phẩm")

# Tạo hai cột
col1, col2 = st.columns(2)
with col1:
    st.write(f"- SL Sản phẩm: {total_products:,}")
    st.write(f'- SL Sản phẩm có đánh giá: {total_products_eval}')
    st.write(f"- SL Đánh giá: {total_eval:,}")
    st.write(f"- SL Bình luận: {total_comments:,}")


# Cột 2: Hiển thị sản phẩm không có bình luận
with col2:
    st.write(f"- SL đánh giá tích cực: {positive_count:,}")
    st.write(f"- SL đánh giá tiêu cực: {negative_count:,}")
    st.write(f"- SL có đánh giá, nhưng không bình luận: {no_comment_count:,}")


# Vẽ biểu đồ Bar Chart
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(categories, values, color=colors, edgecolor='black')

# Thêm số lượng trên đầu mỗi cột
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1, str(height),
            ha='center', fontsize=12, color='black')

# Định dạng biểu đồ
ax.set_title('Phân loại đánh giá theo sản phẩm', fontsize=14)
ax.set_ylabel('Số lượng sản phẩm', fontsize=12)
ax.set_xlabel('Loại đánh giá', fontsize=12)
ax.set_ylim(0, max(values) + 1000)

# Hiển thị biểu đồ trong Streamlit
st.pyplot(fig)

################################ BIỂU ĐỒ PHÂN TÍCH SỐ LƯỢNG BÌNH LUẬN THEO THỜI GIAN

# Hiển thị thông tin 
st.subheader("2. Số lượng bình luận theo thời gian")

# Chuyển đổi cột 'ngay_binh_luan' sang kiểu datetime, loại bỏ các giá trị không hợp lệ
df['ngay_binh_luan'] = pd.to_datetime(df['ngay_binh_luan'], format='%d/%m/%Y', errors='coerce')

# Loại bỏ các dòng có giá trị NaT (Not a Time) trong cột 'ngay_binh_luan'
df_binhluan = df.dropna(subset=['ngay_binh_luan'])

# Nhóm dữ liệu theo tháng và loại đánh giá (positive/negative)
df_binhluan['thang_nam'] = df_binhluan['ngay_binh_luan'].dt.to_period('M')  # Tạo cột 'thang_nam' theo định dạng tháng-năm
df_binhluan['phan_loai_danh_gia'] = df_binhluan['phan_loai_danh_gia'].str.lower()  # Đảm bảo cột 'phan_loai_danh_gia' là chữ thường

# Tính số lượng bình luận tích cực và tiêu cực theo tháng
monthly_comments = df_binhluan.groupby(['thang_nam', 'phan_loai_danh_gia']).size().unstack(fill_value=0)

# Lấy các tháng có trong dữ liệu
available_months = sorted(monthly_comments.index.unique())

# Đảm bảo rằng index mặc định là hợp lệ (0 <= index < length of available_months)
default_start_index = 0
default_end_index = len(available_months) - 1

# Sử dụng st.columns để tạo các cột ngang cho tháng bắt đầu và tháng kết thúc
col1, col2 = st.columns(2)

# Tạo các thanh trượt để chọn tháng bắt đầu và tháng kết thúc trong cột ngang
with col1:
    # Chọn tháng bắt đầu với tháng mặc định là tháng đầu tiên (index=default_start_index)
    start_month = st.selectbox('Chọn tháng bắt đầu', available_months, index=default_start_index)

with col2:
    # Chọn tháng kết thúc với tháng mặc định là tháng cuối cùng (index=default_end_index)
    end_month = st.selectbox('Chọn tháng kết thúc', available_months, index=default_end_index)

# Lọc dữ liệu dựa trên tháng bắt đầu và tháng kết thúc
filtered_data = monthly_comments[(monthly_comments.index >= start_month) & (monthly_comments.index <= end_month)]

# Chọn các tháng cần hiển thị (ví dụ: tháng 3, 6, 9, 12)
selected_months = filtered_data.index.month.isin([3, 6, 9, 12])

# Vẽ biểu đồ bar count với phân chia tích cực và tiêu cực
fig, ax = plt.subplots(figsize=(10, 6))

# Vẽ các thanh cho bình luận tích cực
ax.bar(filtered_data.index.astype(str)[selected_months], filtered_data['positive'][selected_months], label='Tích cực', color='#4CB391', alpha=0.7)

# Vẽ các thanh cho bình luận tiêu cực
ax.bar(filtered_data.index.astype(str)[selected_months], filtered_data['negative'][selected_months], bottom=filtered_data['positive'][selected_months], label='Tiêu cực', color='red', alpha=0.5)

# Thêm tiêu đề và nhãn
ax.set_title('Số lượng bình luận tích cực và tiêu cực theo tháng', fontsize=16)
ax.set_xlabel('Tháng', fontsize=12)
ax.set_ylabel('Số lượng bình luận', fontsize=12)

# Xoay nhãn trục X để dễ đọc
ax.set_xticklabels(filtered_data.index.astype(str)[selected_months], rotation=45)

# Hiển thị legend
ax.legend(title='Loại đánh giá')

# Hiển thị biểu đồ trong Streamlit
st.pyplot(fig)

################################ BIỂU ĐỒ PHÂN PHỐI GIÁ SẢN PHẨM

# Hiển thị thông tin
st.subheader("3. Biểu đồ phân phối giá sản phẩm")

# Vẽ biểu đồ phân phối giá sản phẩm
plt.figure(figsize=(10, 6))
sns.histplot(df['gia_ban'], kde=True, bins=30, color='#4CB391', alpha=0.7)

# Thêm tiêu đề và các nhãn
plt.title('Phân phối giá sản phẩm', fontsize=14)
plt.xlabel('Giá sản phẩm', fontsize=12)
plt.ylabel('Tần suất', fontsize=12)

# Hiển thị biểu đồ trong Streamlit
st.pyplot(plt)

############## BIỂU ĐỒ ĐÁNH GIÁ THEO NHÓM GIÁ SẢN PHẨM

# Chia nhóm giá sản phẩm dựa trên cột gia_ban
bins = [0, 100000, 500000, float('inf')]  # Cài đặt giá trị theo nhóm giá, ví dụ giá thấp, trung bình, cao
labels = ['Giá thấp', 'Giá trung bình', 'Giá cao']
df['gia_nhom'] = pd.cut(df['gia_ban'], bins=bins, labels=labels, right=False)

# Tính toán tỉ lệ đánh giá tích cực/tiêu cực cho từng sản phẩm
sentiment_distribution = df.groupby(['ma_san_pham', 'phan_loai_danh_gia']).size().unstack(fill_value=0)
sentiment_distribution['positive_ratio'] = sentiment_distribution['positive'] / sentiment_distribution.sum(axis=1)
sentiment_distribution['negative_ratio'] = sentiment_distribution['negative'] / sentiment_distribution.sum(axis=1)

# Thêm thông tin nhóm giá vào dữ liệu sentiment_distribution
df_sentiment = df.groupby(['ma_san_pham', 'gia_nhom', 'phan_loai_danh_gia']).size().unstack(fill_value=0)

# Tính số lượng đánh giá tích cực và tiêu cực cho từng nhóm giá
sentiment_by_group = df_sentiment.groupby('gia_nhom')[['positive', 'negative']].sum()

# Chuyển dataframe sentiment_by_group thành dạng dài để seaborn vẽ biểu đồ dễ dàng
sentiment_by_group_reset = sentiment_by_group.reset_index()
sentiment_by_group_melted = sentiment_by_group_reset.melt(id_vars='gia_nhom', value_vars=['positive', 'negative'], 
                                                         var_name='Loại đánh giá', value_name='Số lượng')

# Hàm vẽ biểu đồ
def draw_sentiment_chart():

    # Tạo biểu đồ Seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=sentiment_by_group_melted, 
        x='gia_nhom', 
        y='Số lượng', 
        hue='Loại đánh giá', 
        dodge=True, 
        palette='Set2'
    )

    # Thêm tiêu đề và nhãn
    plt.title('Tỉ lệ đánh giá tích cực và tiêu cực cho từng nhóm giá sản phẩm', fontsize=14)
    plt.xlabel('Nhóm giá sản phẩm', fontsize=12)
    plt.ylabel('Số lượng đánh giá', fontsize=12)
    plt.legend(title='Loại đánh giá')

    # Hiển thị biểu đồ trong Streamlit
    st.pyplot(plt)

st.subheader("4. Tỉ lệ đánh giá theo nhóm giá sản phẩm")
draw_sentiment_chart()

############## SẢN PHẨM CÓ ĐÁNH GIÁ CAO NHẤT VÀ THẤP NHẤT

# Hiển thị thông tin 
st.subheader("5. Sản phẩm có đánh giá thấp nhất và cao nhất")

# Tính điểm đánh giá trung bình cho mỗi sản phẩm
# Giả sử cột 'danh_gia' là điểm đánh giá và cột 'san_pham' là tên sản phẩm
average_ratings = df.groupby('ten_san_pham')['so_sao'].mean().reset_index()

# Sắp xếp các sản phẩm theo điểm đánh giá từ thấp đến cao
sorted_ratings = average_ratings.sort_values(by='so_sao')

# Tạo tab 
tab1, tab2 = st.tabs(["5 sản phẩm có đánh giá cao nhất", "5 sản phẩm có đánh giá thấp nhất"])
# Nội dung cho Tab 1
with tab1:
    # Lấy 5 sản phẩm có đánh giá cao nhất
    highest_rated = sorted_ratings.tail(5)
    st.write(highest_rated)

# Nội dung cho Tab 2
with tab2:
    # Lấy 5 sản phẩm có đánh giá thấp nhất
    lowest_rated = sorted_ratings.head(5)
    st.write(lowest_rated)


########################## WORDCLOUD NỘI DUNG BÌNH LUẬN TRỨC VÀ SAU KHI XỬ LÝ

# Tạo hai tab
st.header('6. WordCloud')

tab1, tab2 = st.tabs(["Nội dung bình luận sau khi xử lý", "Nội dung bình luận trước khi xử lý"])
# Nội dung cho Tab 1
with tab1:
    # st.subheader("Từ tích cực")
    st.image('binh_luan_sau_xu_ly.png')

# Nội dung cho Tab 2
with tab2:
    # st.header("Từ tiêu cực")
    st.image('binh_luan_truoc_xu_ky.png')

##################### WC POSITIVE, NEGATIVE WORDS

# Hàm tạo WordCloud và trả về các từ phổ biến nhất
def plot_wordcloud_and_get_top_words(text, stopwords=None, num_words=10):
    """
    Tạo Word Cloud và trả về các từ xuất hiện nhiều nhất.
    """
    # Tính tần suất từ
    words = text.split()
    word_counts = Counter(words)
    
    # Loại bỏ stopwords (nếu có)
    if stopwords:
        word_counts = Counter({word: count for word, count in word_counts.items() if word not in stopwords})
    
    # Tạo Word Cloud
    wordcloud = WordCloud(stopwords=stopwords, width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
    
    # Vẽ Word Cloud
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)  # Hiển thị Word Cloud trong Streamlit
    
    # Lấy 10 từ phổ biến nhất
    top_words = word_counts.most_common(num_words)
    return top_words

# Giao diện Streamlit POSITIVE
st.subheader("Word Cloud và Top Từ POSITIVE Phổ Biến")

# Đọc văn bản từ tập tin positive_words_VN.txt
text_file_path = "positive_words_VN.txt"  # Đường dẫn đến file văn bản
try:
    with open(text_file_path, 'r', encoding='utf-8') as f:
        text = f.read()  # Đọc nội dung từ file
except FileNotFoundError:
    st.error(f"Không tìm thấy file '{text_file_path}'. Hãy kiểm tra lại đường dẫn!")

# Đọc danh sách stopwords từ tập tin stopwords.txt
stopwords_file_path = "vietnamese-stopwords.txt"  # Đường dẫn đến file stopwords
stopwords = set()
try:
    with open(stopwords_file_path, 'r', encoding='utf-8') as f:
        stopwords_content = f.read()
        stopwords = set(stopwords_content.splitlines())  # Tách mỗi dòng thành một stopword
except FileNotFoundError:
    st.error(f"Không tìm thấy file '{stopwords_file_path}'. Hãy kiểm tra lại đường dẫn!")

# Tạo 2 tab trong Streamlit
tab1, tab2 = st.tabs(["Word Cloud", "Top 10 Từ Phổ Biến"])

# Tab Word Cloud
with tab1:
    st.subheader("Word Cloud")
    top_words = plot_wordcloud_and_get_top_words(text, stopwords=stopwords)

# Tab Top 10 Từ
with tab2:
    st.subheader("Top 10 Từ Phổ Biến Nhất")
    st.write(pd.DataFrame(top_words, columns=["Từ", "Tần suất"]))

#-------------------------
# Giao diện Streamlit NEGATIVE
st.subheader("Word Cloud và Top Từ NEGATIVE Phổ Biến")

# Đọc văn bản từ tập tin positive_words_VN.txt
text_file_path = "negative_words_VN.txt"  # Đường dẫn đến file văn bản
try:
    with open(text_file_path, 'r', encoding='utf-8') as f:
        text = f.read()  # Đọc nội dung từ file
except FileNotFoundError:
    st.error(f"Không tìm thấy file '{text_file_path}'. Hãy kiểm tra lại đường dẫn!")


# Tạo 2 tab trong Streamlit
tab1, tab2 = st.tabs(["Word Cloud", "Top 10 Từ Phổ Biến"])

# Tab Word Cloud
with tab1:
    st.subheader("Word Cloud")
    top_words = plot_wordcloud_and_get_top_words(text, stopwords=stopwords)

# Tab Top 10 Từ
with tab2:
    st.subheader("Top 10 Từ Phổ Biến Nhất")
    st.write(pd.DataFrame(top_words, columns=["Từ", "Tần suất"]))


###################
# Inside the Data: Bên trong dữ liệu.
# Data Unveiled: Hé lộ dữ liệu.
# Beneath the Numbers: Dưới những con số.
# Deep Dive into Data: Đi sâu vào dữ liệu.
# Cracking the Data Code: Giải mã dữ liệu.
