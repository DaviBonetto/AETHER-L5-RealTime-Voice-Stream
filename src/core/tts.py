import edge_tts
import asyncio

class EdgeMouth:
    def __init__(self, voice="en-US-ChristopherNeural"):
        self.voice = voice
    
    async def _save_audio(self, text, filename):
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(filename)

    def speak(self, text, filename="output.mp3"):
        asyncio.run(self._save_audio(text, filename))
        return filename
