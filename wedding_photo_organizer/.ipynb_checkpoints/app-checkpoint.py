import streamlit as st
import os
import shutil
import tempfile
from utils.face_utils import load_and_process_images

st.set_page_config(page_title="Wedding Photo Sorter", layout="wide")
st.title("👰 Wedding Photo Face Sorter")
st.markdown("Upload photos from a wedding, and this tool will automatically group similar faces.")

# Upload section
uploaded_files = st.file_uploader("Upload wedding photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = os.path.join(temp_dir, "input")
        os.makedirs(input_dir, exist_ok=True)

        # Save uploaded files
        for file in uploaded_files:
            file_path = os.path.join(input_dir, file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())

        st.success(f"✅ {len(uploaded_files)} photos uploaded.")

        if st.button("📂 Group Faces"):
            with st.spinner("Analyzing and grouping faces..."):
                load_and_process_images(input_dir, threshold=0.5)

            st.success("✅ Grouping complete!")

            # Display grouped output
            output_dir = "output/grouped_faces"
            if os.path.exists(output_dir):
                st.subheader("📸 Grouped People:")
                for person_folder in sorted(os.listdir(output_dir)):
                    st.markdown(f"### 👤 {person_folder}")
                    person_path = os.path.join(output_dir, person_folder)
                    images = os.listdir(person_path)
                    cols = st.columns(4)
                    for idx, img in enumerate(images):
                        img_path = os.path.join(person_path, img)
                        with open(img_path, "rb") as file:
                            cols[idx % 4].image(file.read(), use_column_width=True)
