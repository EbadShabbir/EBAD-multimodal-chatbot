from PIL import Image
import streamlit as st
import io

class ImageHandler:
    @staticmethod
    def process_uploaded_image(uploaded_file):
        """Process uploaded image file"""
        try:
            image = Image.open(uploaded_file)
            return image
        except Exception as e:
            st.error(f"Error processing image: {e}")
            return None
    
    @staticmethod
    def display_image_with_analysis(image, analysis_text):
        """Display image alongside analysis"""
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(image, caption="Uploaded Image", width=300)
        
        with col2:
            st.markdown(f"**EBAD Analysis:**\n{analysis_text}")

