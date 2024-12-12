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
stopwords_lst = file.read().split('\n')
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

#---START_Hàm thống kế số lượng bình luận theo tháng----------------------------------------
def analyze_comments_by_month(df, product_id):
    """Thống kê số lượng bình luận theo tháng cho một sản phẩm."""
    
    # Use boolean indexing once and store result
    product_comments = df.loc[df['ma_san_pham'] == product_id].copy()
    
    if product_comments.empty:
        st.write(f"Không có dữ liệu cho sản phẩm ID {product_id}")
        return
        
    # Convert date column once at the beginning
    product_comments['ngay_binh_luan'] = pd.to_datetime(product_comments['ngay_binh_luan'], format='%d/%m/%Y')
    product_comments['month'] = product_comments['ngay_binh_luan'].dt.to_period('M')

    # Calculate date range once
    min_month = product_comments['ngay_binh_luan'].min()
    max_month = product_comments['ngay_binh_luan'].max()
    
    # Date input controls
    st.write("**Chọn khoảng thời gian để xem bình luận:**")
    col1, col2 = st.columns(2)
    with col1:
        start_month = st.date_input('Tháng bắt đầu:', value=min_month, key=f'start_month_{product_id}')
    with col2:
        end_month = st.date_input('Tháng kết thúc:', value=max_month, key=f'end_month_{product_id}')
    
    # Convert to period once
    start_period = pd.to_datetime(start_month).to_period('M')
    end_period = pd.to_datetime(end_month).to_period('M')

    # Filter data
    mask = (product_comments['month'] >= start_period) & (product_comments['month'] <= end_period)
    filtered_comments = product_comments[mask]

    if filtered_comments.empty:
        st.write(f"Không có bình luận nào trong khoảng thời gian từ {start_period} đến {end_period}.")
        return

    # Monthly analysis
    display_monthly_analysis(filtered_comments, product_id, start_period, end_period)
    
    # Rating analysis
    display_rating_analysis(filtered_comments, start_month, end_month, product_id)

def display_monthly_analysis(filtered_comments, product_id, start_period, end_period):
    """Display monthly comment analysis."""
    monthly_counts = filtered_comments.groupby('month').size().reset_index(name='count')
    
    st.write(f"**II. Số lượng bình luận theo tháng từ {start_period} đến {end_period} cho sản phẩm ID '{product_id}':**")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(monthly_counts['month'].astype(str), monthly_counts['count'], color='skyblue')
    
    # Configure plot
    ax.set_xlabel('Tháng')
    ax.set_ylabel('Số lượng bình luận')
    ax.set_title(f"Số lượng bình luận theo tháng cho sản phẩm ID {product_id}")
    plt.xticks(rotation=45)
    ax.grid(axis='y')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    st.pyplot(fig)
    plt.close()

def display_rating_analysis(filtered_comments, start_month, end_month, product_id):
    """Display rating analysis."""
    total_comments = len(filtered_comments)
    st.write(f"**Tổng số bình luận có trong khoảng thời gian đã chọn: {total_comments} bình luận.**")
    
    # Rating statistics
    rating_counts = filtered_comments['so_sao'].value_counts()
    rating_counts = rating_counts.reindex(range(1, 6), fill_value=0).reset_index()
    rating_counts.columns = ['so_sao', 'count']
    
    st.write(f"**Thống kê bình luận theo đánh giá trong khoảng thời gian từ {start_month} đến {end_month}:**")
    
    # Display rating statistics
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(rating_counts)
    
    with col2:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.bar(rating_counts['so_sao'].astype(str), rating_counts['count'], color='green')
        ax.set_xlabel('Đánh giá')
        ax.set_ylabel('Số lượng bình luận')
        ax.set_title(f"Số lượng bình luận theo đánh giá\n{start_month} đến {end_month}")
        ax.set_xticks(range(1, 6))
        ax.grid(axis='y')
        st.pyplot(fig)
        plt.close()
    
    # Display detailed comments by rating
    display_rating_tabs(filtered_comments)

