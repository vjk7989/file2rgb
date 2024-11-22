# import streamlit as st
# from PIL import Image
# import numpy as np
# import zlib

# # Set page config and theme to light mode
# st.set_page_config(
#     page_title="File to RGB Image Converter",
#     page_icon="🖼️",
#     initial_sidebar_state="expanded"
# )

# # Force light theme with black text
# st.markdown("""
#     <style>
#         .stApp {
#             background-color: white;
#         }
#         .stMarkdown, .stText, .stButton, .stSelectbox, .stFileUploader, p, label {
#             color: black !important;
#         }
#         .uploadedFile {
#             color: black !important;
#         }
#         .stCheckbox {
#             color: black !important;
#         }
#         button[kind="secondary"] {
#             background: white !important;
#             color: black !important;
#         }
#         .stDownloadButton {
#             color: black !important;
#         }
#         h1 {
#             color: black !important;
#         }
#         .css-10trblm {
#             color: black !important;
#         }
#     </style>
# """, unsafe_allow_html=True)

# def compress_data(data):
#     """Compress data using zlib."""
#     return zlib.compress(data)

# def decompress_data(data):
#     """Decompress data using zlib."""
#     return zlib.decompress(data)

# # ... rest of your existing functions ...
# def file_to_rgb_image(file_path, output_image_path, compress=False):
#     with open(file_path, "rb") as f:
#         data = f.read()

#     if compress:
#         data = compress_data(data)

#     metadata = f"rgb,{'1' if compress else '0'}".encode("utf-8").ljust(24, b'\x00')
#     data_with_metadata = metadata + data

#     pixel_count = -(-len(data_with_metadata) // 3)  # Ceiling division
#     image_size = int(np.ceil(np.sqrt(pixel_count)))

#     image_data = np.zeros((image_size, image_size, 3), dtype=np.uint8)
#     flat_data = np.frombuffer(data_with_metadata, dtype=np.uint8)

#     image_data.flat[:len(flat_data)] = flat_data

#     image = Image.fromarray(image_data)
#     image.save(output_image_path)
#     return image

# def rgb_image_to_file(image_path, output_file_path):
#     img = Image.open(image_path)
#     img_data = np.array(img).flatten()

#     metadata = bytes(img_data[:24]).decode("utf-8").rstrip("\x00")
#     if not metadata.startswith("rgb"):
#         raise ValueError("Invalid metadata in the image file.")

#     compress = metadata.split(",")[1] == "1"

#     with open(output_file_path, "wb") as f:
#         data = img_data[24:]
#         if compress:
#             data = decompress_data(data.tobytes())
#         f.write(data)

# # Streamlit UI
# st.title("File to RGB Image Converter with Compression")
# st.write("Upload a file to compress and encode it into an RGB image or upload an RGB image to reconstruct the file.")

# # Upload file to convert to RGB image
# uploaded_file = st.file_uploader("Upload a file", type=["txt", "java", "py", "json", "csv", "md"])

# if uploaded_file:
#     temp_file_path = "uploaded_file"
#     output_image_path = "output_rgb_image.png"

#     # Save the uploaded file temporarily
#     with open(temp_file_path, "wb") as temp_file:
#         temp_file.write(uploaded_file.read())

#     # Convert the file to RGB image with optional compression
#     compress = st.checkbox("Compress file before encoding?", value=False)
#     rgb_image = file_to_rgb_image(temp_file_path, output_image_path, compress=compress)
#     st.image(rgb_image, caption="Generated RGB Image", width=400)
#     st.success(f"RGB image saved automatically as {output_image_path}")

#     # Provide download button for the RGB image
#     with open(output_image_path, "rb") as file:
#         rgb_bytes = file.read()

#     st.download_button(
#         label="Download RGB Image",
#         data=rgb_bytes,
#         file_name="output_rgb_image.png",
#         mime="image/png"
#     )

# # Upload RGB image to reconstruct the file
# uploaded_rgb_file = st.file_uploader("Upload an RGB image to reconstruct the file", type=["png"])

# if uploaded_rgb_file:
#     temp_rgb_image_path = "uploaded_rgb_image.png"
#     output_file_path = "reconstructed_file"

#     # Save the uploaded RGB image temporarily
#     with open(temp_rgb_image_path, "wb") as temp_file:
#         temp_file.write(uploaded_rgb_file.read())

