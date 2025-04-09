# Ehrlich gesagt hat nichts von dem hier richtig gut funktioniert oder kostet zu viel...



import requests

API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"
headers = {"Authorization": "Bearer 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"}
payload = {
    "messages": [
        {
            "role": "user",
            "content": "How many 'G's in 'huggingface'?"
        }
    ],
    "model": "meta-llama/Llama-3.1-8B-Instruct",
}

# response = requests.post(API_URL, headers=headers, json=payload)
# print(response.json()["choices"][0]["message"])
# print(response.json())






url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
token = "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"  # Replace with your Hugging Face token

parameters = {
    "max_new_tokens": 5000,
    "temperature": 0.01,
    "top_k": 50,
    "top_p": 0.95,
    "return_full_text": False
    }

prompt = "how many 'G's in hugginface?"

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}


payload = {
    "inputs": prompt,
    "parameters": parameters
}

response = requests.post(url, headers=headers, json=payload)
response_text = response.json()[0]['generated_text'].strip()










# Use a pipeline as a high-level helper
# from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
# pipe = pipeline("text-generation", model="meta-llama/Llama-3.1-8B-Instruct", trust_remote_code=True)
# pipe(messages)