def display_rating_tabs(filtered_comments):
    """Display tabs with comments for each rating."""
    st.write("**Chi tiết bình luận theo đánh giá:**")
    tabs = st.tabs([f"Đánh giá {i}" for i in range(1, 6)])
    
    for i, tab in enumerate(tabs, 1):
        with tab:
            comments = filtered_comments[filtered_comments['so_sao'] == i]
            if not comments.empty:
                st.write(f"**Chi tiết bình luận cho đánh giá {i} sao:**")
                st.dataframe(
                    comments[['ngay_binh_luan', 'noi_dung_binh_luan']],
                    use_container_width=True
                )
            else:
                st.write(f"Không có bình luận nào cho đánh giá {i} sao.")

#----------------------------------------END_Hàm thống kế số lượng bình luận theo tháng---

#---START_Hàm thống kế số lượng bình luận theo giờ-------------------------------
def analyze_comments_by_hour(df, product_id):
    """
    Thống kê số lượng bình luận theo khung giờ trong ngày cho một sản phẩm.
    Args:
        df: DataFrame chứa dữ liệu bình luận
        product_id: ID của sản phẩm cần phân tích
    """
    # 1. Data Preprocessing Optimization
    product_comments = df[df['ma_san_pham'] == product_id].copy()  # Use copy() to avoid SettingWithCopyWarning
    if product_comments.empty:
        st.warning(f"Không có bình luận nào cho sản phẩm ID {product_id}")
        return

    # Optimize datetime conversion
    product_comments['hour'] = pd.to_datetime(
        product_comments['gio_binh_luan'].astype(str), 
        format='%H:%M'
    ).dt.hour

    # 2. Hour Range Selection
    hour_range = range(int(product_comments['hour'].min()), int(product_comments['hour'].max()) + 1)
    
    col1, col2 = st.columns(2)
    with col1:
        start_hour = st.selectbox(
            'Giờ bắt đầu:', 
            hour_range, 
            key=f'start_{product_id}'
        )
    with col2:
        end_hour = st.selectbox(
            'Giờ kết thúc:', 
            hour_range,
            index=len(hour_range)-1, 
            key=f'end_{product_id}'
        )

    # 3. Data Filtering
    mask = (product_comments['hour'] >= start_hour) & (product_comments['hour'] <= end_hour)
    filtered_comments = product_comments[mask]

    if filtered_comments.empty:
        st.warning(f"Không có bình luận nào trong khoảng thời gian từ {start_hour}:00 đến {end_hour}:00.")
        return

    # 4. Analysis Functions
    def plot_hourly_distribution(data):
        """Plot hourly comment distribution."""
        hourly_counts = data.groupby('hour').size().reset_index(name='count')
        
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(hourly_counts['hour'], hourly_counts['count'], color='skyblue')
        
        # Styling
        ax.set_xlabel('Khung giờ trong ngày')
        ax.set_ylabel('Số lượng bình luận')
        ax.set_title(f"Phân bố bình luận theo giờ - Sản phẩm ID {product_id}")
        ax.grid(axis='y', alpha=0.3)
        ax.set_xticks(hourly_counts['hour'])
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom')
        
        return fig

    def plot_rating_distribution(data):
        """Plot rating distribution."""
        rating_counts = data['so_sao'].value_counts().reindex(range(1, 6), fill_value=0)
        
        fig, ax = plt.subplots(figsize=(5, 5))
        bars = ax.bar(rating_counts.index.astype(str), rating_counts.values, color='green')
        
        # Styling
        ax.set_xlabel('Đánh giá')
        ax.set_ylabel('Số lượng bình luận')
        ax.set_title('Phân bố đánh giá')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom')
        
        return fig, rating_counts

    # 5. Visualization
    st.write(f"### Phân tích bình luận từ {start_hour}:00 đến {end_hour}:00")
    
    # Plot hourly distribution
    st.pyplot(plot_hourly_distribution(filtered_comments))
    
    # Show total comments
    st.metric("Tổng số bình luận", len(filtered_comments))
    
    # Rating analysis
    col1, col2 = st.columns([1, 2])
    fig_ratings, rating_counts = plot_rating_distribution(filtered_comments)
    
    with col1:
        st.write("#### Thống kê đánh giá")
        st.dataframe(
            rating_counts.reset_index()
            .rename(columns={'index': 'Số sao', 'so_sao': 'Số lượng'})
        )
    
    with col2:
        st.pyplot(fig_ratings)

    # 6. Detailed Comments View
    st.write("### Chi tiết bình luận theo đánh giá")
    tabs = st.tabs([f"{i} sao" for i in range(1, 6)])
    
    for i, tab in enumerate(tabs, 1):
        with tab:
            comments = filtered_comments[filtered_comments['so_sao'] == i]
            if not comments.empty:
                st.dataframe(
                    comments[['gio_binh_luan', 'noi_dung_binh_luan']]
                    .sort_values('gio_binh_luan'),
                    use_container_width=True
                )
            else:
                st.info(f"Không có bình luận {i} sao trong khoảng thời gian này")
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
            # st.write("Các cụm từ tích cực tìm thấy:", ', '.join(found_positive_phrases))
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
            # st.write("Các cụm từ tiêu cực tìm thấy:", ', '.join(found_negative_phrases))
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

