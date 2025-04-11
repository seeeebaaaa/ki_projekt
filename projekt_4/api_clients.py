import os
import ollama
from abc import ABC, abstractmethod
from google import genai

# Base interface for AI API communication
class AIAPI(ABC):
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """Generate text based on the given prompt."""
        pass

# Google GenAI implementation
class GoogleGenAI(AIAPI):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model= "gemini-2.0-flash"

    def generate_text(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )
        return response.text

# Ollama implementation
class OllamaAPI(AIAPI):
    def __init__(self):
        self.server_url = "https://im-kigs.oth-regensburg.de/openwebui/ollama/api/chat"
        self.model = "llama3.2"
        self.client = ollama.Client(
            host=self.server_url,
            model=self.model,
        )

    def generate_text(self, prompt: str) -> str:
        messages = [
                {"role": "user", "content": prompt}
            ]
        return self.client.chat(messages=messages)
