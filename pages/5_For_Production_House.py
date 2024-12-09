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

# Load data
san_pham = pd.read_csv('San_pham.csv')
danh_gia= pd.read_csv('Danh_gia.csv')
khach_hang= pd.read_csv('Khach_hang.csv')

################ START_ Tien xu ly cot noi_dung_binh_luan #####################

# #LOAD EMOJICON
# file = open('emojicon.txt', 'r', encoding="utf8")
# emoji_lst = file.read().split('\n')
# emoji_dict = {}
# for line in emoji_lst:
#     key, value = line.split('\t')
#     emoji_dict[key] = str(value)
# file.close()
# #################
# #LOAD TEENCODE
# file = open('teencode.txt', 'r', encoding="utf8")
# teen_lst = file.read().split('\n')
# teen_dict = {}
# for line in teen_lst:
#     key, value = line.split('\t')
#     teen_dict[key] = str(value)
# file.close()

# with open("teencode.txt", 'r', encoding='utf-8') as file:
#     for line in file:
#         line = line.strip()  # Loại bỏ khoảng trắng ở đầu và cuối dòng
#         if line:  # Chỉ thực hiện nếu dòng không trống
#             try:
#                 key, value = line.split('\t')
#                 # Tiến hành xử lý key và value ở đây
#             except ValueError:
#                 print(f'Line has an unexpected format: {line}')
# ###############
# #LOAD TRANSLATE ENGLISH -> VNMESE
# file = open('english-vnmese.txt', 'r', encoding="utf8")
# english_lst = file.read().split('\n')
# english_dict = {}
# for line in english_lst:
#     key, value = line.split('\t')
#     english_dict[key] = str(value)
# file.close()
# ################
# #LOAD wrong words
# file = open('wrong-word.txt', 'r', encoding="utf8")
# wrong_lst = file.read().split('\n')
# file.close()
# #################
# #LOAD STOPWORDS
# file = open('vietnamese-stopwords.txt', 'r', encoding="utf8")
# stopwords_lst = file.read().split('\n')
# file.close()

# def process_text(text, emoji_dict, teen_dict, wrong_lst):
#     document = text.lower()
#     document = document.replace("’",'')
#     document = regex.sub(r'\.+', ".", document)
#     new_sentence =''
#     for sentence in sent_tokenize(document):
#         # if not(sentence.isascii()):
#         ###### CONVERT EMOJICON
#         sentence = ''.join(emoji_dict[word]+' ' if word in emoji_dict else word for word in list(sentence))
#         ###### CONVERT TEENCODE
#         sentence = ' '.join(teen_dict[word] if word in teen_dict else word for word in sentence.split())
#         ###### DEL Punctuation & Numbers
#         pattern = r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]+\b'
#         sentence = ' '.join(regex.findall(pattern,sentence))
#         # ...
#         ###### DEL wrong words
#         sentence = ' '.join('' if word in wrong_lst else word for word in sentence.split())
#         new_sentence = new_sentence+ sentence + '. '
#     document = new_sentence
#     #print(document)
#     ###### DEL excess blank space
#     document = regex.sub(r'\s+', ' ', document).strip()
#     #...
#     return document


# # Chuẩn hóa unicode tiếng việt
# def loaddicchar():
#     uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
#     unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"

#     dic = {}
#     char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
#         '|')
#     charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
#         '|')
#     for i in range(len(char1252)):
#         dic[char1252[i]] = charutf8[i]
#     return dic

# # Đưa toàn bộ dữ liệu qua hàm này để chuẩn hóa lại
# def covert_unicode(txt):
#     dicchar = loaddicchar()
#     return regex.sub(
#         r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
#         lambda x: dicchar[x.group()], txt)


# def process_special_word(text):
#     # có thể có nhiều từ đặc biệt cần ráp lại với nhau
#     new_text = ''
#     text_lst = text.split()
#     i= 0
#     # không, chẳng, chả...
#     if 'không' in text_lst:
#         while i <= len(text_lst) - 1:
#             word = text_lst[i]
#             #print(word)
#             #print(i)
#             if  word == 'không':
#                 next_idx = i+1
#                 if next_idx <= len(text_lst) -1:
#                     word = word +'_'+ text_lst[next_idx]
#                 i= next_idx + 1
#             else:
#                 i = i+1
#             new_text = new_text + word + ' '
#     else:
#         new_text = text
#     return new_text.strip()

