import os
import time
from colorama import Fore, Style, init
from dotenv import load_dotenv

from core.stt import GroqEar
from core.llm import GroqBrain
from core.tts import EdgeMouth
from utils.audio import AudioInterface

init(autoreset=True)
load_dotenv()

def main():
    print(f"{Fore.CYAN}⚡ AETHER System 06 Initializing...{Style.RESET_ALL}")
    
    try:
        ear = GroqEar()
        brain = GroqBrain()
        mouth = EdgeMouth()
        audio = AudioInterface()
    except Exception as e:
        print(f"{Fore.RED}⚠️ Initialization Error: {e}{Style.RESET_ALL}")
        return

    mode = "VOICE" if audio.has_input else "TEXT"
    print(f"{Fore.YELLOW}ℹ️  Mode: {mode} (Input Device Detected: {audio.has_input}){Style.RESET_ALL}")
    
    while True:
        try:
            user_text = ""
            
            # --- 1. LISTEN ---
            if mode == "VOICE":
                input(f"\n{Fore.GREEN}🎤 Press ENTER to record (3s)...{Style.RESET_ALL}")
                print(f"{Fore.RED}🔴 Recording...{Style.RESET_ALL}")
                success = audio.record(seconds=3, filename="input.wav")
                if success:
                    print(f"{Fore.BLUE}🔄 Transcribing...{Style.RESET_ALL}")
                    try:
                        user_text = ear.transcribe("input.wav")
                    except Exception as e:
                        print(f"{Fore.RED}⚠️ Transcription failed: {e}{Style.RESET_ALL}")
                        continue
                else:
                    print("❌ Audio capture failed.")
                    continue
            else:
                user_text = input(f"\n{Fore.GREEN}⌨️  Input > {Style.RESET_ALL}")

            if not user_text:
                continue
                
            print(f"{Fore.WHITE}👤 User: {user_text}{Style.RESET_ALL}")
            
            # --- 2. THINK ---
            print(f"{Fore.MAGENTA}🧠 Thinking...{Style.RESET_ALL}")
            try:
                response = brain.think(user_text)
                print(f"{Fore.CYAN}🤖 Aether: {response}{Style.RESET_ALL}")
            except Exception as e:
                 print(f"{Fore.RED}⚠️ Thinking failed: {e}{Style.RESET_ALL}")
                 continue
            
            # --- 3. SPEAK ---
            print(f"{Fore.YELLOW}🔊 Speaking...{Style.RESET_ALL}")
            try:
                mouth.speak(response, "output.mp3")
                audio.play("output.mp3")
            except Exception as e:
                print(f"{Fore.RED}⚠️ Speaking failed: {e}{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}🛑 System Shutdown.{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}⚠️ Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
