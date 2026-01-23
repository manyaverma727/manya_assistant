import pyttsx3

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()
        
        # CONFIGURATION
        self.engine.setProperty('rate', 170) 

        # voice ka gender 0 for male and 1 for female
        voices = self.engine.getProperty('voices')
        try:
            self.engine.setProperty('voice', voices[1].id)
        except IndexError:
            self.engine.setProperty('voice', voices[0].id)

    def speak(self, text):
        """
        Input: String (Text)
        Output: Audio (Sound)
        """
        if not text:
            return
            
        print(f"ASSISTANT: {text}")
        self.engine.say(text)
        self.engine.runAndWait()