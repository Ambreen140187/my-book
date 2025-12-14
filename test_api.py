import requests
import json

# Test the backend API
def test_backend():
    url = "http://localhost:8000/ask"

    # Test data
    test_data = {
        "question": "Hello, are you working?",
        "selected_text": None
    }

    try:
        response = requests.post(url, json=test_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend API is working!")
            print(f"Response: {data}")
            return True
        else:
            print(f"❌ Backend API returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend API connection...")
    test_backend()