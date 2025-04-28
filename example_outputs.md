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

# 21.04.25 Ollama Llama 3.3
> uncommented file api_clients. Provided a JSON description for response format

Previous tests with Llama 3.2 were not really successful. Though that was using a 3.2B model, while the default Llama3.3 is a 70B model.

<details>
<summary>response_format</summary>

```python 
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
```
</details>
<details>
<summary>JSON response</summary>

```python
{
  "comments": [
    {
      "type": "module",
      "name": "AI API communication module",
      "documentation": "# Module for communicating with AI APIs. It provides a base interface and two implementations: Google GenAI and OllamaAPI."
    },
    {
      "type": "class",
      "name": "AIAPI",
      "documentation": "# Base interface for AI API communication.\n# Abstract class that defines the methods to be implemented by its subclasses."
    },
    {
      "type": "method",
      "name": "__init__",
      "documentation": "# Initializes the AIAPI object. It sets up the client and model attributes, but does not assign any values to them."
    },
    {
      "type": "method",
      "name": "simple_prompt",
      "documentation": "# Generates text based on the given prompt.\n# Abstract method that must be implemented by subclasses."
    },
    {
      "type": "method",
      "name": "generate_docs",
      "documentation": "# Generates documentation based on the given code.\n# Abstract method that must be implemented by subclasses."
    },
    {
      "type": "class",
      "name": "GoogleGenAI",
      "documentation": "# Google GenAI implementation of the AIAPI interface."
    },
    {
      "type": "method",
      "name": "__init__",
      "documentation": "# Initializes the GoogleGenAI object. It sets up the client and model attributes using the Google API key and 'gemini-2.0-flash' model, respectively."
    },
    {
      "type": "method",
      "name": "simple_prompt",
      "documentation": "# Generates text based on the given prompt using the Google GenAI API.\n# Returns the generated text as a string."
    },
    {
      "type": "method",
      "name": "generate_docs",
      "documentation": "# Generates documentation based on the given code using the Google GenAI API.\n# Returns the generated documentation as a string."
    },
    {
      "type": "class",
      "name": "OllamaAPI",
      "documentation": "# Ollama implementation of the AIAPI interface."
    },
    {
      "type": "method",
      "name": "__init__",
      "documentation": "# Initializes the OllamaAPI object. It sets up the client and model attributes using the 'https://im-kigs.oth-regensburg.de/openwebui/ollama/' server URL and 'llama3.3' model, respectively."
    },
    {
      "type": "method",
      "name": "simple_prompt",
      "documentation": "# Generates text based on the given prompt using the Ollama API.\n# Returns the generated text as a string."
    },
    {
      "type": "method",
      "name": "generate_docs",
      "documentation": "# Generates documentation based on the given code using the Ollama API.\n# Returns the generated documentation in JSON format, with comments for each described code block."
    }
  ]
}
```
</details>

# 21.04.25 Ollama Deepseek-R1:70b
> uncommented file api_clients. Provided a JSON description for response format

<details>
<summary>response_format</summary>

```python 
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
```
</details>

<details>
<summary>JSON response</summary>

```python
{
    "comments": [
        {
            "type": "module",
            "name": "",
            "documentation": "This module provides an interface to interact with different AI APIs for generating documentation.",
        },
        {
            "type": "class",
            "name": "AIAPI",
            "documentation": "Abstract base class providing the interface for AI API communication. It defines methods that must be implemented by subclasses: simple_prompt and generate_docs.",
        },
        {
            "type": "method",
            "name": "simple_prompt",
            "documentation": "Generates text based on a given prompt. This method is abstract and should be implemented by each subclass to handle the specifics of their respective AI API.",
        },
        {
            "type": "method",
            "name": "generate_docs",
            "documentation": "Generates technical documentation for the provided code input. This method is abstract and must be implemented by subclasses according to the specific requirements of each AI service.",
        },
        {
            "type": "class",
            "name": "GoogleGenAI",
            "documentation": "Implementation of AIAPI using Google GenAI. Configures a client with the Gemini model and implements methods for generating text and documentation.",
        },
        {
            "type": "method",
            "name": "simple_prompt",
            "documentation": "Sends a prompt to the Google GenAI API and returns the generated response.",
        },
        {
            "type": "method",
            "name": "generate_docs",
            "documentation": "Generates code comments for the provided input_code using the Gemini model. It constructs appropriate system and user instructions and processes the response accordingly.",
        },
        {
            "type": "class",
            "name": "OllamaAPI",
            "documentation": "Implementation of AIAPI using Ollama. Configures a client to communicate with an external Ollama server and implements methods for generating text and documentation in a specific JSON format.",
        },
        {
            "type": "method",
            "name": "simple_prompt",
            "documentation": "Sends a prompt to the Ollama API and returns the generated response.",
        },
        {
            "type": "method",
            "name": "generate_docs",
            "documentation": "Generates code comments for the provided input_code using the Ollama service. It constructs system instructions, sends the request, and parses the JSON-formatted response containing the documentation.",
        },
    ]
}
```
</details>

