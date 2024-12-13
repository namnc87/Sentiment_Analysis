import streamlit as st
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import underthesea
from underthesea import word_tokenize, pos_tag, sent_tokenize
import re
import regex
import plotly.express as px
import polars as pl
from functools import lru_cache

# Cho 3 file csv nhu sau:

# San_pham.csv: chứa thông tin sản phẩm thuộc nhóm “Chăm sóc da mặt” như ma_san_pham, ten_san_pham, gia_ban, gia_goc, phan_loai, mo_ta, diem_trung_binh
# Khach_hang.csv: chứa thông tin khách hàng gồm ma_khach_hang,ho_ten
# Danh_gia.csv: chứa thông tin đánh giá của khách hàng cho sản phẩm gồm id, ma_khach_hang, noi_dung_binh_luan, ngay_binh_luan, gio_binh_luan, so_sao, ma_san_pham

#################### SET SIDEBAR, PAGE TITLE


st.set_page_config(page_title="Product Analysis", page_icon="🔍")
st.title("🔍 Phân tích sản phẩm:")

st.sidebar.success("Giáo Viên Hướng Dẫn: \n # KHUẤT THUỲ PHƯƠNG")
st.sidebar.success("Học Viên:\n # NGUYỄN CHẤN NAM \n # CHẾ THỊ ANH TUYỀN")
st.sidebar.success("Ngày báo cáo: \n # 16/12/2024")

################################ BIỂU ĐỒ TỔNG QUAN VỀ BÌNH LUẬN VÀ SẢN PHẨM

# "C:/Users/Windows 10/Documents/Zalo Received Files/GUI_project1_Copy/GUI_project1_Copy/"

# Load data
san_pham = pd.read_csv('San_pham.csv')
danh_gia= pd.read_csv('Danh_gia.csv')
khach_hang= pd.read_csv('Khach_hang.csv')
san_pham_image_brand_link = pd.read_csv('San_pham_Link_Image_Brand.csv')

################ START_ Tien xu ly cot noi_dung_binh_luan #####################

#LOAD EMOJICON
file = open('emojicon.txt', 'r', encoding="utf8")
emoji_lst = file.read().split('\n')
emoji_dict = {}
for line in emoji_lst:
    key, value = line.split('\t')
    emoji_dict[key] = str(value)
file.close()
#################
#LOAD TEENCODE
file = open('teencode.txt', 'r', encoding="utf8")
teen_lst = file.read().split('\n')
teen_dict = {}
for line in teen_lst:
    key, value = line.split('\t')
    teen_dict[key] = str(value)
file.close()

with open("teencode.txt", 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()  # Loại bỏ khoảng trắng ở đầu và cuối dòng
        if line:  # Chỉ thực hiện nếu dòng không trống
            try:
                key, value = line.split('\t')
                # Tiến hành xử lý key và value ở đây
            except ValueError:
                print(f'Line has an unexpected format: {line}')
###############
#LOAD TRANSLATE ENGLISH -> VNMESE
file = open('english-vnmese.txt', 'r', encoding="utf8")
english_lst = file.read().split('\n')
english_dict = {}
for line in english_lst:
    key, value = line.split('\t')
    english_dict[key] = str(value)
file.close()
################
#LOAD wrong words
file = open('wrong-word.txt', 'r', encoding="utf8")
wrong_lst = file.read().split('\n')
file.close()
#################
#LOAD STOPWORDS
file = open('vietnamese-stopwords.txt', 'r', encoding="utf8")
stop_words = file.read().split('\n')
file.close()

def process_text(text, emoji_dict, teen_dict, wrong_lst):
    document = text.lower()
    document = document.replace("’",'')
    document = regex.sub(r'\.+', ".", document)
    new_sentence =''
    for sentence in sent_tokenize(document):
        # if not(sentence.isascii()):
        ###### CONVERT EMOJICON
        sentence = ''.join(emoji_dict[word]+' ' if word in emoji_dict else word for word in list(sentence))
        ###### CONVERT TEENCODE
        sentence = ' '.join(teen_dict[word] if word in teen_dict else word for word in sentence.split())
        ###### DEL Punctuation & Numbers
        pattern = r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]+\b'
        sentence = ' '.join(regex.findall(pattern,sentence))
        # ...
        ###### DEL wrong words
        sentence = ' '.join('' if word in wrong_lst else word for word in sentence.split())
        new_sentence = new_sentence+ sentence + '. '
    document = new_sentence
    #print(document)
    ###### DEL excess blank space
    document = regex.sub(r'\s+', ' ', document).strip()
    #...
    return document


# Chuẩn hóa unicode tiếng việt
def loaddicchar():
    uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
    unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"

    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic

# Đưa toàn bộ dữ liệu qua hàm này để chuẩn hóa lại
def covert_unicode(txt):
    dicchar = loaddicchar()
    return regex.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)


def process_special_word(text):
    # có thể có nhiều từ đặc biệt cần ráp lại với nhau
    new_text = ''
    text_lst = text.split()
    i= 0
    # không, chẳng, chả...
    if 'không' in text_lst:
        while i <= len(text_lst) - 1:
            word = text_lst[i]
            #print(word)
            #print(i)
            if  word == 'không':
                next_idx = i+1
                if next_idx <= len(text_lst) -1:
                    word = word +'_'+ text_lst[next_idx]
                i= next_idx + 1
            else:
                i = i+1
            new_text = new_text + word + ' '
    else:
        new_text = text
    return new_text.strip()

# Hàm để chuẩn hóa các từ có ký tự lặp
def normalize_repeated_characters(text):
    # Thay thế mọi ký tự lặp liên tiếp bằng một ký tự đó
    # Ví dụ: "lònggggg" thành "lòng", "thiệtttt" thành "thiệt"
    return re.sub(r'(.)\1+', r'\1', text)


