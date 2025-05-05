import streamlit as st
import subprocess
import tempfile
import shutil
import os

st.title("PDF Metadata Cleaner")
st.markdown("Upload a PDF and this app will remove the Creator and Producer metadata using exiftool.")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file to a temporary file
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, uploaded_file.name)
        output_path = input_path  # exiftool modifies the file in-place if -overwrite_original is used

        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        # Run exiftool to strip Creator and Producer
        result = subprocess.run([
            "exiftool",
            "-Creator=",
            "-Producer=",
            "-overwrite_original",
            input_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            # Read cleaned file
            with open(output_path, "rb") as f:
                cleaned_data = f.read()

            st.success("Metadata cleaned successfully.")
            st.download_button(
                label="Download Cleaned PDF",
                data=cleaned_data,
                file_name=uploaded_file.name,
                mime="application/pdf"
            )
        else:
            st.error("Failed to clean PDF metadata.")
            st.text(result.stderr.decode())
