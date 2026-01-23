import speech_recognition as sr
import pyaudio.  #/*microphone ko access karega and continuous sounds lega*/
import sys         #/* helps python to find file path in src folder*/
import os           #/*work with file paths..accross diff platforms jaise windows,mac,linux*/
import colorama import fore,Style,init         # /*color add karega n terminal fore for red green and cyan(silence,speaking,ystem msg),,style to reset color back to normal */

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))

#import ho rhi meri files*/
from src.core import config
from src.audio import vad
from src.services.stt import STTService
from src.services.tts import TTSService

init() #/*colorama ko initialize karega*/

def main():
    p=pyaudio.PyAudio() #/*microphone setup karega*/
    try:
        stream = p.open(
            format=pyaudio.paInt16,
            channels=config.CHANNELS,
            rate=config.RATE,
            input=True,
            frames_per_buffer=config.CHUNK_SIZE
        )
    except Exception as e:
        print(f"{Fore.RED}Error opening microphone: {e}{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}System Initialized. Listening... (Press Ctrl+C to stop){Style.RESET_ALL}")
    print("-" * 50)

    try:
        while True:
            # audio input read karega
            # exception_on_overflow=False crash hone se bachaega if computer is slow
            rawd=stream.read(config.CHUNK_SIZE, exception_on_overflow=False)
            
            # energy calcs
            ener=vad.calculate_rms(rawd)


            # OUTPUT PART
            # bar which throws energy
            barl=int(ener/20)  # scale down karne ke liye divide by 20
            bar="█"*barl
            # sochega if silence ha ya bol rha
            if ener>config.VAD_THRESHOLD:
                status=f"{Fore.GREEN}SPEAKING{Style.RESET_ALL}"
            else:
                status=f"{Fore.RED}SILENCE{Style.RESET_ALL}"
            
            # Print on the same line using \r
            print(f"\rEnergy:{int(energy):04d}|{status}|{bar}",end="")
            
    except KeyboardInterrupt:
        print("\nStopping...")
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()