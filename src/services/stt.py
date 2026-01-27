import speech_recognition as sr

class STTService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_data):
        try:
            # Send audio to Google
            text = self.recognizer.recognize_google(audio_data, language='en-in')
            return text.lower()
        except Exception:
            return None¸