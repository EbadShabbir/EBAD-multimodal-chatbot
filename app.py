import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import speech_recognition as sr
import io
import base64
import time

# Load environment variables
load_dotenv()

# Configure Google AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@st.cache_resource
def load_models():
    # Text model: Gemma 3n E4B-it for efficient text processing
    text_model = genai.GenerativeModel("gemma-3n-e4b-it")
    # Vision model: Gemini 2.0 Flash for superior image analysis
    vision_model = genai.GenerativeModel("gemini-2.0-flash-exp")
    return text_model, vision_model

def handle_voice_input():
    """Handle voice input using speech recognition"""
    r = sr.Recognizer()
    
    status_placeholder = st.empty()
    
    try:
        with sr.Microphone() as source:
            status_placeholder.markdown('<p class="status-text">🎤 EBAD is listening... Speak now!</p>', unsafe_allow_html=True)
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        
        status_placeholder.markdown('<p class="status-text">🔄 EBAD is processing your voice...</p>', unsafe_allow_html=True)
        text = r.recognize_google(audio)
        status_placeholder.markdown(f'<p class="status-text">✅ Voice recognized: {text}</p>', unsafe_allow_html=True)
        time.sleep(2)
        status_placeholder.empty()
        return text
        
    except sr.WaitTimeoutError:
        status_placeholder.markdown('<p class="status-text">⏰ No speech detected. Please try again.</p>', unsafe_allow_html=True)
        time.sleep(2)
        status_placeholder.empty()
        return None
    except sr.UnknownValueError:
        status_placeholder.markdown('<p class="status-text">❌ Could not understand the audio. Please try again.</p>', unsafe_allow_html=True)
        time.sleep(2)
        status_placeholder.empty()
        return None
    except Exception as e:
        status_placeholder.markdown(f'<p class="status-text">❌ Voice system error: {e}</p>', unsafe_allow_html=True)
        time.sleep(2)
        status_placeholder.empty()
        return None

st.set_page_config(page_title="EBAD", page_icon="🤖", layout="wide")

# Initialize chat history and models (FIXED)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "text_model" not in st.session_state or "vision_model" not in st.session_state:
    st.session_state.text_model, st.session_state.vision_model = load_models()

