import os
import json
import ollama
from abc import ABC, abstractmethod
from google import genai
from google.genai import types

# Base interface for AI API communication
class AIAPI(ABC):
    def __init__(self):
        self.client
        self.model

    @abstractmethod
    def simple_prompt(self, prompt: str) -> str:
        """Generate text based on the given prompt."""
        pass

    @abstractmethod
    def generate_docs(self, input_code):
        """Generate documentation based on the given code."""
        pass

# Google GenAI implementation
class GoogleGenAI(AIAPI):
    def __init__(self):
        api_key=os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model= "gemini-2.0-flash"

    def simple_prompt(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )
        return response.text

    def generate_docs(self, input_code):
        system_instruction = ["You are a code documentation engine. Users will provide you with code snippets and you will generate technical documentation describing what the code does.",
                                "Please provide the documentation in the form of code comments that can be inserted into the code.",
                                "If the snippet already has documentation, check if it correctly describes the code. If so, do NOT generate new documentation."]
        user_instruction = [f"Here is the code snippet: {input_code}"]

        response_format = {
                "type": "object",
                "properties": {
                    "comments": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "description": "The type of the described code block (e.g., class, function, variable, etc.)."
                                },
                                "name": {
                                    "type": "string",
                                    "description": "The name of the code object (e.g., function or class name)."
                                },
                                "documentation": {
                                    "type": "string",
                                    "description": "The generated documentation for the code object."
                                }
                            },
                            "required": ["type", "name", "documentation"]
                        }
                    }
                },
                "required": ["comments"]
            }

        response = self.client.models.generate_content(
            model=self.model,
            contents=user_instruction,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=response_format,
            )
        )
        json_response = json.loads(response.text)
        return json_response

# Ollama implementation
class OllamaAPI(AIAPI):
    def __init__(self):
        self.server_url = "https://im-kigs.oth-regensburg.de/openwebui/ollama/"
        self.model = "deepseek-r1:70b"
        self.client = ollama.Client(
            host=self.server_url,
        )

    def simple_prompt(self, prompt: str) -> str:
        messages = [
                {"role": "user", "content": prompt}
            ]
        response = self.client.chat(model=self.model, messages=messages)
        return response.message.content

    def generate_docs(self, input_code):
        system_instruction = """You are a code documentation engine. Users will provide you with code snippets and you will generate technical documentation describing what the code does.
                                Please provide the documentation in the form of code comments that can be inserted into the code.
                                If the snippet already has documentation, check if it correctly describes the code. If so, do NOT generate new documentation.
                                Respond using JSON."""
        user_instruction = f"Here is the code snippet: {input_code}"

        response_format = {
                "type": "object",
                "properties": {
                    "comments": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "description": "The type of the described code block (e.g., class, function, variable, etc.)."
                                },
                                "name": {
                                    "type": "string",
                                    "description": "The name of the code object (e.g., function or class name)."
                                },
                                "documentation": {
                                    "type": "string",
                                    "description": "The generated documentation for the code object."
                                }
                            },
                            "required": ["type", "name", "documentation"]
                        }
                    }
                },
                "required": ["comments"]
            }

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_instruction},
        ]
        response = self.client.chat(model=self.model, messages=messages, format=response_format)
        # return response.message.content
        json_response = json.loads(response.message.content)
        return json_response