# # Hàm để chuẩn hóa các từ có ký tự lặp
# def normalize_repeated_characters(text):
#     # Thay thế mọi ký tự lặp liên tiếp bằng một ký tự đó
#     # Ví dụ: "lònggggg" thành "lòng", "thiệtttt" thành "thiệt"
#     return re.sub(r'(.)\1+', r'\1', text)


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

# def apply_processing(value):
#     # Kiểm tra xem giá trị có phải là chuỗi không
#     if isinstance(value, str):  # Chỉ xử lý nếu value là string
#         # Chuyển đổi unicode
#         text = covert_unicode(value)
        
#         # Xử lý từ đặc biệt
#         text = process_special_word(text)
        
#         # Chuẩn hóa các ký tự lặp
#         text = normalize_repeated_characters(text)
        
#         # Xử lý văn bản
#         text = process_text(text, emoji_dict, teen_dict, wrong_lst)
        
#         return text
#     else:
#         # Nếu không phải chuỗi, có thể trả về giá trị mặc định hoặc None
#         return ''  



################ END_Tien xu ly cot noi_dung_binh_luan #####################

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
def analyze_comments_by_month(df, product_id):
    """Thống kê số lượng bình luận theo tháng cho một sản phẩm."""
    
    # Chọn ra bình luận của sản phẩm cụ thể
    product_comments = df[df['ma_san_pham'] == product_id]
    
    # Chuyển đổi cột 'ngay_binh_luan' sang kiểu datetime
    product_comments['ngay_binh_luan'] = pd.to_datetime(product_comments['ngay_binh_luan'], format='%d/%m/%Y')
    product_comments['month'] = product_comments['ngay_binh_luan'].dt.to_period('M')  # Lấy tháng và năm

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
    
        # Tạo tab cho từng loại đánh giá
        st.write("**Chi tiết bình luận theo đánh giá:**")
        tabs = st.tabs([f"Đánh giá {i}" for i in range(1, 6)])  # Tạo 5 tab cho các loại đánh giá từ 1 đến 5

        for i in range(1, 6):
            with tabs[i-1]:
                comments_for_rating = filtered_comments[filtered_comments['so_sao'] == i]
                if not comments_for_rating.empty:
                    st.write(f"**Chi tiết bình luận cho đánh giá {i} sao:**")
                    st.dataframe(comments_for_rating[['ngay_binh_luan', 'noi_dung_binh_luan']],use_container_width=True)
                else:
                    st.write(f"Không có bình luận nào cho đánh giá {i} sao.")
    
        # Để giữ cho chiều cao cột cân bằng, tạo một dòng trống bằng cách sử dụng `st.empty()`.
        st.empty()  # Giữ không gian cho chiều cao bằng nhau
    else:
        st.write(f"Không có bình luận nào trong khoảng thời gian từ {start_period} đến {end_period}.")

#------------END_Hàm thống kế số lượng bình luận theo tháng-------------------------------

#------------START_Hàm thống kế số lượng bình luận theo giờ-------------------------------
def analyze_comments_by_hour(df, product_id):
    """Thống kê số lượng bình luận theo khung giờ trong ngày cho một sản phẩm."""
    
    # Chọn ra bình luận của sản phẩm cụ thể
    product_comments = df[df['ma_san_pham'] == product_id]
    
    # Chuyển đổi cột 'gio_binh_luan' sang kiểu datetime để lấy giờ
    product_comments['gio_binh_luan'] = product_comments['gio_binh_luan'].astype(str)
    product_comments['hour'] = pd.to_datetime(product_comments['gio_binh_luan'], format='%H:%M').dt.hour

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

# def plot_product_comments_wordcloud(df, product_id, stopwords=None):
#     """Vẽ Word Cloud cho bình luận của sản phẩm cụ thể với các tab riêng biệt cho từ tích cực và tiêu cực."""
    
#     # Lọc bình luận của sản phẩm cụ thể
#     product_comments = df[df['ma_san_pham'] == product_id]['noi_dung_binh_luan']

#     # Chuyển đổi bình luận thành chuỗi, loại bỏ NaN
#     product_comments = product_comments.dropna()  # Bỏ NaN

#     # Đảm bảo mỗi phần tử đều là kiểu str
#     product_comments = product_comments.astype(str).tolist()

#     # Kết hợp các bình luận thành một chuỗi
#     all_comments_text = " ".join(product_comments)

#     # Lấy các từ tích cực và tiêu cực từ file
#     try:
#         with open("positive_words_VN.txt", 'r', encoding='utf-8') as f:
#             positive_words = f.read().splitlines()
        
