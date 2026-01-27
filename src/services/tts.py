# src/services/tts.py
import asyncio
import edge_tts
import os
import subprocess

class TTSService:
    def __init__(self):
        self.voice = "en-US-JennyNeural"
        self.rate = "-10%"  #slow voice
        self.temp_file = "temp_voice.mp3"
        print(f"✓ Using Microsoft Jenny voice")

    def speak(self, text):
        if not text:
            return
            
        print(f"ASSISTANT: {text}")
        
        try:
            # Generate audio file
            asyncio.run(self._generate_audio(text))
            
            # Play audio using Mac's native player
            subprocess.run(['afplay', self.temp_file], check=True)
            
            # Cleanup temp file
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
                
        except Exception as e:
            print(f"Error in TTS: {e}")

    async def _generate_audio(self, text):
        
        communicate = edge_tts.Communicate(
            text, 
            self.voice,
            rate=self.rate
        )
        await communicate.save(self.temp_file)