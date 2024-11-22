import streamlit as st
from PIL import Image
import numpy as np
import zlib

# Page configuration
st.set_page_config(
    page_title="File to RGB Image Converter",
    page_icon="🖼️",
    initial_sidebar_state="expanded"
)

# Custom Styles
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to bottom right, #0f172a, #000000);
            color: white;
        }
        div.stDownloadButton > button {
            color: black !important;
            background-color: #1f2937 !important;
            border: none !important;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        h1, h2, h3, p, label {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Compression utilities
def compress_data(data):
    """Compress data using zlib."""
    return zlib.compress(data)

def decompress_data(data):
    """Decompress data using zlib."""
    return zlib.decompress(data)

# File to RGB image conversion
def file_to_rgb_image(file_path, output_image_path, compress=False):
    with open(file_path, "rb") as f:
        data = f.read()

    if compress:
        data = compress_data(data)

    metadata = f"rgb,{'1' if compress else '0'}".encode("utf-8").ljust(24, b'\x00')
    data_with_metadata = metadata + data

    pixel_count = -(-len(data_with_metadata) // 3)
    image_size = int(np.ceil(np.sqrt(pixel_count)))

    image_data = np.zeros((image_size, image_size, 3), dtype=np.uint8)
    flat_data = np.frombuffer(data_with_metadata, dtype=np.uint8)

    image_data.flat[:len(flat_data)] = flat_data

    image = Image.fromarray(image_data)
    image.save(output_image_path)
    return image

# RGB image to file reconstruction
def rgb_image_to_file(image_path, output_file_path):
    img = Image.open(image_path)
    img_data = np.array(img).flatten()

    metadata = bytes(img_data[:24]).decode("utf-8").rstrip("\x00")
    if not metadata.startswith("rgb"):
        raise ValueError("Invalid metadata in the image file.")

    compress = metadata.split(",")[1] == "1"

    with open(output_file_path, "wb") as f:
        data = img_data[24:]
        if compress:
            data = decompress_data(data.tobytes())
        f.write(data)

# Streamlit interface
st.title("File to RGB Image Converter with Compression")
st.write("Upload a file to encode it into an RGB image or upload an RGB image to reconstruct the original file.")

# Convert file to RGB image
uploaded_file = st.file_uploader("Upload a file", type=["txt", "java", "py", "json", "csv", "md"])
if uploaded_file:
    temp_file_path = "uploaded_file"
    output_image_path = "output_rgb_image.png"

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())

    compress = st.checkbox("Compress file before encoding?", value=False)
    rgb_image = file_to_rgb_image(temp_file_path, output_image_path, compress=compress)
    st.image(rgb_image, caption="Generated RGB Image", width=400)
    st.success("RGB image generated successfully!")

    with open(output_image_path, "rb") as file:
        rgb_bytes = file.read()

    st.download_button(
        label="Download RGB Image",
        data=rgb_bytes,
        file_name="output_rgb_image.png",
        mime="image/png"
    )

# Reconstruct file from RGB image
uploaded_rgb_file = st.file_uploader("Upload an RGB image to reconstruct the file", type=["png"])
if uploaded_rgb_file:
    temp_rgb_image_path = "uploaded_rgb_image.png"
    output_file_path = "reconstructed_file"

    with open(temp_rgb_image_path, "wb") as temp_file:
        temp_file.write(uploaded_rgb_file.read())

    try:
        rgb_image_to_file(temp_rgb_image_path, output_file_path)
        st.success("File reconstructed successfully!")

        with open(output_file_path, "rb") as file:
            file_bytes = file.read()

        st.download_button(
            label="Download Reconstructed File",
            data=file_bytes,
            file_name="reconstructed_file",
            mime="application/octet-stream"
        )
    except ValueError as e:
        st.error(f"Error: {str(e)}")
