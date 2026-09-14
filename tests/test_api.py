from fastapi.testclient import TestClient
from app.main import app

# This creates a dummy client that can send HTTP requests directly to our FastAPI app
# without actually needing to spin up the web server on a port!
client = TestClient(app)

def test_health_check():
    """Verifies the health endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_validation_missing_message():
    """Verifies that Pydantic blocks requests missing the 'message' field."""
    response = client.post("/chat", json={})
    # 422 is the standard HTTP Unprocessable Entity code (Validation Error)
    assert response.status_code == 422 

def test_chat_validation_empty_message():
    """Verifies that Pydantic blocks empty strings to save API tokens."""
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 422

def test_chat_validation_too_long():
    """Verifies that Pydantic blocks massive payloads (DDOS protection)."""
    # Create a string of 600 characters
    massive_string = "A" * 600 
    response = client.post("/chat", json={"message": massive_string})
    assert response.status_code == 422
