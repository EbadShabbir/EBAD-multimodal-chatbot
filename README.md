
# EBAD API - Electronic Brain and Assistant Droid 🤖

A sophisticated multimodal AI chatbot API inspired by Iron Man's JARVIS, built with FastAPI and powered by Google's hybrid AI approach: Gemma 3n E4B-it for efficient text processing and Gemini 2.0 Flash for superior image analysis. EBAD API provides secure, scalable endpoints for voice input, image analysis, and natural language processing.

![EBAD API](https://img.shields.io/badge/EBAD%20API-Multimodal%20AI-blue?style=for-the-badge&logo=robot)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
![Google AI](https://img.shields.io/badge/Google%20AI-4285F4?style=for-the-badge&logo=google)

## 🌟 Features

- **💬 Natural Language Chat API**: RESTful endpoint for intelligent conversations using Gemma 3n E4B-it
- **🎤 Voice Transcription API**: Upload audio files for speech-to-text conversion
- **👁️ Computer Vision API**: Upload and analyze images with advanced Gemini 2.0 Flash model
- **🔐 API Key Authentication**: Secure endpoints with header-based authentication
- **📊 Error Handling & Logging**: Comprehensive error handling with detailed logging
- **⚡ Hybrid Processing**: Optimized text processing with Gemma 3n E4B-it and superior image analysis with Gemini 2.0 Flash
- **🚀 Production Ready**: Built with FastAPI and Uvicorn for high-performance deployment

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **Text AI Model**: Google Gemma 3n E4B-it (Efficient text processing)
- **Vision AI Model**: Google Gemini 2.0 Flash (Advanced image analysis)
- **Voice Recognition**: SpeechRecognition
- **Image Processing**: PIL (Pillow)
- **Environment Management**: python-dotenv
- **Language**: Python 3.9+

## 📋 Prerequisites

- Python 3.9 or higher
- Google AI Studio API key
- Audio files (for voice transcription)
- Image files (for vision analysis)

## 🚀 Quick Start

### 1. Setup Project Structure

Create the project directory structure:

**Windows:**
```
mkdir multimodal-chatbot
cd multimodal-chatbot
mkdir utils uploads
echo. > api.py
echo. > utils\__init__.py
echo. > utils\gemini_client.py
echo. > utils\image_handler.py
echo. > utils\voice_handler.py
echo. > .env
echo. > .env.example
echo. > requirements.txt
echo. > README.md
echo. > .gitignore
```

**Linux/Mac:**
```
mkdir multimodal-chatbot
cd multimodal-chatbot
mkdir -p utils uploads
touch api.py utils/__init__.py utils/gemini_client.py utils/image_handler.py utils/voice_handler.py
touch .env .env.example requirements.txt README.md .gitignore
```

### 2. Install Dependencies

Create `requirements.txt`:
```
fastapi>=0.100.0
uvicorn>=0.22.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
pillow>=10.0.0
speechrecognition>=3.10.0
```

Install all dependencies:
```
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Get Google AI Studio API Key

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Navigate to "Get API Key" in the left sidebar
4. Click "Create API Key"
5. Copy the generated API key

### 4. Configure Environment

Create `.env` file:
```
GOOGLE_API_KEY=your_actual_google_ai_studio_api_key_here
```

Create `.env.example`:
```
GOOGLE_API_KEY=your_api_key_here
APP_TITLE=EBAD API - Electronic Brain and Assistant Droid
MAX_FILE_SIZE=10
```

### 5. Create Main API Application

Create `api.py`:
```
from fastapi import FastAPI, Body, UploadFile, File, Depends, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from utils.voice_handler import VoiceHandler
from utils.image_handler import ImageHandler
from utils.gemini_client import EBADClient
import io
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="EBAD API", description="API for EBAD client interactions", version="1.0")

# Create instances (using lowercase for instances to avoid conflicts)
voice_handler = VoiceHandler()
ebad_client = EBADClient()

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error: {str(exc)}")
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

# API key verification dependency
async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != "your-secret-key":  # Replace with a real secret (use env vars in production)
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# Voice analysis endpoint with API key dependency
@app.post("/voice")
def analyze_voice(prompt: str, file: UploadFile = File(...), api_key: str = Depends(verify_api_key)):
    """
    Endpoint to handle voice analysis requests.
    """
    audio_data = io.BytesIO(file.file.read())
    text = voice_handler.transcribe_audio(audio_data)
    return {"transcription": text}

# Image analysis endpoint with API key dependency
@app.post("/upload")
def analyze_image(prompt: str, file: UploadFile = File(...), api_key: str = Depends(verify_api_key)):
    image = ImageHandler.process_uploaded_image(file.file)
    if not image:
        return {"error": "Invalid image format or processing failed."}
    response = ebad_client.generate_response(prompt, image)
    return {"response": response}

# Chat endpoint with API key dependency
@app.post("/chat")
def chat(prompt: str = Body(...), api_key: str = Depends(verify_api_key)):
    """
    Endpoint to handle chat requests.
    """
    response = ebad_client.generate_response(prompt)
    return {"response": response}
```

### 6. Create Utility Files

Create `utils/gemini_client.py`:
```
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class EBADClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # Hybrid model setup
        self.text_model = genai.GenerativeModel("gemma-3n-e4b-it")
        self.vision_model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
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
```

Create `utils/voice_handler.py`:
```
import speech_recognition as sr
import io
import tempfile
import os

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def transcribe_audio(self, audio_data):
        """
        Transcribe uploaded audio data to text using Google Speech Recognition.
        """
        try:
            # Save audio_data to a temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data.getvalue())
                temp_file_path = temp_file.name

            # Process the file with SpeechRecognition
            with sr.AudioFile(temp_file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)

            # Clean up the temp file
            os.unlink(temp_file_path)

            return text

        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError as e:
            return f"Speech recognition service error: {e}"
        except Exception as e:
            return f"Audio processing error: {e}"
```

Create `utils/image_handler.py`:
```
from PIL import Image

class ImageHandler:
    @staticmethod
    def process_uploaded_image(uploaded_file):
        """Process uploaded image file"""
        try:
            image = Image.open(uploaded_file)
            return image
        except Exception as e:
            return None
```

### 7. Create Configuration Files

Create `.gitignore`:
```
.env
__pycache__/
*.pyc
uploads/
*.log
venv/
.vscode/
```

## 🏃‍♂️ Running EBAD API

Start the API server:
```
uvicorn api:app --reload
```

The API will be available at:
- **API Base URL**: `http://127.0.0.1:8000`
- **Interactive Docs**: `http://127.0.0.1:8000/docs`
- **OpenAPI Schema**: `http://127.0.0.1:8000/openapi.json`

## 📁 Final Project Structure

```
multimodal-chatbot/
├── utils/
│   ├── __init__.py
│   ├── gemini_client.py      # Google AI hybrid client
│   ├── voice_handler.py      # Voice processing
│   └── image_handler.py      # Image processing
├── uploads/                  # Temporary file storage
├── .env                      # Environment variables
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── api.py                  # Main FastAPI application
```

## 🔗 API Endpoints

### Authentication
All endpoints require an API key in the header:
```
x-api-key: your-secret-key
```

### Endpoints

#### 1. Chat Endpoint
**POST** `/chat`

{
  "prompt": "Hello, EBAD!"
}


#### 2. Voice Transcription Endpoint
**POST** `/voice`
- **Form Data**: 
  - `prompt`: Text prompt
  - `file`: Audio file (WAV, MP3, etc.)

#### 3. Image Analysis Endpoint
**POST** `/upload`
- **Form Data**: 
  - `prompt`: Text prompt for image analysis
  - `file`: Image file (JPG, PNG, etc.)

## 🤖 Hybrid AI Architecture

- **Text Processing**: Gemma 3n E4B-it provides efficient, fast responses for conversations and voice input
- **Image Analysis**: Gemini 2.0 Flash delivers superior computer vision capabilities for image understanding
- **Optimized Performance**: Best of both models - speed for text, accuracy for vision
- **Cost Effective**: Uses appropriate model complexity for each task type

## 🐛 Troubleshooting

### Common Issues

1. **401 Unauthorized**: Check if API key is correctly set in request headers
2. **Import Errors**: Ensure all dependencies are installed
3. **API Errors**: Verify Google AI Studio API key is active
4. **Audio Processing Issues**: Ensure audio files are in supported formats (WAV recommended)
5. **Model Loading**: Ensure both Gemma 3n E4B-it and Gemini 2.0 Flash are accessible via your API key

### Testing Your Setup

Create a test file to verify everything works:


# test_api.py
import requests
import json

# Test chat endpoint
def test_chat():
    url = "http://127.0.0.1:8000/chat"
    headers = {"x-api-key": "your-secret-key"}
    data = {"prompt": "Hello, EBAD!"}
    
    response = requests.post(url, json=data, headers=headers)
    print("Chat Response:", response.json())

# Test voice endpoint
def test_voice():
    url = "http://127.0.0.1:8000/voice"
    headers = {"x-api-key": "your-secret-key"}
    
    with open("test_audio.wav", "rb") as audio_file:
        files = {"file": audio_file}
        data = {"prompt": "Transcribe this audio"}
        response = requests.post(url, files=files, data=data, headers=headers)
        print("Voice Response:", response.json())

if __name__ == "__main__":
    test_chat()
    # test_voice()  # Uncomment when you have an audio file


Run: `python test_api.py`

## 🚀 Deployment

### Local Development

uvicorn api:app --reload --host 0.0.0.0 --port 8000


### Production Deployment

uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4


### Docker Deployment
Create `Dockerfile`:

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]


Build and run:

docker build -t ebad-api .
docker run -p 8000:8000 ebad-api


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
- FastAPI team for the amazing framework
- Marvel Studios for Iron Man inspiration
- Open source community for various libraries
- Smartera Organization for project mentorship and technical guidance

## 🚀 Future Enhancements

- [ ] Async endpoint optimization
- [ ] Rate limiting and throttling
- [ ] Database integration for conversation history
- [ ] WebSocket support for real-time communication
- [ ] Docker containerization
- [ ] Health check endpoints
- [ ] API versioning
- [ ] Comprehensive testing suite
- [ ] Performance monitoring and analytics
- [ ] Multi-language support

---

**Made with ❤️ and inspired by Tony Stark's JARVIS**

*"Sometimes you gotta run before you can walk." - Tony Stark*