def find_words(document, list_of_words):
    document_lower = document.lower()
    word_count = 0
    word_list = []

    for word in list_of_words:
        if word in document_lower:
            print(word)
            word_count += document_lower.count(word)
            word_list.append(word)

    return word_count, word_list

def apply_processing(value):
    # Kiểm tra xem giá trị có phải là chuỗi không
    if isinstance(value, str):  # Chỉ xử lý nếu value là string
        # Chuyển đổi unicode
        text = covert_unicode(value)
        
        # Xử lý từ đặc biệt
        text = process_special_word(text)
        
        # Chuẩn hóa các ký tự lặp
        text = normalize_repeated_characters(text)
        
        # Xử lý văn bản
        text = process_text(text, emoji_dict, teen_dict, wrong_lst)
        
        return text
    else:
        # Nếu không phải chuỗi, có thể trả về giá trị mặc định hoặc None
        return ''  



################ END_Tien xu ly cot noi_dung_binh_luan #####################

# Hàm phân loại dựa trên giá trị của cột 'so_sao'
def classify_rating(star_rating):
    if star_rating <= 4:
        return 'negative'
    elif star_rating == 5:
        return 'positive'

# Áp dụng hàm vào cột 'so_sao' để tạo cột mới 'phan_loai_danh_gia'
danh_gia['phan_loai_danh_gia'] = danh_gia['so_sao'].apply(classify_rating)


san_pham = san_pham.merge(san_pham_image_brand_link,on="ma_san_pham", how='left')

danhgia_sanpham = danh_gia.merge(san_pham,on="ma_san_pham", how='left')
df=danhgia_sanpham.copy()
st.write(df)

#---START_Hàm thống kế số lượng bình luận theo tháng----------------------------------------
def analyze_comments_by_month(df, product_id):
    """Thống kê số lượng bình luận theo tháng cho một sản phẩm."""
    
    # Chọn ra bình luận của sản phẩm cụ thể
    product_comments = df[df['ma_san_pham'] == product_id]
    
    # Chuyển đổi cột 'ngay_binh_luan' sang kiểu datetime
    product_comments['ngay_binh_luan'] = pd.to_datetime(product_comments['ngay_binh_luan'], format='%d/%m/%Y')
    product_comments.loc[:, 'month'] = product_comments['ngay_binh_luan'].dt.to_period('M')  # Lấy tháng và năm

    # Thiết lập tháng bắt đầu và tháng kết thúc với giá trị mặc định là tháng nhỏ nhất và lớn nhất
    min_month = product_comments['ngay_binh_luan'].min().to_period('M')
    max_month = product_comments['ngay_binh_luan'].max().to_period('M')
    
    st.write("**Chọn khoảng thời gian để xem bình luận:**")
    
    # Tạo hai cột cho ô nhập tháng bắt đầu và tháng kết thúc
    col1, col2 = st.columns(2)
    
    with col1:
        start_month = st.date_input('Tháng bắt đầu:', value=min_month.to_timestamp(), key=f'start_month_{product_id}')
        
    with col2:
        end_month = st.date_input('Tháng kết thúc:', value=max_month.to_timestamp(), key=f'end_month_{product_id}')
    
    # Chuyển đổi đến định dạng Timestamp để sử dụng với to_period
    start_period = pd.to_datetime(start_month).to_period('M')
    end_period = pd.to_datetime(end_month).to_period('M')

    # Lọc bình luận trong khoảng thời gian đã chọn
    filtered_comments = product_comments[(product_comments['month'] >= start_period) & (product_comments['month'] <= end_period)]

    # Đếm số lượng bình luận theo tháng
    monthly_counts = filtered_comments.groupby('month').size().reset_index(name='count')
    
    # Hiển thị bảng thống kê
    st.write(f"**II. Số lượng bình luận theo tháng từ {start_period} đến {end_period} cho sản phẩm ID '{product_id}':**")

    # Trực quan hóa bằng matplotlib
    plt.figure(figsize=(10, 5))
    bars = plt.bar(monthly_counts['month'].astype(str), monthly_counts['count'], color='skyblue')
    plt.xlabel('Tháng')
    plt.ylabel('Số lượng bình luận')
    plt.title(f"Số lượng bình luận theo tháng cho sản phẩm ID {product_id}")
    plt.xticks(rotation=45)  # Xoay tiêu đề trục hoành
    plt.grid(axis='y')

    # Thêm nhãn số liệu lên từng cột trong biểu đồ
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom')  # va='bottom' để đặt nhãn ở trên cột

    # Hiển thị đồ thị trong Streamlit
    st.pyplot(plt)

    if not monthly_counts.empty:
        # Lọc bình luận theo đánh giá
        rating_counts = filtered_comments['so_sao'].value_counts().reindex(range(1, 6), fill_value=0).reset_index()
        rating_counts.columns = ['so_sao', 'count']
    
        # Hiển thị tổng số lượng bình luận
        total_comments = filtered_comments.shape[0]
        st.write(f"**Tổng số bình luận có trong khoảng thời gian đã chọn: {total_comments} bình luận.**")

        # Hiển thị thống kê đánh giá
        st.write(f"**Thống kê bình luận theo đánh giá trong khoảng thời gian từ {start_month} đến {end_month}:**")
    
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
            plt.title(f"Số lượng bình luận theo đánh giá từ {start_month} đến {end_month} cho sản phẩm ID {product_id}")
            plt.xticks(rating_counts['so_sao'].astype(str))  # Đảm bảo tất cả các đánh giá được hiển thị
            plt.grid(axis='y')
            st.pyplot(plt)

            # Close the figure to free memory
            plt.close()
    
        # Tạo tab cho từng loại đánh giá
        st.write("**Chi tiết bình luận theo đánh giá:**")
        tabs = st.tabs([f"Đánh giá {i}" for i in range(1, 6)])  # Tạo 5 tab cho các loại đánh giá từ 1 đến 5

        for i in range(1, 6):
            with tabs[i-1]:
                comments_for_rating = filtered_comments[filtered_comments['so_sao'] == i]
                if not comments_for_rating.empty:
                    st.write(f"**Chi tiết bình luận cho đánh giá {i} sao:**")
                    st.dataframe(comments_for_rating[['ngay_binh_luan', 'noi_dung_binh_luan']], use_container_width=True)
                    st.write(comments_for_rating)
                    
                    # Thống kê cho từng cột
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**Thống kê Sản phẩm:**")
                        pos_data = comments_for_rating[comments_for_rating['san_pham'] == 'positive']
                        neg_data = comments_for_rating[comments_for_rating['san_pham'] == 'negative']
                        pos_count = len(pos_data)
                        neg_count = len(neg_data)
                        st.write(f"- Positive: {pos_count}")
                        st.write(f"- Negative: {neg_count}")
                        
                        # WordCloud cho positive
                        if pos_count > 0:
                            pos_wordcloud = create_wordcloud(pos_data['noi_dung_binh_luan'].tolist(), 'Positive Words')
                            if pos_wordcloud:
                                st.pyplot(pos_wordcloud)
                        
                        # WordCloud cho negative
                        if neg_count > 0:
                            neg_wordcloud = create_wordcloud(neg_data['noi_dung_binh_luan'].tolist(), 'Negative Words')
                            if neg_wordcloud:
                                st.pyplot(neg_wordcloud)
                    
                    with col2:
                        st.write("**Thống kê Dịch vụ:**")
                        pos_data = comments_for_rating[comments_for_rating['dich_vu'] == 'positive']
                        neg_data = comments_for_rating[comments_for_rating['dich_vu'] == 'negative']
                        pos_count = len(pos_data)
                        neg_count = len(neg_data)
                        st.write(f"- Positive: {pos_count}")
                        st.write(f"- Negative: {neg_count}")
                        
                        # WordCloud cho positive
                        if pos_count > 0:
                            pos_wordcloud = create_wordcloud(pos_data['noi_dung_binh_luan'].tolist(), 'Positive Words')
                            if pos_wordcloud:
                                st.pyplot(pos_wordcloud)
                        
                        # WordCloud cho negative
                        if neg_count > 0:
                            neg_wordcloud = create_wordcloud(neg_data['noi_dung_binh_luan'].tolist(), 'Negative Words')
                            if neg_wordcloud:
                                st.pyplot(neg_wordcloud)
                    
                    with col3:
                        st.write("**Thống kê Giao hàng:**")
                        pos_data = comments_for_rating[comments_for_rating['giao_hang'] == 'positive']
                        neg_data = comments_for_rating[comments_for_rating['giao_hang'] == 'negative']
                        pos_count = len(pos_data)
                        neg_count = len(neg_data)
                        st.write(f"- Positive: {pos_count}")
                        st.write(f"- Negative: {neg_count}")
                        
                        # WordCloud cho positive
                        if pos_count > 0:
                            pos_wordcloud = create_wordcloud(pos_data['noi_dung_binh_luan'].tolist(), 'Positive Words')
                            if pos_wordcloud:
                                st.pyplot(pos_wordcloud)
                        
                        # WordCloud cho negative
                        if neg_count > 0:
                            neg_wordcloud = create_wordcloud(neg_data['noi_dung_binh_luan'].tolist(), 'Negative Words')
                            if neg_wordcloud:
                                st.pyplot(neg_wordcloud)
                        
                else:
                    st.write(f"Không có bình luận nào cho đánh giá {i} sao.")
        
        # Để giữ cho chiều cao cột cân bằng, tạo một dòng trống bằng cách sử dụng `st.empty()`.
        st.empty()  # Giữ không gian cho chiều cao bằng nhau
    else:
        st.write(f"Không có bình luận nào trong khoảng thời gian từ {start_period} đến {end_period}.")