# Red Arc Reactor Theme CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #2a0d0d 0%, #8a1e1e 50%, #5d1a1a 100%);
    }
    
    .arc-reactor-bg {
        position: fixed;
        top: 45%;
        left: 60%;
        transform: translate(-50%, -50%);
        width: 250px;
        height: 250px;
        border-radius: 50%;
        background: radial-gradient(circle, 
            rgba(239, 68, 68, 0.4) 0%, 
            rgba(220, 38, 38, 0.3) 30%, 
            rgba(185, 28, 28, 0.2) 60%, 
            transparent 80%);
        animation: pulse 4s ease-in-out infinite;
        z-index: 1;
    }
    
    .arc-reactor-bg::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: rgba(255, 200, 200, 0.9);
        box-shadow: 0 0 40px rgba(239, 68, 68, 0.8);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; transform: translate(-50%, -50%) scale(1); }
        50% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
    }
    
    .main-title {
        color: #000000 !important;
        text-align: center;
        font-size: 4rem;
        text-shadow: 0 0 30px #ef4444, 0 0 50px #dc2626;
        margin-bottom: 1rem;
        font-weight: bold;
        font-family: 'Roboto', sans-serif;
    }
    
    .subtitle {
        color: #000000 !important;
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .stMarkdown h3 {
        color: #000000 !important;
        text-shadow: 0 0 20px #ef4444;
        font-size: 1.8rem !important;
        font-weight: bold !important;
    }
    
    .stMarkdown p, .stMarkdown div {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 3px solid #ef4444 !important;
        border-radius: 15px !important;
        color: #000000 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        text-shadow: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #333333 !important;
        font-weight: 500 !important;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #991b1b, #dc2626, #ef4444) !important;
        border: none !important;
        border-radius: 15px !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.7) !important;
        font-size: 18px !important;
        padding: 0.75rem 1.5rem !important;
    }
    
    .user-msg {
        background: rgba(255, 245, 245, 0.9) !important;
        color: #000000 !important;
        padding: 1.2rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        border: 2px solid #ef4444;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 20px rgba(185, 28, 28, 0.4);
        text-shadow: none !important;
    }
    
    .bot-msg {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #000000 !important;
        padding: 1.2rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        border: 2px solid #dc2626;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 20px rgba(185, 28, 28, 0.5);
        text-shadow: none !important;
    }
    
    .status-text {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        text-shadow: 0 0 15px #ef4444 !important;
    }
    
    .stSidebar {
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    .stSidebar .stMarkdown p, .stSidebar .stMarkdown div, .stSidebar .stMarkdown li {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    .stSidebar .stMarkdown ul li {
        color: #000000 !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px dashed #ef4444 !important;
        border-radius: 15px !important;
        padding: 1rem !important;
    }
    
    .stFileUploader label {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    .stFileUploader div[data-testid="stFileUploaderDropzone"] {
        color: #000000 !important;
    }
    
    .empty-chat-msg {
        color: #000000 !important;
        font-style: italic !important;
        font-size: 18px !important;
        text-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Arc reactor background
st.markdown('<div class="arc-reactor-bg"></div>', unsafe_allow_html=True)

# Title with theme
st.markdown('<h1 class="main-title">EBAD</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Electronic Brain and Assistant Droid - Now with Vision & Voice</p>', unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.markdown("### 🎛️ EBAD Controls")
    
    # Voice input button
    if st.button("🎤 Voice Input", use_container_width=True):
        voice_text = handle_voice_input()
        if voice_text:
            st.session_state.voice_input = voice_text
            st.rerun()
    
    # Image upload
    st.markdown("### 📸 Image Upload")
    uploaded_image = st.file_uploader(
        "Upload an image for EBAD to analyze",
        type=['png', 'jpg', 'jpeg'],
        help="Upload images for visual analysis"
    )
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Instructions
    st.markdown("""
    ### 📋 EBAD Capabilities:
    - **💬 Text Chat**: Natural conversation
    - **🎤 Voice Input**: Speak to EBAD
    - **👁️ Vision**: Upload & analyze images
    - **🧠 Memory**: Remembers conversation
    """)

# Chat History
st.markdown("### 💬 Chat History")
chat_container = st.container()

with chat_container:
    if st.session_state.messages:
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                if message.get("image"):
                    st.image(message["image"], width=300)
                if message.get("voice_input"):
                    st.markdown(f'<div class="user-msg">🎤 <strong>You (Voice):</strong> {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="user-msg">👤 <strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-msg">🤖 <strong>EBAD:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="empty-chat-msg">EBAD memory is empty. Start chatting below!</p>', unsafe_allow_html=True)

# Handle voice input from session state (FIXED)
if hasattr(st.session_state, 'voice_input'):
    voice_text = st.session_state.voice_input
    del st.session_state.voice_input
    
    # Add voice message to chat
    st.session_state.messages.append({
        "role": "user", 
        "content": voice_text,
        "voice_input": True
    })
    
    # Generate EBAD response for voice using TEXT MODEL
    with st.spinner("🤖 EBAD is thinking..."):
        try:
            response = st.session_state.text_model.generate_content(f"You are EBAD (Electronic Brain and Assistant Droid), an AI assistant inspired by JARVIS from Iron Man. Respond in a helpful, intelligent, and slightly sophisticated manner. User said via voice: {voice_text}")
            ebad_response = response.text
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": ebad_response
            })
            st.rerun()
        except Exception as e:
            error_msg = f"EBAD systems encountered an error: {str(e)}"
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_msg
            })
            st.rerun()

# Chat Input Section
st.markdown("### 🚀 Send Message")

# Create columns for input and buttons
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    user_input = st.text_input("Type your message:", placeholder="Ask EBAD anything...", label_visibility="collapsed")

with col2:
    send_button = st.button("Send", type="primary", use_container_width=True)

with col3:
    if uploaded_image:
        analyze_button = st.button("🔍 Analyze Image", use_container_width=True)
    else:
        st.button("🔍 Analyze Image", disabled=True, use_container_width=True)

# Handle text message sending (FIXED)
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate EBAD response using TEXT MODEL
    with st.spinner("🤖 EBAD is processing..."):
        try:
            response = st.session_state.text_model.generate_content(f"You are EBAD (Electronic Brain and Assistant Droid), an AI assistant inspired by JARVIS from Iron Man. Respond in a helpful, intelligent, and slightly sophisticated manner. User query: {user_input}")
            ebad_response = response.text
            
            st.session_state.messages.append({"role": "assistant", "content": ebad_response})
            st.rerun()
        except Exception as e:
            error_msg = f"EBAD systems encountered an error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()

# Handle image analysis (FIXED)
if uploaded_image and (analyze_button or (send_button and user_input)):
    # Process the uploaded image
    image = Image.open(uploaded_image)
    
    # Prepare prompt
    image_prompt = user_input if user_input else "Analyze this image in detail. What do you see?"
    
    # Add user message with image
    st.session_state.messages.append({
        "role": "user", 
        "content": image_prompt,
        "image": image
    })
    
    # Generate EBAD response for image using VISION MODEL
    with st.spinner("🤖 EBAD is analyzing the image..."):
        try:
            response = st.session_state.vision_model.generate_content([
                f"You are EBAD (Electronic Brain and Assistant Droid), an AI assistant inspired by JARVIS from Iron Man. Analyze this image and respond in a helpful, intelligent manner. User query: {image_prompt}",
                image
            ])
            ebad_response = response.text
            
            st.session_state.messages.append({"role": "assistant", "content": ebad_response})
            st.rerun()
        except Exception as e:
            error_msg = f"EBAD visual systems encountered an error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()

# Status with updated model names (FIXED)
st.markdown("---")
st.markdown(f'<p class="status-text">🟢 Status: EBAD Online | 💬 Messages: {len(st.session_state.messages)} | 🧠 Text: Gemma 3n E4B-it | 👁️ Vision: Gemini 2.0 Flash</p>', unsafe_allow_html=True)
