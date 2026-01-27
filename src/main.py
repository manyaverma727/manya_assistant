import sys
sys.dont_write_bytecode = True  # Prevent __pycache__ folders

import speech_recognition as sr
import pyaudio  #/*microphone ko access karega and continuous sounds lega*/
import os           #/*work with file paths..accross diff platforms jaise windows,mac,linux*/
from colorama import Fore, Style, init         # /*color add karega n terminal fore for red green and cyan(silence,speaking,ystem msg),,style to reset color back to normal */

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))

#import ho rhi meri files*/
from src.core import config
from src.audio import vad
from src.services.stt import STTService
from src.services.tts import TTSService

init() #/*colorama ko initialize karega*/

def main():
    stt = STTService()
    tts = TTSService()
    
    # /* Microphone ko access karega smartly using speech_recognition lib */
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone(sample_rate=config.RATE) as source:
            print(f"{Fore.CYAN}System Initialized. Adjusting for noise...{Style.RESET_ALL}")
            
            # /* Background noise (fan/AC) ko measure karke ignore karega */
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            # /* Humara calibrated threshold set karega taaki sensitivity perfect ho */
            recognizer.energy_threshold = config.VAD_THRESHOLD
            tts.speak("Hello, I am online.")
            
            print("-" * 50)
            print(f"{Fore.GREEN}Ready! Listening... (Ctrl+C to stop){Style.RESET_ALL}")

            while True:
                try:
                    print("Listening...", end="\r")
                    
                    # /* It captures continuous sounds until silence is detected (Auto VAD) */
                    audio = recognizer.listen(source, timeout=None)
                    
                    print(f"\n{Fore.YELLOW}Processing...{Style.RESET_ALL}")
                    
                    # /* Audio bucket ko Text me convert karega (Google API call) */
                    text = stt.transcribe(audio)
                    
                    if text:
                        print(f"{Fore.CYAN}YOU SAID: {text}{Style.RESET_ALL}")
                        
                        if "hello" in text:
                            tts.speak("Hello!, i am jenny.How can i help you?")
                        elif "how are you" in text:
                            tts.speak("I am good, thank you! How about you?")
                        elif "play" in text:
                            song_name=text.replace("play", "").strip()
                            
                            tts.speak(f"Playing {song_name} on YouTube")
                            
                            pywhatkit.playonyt(song_name)
                        elif "time" in text:
                            from datetime import datetime
                            current_time = datetime.now().strftime("%I:%M %p")
                            tts.speak(f"It is currently {current_time}")
                            
                        elif "stop" in text or "exit" in text:
                            tts.speak("Goodbye!, glad to help you")
                            break
                            
                        else:
                            # /* Echo back logic if command not found */
                            tts.speak("I heard " + text)
                    
                    else:
                        print(f"{Fore.RED}Could not understand.{Style.RESET_ALL}")
                        
                except KeyboardInterrupt:
                    print("\nStopping...")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    
    except Exception as e:
        print(f"{Fore.RED}Error opening microphone: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()