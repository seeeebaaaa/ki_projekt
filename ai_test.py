import os
from dotenv import load_dotenv
from projekt_4.api_clients import GoogleGenAI_API, Ollama_API
from parser.parse_file import python_parse_file

code = None
file_path = os.path.join(os.path.dirname(__file__), "projekt_4", "api_clients.py")
with open (file_path, "r") as file:
    code = file.read()

ast_code = python_parse_file(file_path)

# Example usage
if __name__ == "__main__":
    load_dotenv()
    gemini = GoogleGenAI_API(GoogleGenAI_API.Models.GEMINI_2x0_FLASH)
    ollama = Ollama_API(Ollama_API.Models.LLAMA3_70B)
    # print(ai_api.simple_prompt("what is the capital of denmark?"))
    docu = ollama.generate_docs(code)

    # docu = gemini.generate_docs(code)

    print(docu.model_dump_json())