#         with open("negative_words_VN.txt", 'r', encoding='utf-8') as f:
#             negative_words = f.read().splitlines()
        
#         # Lấy stopwords nếu có
#         if stopwords is None:
#             stopwords = set()  # Khởi tạo với tập rỗng nếu không có stopwords
        
#         with open("vietnamese-stopwords.txt", 'r', encoding='utf-8') as f:
#             stopwords.update(f.read().splitlines())
    
#     except FileNotFoundError as e:
#         st.error(f"Không tìm thấy file: {e.filename}. Hãy kiểm tra đường dẫn!")
#         return

#     # Tạo slider cho số lượng từ hiển thị trong Word Cloud
#     num_words = st.slider("**Chọn số lượng từ hiển thị:**", min_value=1, max_value=100, value=10, key=f'wordcloud_slider_{product_id}')

#     # Tạo tabs cho wordcloud
#     tabs = st.tabs(["Từ Tích Cực", "Từ Tiêu Cực"])

#     # Tạo hàm để vẽ Word Cloud từ chuỗi văn bản
#     def create_wordcloud(text):
#         # Kiểm tra nếu văn bản không rỗng
#         if text:
#             wordcloud = WordCloud(width=800, height=400, 
#                                   background_color='white', 
#                                   stopwords=stopwords, 
#                                   max_words=num_words).generate(text)  # Số từ tối đa hiển thị
#             plt.figure(figsize=(10, 5))
#             plt.imshow(wordcloud, interpolation='bilinear')
#             plt.axis('off')
#             st.pyplot(plt)
#         else:
#             st.write("Không có dữ liệu để hiển thị Word Cloud.")

#     # Tạo Word Cloud cho từ tích cực trong tab Từ Tích Cực
#     with tabs[0]:
#         st.subheader("Word Cloud cho Từ Tích Cực")
#         positive_text = " ".join([word for word in all_comments_text.split() 
#                                    if word in positive_words and word not in stopwords])
#         create_wordcloud(positive_text)

#     # Tạo Word Cloud cho từ tiêu cực trong tab Từ Tiêu Cực
#     with tabs[1]:
#         st.subheader("Word Cloud cho Từ Tiêu Cực")
#         negative_text = " ".join([word for word in all_comments_text.split() 
#                                    if word in negative_words and word not in stopwords])
#         create_wordcloud(negative_text)


#####try 
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
            stopwords = set()  # Khởi tạo với tập rỗng nếu không có stopwords
        
        with open("vietnamese-stopwords.txt", 'r', encoding='utf-8') as f:
            stopwords.update(f.read().splitlines())
    
    except FileNotFoundError as e:
        st.error(f"Không tìm thấy file: {e.filename}. Hãy kiểm tra đường dẫn!")
        return

    # Tạo slider cho số lượng từ hiển thị trong Word Cloud
    num_words = st.slider("**Chọn số lượng từ hiển thị:**", min_value=1, max_value=100, value=10, key=f'wordcloud_slider_{product_id}')

    # Tạo tabs cho wordcloud
    tabs = st.tabs(["Từ Tích Cực", "Từ Tiêu Cực"])

    # Tạo hàm để vẽ Word Cloud từ chuỗi văn bản
    def create_wordcloud(text):
        # Kiểm tra nếu văn bản không rỗng
        if text:
            wordcloud = WordCloud(width=800, height=400, 
                                  background_color='white', 
                                  stopwords=stopwords, 
                                  max_words=num_words).generate(text)  # Số từ tối đa hiển thị
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)
        else:
            st.write("Không có dữ liệu để hiển thị Word Cloud.")

    # Tạo Word Cloud cho từ tích cực trong tab Từ Tích Cực
    with tabs[0]:
        st.subheader("Word Cloud cho Từ Tích Cực")
        positive_words_in_comments = []
        for comment in product_comments:
            words = comment.split()
            # Lấy các từ tích cực không nằm trong stopwords
            positive_words_in_comments.extend([word for word in words if word in positive_words and word not in stopwords])
        
        positive_text = " ".join(positive_words_in_comments)
        create_wordcloud(positive_text)

    # Tạo Word Cloud cho từ tiêu cực trong tab Từ Tiêu Cực
    with tabs[1]:
        st.subheader("Word Cloud cho Từ Tiêu Cực")
        negative_words_in_comments = []
        for comment in product_comments:
            words = comment.split()
            # Lấy các từ tiêu cực không nằm trong stopwords
            negative_words_in_comments.extend([word for word in words if word in negative_words and word not in stopwords])
        
        negative_text = " ".join(negative_words_in_comments)
        create_wordcloud(negative_text)

