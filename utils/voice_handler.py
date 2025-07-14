import speech_recognition as sr
import io
import wave
import tempfile
import os

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Add any other init logic from your original code here

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