#----------------------------------------END_Hàm thống kế số lượng bình luận theo tháng---

#---START_Hàm thống kế số lượng bình luận theo giờ-------------------------------
def analyze_comments_by_hour(df, product_id):
    """Thống kê số lượng bình luận theo khung giờ trong ngày cho một sản phẩm."""
    
    # Chọn ra bình luận của sản phẩm cụ thể
    product_comments = df.loc[df['ma_san_pham'] == product_id].copy()
    
    # Chuyển đổi cột 'gio_binh_luan' sang kiểu datetime để lấy giờ
    product_comments['gio_binh_luan'] = product_comments['gio_binh_luan'].astype(str)
    product_comments.loc[:, 'hour'] = pd.to_datetime(product_comments['gio_binh_luan'], format='%H:%M').dt.hour

    # Thiết lập giờ bắt đầu và giờ kết thúc với giá trị mặc định là giờ nhỏ nhất và lớn nhất
    min_hour = int(product_comments['hour'].min())  # Chuyển về kiểu int
    max_hour = int(product_comments['hour'].max())  # Chuyển về kiểu int
    
    st.write("**Chọn khoảng thời gian (giờ) để xem bình luận:**")
    
    # Tạo hai cột cho ô nhập giờ bắt đầu và giờ kết thúc
    col1, col2 = st.columns(2)

    with col1:
        start_hour = st.selectbox('Giờ bắt đầu:', range(min_hour, max_hour + 1), index=0, key=f'start_hour_{product_id}')  # Unique key
    
    with col2:
        end_hour = st.selectbox('Giờ kết thúc:', range(min_hour, max_hour + 1), index=max_hour - min_hour, key=f'end_hour_{product_id}')  # Unique key
    
    # Lọc bình luận trong khoảng thời gian đã chọn
    filtered_comments = product_comments[(product_comments['hour'] >= start_hour) & (product_comments['hour'] <= end_hour)]

    # Đếm số lượng bình luận theo giờ
    hourly_counts = filtered_comments.groupby('hour').size().reset_index(name='count')

    # Hiển thị bảng thống kê
    st.write(f"**II. Số lượng bình luận theo giờ từ {start_hour}:00 đến {end_hour}:00 cho sản phẩm ID '{product_id}':**")

    # Trực quan hóa bằng matplotlib
    plt.figure(figsize=(10, 5))
    if not hourly_counts.empty:
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

        # Nếu có bình luận trong khoảng thời gian đã chọn, hiển thị chi tiết
        if not filtered_comments.empty:
            # st.write(f"**Chi tiết bình luận trong khung giờ từ {start_hour}:00 đến {end_hour}:00:**")
            # st.dataframe(filtered_comments[['gio_binh_luan', 'noi_dung_binh_luan', 'so_sao']])

            # Thống kê số lượng bình luận theo đánh giá
            rating_counts = filtered_comments['so_sao'].value_counts().reindex(range(1, 6), fill_value=0).reset_index()
            rating_counts.columns = ['so_sao', 'count']

            # Hiển thị tổng số lượng bình luận
            total_comments = filtered_comments.shape[0]
            st.write(f"**Tổng số bình luận có trong khoảng thời gian đã chọn: {total_comments} bình luận.**")

            # Hiển thị thống kê đánh giá
            st.write(f"**Thống kê bình luận theo đánh giá từ {start_hour}:00 đến {end_hour}:00:**")
            
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
                plt.title(f"Số lượng bình luận theo đánh giá từ {start_hour}:00 đến {end_hour}:00 cho sản phẩm ID {product_id}")
                plt.xticks(rating_counts['so_sao'].astype(str))  # Đảm bảo tất cả các đánh giá được hiển thị
                plt.grid(axis='y')
                st.pyplot(plt)

            # Tạo tab cho từng loại đánh giá
            st.write("**Chi tiết bình luận theo đánh giá:**")
            tabs = st.tabs([f"Đánh giá {i}" for i in range(1, 6)])  # Tạo 5 tab cho các loại đánh giá từ 1 đến 5

            for i in range(1, 6):
                with tabs[i-1]:
                    comments_for_rating = filtered_comments[filtered_comments['so_sao'] == i]
                    if not comments_for_rating.empty:
                        st.write(f"**Chi tiết bình luận cho đánh giá {i} sao:**")
                        st.dataframe(comments_for_rating[['gio_binh_luan', 'noi_dung_binh_luan']], use_container_width=True)
                    else:
                        st.write(f"Không có bình luận nào cho đánh giá {i} sao.")

            # Để giữ cho chiều cao cột cân bằng, tạo một dòng trống bằng cách sử dụng `st.empty()`.
            st.empty()
        else:
            st.write(f"Không có bình luận nào trong khoảng thời gian từ {start_hour}:00 đến {end_hour}:00.")
    else:
        st.write(f"Không có bình luận nào trong khoảng thời gian từ {start_hour}:00 đến {end_hour}:00.")

