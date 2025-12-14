import requests
import socket

# Test if the server is listening on port 8000
def test_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8000))
    sock.close()
    return result == 0

# Test with a short timeout
def test_with_short_timeout():
    try:
        response = requests.get("http://localhost:8000/", timeout=2)
        return response.status_code, response.text[:100]  # First 100 chars
    except requests.exceptions.Timeout:
        return "TIMEOUT", "Request timed out after 2 seconds"
    except requests.exceptions.ConnectionError:
        return "CONNECTION_ERROR", "Could not connect to server"
    except Exception as e:
        return "ERROR", str(e)

if __name__ == "__main__":
    print("Testing server...")
    port_open = test_port()
    print(f"Port 8000 open: {port_open}")

    if port_open:
        status, response = test_with_short_timeout()
        print(f"Status: {status}")
        print(f"Response preview: {response}")
    else:
        print("Server doesn't appear to be listening on port 8000")