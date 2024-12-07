import streamlit as st

st.set_page_config(
    page_title="PROJECT_1",
    page_icon="favicon.png",
)
# Đặt hình ảnh header
st.image("banner.jpg", caption="Header Image", use_column_width=True)

st.write("# Welcome to PROJECT 1 👋")

st.sidebar.success("Giáo Viên Hướng Dẫn: \n # KHUẤT THUỲ PHƯƠNG")
st.sidebar.success("Học Viên:\n # NGUYỄN CHẤN NAM \n # CHẾ THỊ ANH TUYỀN")
st.sidebar.success("Ngày báo cáo: \n # 16/12/2024")


st.markdown(
    """
    ### *SUBJECT:*
    # HASAKI.VN - SENTIMENT ANALYSIS 
    ### Business Objective/Problem
    #### * “HASAKI.VN là hệ thống cửa hàng mỹ phẩm chính hãng và dịch vụ chăm sóc sắc đẹp chuyên sâu với hệ thống cửa hàng trải dài trên toàn quốc và hiện đang là đối tác phân phối chiến lược tại thị trường Việt Nam của hàng loạt thương hiệu lớn...
        
    #### * Khách hàng có thể lên đây để lựa chọn sản phẩm,xem các đánh giá/ nhận xét cũng như đặt mua sản phẩm.

    #### Target: 

    ### Danh mục các việc cần thực hiện:
"""
)

# Tạo hyperlink thủ công
st.markdown("##### [- Data Exploration 🔍](pages/1_🔍_Data_Exploration.py)", unsafe_allow_html=True)
st.markdown("##### [- Models 🔍](pages/2_📊_Models.py)", unsafe_allow_html=True)
st.markdown("##### [- New Predict 🔍](pages/3_🎯_New_Predict.py)", unsafe_allow_html=True)
st.markdown("##### [- Login 🔍](pages/4_🔑_Login.py)", unsafe_allow_html=True)