#----------------------------------------END_Hàm thống kế số lượng bình luận theo giờ---

#---START_Hàm thống kế số lượng bình luận theo loại sao-------------------------------
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
#---------------------------------------END_Hàm thống kế số lượng bình luận theo loại sao--

#---START_Hàm vẽ wordcloud bình luận theo sản phẩm-------------------------------
def plot_product_comments_wordcloud(df, product_id, stopwords=None):
    """Vẽ Word Cloud cho bình luận của sản phẩm cụ thể với các tab riêng biệt cho từ tích cực và tiêu cực."""
    
    # Lọc bình luận của sản phẩm cụ thể
    product_comments = df[df['ma_san_pham'] == product_id]['noi_dung_binh_luan']

    # Chuyển đổi bình luận thành danh sách, loại bỏ NaN
    product_comments = product_comments.dropna().astype(str).tolist()

    # Lấy các từ tích cực và tiêu cực từ file
    try:
        with open("positive_words.txt", 'r', encoding='utf-8') as f:
            positive_words = f.read().splitlines()
        
        with open("negative_words.txt", 'r', encoding='utf-8') as f:
            negative_words = f.read().splitlines()
        
        # Lấy stopwords nếu có
        if stopwords is None:
            stopwords = set()
        
        with open("vietnamese-stopwords.txt", 'r', encoding='utf-8') as f:
            stopwords.update(f.read().splitlines())
    
    except FileNotFoundError as e:
        st.error(f"Không tìm thấy file: {e.filename}. Hãy kiểm tra đường dẫn!")
        return

    # Tạo slider cho số lượng từ hiển thị trong Word Cloud
    num_words = st.slider("**Chọn số lượng từ hiển thị:**", min_value=1, max_value=100, value=10, key=f'wordcloud_slider_{product_id}')

    # Tạo tabs cho wordcloud
    tabs = st.tabs(["Từ Tích Cực", "Từ Tiêu Cực"])

    # Tạo hàm để vẽ Word Cloud từ danh sách cụm từ
    def create_wordcloud(phrases):
        if phrases:
            # Tạo từ điển tần suất cho các cụm từ
            freq_dict = {phrase: phrases.count(phrase) for phrase in set(phrases)}
            
            # Tạo WordCloud với collocations=False để giữ nguyên cụm từ
            wordcloud = WordCloud(width=800, height=400,
                                background_color='white',
                                stopwords=stopwords,
                                max_words=num_words,
                                collocations=False).generate_from_frequencies(freq_dict)
            
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)
        else:
            st.write("Không có dữ liệu để hiển thị Word Cloud.")

    # Tạo Word Cloud cho từ tích cực trong tab Từ Tích Cực
    with tabs[0]:
        st.subheader("Word Cloud cho Từ Tích Cực")
        found_positive_phrases = []

        for positive_phrase in positive_words:
            if any(positive_phrase in comment for comment in product_comments):
                found_positive_phrases.append(positive_phrase)

        if found_positive_phrases:
            st.write("Các cụm từ tích cực tìm thấy:", ', '.join(found_positive_phrases))
            create_wordcloud(found_positive_phrases)
        else:
            st.write("Không có từ tích cực nào được tìm thấy.")

    # Tạo Word Cloud cho từ tiêu cực trong tab Từ Tiêu Cực
    with tabs[1]:
        st.subheader("Word Cloud cho Từ Tiêu Cực")
        found_negative_phrases = []

        for negative_phrase in negative_words:
            if any(negative_phrase in comment for comment in product_comments):
                found_negative_phrases.append(negative_phrase)

        if found_negative_phrases:
            st.write("Các cụm từ tiêu cực tìm thấy:", ', '.join(found_negative_phrases))
            create_wordcloud(found_negative_phrases)
        else:
            st.write("Không có từ tiêu cực nào được tìm thấy.")