# ------------START_ Main Streamlit App--------------------
# Tạo giao diện tìm kiếm sản phẩm
st.title("Tìm Kiếm Sản Phẩm")

# Convert relevant columns to string, handling possible None values
df['ma_san_pham'] = df['ma_san_pham'].astype(str)
df['ten_san_pham'] = df['ten_san_pham'].astype(str)
danh_gia['ma_san_pham'] = danh_gia['ma_san_pham'].astype(str)

# Tạo hai tab: "Theo sản phẩm" và "Theo thương hiệu"
main_tabs = st.tabs(["Theo sản phẩm", "Theo từng thương hiệu", "Theo nhiều thương hiệu"])

# Tab 1: Theo sản phẩm
with main_tabs[0]:
    # Remove duplicates based on 'ma_san_pham'
    filtered_df = df.drop_duplicates(subset='ma_san_pham')

    # Display the filtered products in a dropdown
    if not filtered_df.empty:
        # Create a list of products with their codes for selection
        product_list = filtered_df.apply(lambda x: f"{x['ten_san_pham']} (Code: {x['ma_san_pham']})", axis=1).tolist()

        # Dropdown cho lựa chọn sản phẩm
        product_list.insert(0, "Chọn sản phẩm")  # Thêm tùy chọn mặc định

        selected_product = st.selectbox("Vui lòng nhập tên sản phẩm, mã sản phẩm hoặc chọn 1 sản phẩm:", product_list, index=0, key='product_selection')
        
        if selected_product != "Chọn sản phẩm":  # Kiểm tra nếu không phải là tùy chọn mặc định
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
                image_url = selected_row['hinh_anh']
                st.image(image_url, caption=selected_row['ten_san_pham'])

            with col2:
                # Display product description
                # Format and display product price and average rating
                formatted_price = format_currency(selected_row['gia_ban'])
                st.markdown(f"<h4>Giá bán: {formatted_price}</h4>", unsafe_allow_html=True)
                st.markdown(f"<h4>Điểm trung bình: {selected_row['diem_trung_binh']}</h4>", unsafe_allow_html=True)
                st.page_link(page=selected_row['chi_tiet'],label='**Nhấn vào để xem chi tiết**')

            # Call the functions to analyze data based on the selected product
            sub1_tabs = st.tabs(['Tháng', 'Giờ', 'WordCloud'])
            with sub1_tabs[0]:
                analyze_comments_by_month(danh_gia, selected_code)
            with sub1_tabs[1]:   
                analyze_comments_by_hour(danh_gia, selected_code)
                # plot_star_ratings(danh_gia, selected_code)
            with sub1_tabs[2]:
                plot_product_comments_wordcloud(danh_gia, selected_code)

    else:
        st.write("Không tìm thấy sản phẩm.")

