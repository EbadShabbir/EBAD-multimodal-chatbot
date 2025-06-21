# EBAD - Electronic Brain and Assistant Droid 🤖

A sophisticated multimodal AI chatbot inspired by Iron Man's JARVIS, built with Streamlit and powered by Google's hybrid AI approach: Gemma 3n E4B-it for efficient text processing and Gemini 2.0 Flash for superior image analysis. EBAD combines voice input, image analysis, and natural language processing in a sleek, Iron Man-themed interface.

![EBAD Interface](https://img.shields.io/badge/EBAD-Multimodal%20AI-blue?style=for-the-badge&logo=robot)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Google AI](https://img.shields.io/badge/Google%20AI-4285F4?style=for-the-badge&logo=google)

## 🌟 Features

- **💬 Natural Language Chat**: Engage in intelligent conversations with EBAD using Gemma 3n E4B-it
- **🎤 Voice Input**: Speak directly to EBAD using speech recognition
- **👁️ Computer Vision**: Upload and analyze images with advanced Gemini 2.0 Flash model
- **🎨 Iron Man Theme**: Beautiful dark blue interface with arc reactor animation
- **🧠 Memory**: Maintains conversation context throughout your session
- **⚡ Hybrid Processing**: Optimized text processing with Gemma 3n E4B-it and superior image analysis with Gemini 2.0 Flash

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Text AI Model**: Google Gemma 3n E4B-it (Efficient text processing)
- **Vision AI Model**: Google Gemini 2.0 Flash (Advanced image analysis)
- **Voice Recognition**: SpeechRecognition + PyAudio
- **Image Processing**: PIL (Pillow)
- **Environment Management**: python-dotenv
- **Language**: Python 3.9+

## 📋 Prerequisites

- Python 3.9 or higher
- Google AI Studio API key
- Microphone (for voice input)
- Webcam or image files (for vision features)

## 🚀 Quick Start

### 1. Setup Project Structure

Create the project directory structure using command prompt:

**Windows:**
mkdir multimodal-chatbot
cd multimodal-chatbot
mkdir .streamlit assets assets\styles utils uploads
echo. > app.py
echo. > utils_init_.py
echo. > utils\gemini_client.py
echo. > utils\image_handler.py
echo. > utils\voice_handler.py
echo. > config.py
echo. > .env
echo. > .env.example
echo. > requirements.txt
echo. > README.md
echo. > .gitignore
echo. > .streamlit\config.toml
echo. > assets\styles\custom.css

text

**Linux/Mac:**
mkdir multimodal-chatbot
cd multimodal-chatbot
mkdir -p .streamlit assets/styles utils uploads
touch app.py utils/init.py utils/gemini_client.py utils/image_handler.py utils/voice_handler.py
touch config.py .env .env.example requirements.txt README.md .gitignore
touch .streamlit/config.toml assets/styles/custom.css

text

### 2. Install Dependencies

Create `requirements.txt`:
streamlit>=1.28.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
pillow>=10.0.0
speechrecognition>=3.10.0
pyaudio>=0.2.11

text

Install all dependencies:
Create virtual environment
python -m venv venv

Activate virtual environment
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Install dependencies
pip install streamlit
pip install google-generativeai
pip install python-dotenv
pip install pillow
pip install speechrecognition
pip install pyaudio

text

### 3. Get Google AI Studio API Key

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Navigate to "Get API Key" in the left sidebar
4. Click "Create API Key"
5. Copy the generated API key

### 4. Configure Environment

Create `.env` file:
GOOGLE_API_KEY=your_actual_google_ai_studio_api_key_here

text

Create `.env.example`:
GOOGLE_API_KEY=your_api_key_here
APP_TITLE=EBAD - Electronic Brain and Assistant Droid
MAX_FILE_SIZE=10

text

### 5. Create Main Application

Create `app.py` with the hybrid EBAD implementation using both Gemma 3n E4B-it for text processing and Gemini 2.0 Flash for image analysis.

### 6. Create Utility Files

Create `utils/gemini_client.py`:
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class EBADClient:
def init(self):
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Hybrid model setup
self.text_model = genai.GenerativeModel("gemma-3n-e4b-it")
self.vision_model = genai.GenerativeModel("gemini-2.0-flash-exp")

text
def generate_response(self, prompt, image=None):
    """Generate response from EBAD using appropriate model"""
    try:
        if image:
            # Use vision model for image analysis
            response = self.vision_model.generate_content([prompt, image])
        else:
            # Use text model for regular conversation
            response = self.text_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"EBAD systems error: {str(e)}"
text

Create `utils/voice_handler.py`:
import speech_recognition as sr
import streamlit as st

class VoiceHandler:
def init(self):
self.recognizer = sr.Recognizer()

text
def listen_and_transcribe(self):
    """Listen to microphone and transcribe speech"""
    try:
        with sr.Microphone() as source:
            st.info("🎤 EBAD is listening... Speak now!")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        st.info("🔄 EBAD is processing your voice...")
        text = self.recognizer.recognize_google(audio)
        st.success(f"✅ Voice recognized: {text}")
        return text
        
    except Exception as e:
        st.error(f"❌ Voice system error: {e}")
        return None
text

Create `utils/image_handler.py`:
from PIL import Image
import streamlit as st

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

text

### 7. Create Configuration Files

Create `.gitignore`:
.env
pycache/
*.pyc
uploads/
.streamlit/secrets.toml
*.log
venv/
.vscode/

text

Create `.streamlit/config.toml`:
[theme]
primaryColor = "#60a5fa"
backgroundColor = "#0d1b2a"
secondaryBackgroundColor = "#1e3a8a"
textColor = "#f8fafc"
font = "sans serif"

[server]
maxUploadSize = 10
enableXsrfProtection = false

text

## 🏃‍♂️ Running EBAD

streamlit run app.py

text

The application will open in your browser at `http://localhost:8501`

## 📁 Final Project Structure

multimodal-chatbot/
├── .streamlit/
│ └── config.toml # App configuration
├── assets/
│ └── styles/
│ └── custom.css # Custom CSS styling
├── utils/
│ ├── init.py
│ ├── gemini_client.py # Google AI hybrid client
│ ├── voice_handler.py # Voice processing
│ └── image_handler.py # Image processing
├── uploads/ # Temporary file storage
├── .env # Environment variables
├── .env.example # Environment template
├── .gitignore # Git ignore rules
├── requirements.txt # Python dependencies
├── README.md # This file
├── config.py # App configuration
└── app.py # Main Streamlit application

text

## 🎨 Interface Features

- **Arc Reactor Animation**: Pulsing blue energy core
- **Iron Man Color Scheme**: Dark blue gradients with glowing accents
- **Enhanced Text Contrast**: Improved readability with better color choices
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Status**: Live updates on EBAD's processing state
- **Message History**: Persistent chat history during session

## 🤖 Hybrid AI Architecture

- **Text Processing**: Gemma 3n E4B-it provides efficient, fast responses for conversations and voice input
- **Image Analysis**: Gemini 2.0 Flash delivers superior computer vision capabilities for image understanding
- **Optimized Performance**: Best of both models - speed for text, accuracy for vision
- **Cost Effective**: Uses appropriate model complexity for each task type

## 🐛 Troubleshooting

### PyAudio Installation Issues

**Windows:**
pip install pipwin
pipwin install pyaudio

text

**macOS:**
brew install portaudio
pip install pyaudio

text

**Linux:**
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio

text

### Common Issues

1. **Blank Page**: Check if `.env` file exists with correct API key
2. **Import Errors**: Ensure all dependencies are installed
3. **API Errors**: Verify Google AI Studio API key is active
4. **Microphone Issues**: Check system permissions and microphone access
5. **Model Loading**: Ensure both Gemma 3n E4B-it and Gemini 2.0 Flash are accessible via your API key

### Testing Your Setup

Create a test file to verify everything works:

test_setup.py
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

st.title("🤖 EBAD Hybrid Setup Test")

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

try:
# Test text model
text_model = genai.GenerativeModel("gemma-3n-e4b-it")
st.success("✅ Gemma 3n E4B-it text model loaded successfully")
except Exception as e:
st.error(f"❌ Text model failed: {e}")

try:
# Test vision model
vision_model = genai.GenerativeModel("gemini-2.0-flash-exp")
st.success("✅ Gemini 2.0 Flash vision model loaded successfully")
except Exception as e:
st.error(f"❌ Vision model failed: {e}")

st.success("🎉 Hybrid setup test complete!")

text

Run: `streamlit run test_setup.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google AI for the Gemma 3n E4B-it and Gemini 2.0 Flash models
- Streamlit team for the amazing framework
- Marvel Studios for Iron Man inspiration
- Open source community for various libraries
- Smartera organization for project mentorship and technical guidance

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Voice synthesis for EBAD responses
- [ ] Document processing (PDF, DOCX)
- [ ] Integration with external APIs
- [ ] Mobile app version
- [ ] Advanced conversation memory
- [ ] Custom voice commands
- [ ] Model switching interface
- [ ] Performance analytics dashboard

---

**Made with ❤️ and inspired by Tony Stark's JARVIS**

*"Sometimes you gotta run before you can walk." - Tony Stark*