#----------------------------------------END_Hàm vẽ wordcloud bình luận theo sản phẩm---

# ----START_Hàm chuyển đổi đơn vị tiền tệ VND--------------------
def format_currency(value):
    return f"{value:,.0f} VND"
# -----------------------------END_Hàm chuyển đổi đơn vị tiền tệ VND---


# ------------START_Hàm để thống kê số lượng đánh giá theo thương hiệu và loại đánh giá--------------------
def analyze_product_reviews(df, selected_brands, review_type):
    filtered_df = df[df['thuong_hieu'].isin(selected_brands)]
    review_counts = filtered_df[filtered_df['so_sao'] == review_type].groupby('thuong_hieu').size()
    return review_counts
# ------------END_Hàm để thống kê số lượng đánh giá theo thương hiệu và loại đánh giá--------------------


@lru_cache(maxsize=None)
def load_keywords(filename):
    keywords = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                key, values = line.strip().split(':')
                keywords[key.strip()] = set(v.strip() for v in values.split(','))
    return keywords



def check_content_pandas(df: pd.DataFrame, category: str, keywords: dict, stop_words: set) -> pd.DataFrame:
    # Extract keywords from the keywords dictionary
    key_phrases = keywords['key_phrases']
    positive_words = set(keywords['positive_words'])  # Use set for faster lookup
    negative_words = set(keywords['negative_words'])
    
    # Convert content to lowercase
    df['content_lower'] = df['noi_dung_binh_luan'].str.lower()

    # Remove stop words and create cleaned content
    df['cleaned_content'] = df['content_lower'].astype(str).apply(
        lambda x: ' '.join([word for word in x.split() if word not in stop_words])
    )
    
    # Initialize lists for results
    sentiment_col = []
    keyword_col = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        found = False
        
        # Check if cleaned_content is None or empty
        cleaned_content = row['cleaned_content'] or '' 
        
        for phrase in key_phrases:
            if phrase in cleaned_content:
                # Check negative words first
                for neg_word in negative_words:
                    if neg_word in cleaned_content:
                        sentiment_col.append('negative')
                        keyword_col.append(f'{phrase} {neg_word}')
                        found = True
                        break  # Break out of the negative check
                if found:  # If already found a negative word, no need to check further
                    break
                
                # If no negatives, check for positives
                for pos_word in positive_words:
                    if pos_word in cleaned_content:
                        sentiment_col.append('positive')
                        keyword_col.append(f'{phrase} {pos_word}')
                        found = True
                        break
                if found:
                    break  # Break out if we've found a sentiment
        
        if not found:
            # No phrases found or no sentiment detected; check based on the category
            if category == 'san_pham':
                # Check for any negative word in the entire cleaned content
                for neg_word in negative_words:
                    if neg_word in cleaned_content:
                        sentiment_col.append('negative')
                        keyword_col.append(f'sản phẩm {neg_word}')
                        found = True
                        break

                if not found:
                    # Check for positive words
                    for pos_word in positive_words:
                        if pos_word in cleaned_content:
                            sentiment_col.append('positive')
                            keyword_col.append(f'sản phẩm {pos_word}')
                            found = True
                            break

            if not found:  # If nothing matched, it's neutral
                sentiment_col.append('neutral')
                keyword_col.append('')
    
    # Add the results to the DataFrame
    df[f"{category}"] = sentiment_col
    df[f"{category}_kw"] = keyword_col
    
    return df


def analyze_comments(df: pl.DataFrame) -> pl.DataFrame:
    # Load keywords for each type
    san_pham_kw = load_keywords('san_pham_keywords.txt')
    dich_vu_kw = load_keywords('dich_vu_keywords.txt')
    giao_hang_kw = load_keywords('giao_hang_keywords.txt')

    with open('vietnamese-stopwords.txt', 'r', encoding='utf-8') as file:
        stop_words = set(file.read().splitlines())  
    
    # Process each category and extend DataFrame accordingly
    df = check_content_pandas(df, 'san_pham', san_pham_kw, stop_words)
    df = check_content_pandas(df, 'dich_vu', dich_vu_kw, stop_words)
    df = check_content_pandas(df, 'giao_hang', giao_hang_kw, stop_words)
        
    return df



# Phân tích comments
danh_gia = analyze_comments(danh_gia) 




def create_wordcloud(text_data, title):
    if not text_data:  # Nếu không có dữ liệu
        return None
        
    # Tạo WordCloud (đã bỏ font_path)
    wordcloud = WordCloud(
        width=300,
        height=200,
        background_color='white',
        max_words=10
    ).generate(' '.join(text_data))
    
    # Tạo figure
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title)
    return fig




def get_unique_brands(df):
    """Get unique brands from DataFrame."""
    brands = df['thuong_hieu'].astype(str).unique().tolist()
    return sorted([brand for brand in brands if brand.lower() != 'nan'])

