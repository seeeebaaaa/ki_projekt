import os
from dotenv import load_dotenv
from api_clients import GoogleGenAI, OllamaAPI

code = None
file_path = os.path.join(os.path.dirname(__file__), "api_clients.py")
with open (file_path, "r") as file:
    code = file.read()

# Example usage
if __name__ == "__main__":
    load_dotenv()
    ai_api = GoogleGenAI()
    # ai_api = OllamaAPI()
    # print(ai_api.simple_prompt("what is the capital of denmark?"))
    print(ai_api.generate_docs(code))