# Tab 2: Theo từng thương hiệu
with main_tabs[1]:    
    # Lấy danh sách thương hiệu từ DataFrame df    
    brands = df['thuong_hieu'].astype(str).unique().tolist()
    brands = sorted(set(brand for brand in brands if brand.lower() != 'nan'))  # Remove 'nan' and sort
    
    # Thêm tùy chọn "Chọn thương hiệu" vào đầu danh sách
    brands.insert(0, "Chọn thương hiệu") 
    
    # Dropdown cho lựa chọn thương hiệu
    selected_brand = st.selectbox("Vui lòng nhập hoặc chọn 1 thương hiệu:", brands, index=0, key='brand_selection')

    if selected_brand != "Chọn thương hiệu":
        # Lọc DataFrame sản phẩm theo thương hiệu đã chọn
        filtered_brand_df = df[df['thuong_hieu'].str.contains(selected_brand, case=False, na=False)].drop_duplicates(subset='ma_san_pham')

        if not filtered_brand_df.empty:
            # Tạo danh sách sản phẩm
            product_list_brands = filtered_brand_df.apply(lambda x: f"{x['ten_san_pham']} (Code: {x['ma_san_pham']})", axis=1).tolist()

            dis_tabs = st.tabs(['Tổng sản phẩm','Dòng sản phẩm'])

            with dis_tabs[0]:  # 'Tổng sản phẩm'
                # Hiển thị tổng số lượng sản phẩm
                product_count = filtered_brand_df.shape[0]
                st.write(f"Có {product_count} sản phẩm của thương hiệu {selected_brand}.")

                # Trực quan hóa số lượng đánh giá theo số sao
                rating_counts = filtered_brand_df[['ma_san_pham', 'ten_san_pham']].copy()
                rating_counts['ma_san_pham'] = rating_counts['ma_san_pham'].astype(str)

                # Tính số lượng đánh giá cho từng sản phẩm
                rating_summary = danh_gia.groupby('ma_san_pham')['so_sao'].value_counts().unstack(fill_value=0)
                rating_summary['tong_danh_gia'] = rating_summary.sum(axis=1)
                rating_counts = rating_counts.merge(rating_summary[['tong_danh_gia']], on='ma_san_pham', how='left')

                # Vẽ biểu đồ
                fig, ax = plt.subplots(figsize=(10, 5))
                bars = ax.barh(rating_counts['ten_san_pham'], rating_counts['tong_danh_gia'], color='skyblue')
                ax.set_xlabel('Số lượng đánh giá')
                ax.set_title(f'Số lượng đánh giá theo sản phẩm của thương hiệu {selected_brand}')
                for bar in bars:
                    ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va='center')
                plt.tight_layout()
                st.pyplot(fig)

                # Phân tích cho từng sản phẩm
                selected_product_brand = st.selectbox("Chọn sản phẩm để phân tích:", product_list_brands, key='product_brand_selection')
                selected_code_brand = selected_product_brand.split(" (Code: ")[-1].rstrip(")")
                selected_row_2 = filtered_brand_df[filtered_brand_df['ma_san_pham'] == selected_code_brand].iloc[0]

                st.write("Bạn đã chọn sản phẩm:", selected_product_brand)
                st.write("Mã sản phẩm:", selected_code_brand)

                # Hiển thị hình ảnh và mô tả sản phẩm
                subcol1, subcol2 = st.columns([2, 1.5])  # Adjust proportions

                with subcol1:
                    st.image(selected_row_2['hinh_anh'], caption=selected_row_2['ten_san_pham'])
                with subcol2:
                    st.markdown(f"<h4>Giá bán: {format_currency(selected_row_2['gia_ban'])}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<h4>Điểm trung bình: {selected_row_2['diem_trung_binh']}</h4>", unsafe_allow_html=True)
                    st.page_link(page=selected_row_2['chi_tiet'], label='**Nhấn vào để xem chi tiết**')

                # Thống kê bình luận
                st.write("Thống kê số lượng bình luận:")
                sub2_tabs = st.tabs(["Tháng", "Giờ", "WordCloud"])
                with sub2_tabs[0]:
                    analyze_comments_by_month(danh_gia, selected_code_brand)
                with sub2_tabs[1]:
                    analyze_comments_by_hour(danh_gia, selected_code_brand)
                with sub2_tabs[2]:
                    plot_product_comments_wordcloud(danh_gia, selected_code_brand)

            with dis_tabs[1]:  # 'Dòng sản phẩm'
                # Đếm số lượng sản phẩm theo từng dòng sản phẩm
                product_line_counts = filtered_brand_df['dong_san_pham'].value_counts()
                total_product_lines = product_line_counts.count()  
                st.write(f"Tổng số dòng sản phẩm của thương hiệu {selected_brand}: {total_product_lines}")

                # Tạo tabs cho các phân mục
                dong_tabs = st.tabs(['Sản phẩm', 'Bình luận', 'Đánh giá'])

                with dong_tabs[0]:  # 'Sản phẩm'                   
                    product_line_df = pd.DataFrame({
                        'Dòng sản phẩm': product_line_counts.index,
                        'Số lượng sản phẩm': product_line_counts.values
                    })

                    # Vẽ biểu đồ phân bố số lượng sản phẩm theo dòng
                    fig = px.bar(product_line_df, x='Số lượng sản phẩm', y='Dòng sản phẩm',
                                 orientation='h', text='Số lượng sản phẩm',
                                 title=f'Phân bố số lượng sản phẩm theo dòng - {selected_brand}')
                    fig.update_traces(textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)

                    # Dropdown để chọn dòng sản phẩm
                    product_lines = sorted(filtered_brand_df['dong_san_pham'].unique().tolist())
                    selected_product_line = st.selectbox("Chọn dòng sản phẩm để xem chi tiết:", ["Chọn dòng sản phẩm"] + product_lines, key='product_line_selection')

                    if selected_product_line != "Chọn dòng sản phẩm":
                        product_line_df = filtered_brand_df[filtered_brand_df['dong_san_pham'] == selected_product_line]
                        st.write(f"Có {len(product_line_df)} sản phẩm trong dòng {selected_product_line}")
                        
                        cols = st.columns(3)
                        for idx, row in enumerate(product_line_df.itertuples()):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                st.write(f"**{row.ten_san_pham}**")
                                st.write(f"Mã SP: {row.ma_san_pham}")
                                if hasattr(row, 'hinh_anh') and pd.notna(row.hinh_anh):
                                    st.image(row.hinh_anh, caption=row.ten_san_pham, use_container_width=True)
                                st.write("---")  # Separator

                with dong_tabs[1]:
                    product_comments = pd.merge(
                        filtered_brand_df[['ma_san_pham', 'dong_san_pham']],
                        danh_gia[['ma_san_pham', 'noi_dung_binh_luan', 'phan_loai_danh_gia']], 
                        on='ma_san_pham', how='left'
                    )
                    comments_by_line = product_comments.groupby('dong_san_pham')['noi_dung_binh_luan'].count().reset_index()
                    comments_by_line.columns = ['Dòng sản phẩm', 'Số lượng bình luận']
                    
                    # Vẽ biểu đồ phân bố số lượng bình luận
                    fig1 = px.bar(comments_by_line, x='Dòng sản phẩm', y='Số lượng bình luận',
                                   text='Số lượng bình luận', title=f'Phân bố số lượng bình luận theo dòng sản phẩm - {selected_brand}')
                    fig1.update_traces(textposition='outside')
                    st.plotly_chart(fig1, use_container_width=True)

                    # Tính số lượng bình luận positive và negative theo từng dòng sản phẩm
                    sentiment_by_line = product_comments.groupby(['dong_san_pham', 'phan_loai_danh_gia']).size().unstack(fill_value=0)
                    st.write("Số lượng bình luận theo sentiment cho từng dòng sản phẩm:")
                    st.dataframe(sentiment_by_line)

                    if not sentiment_by_line.empty:
                        for dong_sp, row in sentiment_by_line.iterrows():
                            col = st.columns(2)  # Limiting to 2 per row
                            with col[0]:
                                fig = px.pie(values=row.values, names=row.index,
                                             title=f'Phân bố bình luận - {dong_sp}',
                                             color_discrete_map={'positive': '#2ECC71', 'negative': '#E74C3C'})
                                st.plotly_chart(fig)
                                st.write(f"Tích cực: {row.get('positive', 0)}")
                                st.write(f"Tiêu cực: {row.get('negative', 0)}")

                with dong_tabs[2]:  # 'Đánh giá'
                    rating_counts = (
                        pd.merge(
                            filtered_brand_df[['ma_san_pham', 'dong_san_pham']], 
                            danh_gia[['ma_san_pham', 'so_sao']], 
                            on='ma_san_pham', how='left'
                        )
                        .groupby(['dong_san_pham', 'so_sao'])
                        .size()
                        .unstack(fill_value=0)
                    )

                    st.write("Số lượng các loại so_sao theo từng dòng sản phẩm:")
                    st.dataframe(rating_counts)

                    rating_counts_long = rating_counts.reset_index().melt(id_vars='dong_san_pham', var_name='Loại so_sao', value_name='Số lượng')

                    # Vẽ biểu đồ cột cho số lượng từng loại so_sao theo từng dòng sản phẩm
                    fig_bar = px.bar(rating_counts_long, x='dong_san_pham', y='Số lượng', 
                                     color='Loại so_sao', title=f'Số lượng từng loại so_sao theo từng dòng sản phẩm - {selected_brand}',
                                     labels={'Số lượng': 'Số lượng', 'dong_san_pham': 'Dòng sản phẩm'}, barmode='group')
                    st.plotly_chart(fig_bar, use_container_width=True)

                    # Vẽ biểu đồ tròn tỷ lệ phần trăm giữa các loại so_sao
                    if not rating_counts.empty:
                        for dong_sp in rating_counts.index:
                            row = rating_counts.loc[dong_sp]
                            fig = px.pie(values=row.values, names=row.index,
                                         title=f'Tỷ lệ phần trăm các loại so_sao - {dong_sp}')
                            st.plotly_chart(fig)
                            st.write("Tổng số lượng so_sao:", row.sum())
                    else:
                        st.write("Không có dữ liệu để hiển thị.")
        else:
            st.write("Không tìm thấy sản phẩm cho thương hiệu này.")