def visualize_rating_counts(rating_counts, title):
    """Visualize rating counts with a horizontal bar chart."""
    plt.figure(figsize=(10, 5))
    bars = plt.barh(rating_counts['ten_san_pham'], rating_counts['tong_danh_gia'], color='skyblue')
    for bar in bars:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, 
                 f'{int(bar.get_width())}', va='center')
    plt.xlabel('Số lượng đánh giá')
    plt.title(title)
    plt.tight_layout()
    st.pyplot(plt)


def plot_sentiment_distribution(sentiment_by_line):
    """Plot pie charts for sentiment distribution across product lines."""
    num_cols = 2
    cols = st.columns(num_cols)

    for idx, (dong_sp, row) in enumerate(sentiment_by_line.iterrows()):
        col_idx = idx % num_cols
        with cols[col_idx]:
            fig = px.pie(values=row.values,
                         names=row.index,
                         title=f'Phân bố bình luận - {dong_sp}',
                         color_discrete_map={'positive': '#2ECC71', 'negative': '#E74C3C'})
            fig.update_traces(textposition='inside', textinfo='percent+value', hole=.3)
            fig.update_layout(showlegend=True, height=300, width=300)
            st.plotly_chart(fig)



def format_product_selection(filtered_df):
    """Format the product selection list for dropdown."""
    return filtered_df.apply(lambda x: f"{x['ten_san_pham']} (Code: {x['ma_san_pham']})", axis=1).tolist()

def display_product_info(selected_row):
    """Display the product's information in the Streamlit app."""
    formatted_price = format_currency(selected_row['gia_ban'])
    
    col1, col2 = st.columns([2, 1.5])  # Adjust the weights as needed
    
    with col1:
        st.image(selected_row['hinh_anh'], caption=selected_row['ten_san_pham'])
    
    with col2:
        st.markdown(f"<h4>Giá bán: {formatted_price}</h4>", unsafe_allow_html=True)
        st.markdown(f"<h4>Điểm trung bình: {selected_row['diem_trung_binh']}</h4>", unsafe_allow_html=True)
        st.page_link(page=selected_row['chi_tiet'], label='**Nhấn vào để xem chi tiết**')

def display_analysis_tabs(selected_code):
    """Create and display tabs for product analysis."""
    analysis_tabs = st.tabs(['Tháng', 'Giờ', 'WordCloud'])
    with analysis_tabs[0]:
        analyze_comments_by_month(danh_gia, selected_code)
    with analysis_tabs[1]:   
        analyze_comments_by_hour(danh_gia, selected_code)
    with analysis_tabs[2]:
        plot_product_comments_wordcloud(danh_gia, selected_code)



def prepare_data(df):
    """Pre-process data: Convert date and time columns and filter necessary columns."""
    df = df.copy()
    df['ngay_binh_luan'] = pd.to_datetime(df['ngay_binh_luan'], format='%d/%m/%Y', errors='coerce')
    df.dropna(subset=['ngay_binh_luan'], inplace=True)
    df['month'] = df['ngay_binh_luan'].dt.to_period('M')
    df['hour'] = pd.to_datetime(df['gio_binh_luan'].astype(str), format='%H:%M').dt.hour
    df['dong_san_pham'] = df['dong_san_pham'].astype(str)
    return df

@st.cache_data
def filter_data(df, selected_params):
    """Filter DataFrame based on selected parameters."""
    mask = (
        df['dong_san_pham'].isin(selected_params['dong_san_pham']) &
        df['thuong_hieu'].isin(selected_params['brands']) &
        df['so_sao'].isin(selected_params['review_types']) &
        (df['month'] >= pd.to_datetime(selected_params['start_month']).to_period('M')) &
        (df['month'] <= pd.to_datetime(selected_params['end_month']).to_period('M')) &
        (df['hour'] >= selected_params['start_hour']) &
        (df['hour'] <= selected_params['end_hour'])
    )
    return df[mask]

