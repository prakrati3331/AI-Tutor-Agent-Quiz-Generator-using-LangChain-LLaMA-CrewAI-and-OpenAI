import requests
import json

def test_quiz_endpoint():
    url = "http://127.0.0.1:8000/quiz"
    payload = {
        "subject": "Mathematics",
        "level": "Beginner",
        "num_questions": 2,
        "reveal_format": True
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_quiz_endpoint()
