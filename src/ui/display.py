from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.spinner import Spinner
import datetime

console = Console()

class AetherUI:
    def __init__(self):
        self.layout = Layout()
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="status", size=3)
        )
        self.console = console

    def header(self):
        title = Text("AETHER - SYSTEM 06/300", style="bold cyan")
        time_str = datetime.datetime.now().strftime("%H:%M")
        header_text = Text(f"{time_str} | L5 Access Granted", style="dim white")
        return Panel(Align.center(title + "\n" + header_text), style="cyan")

    def status_panel(self, status="IDLE", color="green"):
        return Panel(Align.center(f"STATUS: {status}"), style=f"bold {color}")

    def display_message(self, role, content, color="white"):
        self.console.print(Panel(content, title=role, style=color))

    def show_listening(self):
        self.console.print(Align.center(Spinner("dots", text="Listening...", style="green")))

    def show_thinking(self):
        self.console.print(Align.center(Spinner("bouncingBar", text="Thinking...", style="magenta")))
