import pickle
import streamlit as st

st.set_page_config(page_title="Predict New", page_icon="🎯")

st.sidebar.success("Giáo Viên Hướng Dẫn: \n # KHUẤT THUỲ PHƯƠNG")
st.sidebar.success("Học Viên:\n # NGUYỄN CHẤN NAM \n # CHẾ THỊ ANH TUYỀN")
st.sidebar.success("Ngày báo cáo: \n # 16/12/2024")


# Hàm dự đoán giá trị mới cho các bình luận
def predict_new_data(model, new_texts, vectorizer):
    # Chuyển đổi văn bản mới thành vector sử dụng vectorizer đã huấn luyện
    new_texts_transformed = vectorizer.transform(new_texts)
    
    # Dự đoán kết quả với mô hình đã huấn luyện
    predictions = model.predict(new_texts_transformed)
    
    return predictions

# Tải mô hình và vectorizer từ các file pickle
model_filename = 'svm_model.pkl'  # Đảm bảo rằng file mô hình SVM của bạn ở đây
vectorizer_filename = 'svm_vectorizer.pkl'  # Đảm bảo rằng file vectorizer của bạn ở đây

# Ứng dụng Streamlit
st.title("🔮 Sentiment Prediction")
st.write("Dự đoán cảm xúc (tích cực/tiêu cực) của bình luận dựa trên mô hình học máy.")

try:
    # Tải mô hình SVM từ file
    with open(model_filename, 'rb') as f:
        model = pickle.load(f)
    
    # Tải vectorizer từ file
    with open(vectorizer_filename, 'rb') as f:
        vectorizer = pickle.load(f)
    
    # Nhập dữ liệu bình luận từ người dùng
    st.subheader("📝 Nhập các bình luận để dự đoán:")

#-----------
    # Nội dung text
    comments = [
        "Đã mua đủ màu, rồi đổi sp khác nhưng vẫn phải quay lại với màu Hồng, dùng màu Hồng đi mn ơi, rất mềm mịn da, dùng 2-3 ngày thấy ngay khác biệt",
        "Da em là da hỗn hợp thiên dầu, rất rất nhạy cảm và đang kích ứng rất nặng, nhưng mà dùng xong em sữa rửa mặt này là cảm giác mê luôn. Rửa xong mềm da, không hề khô, không ngứa, không đỏ ửng mụn",
        "2 chai trước nghe mùi tràm trà giống nhau. Chai này mua bên Hasaki thấy mùi hôi kinh khủng khác mùi hoàn toàn so với chai trước dùng"
        ]
    # Hiển thị tiêu đề
    st.write("📜 Nội dung bình luận mẫu")

    # Hiển thị từng bình luận
    for i, comment in enumerate(comments, start=1):
        st.markdown(f"**Bình luận {i}:** \n {comment}")
#-----------
    new_text = st.text_area("Nhập bình luận, mỗi bình luận trên một dòng:")

    if st.button("🎯 Dự đoán"):
        if new_text.strip():
            # Chuyển đổi bình luận thành danh sách
            comments = new_text.splitlines()
            
            # Dự đoán cho các bình luận mới
            predictions = predict_new_data(model, comments, vectorizer)

            # Hiển thị kết quả dự đoán
            st.subheader("🔍 Kết quả Dự đoán:")
            results = []
            for text, prediction in zip(comments, predictions):
                sentiment = 'positive' if prediction == 1 else 'negative'
                results.append({"Bình luận": text, "Cảm xúc": sentiment})

            # Hiển thị kết quả dưới dạng bảng
            st.table(results)
        else:
            st.warning("Vui lòng nhập bình luận để dự đoán!")
            
except FileNotFoundError:
    st.error(f"Không tìm thấy file '{model_filename}' hoặc '{vectorizer_filename}'. Vui lòng kiểm tra lại đường dẫn file.")
except Exception as e:
    st.error(f"Đã xảy ra lỗi khi tải mô hình hoặc vectorizer: {e}")


