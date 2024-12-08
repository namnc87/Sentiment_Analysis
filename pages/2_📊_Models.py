import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

################################
st.set_page_config(page_title="Models Analysis", page_icon="📈")

st.sidebar.success("Giáo Viên Hướng Dẫn: \n # KHUẤT THUỲ PHƯƠNG")
st.sidebar.success("Học Viên:\n # NGUYỄN CHẤN NAM \n # CHẾ THỊ ANH TUYỀN")
st.sidebar.success("Ngày báo cáo: \n # 16/12/2024")

################################ MODEL COMPARISION

# Đọc dữ liệu từ file JSON
output_file = 'model_results.json'

try:
    with open(output_file, 'r') as json_file:
        results = json.load(json_file)

    # Tạo một danh sách để lưu các thông tin cho từng mô hình
    model_comparison_data = []

    # Vòng lặp truy xuất các kết quả của từng mô hình
    for model_name, model_info in results.items():
        # Truy xuất các thông tin về mô hình
        time_taken = model_info.get('Time taken', 'N/A')
        best_score = model_info.get('Best score', 'N/A')
        accuracy = model_info.get('Accuracy', 'N/A')
        f1_score = model_info.get('F1 Score', 'N/A')
        auc = model_info.get('ROC Curve', {}).get('auc', 'N/A')

        # Kiểm tra và format các giá trị nếu không phải là 'N/A'
        time_taken_display = f"{time_taken:.4f}" if time_taken != 'N/A' and time_taken is not None else "N/A"
        best_score_display = f"{best_score:.4f}" if best_score != 'N/A' and best_score is not None else "N/A"
        accuracy_display = f"{accuracy:.4f}" if accuracy != 'N/A' and accuracy is not None else "N/A"
        f1_score_display = f"{f1_score:.4f}" if f1_score != 'N/A' and f1_score is not None else "N/A"
        auc_display = f"{auc:.4f}" if auc != 'N/A' and auc is not None else "N/A"

        # Lưu thông tin mô hình vào danh sách
        model_comparison_data.append({
            'Model': model_name,
            'Time taken (s)': time_taken_display,
            'Best Score': best_score_display,
            'Accuracy': accuracy_display,
            'F1 Score': f1_score_display,
            'AUC': auc_display
        })
    
    # Tạo DataFrame từ danh sách model_comparison_data
    comparison_df = pd.DataFrame(model_comparison_data)

    # Hiển thị bảng so sánh các mô hình
    st.title("📊 Model Comparison")
    st.dataframe(comparison_df)

    # Tạo tab để hiển thị thông tin chi tiết cho từng mô hình
    tabs = st.tabs([model_name for model_name in results.keys()])

    for idx, (model_name, model_info) in enumerate(results.items()):
        with tabs[idx]:
            # st.subheader(f"Model: {model_name}")

            # Hiển thị Classification Report
            st.markdown("#### Classification Report")
            st.text(model_info.get('Classification Report', 'N/A'))

            # Hiển thị Confusion Matrix
            cm = model_info.get('Confusion Matrix', [])
            if cm:
                st.markdown("#### Confusion Matrix")
                st.write(cm)

except FileNotFoundError:
    st.error(f"Không tìm thấy file '{output_file}'. Vui lòng kiểm tra lại đường dẫn file.")
except Exception as e:
    st.error(f"Đã xảy ra lỗi khi đọc file JSON: {e}")


######## VẼ ROC CUVER
try:
    with open(output_file, 'r') as json_file:
        results = json.load(json_file)

    # Tạo tab cho các ROC Curve
    st.subheader("ROC Curve for Models")
    fig, ax = plt.subplots(figsize=(10, 6))

    for model_name, model_info in results.items():
        # Lấy thông tin fpr, tpr và auc
        roc_data = model_info.get('ROC Curve', {})
        fpr = roc_data.get('fpr', [])
        tpr = roc_data.get('tpr', [])
        auc = roc_data.get('auc', None)

        # Nếu đủ thông tin, vẽ đường ROC cho model
        if fpr and tpr and auc is not None:
            ax.plot(fpr, tpr, lw=2, label=f"{model_name} (AUC = {auc:.2f})")

    # Vẽ đường chéo (random classifier)
    ax.plot([0, 1], [0, 1], color='gray', linestyle='--', lw=1)

    # Thêm thông tin cho biểu đồ
    ax.set_title("ROC Curve for Models", fontsize=16)
    ax.set_xlabel("False Positive Rate", fontsize=12)
    ax.set_ylabel("True Positive Rate", fontsize=12)
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(True)

    # Hiển thị biểu đồ trong Streamlit
    st.pyplot(fig)

except FileNotFoundError:
    st.error(f"Không tìm thấy file '{output_file}'. Vui lòng kiểm tra lại đường dẫn file.")
except Exception as e:
    st.error(f"Đã xảy ra lỗi khi đọc file JSON hoặc vẽ ROC Curve: {e}")

st.markdown("## Dựa số liệu ở trên, chọn model SVM")