@st.cache_data
def create_bar_chart(filtered_df):
    """Create a bar chart of review counts by brand and review type."""
    review_counts = filtered_df.groupby(['thuong_hieu', 'so_sao']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    review_counts.plot(kind='bar', width=0.8, ax=ax)
    for container in ax.containers:
        ax.bar_label(container, padding=3)
        
    ax.set_title('Số lượng Đánh giá theo Thương hiệu và Loại Đánh giá')
    ax.set_xlabel('Thương hiệu')
    ax.set_ylabel('Số lượng Đánh giá')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Loại Đánh giá')
    
    return fig, review_counts

@st.cache_data
def create_pie_chart(review_counts, review_type):
    """Create a pie chart for the specific review type."""
    fig, ax = plt.subplots(figsize=(8, 8))
    review_counts[review_type].plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
    ax.set_title(f'Tỷ lệ đánh giá {review_type} sao giữa các thương hiệu')
    ax.set_ylabel('')
    
    return fig


# ------------START_ Main Streamlit App--------------------
# Tạo giao diện tìm kiếm sản phẩm
st.title("Tìm Kiếm Sản Phẩm")

# Convert relevant columns to string, handling possible None values
df['ma_san_pham'] = df['ma_san_pham'].astype(str)
df['ten_san_pham'] = df['ten_san_pham'].astype(str)
danh_gia['ma_san_pham'] = danh_gia['ma_san_pham'].astype(str)

# Tạo ba tab: "Theo sản phẩm" và "Theo từng thương hiệu", "Theo nhiều thương hiệu"
main_tabs = st.tabs(["Theo sản phẩm", "Theo từng thương hiệu", "Theo nhiều thương hiệu"])

# Tab 1: Theo sản phẩm
with main_tabs[0]:
    filtered_df = df.drop_duplicates(subset='ma_san_pham')

    if not filtered_df.empty:
        product_list = format_product_selection(filtered_df)
        product_list.insert(0, "Chọn sản phẩm")  # Default option

        selected_product = st.selectbox("Vui lòng nhập tên sản phẩm, mã sản phẩm hoặc chọn 1 sản phẩm:", product_list, index=0, key='product_selection')
        
        if selected_product != "Chọn sản phẩm":
            selected_code = selected_product.split(" (Code: ")[-1].rstrip(")")
            selected_row = filtered_df[filtered_df['ma_san_pham'] == selected_code].iloc[0]

            st.write("Bạn đã chọn:", selected_product)
            st.write("Mã sản phẩm:", selected_code)

            # Display product information
            display_product_info(selected_row)

            # Call analysis functions
            display_analysis_tabs(selected_code)
    else:
        st.write("Không tìm thấy sản phẩm.")

# Tab 2: Theo từng thương hiệu
with main_tabs[1]:
    brands = get_unique_brands(df)
    brands.insert(0, "Chọn thương hiệu")
    
    selected_brand = st.selectbox("Vui lòng nhập hoặc chọn 1 thương hiệu:", brands)

    if selected_brand != "Chọn thương hiệu":
        filtered_brand_df = df[df['thuong_hieu'].str.contains(selected_brand, case=False, na=False)].drop_duplicates(subset='ma_san_pham')
        
        if not filtered_brand_df.empty:
            product_list_brands = filtered_brand_df.apply(lambda x: f"{x['ten_san_pham']} (Code: {x['ma_san_pham']})", axis=1).tolist()

            dis_tabs = st.tabs(['Tổng sản phẩm', 'Dòng sản phẩm'])

            with dis_tabs[0]:  # 'Tổng sản phẩm'
                st.write(f"Có {filtered_brand_df.shape[0]} sản phẩm của thương hiệu {selected_brand}.")

                rating_counts = (danh_gia.groupby('ma_san_pham')['so_sao'].value_counts().unstack(fill_value=0)).sum(axis=1).reset_index()
                rating_counts.columns = ['ma_san_pham', 'tong_danh_gia']

                rating_summary = filtered_brand_df.merge(rating_counts, on='ma_san_pham', how='left')
                visualize_rating_counts(rating_summary, f'Số lượng đánh giá theo sản phẩm của thương hiệu {selected_brand}')

                selected_product_brand = st.selectbox("Chọn sản phẩm để phân tích:", product_list_brands)
                selected_code_brand = selected_product_brand.split(" (Code: ")[-1].rstrip(")")
                selected_row_2 = filtered_brand_df[filtered_brand_df['ma_san_pham'] == selected_code_brand].iloc[0]

                st.write("Bạn đã chọn sản phẩm:", selected_product_brand)
                st.write("Mã sản phẩm:", selected_code_brand)

                display_product_info(selected_row_2)

                st.write("Thống kê số lượng bình luận:")
                sub2_tabs = st.tabs(["Tháng", "Giờ", "WordCloud"])
                with sub2_tabs[0]:
                    analyze_comments_by_month(danh_gia, selected_code_brand)
                with sub2_tabs[1]:
                    analyze_comments_by_hour(danh_gia, selected_code_brand)
                with sub2_tabs[2]:
                    plot_product_comments_wordcloud(danh_gia, selected_code_brand)

            # 'Dòng sản phẩm' logic
            with dis_tabs[1]:
                product_line_counts = filtered_brand_df['dong_san_pham'].value_counts()
                st.write(f"Tổng số dòng sản phẩm của thương hiệu {selected_brand}: {len(product_line_counts)}")

                # Creating tabs for further analysis
                dong_tabs = st.tabs(['Sản phẩm', 'Bình luận', 'Đánh giá'])

                with dong_tabs[0]:  # 'Sản phẩm'
                    # Product line visualization
                    product_line_df = pd.DataFrame({
                        'Dòng sản phẩm': product_line_counts.index,
                        'Số lượng sản phẩm': product_line_counts.values
                    })
                    fig = px.bar(product_line_df, x='Số lượng sản phẩm', y='Dòng sản phẩm',
                                 orientation='h', text='Số lượng sản phẩm', title=f'Phân bố số lượng sản phẩm theo dòng - {selected_brand}')
                    
                    fig.update_traces(textposition='outside')
                    fig.update_layout(yaxis_title="Dòng sản phẩm", xaxis_title="Số lượng sản phẩm")
                    st.plotly_chart(fig)

                    # Dropdown to select product line
                    selected_product_line = st.selectbox("Chọn dòng sản phẩm để xem chi tiết:", ["Chọn dòng sản phẩm"] + filtered_brand_df['dong_san_pham'].unique().tolist())

                    if selected_product_line != "Chọn dòng sản phẩm":
                        product_line_df = filtered_brand_df[filtered_brand_df['dong_san_pham'] == selected_product_line]
                        st.write(f"Có {len(product_line_df)} sản phẩm trong dòng {selected_product_line}")

                        cols = st.columns(3)  # For displaying product images
                        for idx, row in enumerate(product_line_df.itertuples()):
                            with cols[idx % 3]:
                                st.write(f"**{row.ten_san_pham}**")
                                st.write(f"Mã SP: {row.ma_san_pham}")
                                if pd.notna(row.hinh_anh):
                                    st.image(row.hinh_anh, caption=row.ten_san_pham)
                                st.write("---")

                with dong_tabs[1]:  # 'Bình luận'
                    product_comments = pd.merge(filtered_brand_df[['ma_san_pham', 
                                                                  'dong_san_pham']], 
                                                danh_gia[['ma_san_pham', 
                                                           'noi_dung_binh_luan', 
                                                           'phan_loai_danh_gia']], 
                                                on='ma_san_pham', 
                                                how='left')
                    
                    comments_by_line = product_comments.groupby('dong_san_pham')['noi_dung_binh_luan'].count().reset_index(name='Số lượng bình luận')
                    fig1 = px.bar(comments_by_line, 
                                   x='dong_san_pham', 
                                   y='Số lượng bình luận', 
                                   text='Số lượng bình luận',
                                   title=f'Phân bố số lượng bình luận theo dòng sản phẩm - {selected_brand}')
                    st.plotly_chart(fig1)

                    sentiment_by_line = product_comments.groupby(['dong_san_pham', 'phan_loai_danh_gia']).size().unstack(fill_value=0)
                    st.write("Số lượng bình luận theo sentiment cho từng dòng sản phẩm:")
                    st.dataframe(sentiment_by_line)

                    plot_sentiment_distribution(sentiment_by_line)

                with dong_tabs[2]:  # 'Đánh giá'
                    rating_counts = pd.merge(filtered_brand_df[['ma_san_pham', 'dong_san_pham']], 
                                                danh_gia[['ma_san_pham', 'so_sao']], 
                                                on='ma_san_pham', 
                                                how='left').groupby(['dong_san_pham', 'so_sao']).size().unstack(fill_value=0)
                    
                    st.write("Số lượng các loại so_sao theo từng dòng sản phẩm:")
                    st.dataframe(rating_counts)

                    rating_counts_long = rating_counts.reset_index().melt(id_vars='dong_san_pham', var_name='Loại so_sao', value_name='Số lượng')

                    fig_bar = px.bar(rating_counts_long, 
                                    x='dong_san_pham', 
                                    y='Số lượng', 
                                    color='Loại so_sao', 
                                    title=f'Số lượng từng loại so_sao theo từng dòng sản phẩm - {selected_brand}',
                                    labels={'Số lượng': 'Số lượng', 'dong_san_pham': 'Dòng sản phẩm'},
                                    barmode='group')
                    fig_bar.update_layout(height=400)
                    st.plotly_chart(fig_bar)

                    if not rating_counts.empty:
                        for column in range(0, len(rating_counts.columns), 2):
                            # Create subplots for every two columns
                            cols = st.columns(2)
                            for col in range(2):
                                idx = column + col
                                if idx < len(rating_counts):
                                    dong_sp = rating_counts.index[idx]
                                    row = rating_counts.loc[dong_sp]
                                    
                                    with cols[col]:
                                        fig = px.pie(values=row.values,
                                                     names=row.index,
                                                     title=f'Tỷ lệ phần trăm các loại so_sao - {dong_sp}',
                                                     color_discrete_sequence=px.colors.sequential.Plasma)
                                        fig.update_traces(textposition='inside',
                                                          textinfo='percent+value',
                                                          hole=.3)
                                        st.plotly_chart(fig)

                    else:
                        st.write("Không có dữ liệu để hiển thị.")
        else:
            st.write("Không tìm thấy sản phẩm cho thương hiệu này.")

# Tab 3: Theo nhiều thương hiệu
with main_tabs[2]:
    # Streamlit Configuration
    st.title('Thống kê Đánh giá Sản phẩm theo Thương hiệu')

    # Pre-process data once
    df = prepare_data(df)

    # Filter Controls
    col1, col2 = st.columns(2)
    with col1:
        selected_dong_san_pham = st.multiselect('Chọn Dòng Sản Phẩm:', sorted(df['dong_san_pham'].unique()))
    with col2:
        if selected_dong_san_pham:
            filtered_brands = sorted(df[df['dong_san_pham'].isin(selected_dong_san_pham)]['thuong_hieu'].unique())
            selected_brands = st.multiselect('Chọn Thương hiệu:', filtered_brands)
        else:
            selected_brands = []

    # Review type selection
    review_types = sorted(df['so_sao'].dropna().unique())  # Handle NaN
    selected_review_types = st.multiselect('Chọn Loại Đánh giá:', review_types)

    # Date range selection
    col3, col4 = st.columns(2)
    with col3:
        start_month = st.date_input('Tháng bắt đầu:', value=df['ngay_binh_luan'].min())
    with col4:
        end_month = st.date_input('Tháng kết thúc:', value=df['ngay_binh_luan'].max())

    # Hour range selection
    col5, col6 = st.columns(2)
    min_hour, max_hour = df['hour'].min(), df['hour'].max()
    with col5:
        start_hour = st.number_input('Giờ bắt đầu:', min_value=min_hour, max_value=max_hour, value=min_hour)
    with col6:
        end_hour = st.number_input('Giờ kết thúc:', min_value=start_hour, max_value=max_hour, value=max_hour)

    # Analysis button
    if st.button('Thống kê'):
        if not (selected_brands and selected_dong_san_pham):
            st.warning('Vui lòng chọn ít nhất một thương hiệu và một dòng sản phẩm.')
            st.stop()

        selected_params = {
            'dong_san_pham': selected_dong_san_pham,
            'brands': selected_brands,
            'review_types': selected_review_types,
            'start_month': start_month,
            'end_month': end_month,
            'start_hour': start_hour,
            'end_hour': end_hour
        }
        
        filtered_df = filter_data(df, selected_params)
        
        if filtered_df.empty:
            st.warning('Không có dữ liệu phù hợp với các tiêu chí đã chọn.')
            st.stop()

        # Create and display charts
        bar_fig, review_counts = create_bar_chart(filtered_df)
        st.pyplot(bar_fig)

        # Create pie chart tabs
        valid_review_types = sorted(set(selected_review_types) & set(review_counts.columns))
        if valid_review_types:
            pie_tabs = st.tabs([f"{review_type} sao" for review_type in valid_review_types])
            for tab, review_type in zip(pie_tabs, valid_review_types):
                with tab:
                    pie_fig = create_pie_chart(review_counts, review_type)
                    st.pyplot(pie_fig)
        else:
            st.warning("Không có loại đánh giá nào để hiển thị.")

# ------------END_ Main Streamlit App--------------------