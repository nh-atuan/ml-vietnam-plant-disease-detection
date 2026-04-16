import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Plant Disease Diagnosis", layout="centered")

st.title("🌿 Plant Disease Diagnosis System")
st.write("Supporting Vietnamese Coffee & Rice Farmers")

uploaded_file = st.file_uploader("Choose an image of a leaf...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Leaf Image', use_column_width=True)
    
    if st.button('Diagnose'):
        with st.spinner('Analyzing...'):
            # Convert image to bytes for API call
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            files = {"file": img_byte_arr.getvalue()}
            
            try:
                # Assuming API is running locally or on a known host
                response = requests.post("http://localhost:8000/predict", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Diagnosis: {result['disease']}")
                    st.metric("Confidence", f"{result['confidence']*100:.2f}%")
                else:
                    st.error("Error connecting to the diagnosis engine.")
            except Exception as e:
                st.error(f"Error: {e}")