# Tab 3: Theo nhiều thương hiệu
with main_tabs[2]:
    # Cấu hình Streamlit
    st.title('Thống kê Đánh giá Sản phẩm theo Thương hiệu')

    # Lấy danh sách các dòng sản phẩm duy nhất từ cột 'dong_san_pham'
    dong_san_pham_list = df['dong_san_pham'].unique().tolist()

    # Chọn dòng sản phẩm từ danh sách
    selected_dong_san_pham = st.multiselect('Chọn Dòng Sản Phẩm:', dong_san_pham_list)

    # Lọc thương hiệu theo dòng sản phẩm đã chọn
    filtered_brands = df[df['dong_san_pham'].isin(selected_dong_san_pham)]['thuong_hieu'].unique().tolist() if selected_dong_san_pham else []

    # Chọn thương hiệu từ danh sách đã lọc
    selected_brands = st.multiselect('Chọn Thương hiệu:', filtered_brands)

    # Chọn loại đánh giá
    selected_review_types = st.multiselect('Chọn Loại Đánh giá:', df['so_sao'].unique())

    # Chuyển đổi ngày bình luận và tạo cột tháng
    df['ngay_binh_luan'] = pd.to_datetime(df['ngay_binh_luan'], format='%d/%m/%Y', errors='coerce').dropna()
    df['month'] = df['ngay_binh_luan'].dt.to_period('M')

    # Thiết lập tháng bắt đầu và tháng kết thúc
    min_month, max_month = df['month'].min().to_timestamp(), df['month'].max().to_timestamp()
    # Tạo hai cột cho ô nhập tháng bắt đầu và tháng kết thúc
    col1, col2 = st.columns(2)
    with col1:
        start_month = st.date_input('Tháng bắt đầu:', value=min_month, key='start_month')

    with col2:
        end_month = st.date_input('Tháng kết thúc:', value=max_month, key='end_month')

    # Xử lý giờ
    df['hour'] = pd.to_datetime(df['gio_binh_luan'].astype(str), format='%H:%M').dt.hour
    min_hour, max_hour = df['hour'].min(), df['hour'].max()
    # Tạo hai cột cho ô nhập giờ bắt đầu và giờ kết thúc
    col3, col4 = st.columns(2)
    with col3:
        start_hour = st.number_input('Giờ bắt đầu:', min_value=min_hour, max_value=max_hour, value=min_hour, key='start_hour_input')
    with col4:
        end_hour = st.number_input('Giờ kết thúc:', min_value=start_hour, max_value=max_hour, value=max_hour, key='end_hour_input')

    # Nút để thực hiện phân tích
    if st.button('Thống kê'):
        if selected_brands and selected_dong_san_pham:
            # Lọc dữ liệu
            filtered_df = df[df['dong_san_pham'].isin(selected_dong_san_pham) & 
                            df['thuong_hieu'].isin(selected_brands) & 
                            df['so_sao'].notnull()]

            # Lọc dữ liệu theo khoảng thời gian
            start_period = pd.to_datetime(start_month).to_period('M')
            end_period = pd.to_datetime(end_month).to_period('M')
            filtered_df = filtered_df[(filtered_df['month'] >= start_period) & 
                                    (filtered_df['month'] <= end_period) & 
                                    (filtered_df['hour'] >= start_hour) & 
                                    (filtered_df['hour'] <= end_hour)]

            # Nhóm và đếm số lượng đánh giá cho từng loại đánh giá
            review_counts = filtered_df[filtered_df['so_sao'].isin(selected_review_types)].groupby(['thuong_hieu', 'so_sao']).size().unstack(fill_value=0)

            # Hiển thị kết quả
            if not review_counts.empty:
                st.write(f'Số lượng đánh giá cho các loại **{", ".join(map(str, selected_review_types))}**:')
                
                # Vẽ biểu đồ cột
                plt.figure(figsize=(10, 6))
                ax = review_counts.plot(kind='bar', width=0.8)
                for container in ax.containers:
                    for bar in container:
                        height = bar.get_height()
                        ax.annotate(f'{height}', 
                                    xy=(bar.get_x() + bar.get_width() / 2, height), 
                                    xytext=(0, 3),  
                                    textcoords='offset points',
                                    ha='center', va='bottom')

                plt.title('Số lượng Đánh giá theo Thương hiệu và Loại Đánh giá')
                plt.xlabel('Thương hiệu')
                plt.ylabel('Số lượng Đánh giá')
                plt.xticks(rotation=45)
                plt.legend(title='Loại Đánh giá')
                st.pyplot(plt)  
                        
                # Tạo tabs cho biểu đồ tròn đã được sắp xếp
                valid_review_types = sorted([rt for rt in selected_review_types if rt in review_counts.columns])
                if valid_review_types:
                    pie_tabs = st.tabs([f"{rt} sao" for rt in valid_review_types])
                    for i, review_type in enumerate(valid_review_types):
                        with pie_tabs[i]:
                            pie_data = review_counts[review_type]
                            fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
                            pie_data.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax_pie)
                            ax_pie.set_title(f'Tỷ lệ đánh giá {review_type} sao giữa các thương hiệu')
                            ax_pie.set_ylabel('')
                            st.pyplot(fig_pie)
                else:
                    st.warning("Không có loại đánh giá nào đáng để hiển thị.")
            else:    
                st.warning("Vui lòng chọn ít nhất một thương hiệu và một dòng sản phẩm.")
        else:
            st.write('Vui lòng chọn ít nhất một thương hiệu và một dòng sản phẩm.')