#     # Reconstruct the file
#     try:
#         rgb_image_to_file(temp_rgb_image_path, output_file_path)
#         st.success(f"File reconstructed and saved automatically as {output_file_path}")

#         # Provide download button for the reconstructed file
#         with open(output_file_path, "rb") as file:
#             file_bytes = file.read()

#         st.download_button(
#             label="Download Reconstructed File",
#             data=file_bytes,
#             file_name="reconstructed_file",
#             mime="application/octet-stream"
#         )
#     except ValueError as e:
#         st.error(f"Error: {str(e)}") 

import streamlit as st
from PIL import Image
import numpy as np
import zlib

# Set page config
st.set_page_config(
    page_title="File to RGB Image Converter",
    page_icon="🖼️",
    initial_sidebar_state="expanded"
)

# Add gradient background
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to bottom right, #0f172a, #000000); /* from-blue-900 to-black */
            color: white;
        }
        .stMarkdown, .stText, .stButton, .stSelectbox, .stFileUploader,p, label {
            color: white !important;
        }
        .uploadedFile {
            color: white !important;
        }
        .stCheckbox {
            color: white !important;
        }
        button[kind="secondary"] {
            background: white !important;
            color: black !important;
        }
        .stDownloadButton, label {
            color: black !important;
        }
        div.stDownloadButton > button {
            color: black !important;  /* Change text color to white */
            background-color: #1f2937 !important; /* Optional: Add a dark background */
            border: none !important;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        h1 {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

def compress_data(data):
    """Compress data using zlib."""
    return zlib.compress(data)

def decompress_data(data):
    """Decompress data using zlib."""
    return zlib.decompress(data)

def file_to_rgb_image(file_path, output_image_path, compress=False):
    with open(file_path, "rb") as f:
        data = f.read()

    if compress:
        data = compress_data(data)

    metadata = f"rgb,{'1' if compress else '0'}".encode("utf-8").ljust(24, b'\x00')
    data_with_metadata = metadata + data

    pixel_count = -(-len(data_with_metadata) // 3)  # Ceiling division
    image_size = int(np.ceil(np.sqrt(pixel_count)))

    image_data = np.zeros((image_size, image_size, 3), dtype=np.uint8)
    flat_data = np.frombuffer(data_with_metadata, dtype=np.uint8)

    image_data.flat[:len(flat_data)] = flat_data

    image = Image.fromarray(image_data)
    image.save(output_image_path)
    return image

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

# Streamlit UI
st.title("File to RGB Image Converter with Compression")
st.write("Upload a file to compress and encode it into an RGB image or upload an RGB image to reconstruct the file.")

# Upload file to convert to RGB image
uploaded_file = st.file_uploader("Upload a file", type=["txt", "java", "py", "json", "csv", "md"])

if uploaded_file:
    temp_file_path = "uploaded_file"
    output_image_path = "output_rgb_image.png"

    # Save the uploaded file temporarily
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())

    # Convert the file to RGB image with optional compression
    compress = st.checkbox("Compress file before encoding?", value=False)
    rgb_image = file_to_rgb_image(temp_file_path, output_image_path, compress=compress)
    st.image(rgb_image, caption="Generated RGB Image", width=400)
    st.success(f"RGB image saved automatically as {output_image_path}")

    # Provide download button for the RGB image
    with open(output_image_path, "rb") as file:
        rgb_bytes = file.read()

    st.download_button(
        label="Download RGB Image",
        data=rgb_bytes,
        file_name="output_rgb_image.png",
        mime="image/png"
    )

# Upload RGB image to reconstruct the file
uploaded_rgb_file = st.file_uploader("Upload an RGB image to reconstruct the file", type=["png"])

if uploaded_rgb_file:
    temp_rgb_image_path = "uploaded_rgb_image.png"
    output_file_path = "reconstructed_file"

    # Save the uploaded RGB image temporarily
    with open(temp_rgb_image_path, "wb") as temp_file:
        temp_file.write(uploaded_rgb_file.read())

    # Reconstruct the file
    try:
        rgb_image_to_file(temp_rgb_image_path, output_file_path)
        st.success(f"File reconstructed and saved automatically as {output_file_path}")

        # Provide download button for the reconstructed file
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
