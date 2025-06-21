import speech_recognition as sr
import streamlit as st

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
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
            
        except sr.WaitTimeoutError:
            st.error("⏰ No speech detected. Please try again.")
            return None
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio. Please try again.")
            return None
        except Exception as e:
            st.error(f"❌ Voice system error: {e}")
            return None

