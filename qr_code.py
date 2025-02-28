import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import pyzbar.pyzbar as pyzbar

def generate_qr(data):
    qr = qrcode.make(data)
    img_bytes = BytesIO()
    qr.save(img_bytes, format="PNG")
    return img_bytes.getvalue()

def decode_qr(image):
    decoded_objects = pyzbar.decode(image)
    return decoded_objects[0].data.decode('utf-8') if decoded_objects else "No QR code found."

st.title("QR Code Generator & Scanner")

# QR Code Generator
text = st.text_input("Enter text or URL:")
if st.button("Generate QR Code"):
    if text:
        img = generate_qr(text)
        st.image(img, caption="Generated QR Code")
        st.download_button("Download QR Code", img, file_name="qrcode.png", mime="image/png")
    else:
        st.warning("Enter text to generate QR code.")

# QR Code Decoder
uploaded_file = st.file_uploader("Upload QR Code Image:", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded QR Code")
    decoded_data = decode_qr(image)
    if decoded_data:
        st.success(f"Decoded Data: {decoded_data}")
    else:
        st.error("Could not decode QR code.")
