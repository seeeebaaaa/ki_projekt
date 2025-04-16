# 12.04.25 Gemini Flash 2.0
> used completely uncommented file api_clients for test
<details>
<summary>Commented code</summary>

```python
import os
import ollama
from abc import ABC, abstractmethod
from google import genai
from google.genai import types

# Base interface for AI API communication
class AIAPI(ABC):
    """
    Abstract base class for interacting with different AI APIs.
    Defines the basic structure for AI API implementations.
    """
    def __init__(self):
        """
        Initializes the AIAPI class.
        Defines client and model attributes. These should be initialized in the subclasses.
        """
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
    """
    Implementation of the AIAPI for Google's Gemini GenAI model.
    Uses the google-generative-ai library to interact with the Gemini API.
    """
    def __init__(self):
        """
        Initializes the GoogleGenAI client with the API key and model.
        The API key is retrieved from the environment variable GOOGLE_API_KEY.
        The model is set to "gemini-2.0-flash".
        """
        api_key=os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model= "gemini-2.0-flash"

    def simple_prompt(self, prompt: str) -> str:
        """
        Generates text based on the given prompt using the Gemini model.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            str: The generated text response from the model.
        """
        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )
        return response.text

    def generate_docs(self, input_code):
        """
        Generates documentation for the given code snippet using the Gemini model.

        Args:
            input_code (str): The code snippet to document.

        Returns:
            str: The generated documentation for the code snippet.
        """
        system_instruction = ["You are a code documentation engine. Users will provide you with code snippets and you will generate technical documentation describing what the code does.",
                                "Please provide the documentation in the form of code comments that can be inserted into the code.",
                                "If the snippet already has documentation, check if it correctly describes the code. If so, do NOT generate new documentation."]
        user_instruction = [f"Here is the code snippet: {input_code}"]

        response = self.client.models.generate_content(
            model=self.model,
            contents=user_instruction,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            )
        )
        return response.text

# Ollama implementation
class OllamaAPI(AIAPI):
    """
    Implementation of the AIAPI for the Ollama model.
    Uses the ollama library to interact with the Ollama API.
    """
    def __init__(self):
        """
        Initializes the OllamaAPI client with the server URL and model.
        The server URL is set to "https://im-kigs.oth-regensburg.de/openwebui/ollama/".
        The model is set to "llama3.2".
        """
        self.server_url = "https://im-kigs.oth-regensburg.de/openwebui/ollama/"
        self.model = "llama3.2"
        self.client = ollama.Client(
            host=self.server_url,
        )

    def simple_prompt(self, prompt: str) -> str:
        """
        Generates text based on the given prompt using the Ollama model.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            str: The generated text response from the model.
        """
        messages = [
                {"role": "user", "content": prompt}
            ]
        response = self.client.chat(model=self.model, messages=messages)
        return response.message.content

    def generate_docs(self, input_code):
        """
        Generates documentation for the given code snippet using the Ollama model.

        Args:
            input_code (str): The code snippet to document.

        Returns:
            str: The generated documentation for the code snippet.
        """
        system_instruction = ["You are a code documentation engine. Users will provide you with code snippets and you will generate technical documentation describing what the code does.",
                                "Please provide the documentation in the form of code comments that can be inserted into the code.",
                                "If the snippet already has documentation, check if it correctly describes the code. If so, do NOT generate new documentation."]
        user_instruction = [f"Here is the code snippet: {input_code}"]
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_instruction}
        ]
        response = self.client.chat(model=self.model, messages=messages)
        return response.message.content
```
</details>