import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "HTTP-Referer": "http://localhost:3000",
    "Content-Type": "application/json"
}

data = {
    "model": "openai/gpt-3.5-turbo",  # Using a verified model
    "messages": [
        {"role": "user", "content": "Hello, testing my API key with OpenRouter!"}
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    print("Response:", result['choices'][0]['message']['content'])
except Exception as e:
    print(f"Error: {e}")
    if 'response' in locals():
        print("Response content:", response.text)