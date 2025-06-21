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
    
    def get_ebad_prompt(self, user_input):
        """Format user input with EBAD personality"""
        return f"You are EBAD (Electronic Brain and Assistant Droid), an AI assistant inspired by JARVIS from Iron Man. Respond in a helpful, intelligent, and slightly sophisticated manner. User query: {user_input}"