#------------END_Hàm vẽ wordcloud bình luận theo sản phẩm-------------------------------

# ------------START_Hàm chuyển đổi đơn vị tiền tệ VND--------------------
# Function to format numbers to Vietnamese currency
def format_currency(value):
    return f"{value:,.0f} VND"
# ------------END_Hàm chuyển đổi đơn vị tiền tệ VND--------------------


# Hàm để xác định giá trị của cột dong_san_pham
def assign_dong_san_pham(ten_san_pham):
    for product in dong_san_pham_list:
        if product in ten_san_pham:
            return product
    return 'Khac'


# Hàm để xác định giá trị của cột thuong_hieu
# Đọc danh sách thương hiệu từ file CSV
brand_df = pd.read_csv('Brand_lst.csv')
brands = brand_df['thuong_hieu'].tolist()
def assign_thuong_hieu(ten_san_pham):
    for brand in brands:
        if brand in ten_san_pham:
            return brand
    return 'Khac'

# ------------START_Hàm để thống kê số lượng đánh giá theo thương hiệu và loại đánh giá--------------------
def analyze_product_reviews(df, selected_brands, review_type):
    filtered_df = df[df['thuong_hieu'].isin(selected_brands)]
    review_counts = filtered_df[filtered_df['so_sao'] == review_type].groupby('thuong_hieu').size()
    return review_counts
# ------------END_Hàm để thống kê số lượng đánh giá theo thương hiệu và loại đánh giá--------------------

# ------------START_ Main Streamlit App--------------------
# Tạo giao diện tìm kiếm sản phẩm
st.title("Tìm Kiếm Sản Phẩm")

# Convert relevant columns to string, handling possible None values
df['ma_san_pham'] = df['ma_san_pham'].astype(str)
df['ten_san_pham'] = df['ten_san_pham'].astype(str)
danh_gia['ma_san_pham'] = danh_gia['ma_san_pham'].astype(str)

# Tạo hai tab: "Theo sản phẩm" và "Theo thương hiệu"
tabs = st.tabs(["Theo sản phẩm", "Theo từng thương hiệu", "Theo nhiều thương hiệu"])

# Tab 1: Theo sản phẩm
with tabs[0]:
    # Remove duplicates based on 'ma_san_pham'
    filtered_df = df.drop_duplicates(subset='ma_san_pham')

    # Display the filtered products in a dropdown
    if not filtered_df.empty:
        # Create a list of products with their codes for selection
        product_list = filtered_df.apply(lambda x: f"{x['ten_san_pham']} (Code: {x['ma_san_pham']})", axis=1).tolist()
        selected_product = st.selectbox("Vui lòng nhập tên sản phẩm, mã sản phẩm hoặc chọn 1 sản phẩm:", product_list, key='product_selection')
        
        # Extract the selected code from the product string
        selected_code = selected_product.split(" (Code: ")[-1].rstrip(")")
        selected_row = filtered_df[filtered_df['ma_san_pham'] == selected_code].iloc[0]

        # Display the selected product information
        st.write("Bạn đã chọn:", selected_product)
        st.write("Mã sản phẩm:", selected_code)


        # Use columns to display product description and image side by side
        col1, col2 = st.columns([2, 1.5])  # Adjust the weights as needed

        with col1:
            # Display product image
            # image_url = selected_row['hinh_anh']  # Ensure you have a column with image URLs
            image_url = 'https://media.hcdn.vn/catalog/product/p/r/promotions-auto-nuoc-hoa-hong-khong-mui-klairs-danh-cho-da-nhay-cam-180ml_mcaFpgMJ17XnfQwS.png'
            st.image(image_url, caption=selected_row['ten_san_pham'])

        with col2:
            # Display product description
            # Format and display product price and average rating
            formatted_price = format_currency(selected_row['gia_ban'])
            st.markdown(f"<h4>Giá bán: {formatted_price}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4>Điểm trung bình: {selected_row['diem_trung_binh']}</h4>", unsafe_allow_html=True)

        # Call the functions to analyze data based on the selected product
        # tabs = st.tabs(['Tháng', 'Giờ', 'WordCloud'])
        # with tabs[0]:
        analyze_comments_by_month(danh_gia, selected_code)
        # with tabs[1]:   
        analyze_comments_by_hour(danh_gia, selected_code)
        # plot_star_ratings(danh_gia, selected_code)
        # with tabs[2]:
        plot_product_comments_wordcloud(danh_gia, selected_code)

    else:
        st.write("Không tìm thấy sản phẩm.")

