import streamlit as st
from PIL import Image
import os

# ===== Page config =====

st.set_page_config(
    page_title="Happy Birthday 🎂",
    layout="wide"
)

# ===== Load hearts animation =====

with open("hearts.html", "r", encoding="utf-8") as f:
    hearts_html = f.read()

st.components.v1.html(
    hearts_html,
    height=0,
    scrolling=False
)

# ===== Title =====

st.markdown(
    """
    <h1 style='text-align:center;
               color:#ff4b6e;
               font-size:60px;'>
        🎂 Happy Birthday 🎂
    </h1>
    """,
    unsafe_allow_html=True
)

# ===== Message =====

st.markdown(
    """
    <h3 style='text-align:center; color:#ffffff;'>
    Chúc mừng sinh nhật!  
    Chúc bạn luôn vui vẻ, hạnh phúc  
    và đạt được mọi điều mong muốn 💖
    </h3>
    """,
    unsafe_allow_html=True
)

# ===== Load Images =====

image_folder = "images"

if os.path.exists(image_folder):

    files = os.listdir(image_folder)

    image_files = [
        f for f in files
        if f.endswith(("png", "jpg", "jpeg"))
    ]

    if image_files:

        st.markdown("## 📸 Kỷ niệm")

        cols = st.columns(3)

        for i, img_file in enumerate(image_files):

            img_path = os.path.join(
                image_folder,
                img_file
            )

            image = Image.open(img_path)

            cols[i % 3].image(
                image,
                use_container_width=True
            )

    else:

        st.warning(
            "Chưa có ảnh trong folder images"
        )

else:

    st.error(
        "Không tìm thấy folder images"
    )