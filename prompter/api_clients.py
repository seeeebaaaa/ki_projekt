import os
import ollama
from abc import ABC, abstractmethod
from typing import Literal
from enum import Enum
from google import genai
from google.genai import types
from pydantic import BaseModel


class CodeComment(BaseModel):
    type: Literal["function", "class"]
    name: str
    documentation: str


class CommentList(BaseModel):
    comments: list[CodeComment]


# Base interface for AI API communication
class AI_API(ABC):
    file_path = os.path.dirname(__file__)
    with open(os.path.join(file_path, "prompt_system"), "r") as file:
        system_instruction = file.read()
    with open(os.path.join(file_path, "prompt_user"), "r") as file:
        user_instruction = file.read()

    class Models(str, Enum):
        pass

    def __init__(self, model: Models):
        self.client
        self.model

    @abstractmethod
    def simple_prompt(self, prompt: str) -> str:
        """Generate text based on the given prompt."""
        pass

    @abstractmethod
    def generate_docs(self, input_code) -> CommentList:
        """Generate documentation based on the given code."""
        pass


# Google GenAI implementation
class GoogleGenAI_API(AI_API):

    class Models(AI_API.Models):
        GEMINI_2x0_FLASH = "gemini-2.0-flash"
        GEMINI_2x0 = "gemini-2.0"
        GEMINI_1x5 = "gemini-1.5"
        GEMINI_1x5_FLASH = "gemini-1.5-flash"

    def __init__(self, model: Models = Models.GEMINI_2x0_FLASH):
        api_key = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def simple_prompt(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )
        return response.text

    def generate_docs(self, input_code):
        user_instruction = (
            self.user_instruction + f"Here is a code snippet: {input_code}"
        )

        response_format = CommentList.model_json_schema()

        response = self.client.models.generate_content(
            model=self.model,
            contents=user_instruction,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                response_mime_type="application/json",
                response_schema=response_format,
            ),
        )
        comment_list = CommentList.model_validate_json(response.text)
        return comment_list


# Ollama implementation
class Ollama_API(AI_API):

    class Models(AI_API.Models):
        CODELLAMA_70B = "codellama:70b"
        CODELLAMA_7B_INSTRUCT = "codellama:7b-instruct"
        DEEPSSEKR1_14B = "deepseek-r1:14b"
        DEEPSSEKR1_70B = "deepseek-r1:70b"
        DEEPSSEKR1_LATEST = "deepseek-r1:latest"
        DEEPSSEKR1_1x5B = "deepseek-r1:1.5b"
        LLAMA33_70B = "llama3.3:70b"
        LLAMA33_LATEST = "llama3.3:latest"
        LLAMA33_70B_INSTRUCT = "llama3.3:70b-instruct-q3_K_M"
        LLAMA31_70B = "llama3.1:70b"
        LLAMA33_70B_TEXT = "llama3:70b-text"
        LLAMA3_8B = "llama3:8b"
        LLAMA31_8B = "llama3.1:8b"
        LLAMA31_LATEST = "llama3.1:latest"
        LLAMA32_LATEST = "llama3.2:latest"
        LLAMA3_LATEST = "llama3:latest"
        LLAMA3_70B = "llama3:70b"
        MIXTRAL_8x7B = "mixtral:8x7b"
        NEMOTRON_LATEST = "nemotron:latest"
        NOMIC_EMBED_TEXT_LATEST = "nomic-embed-text:latest"

    server_url = "https://im-kigs-openwebui.oth-regensburg.de/ollama/"

    def __init__(self, model: Models = Models.DEEPSSEKR1_70B):
        self.model = model
        api_key = os.getenv("OPENWEBUI_API_KEY")
        self.client = ollama.Client(
            host=self.server_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )

    def simple_prompt(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat(model=self.model, messages=messages)
        return response.message.content

    def generate_docs(self, input_code):
        # self.user_instruction = "Follow common Python docstring conventions."
        code_prompt = f"Here is a code snippet: {input_code}"

        response_format = CommentList.model_json_schema()

        messages = [
            {"role": "system", "content": self.system_instruction},
            {"role": "user", "content": self.user_instruction},
            {"role": "user", "content": code_prompt},
        ]
        response = self.client.chat(
            model=self.model, messages=messages, format=response_format
        )
        comment_list = CommentList.model_validate_json(response.message.content)
        return comment_list
