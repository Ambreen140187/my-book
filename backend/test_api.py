import requests
import json
import time

def test_rag_api():
    """Test the RAG API with sample questions."""
    base_url = "http://localhost:8000"

    # Wait a moment for the server to start
    time.sleep(3)

    # Test questions
    test_questions = [
        {
            "question": "What is the main topic of this book?",
            "description": "General book topic question"
        },
        {
            "question": "What are the learning outcomes of the introduction chapter?",
            "description": "Specific content question"
        },
        {
            "question": "Can you explain artificial intelligence briefly?",
            "description": "Definition question"
        }
    ]

    print("Testing RAG API...")
    print("="*50)

    for i, test in enumerate(test_questions, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"Question: {test['question']}")

        try:
            response = requests.post(
                f"{base_url}/ask",
                json={
                    "question": test['question'],
                    "top_k": 3
                },
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                print(f"Answer: {data['answer'][:200]}...")
                print(f"Sources: {len(data['sources'])} found")
                print(f"Used selected text: {data['selected_text_used']}")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Exception occurred: {str(e)}")

    # Test with selected text
    print(f"\nTest {len(test_questions)+1}: Question with selected text")
    print("Question: What does this text explain?")

    try:
        response = requests.post(
            f"{base_url}/ask",
            json={
                "question": "What does this text explain?",
                "selected_text": "Artificial Intelligence is about creating machines that can think, reason, and learn like humans. It's not just about robots; it's about software that can perform tasks that typically require human intelligence.",
                "top_k": 3
            },
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"Answer: {data['answer'][:200]}...")
            print(f"Sources: {len(data['sources'])} found")
            print(f"Used selected text: {data['selected_text_used']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")

    print("\n" + "="*50)
    print("Testing completed!")

if __name__ == "__main__":
    test_rag_api()