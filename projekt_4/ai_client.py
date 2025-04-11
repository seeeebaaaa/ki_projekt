from api_clients import AIAPI, GoogleGenAI, OllamaAPI

# AI Client wrapper
class AIClient:
    def __init__(self, api: AIAPI):
        self.api = api

    def generate_text(self, prompt: str) -> str:
        return self.api.generate_text(prompt)

# Example usage
if __name__ == "__main__":
    # Use Google GenAI
    google_api = GoogleGenAI(api_key="your-google-api-key")
    client = AIClient(api=google_api)
    print(client.generate_text("Hello, world!"))

    # Switch to Ollama
    ollama_api = OllamaAPI(server_url="http://localhost:8000")
    client = AIClient(api=ollama_api)
    print(client.generate_text("Hello, world!"))