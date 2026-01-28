import os
from groq import Groq

class GroqBrain:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.history = [
            {"role": "system", "content": "You are Aether, a concise and witty AI assistant. Keep answers under 2 sentences."}
        ]
    
    def think(self, user_text):
        self.history.append({"role": "user", "content": user_text})
        completion = self.client.chat.completions.create(
            messages=self.history,
            model="llama3-70b-8192"
        )
        response = completion.choices[0].message.content
        self.history.append({"role": "assistant", "content": response})
        return response