# 28.04.25 Gemini Flash 2.0
> uncommented file api_clients. Provided an output format defined through Pydantic classes

<details>
<summary>Pydantic definition</summary>

```python
class CodeComment(BaseModel):
    type: Literal["function", "class"]
    name: str
    documentation: str


class CommentList(BaseModel):
    comments: list[CodeComment]
```
</details>

<details>
<summary>Response, parsed to JSON</summary>

```python
comments = [
    CodeComment(
        type="function",
        name="import",
        documentation="Imports necessary libraries and modules for the code, including os, json, ollama, abc, typing, enum, google.genai, google.genai.types and pydantic.",
    ),
    CodeComment(
        type="class",
        name="CodeComment",
        documentation="Represents a code comment with its type, name, and documentation string.",
    ),
    CodeComment(
        type="class",
        name="CommentList",
        documentation="Represents a list of code comments.",
    ),
    CodeComment(
        type="class",
        name="AI_API",
        documentation="Base interface for AI API communication. Attributes: system_instruction (str): Instructions for the AI model to act as a code documentation engine. user_instruction (str): Instructions for the AI model to generate documentation based on a given schema. Models (Enum): An enumeration of available models (to be implemented in subclasses). ",
    ),
    CodeComment(
        type="function",
        name="simple_prompt",
        documentation="Abstract method for generating text based on the given prompt. Args: prompt (str): The input prompt for text generation. Returns: str: The generated text. ",
    ),
    CodeComment(
        type="function",
        name="generate_docs",
        documentation="Abstract method for generating documentation based on the given code. Args: input_code (str): The code snippet to generate documentation for. Returns: CommentList: A list of code comments. ",
    ),
    CodeComment(
        type="class",
        name="GoogleGenAI_API",
        documentation="Google GenAI implementation of the AI_API. Attributes: client: The Google GenAI client. model: The selected Google GenAI model. ",
    ),
    CodeComment(
        type="function",
        name="__init__",
        documentation="Initializes the GoogleGenAI_API with a specified model and sets up the client. Args: model (Models): The Google GenAI model to use. Defaults to GEMINI_2x0_FLASH. ",
    ),
    CodeComment(
        type="function",
        name="simple_prompt",
        documentation="Generates text based on the given prompt using the Google GenAI model. Args: prompt (str): The input prompt for text generation. Returns: str: The generated text from the Google GenAI model. ",
    ),
    CodeComment(
        type="function",
        name="generate_docs",
        documentation="Generates documentation based on the given code using the Google GenAI model. Args: input_code (str): The code snippet to generate documentation for. Returns: CommentList: A list of code comments generated by the Google GenAI model. ",
    ),
    CodeComment(
        type="class",
        name="Ollama_API",
        documentation="Ollama implementation of the AI_API. Attributes: model: The selected Ollama model. client: The Ollama client. server_url (str): The URL of the Ollama server. ",
    ),
    CodeComment(
        type="function",
        name="__init__",
        documentation="Initializes the Ollama_API with a specified model and sets up the client. Args: model (Models): The Ollama model to use. Defaults to DEEPSSEKR1_70B. ",
    ),
    CodeComment(
        type="function",
        name="simple_prompt",
        documentation="Generates text based on the given prompt using the Ollama model. Args: prompt (str): The input prompt for text generation. Returns: str: The generated text from the Ollama model. ",
    ),
    CodeComment(
        type="function",
        name="generate_docs",
        documentation="Generates documentation based on the given code using the Ollama model. Args: input_code (str): The code snippet to generate documentation for. Returns: CommentList: A list of code comments generated by the Ollama model. ",
    ),
]
```