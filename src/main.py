import os
import time
from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv

from core.stt import GroqEar
from core.llm import GroqBrain
from core.tts import EdgeMouth
from utils.audio import AudioInterface
from ui.display import AetherUI

load_dotenv()

def main():
    ui = AetherUI()
    console = Console()
    
    console.print(ui.header())
    
    try:
        ear = GroqEar()
        brain = GroqBrain()
        mouth = EdgeMouth()
        audio = AudioInterface()
    except Exception as e:
        ui.status_panel("INIT ERROR", "red")
        console.print(f"[bold red]System Failure: {e}[/]")
        return

    mode = "VOICE" if audio.has_input else "TEXT"
    console.print(ui.status_panel(f"ONLINE ({mode})", "green"))
    
    while True:
        try:
            user_text = ""
            
            # --- 1. LISTEN ---
            if mode == "VOICE":
                console.print("[dim]Press ENTER to speak...[/]")
                input() 
                ui.show_listening()
                # Increased to 15s per user request
                success = audio.record(seconds=15, filename="input.wav")
                if success:
                    try:
                        user_text = ear.transcribe("input.wav")
                    except Exception as e:
                        console.print(f"[red]Stt Error: {e}[/]")
                        continue
                else:
                    console.print("[red]Mic Error[/]")
                    continue
            else:
                user_text = Prompt.ask("[bold green]Input >[/]")

            if not user_text:
                continue
                
            ui.display_message("User", user_text, "green")
            
            # --- 2. THINK ---
            ui.show_thinking()
            try:
                response = brain.think(user_text)
                ui.display_message("Aether", response, "cyan")
            except Exception as e:
                 console.print(f"[red]Thinking Error: {e}[/]")
                 continue
            
            # --- 3. SPEAK ---
            try:
                mouth.speak(response, "output.mp3")
                audio.play("output.mp3")
            except Exception as e:
                console.print(f"[red]TTS Error: {e}[/]")
            
        except KeyboardInterrupt:
            console.print(ui.status_panel("OFFLINE", "red"))
            break
        except Exception as e:
            console.print(f"[bold red]Critical Error: {e}[/]")

if __name__ == "__main__":
    main()