# Tab 2: Theo từng thương hiệu
with tabs[1]:
    # Đọc file brand_lst.csv
    brand_df = pd.read_csv('Brand_lst.csv')
    brands = brand_df['thuong_hieu'].tolist()

    # Dropdown cho lựa chọn thương hiệu
    selected_brand = st.selectbox("Vui lòng nhập hoặc chọn 1 thương hiệu:", brands, key='brand_selection')

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
            selected_product_brand = st.selectbox("Chọn sản phẩm để phân tích:", product_list_brands, key='product_brand_selection')
            selected_code_brand = selected_product_brand.split(" (Code: ")[-1].rstrip(")")

            st.write("Bạn đã chọn sản phẩm:", selected_product_brand)
            st.write("Mã sản phẩm:", selected_code_brand)

            # Gọi các hàm phân tích dựa trên mã sản phẩm đã chọn
            st.write("Thống kê số lượng bình luận:")
            tabs = st.tabs(["Tháng", "Giờ", "WordCloud"])
            with tabs[0]:
                analyze_comments_by_month(danh_gia, selected_code_brand)
            with tabs[1]:
                analyze_comments_by_hour(danh_gia, selected_code_brand)
            with tabs[2]:
                # plot_star_ratings(danh_gia, selected_code_brand)
                plot_product_comments_wordcloud(danh_gia, selected_code_brand)

                #################
                
                # def generate_wordcloud_and_top_words(text, stopwords=None, slider_key="slider"):
                #     """
                #     Tạo Word Cloud và trả về từ điển chứa các từ phổ biến nhất.
                #     """
                #     # Tính tần suất từ
                #     words = text.split()
                #     word_counts = Counter(words)

                #     # Loại bỏ stopwords (nếu có)
                #     if stopwords:
                #         word_counts = Counter({word: count for word, count in word_counts.items() if word not in stopwords})

                #     # Chỉ giữ lại các từ phổ biến nhất thông qua slider (thêm key để tránh lỗi)
                #     num_words = st.slider("Chọn số lượng từ phổ biến để hiển thị", min_value=5, max_value=50, value=10, step=1, key=slider_key)
                #     top_words = word_counts.most_common(num_words)
                #     top_words_dict = dict(top_words)

                #     # Trả về Word Cloud và danh sách top từ phổ biến
                #     wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(top_words_dict)
                #     return wordcloud, top_words


                # # POSITIVE
                # st.subheader("Word Cloud và Top Từ POSITIVE Phổ Biến")

                # try:
                #     with open("positive_words.txt", 'r', encoding='utf-8') as f:
                #         text_positive = f.read()
                # except FileNotFoundError:
                #     st.error("Không tìm thấy file 'positive_words.txt'.")

                # # Gọi hàm và chia tab
                # wordcloud_positive, top_words_positive = generate_wordcloud_and_top_words(text_positive, slider_key="slider_positive")
                # tab1_positive, tab2_positive = st.tabs(["Word Cloud POSITIVE", "Top Từ Phổ Biến POSITIVE"])

                # with tab1_positive:
                #     st.write("### Word Cloud POSITIVE")
                #     fig, ax = plt.subplots(figsize=(10, 5))
                #     ax.imshow(wordcloud_positive, interpolation='bilinear')
                #     ax.axis('off')
                #     st.pyplot(fig)

                # with tab2_positive:
                #     st.write("### Top Từ POSITIVE Phổ Biến")
                #     for word, count in top_words_positive:
                #         st.write(f"{word}: {count}")

                # # NEGATIVE
                # st.subheader("Word Cloud và Top Từ NEGATIVE Phổ Biến")

                # try:
                #     with open("negative_words_VN.txt", 'r', encoding='utf-8') as f:
                #         text_negative = f.read()
                # except FileNotFoundError:
                #     st.error("Không tìm thấy file 'negative_words_VN.txt'.")

                # # Gọi hàm và chia tab
                # wordcloud_negative, top_words_negative = generate_wordcloud_and_top_words(text_negative, slider_key="slider_negative")
                # tab1_negative, tab2_negative = st.tabs(["Word Cloud NEGATIVE", "Top Từ Phổ Biến NEGATIVE"])

                # with tab1_negative:
                #     st.write("### Word Cloud NEGATIVE")
                #     fig, ax = plt.subplots(figsize=(10, 5))
                #     ax.imshow(wordcloud_negative, interpolation='bilinear')
                #     ax.axis('off')
                #     st.pyplot(fig)

                # with tab2_negative:
                #     st.write("### Top Từ NEGATIVE Phổ Biến")
                #     for word, count in top_words_negative:
                #         st.write(f"{word}: {count}")

        else:
            st.write("Không tìm thấy sản phẩm cho thương hiệu này.")

