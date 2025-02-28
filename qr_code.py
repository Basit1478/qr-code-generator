import streamlit as st
import qrcode
import cv2
import numpy as np
from PIL import Image
import io

st.title("QR Code Encoder & Decoder")

# QR Code Generator
st.header("Generate QR Code")
text = st.text_input("Enter text or URL:")
if st.button("Generate QR Code"):
    if text:
        qr = qrcode.make(text)
        img_bytes = io.BytesIO()
        qr.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        st.image(img_bytes, caption="Generated QR Code", use_container_width=True)
        st.download_button("Download QR Code", img_bytes, file_name="qrcode.png", mime="image/png")
    else:
        st.warning("Please enter some text.")

# QR Code Decoder
st.header("Decode QR Code")
uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert image to OpenCV format
    img_array = np.array(image.convert("RGB"))  # Ensure image is in RGB mode
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)  # Convert to BGR

    # Decode QR Code
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img_bgr)

    if data:
        st.success(f"Decoded Data: {data}")
    else:
        st.error("No QR code found in the image.")
