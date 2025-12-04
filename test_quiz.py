import requests
import json

response = requests.post(
    "http://127.0.0.1:8000/quiz",
    json={
        "subject": "Mathematics",
        "level": "Beginner",
        "num_questions": 2,
        "reveal_format": True
    }
)

print(f"Status Code: {response.status_code}")
print("Response:")
print(json.dumps(response.json(), indent=2))
