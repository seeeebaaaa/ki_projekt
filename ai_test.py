import os
from dotenv import load_dotenv
from projekt_4.api_clients import GoogleGenAI, OllamaAPI
from parser.parse_file import python_parse_file

code = None
file_path = os.path.join(os.path.dirname(__file__), "projekt_4", "api_clients.py")
with open (file_path, "r") as file:
    code = file.read()

ast_code = python_parse_file(file_path)

# Example usage
if __name__ == "__main__":
    load_dotenv()
    gemini = GoogleGenAI(GoogleGenAI.Models.GEMINI_2x0_FLASH)
    ollama = OllamaAPI(OllamaAPI.Models.DEEPSSEKR1_70B)
    # print(ai_api.simple_prompt("what is the capital of denmark?"))
    # docu_ollama = ollama.generate_docs(code)

    docu_gemini = gemini.generate_docs(code)

    print(docu_gemini.comments[2].model_dump_json())