# Tab 3: Theo nhiều thương hiệu
with tabs[2]:
    # Cấu hình Streamlit
    st.title('Thống kê Đánh giá Sản phẩm theo Thương hiệu')

    # Đọc danh sách dòng sản phẩm từ file
    with open("Dong_san_pham.txt", "r", encoding="utf-8") as file:
        dong_san_pham_list = [line.strip() for line in file.readlines()]

    # Tạo cột dong_san_pham với giá trị mặc định là "Khac"
    df['dong_san_pham'] = 'Khac'
    
    # Áp dụng hàm cho cột ten_san_pham
    df['dong_san_pham'] = df['ten_san_pham'].str.lower().apply(assign_dong_san_pham)

    # Tạo cột thuong_hieu với giá trị mặc định là "Khac"
    df['thuong_hieu'] = 'Khac'

    # Áp dụng hàm cho cột ten_san_pham
    df['thuong_hieu'] = df['ten_san_pham'].apply(assign_thuong_hieu)

    # Chọn dòng sản phẩm từ danh sách
    selected_dong_san_pham = st.multiselect('Chọn Dòng Sản Phẩm:', dong_san_pham_list)

    # Lọc DataFrame để lấy các thương hiệu có dòng sản phẩm đã chọn
    if selected_dong_san_pham:
        filtered_brands = df[df['dong_san_pham'].isin(selected_dong_san_pham)]['thuong_hieu'].unique().tolist()
    else:
        filtered_brands = []

    # Chọn thương hiệu từ danh sách đã lọc
    selected_brands = st.multiselect('Chọn Thương hiệu:', filtered_brands)

    # Chọn loại đánh giá
    review_types = df['so_sao'].unique()  # Giả sử bạn có cột loại đánh giá trong df
    selected_review_types = st.multiselect('Chọn Loại Đánh giá:', review_types)

    # Nút để thực hiện phân tích
    if st.button('Thống kê'):
        if selected_brands and selected_dong_san_pham:
            filtered_df = df[df['dong_san_pham'].isin(selected_dong_san_pham)]
            filtered_df = filtered_df[filtered_df['thuong_hieu'].isin(selected_brands)]

            # Loại bỏ giá trị NaN trong cột 'so_sao'
            filtered_df = filtered_df[filtered_df['so_sao'].notnull()]

            # Nhóm và đếm số lượng đánh giá cho mỗi thương hiệu theo loại đánh giá
            review_counts = filtered_df[filtered_df['so_sao'].isin(selected_review_types)].groupby(['thuong_hieu', 'so_sao']).size().unstack(fill_value=0)

            # Hiển thị kết quả
            if not review_counts.empty:
                st.write(f'Số lượng đánh giá cho các loại **{", ".join(map(str, selected_review_types))}**:')
                
                # Vẽ biểu đồ cột
                plt.figure(figsize=(10, 6))
                ax = review_counts.plot(kind='bar', width=0.8)

                # Thêm số lượng bình luận vào các thanh biểu đồ
                for container in ax.containers:
                    for bar in container:
                        height = bar.get_height()
                        ax.annotate(f'{height}', 
                                    xy=(bar.get_x() + bar.get_width() / 2, height), 
                                    xytext=(0, 3),  # 3 points vertical offset
                                    textcoords='offset points',
                                    ha='center', va='bottom')

                plt.title('Số lượng Đánh giá theo Thương hiệu và Loại Đánh giá')
                plt.xlabel('Thương hiệu')
                plt.ylabel('Số lượng Đánh giá')
                plt.xticks(rotation=45)
                plt.legend(title='Loại Đánh giá')
                st.pyplot(plt)  # Hiển thị biểu đồ trong Streamlit
            else:
                st.write('Không có dữ liệu đánh giá cho thương hiệu hoặc dòng sản phẩm đã chọn.')
        else:
            st.write('Vui lòng chọn ít nhất một thương hiệu và một dòng sản phẩm.')