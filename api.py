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
