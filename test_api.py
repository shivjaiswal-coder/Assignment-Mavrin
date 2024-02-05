from fastapi.testclient import TestClient
import json
import os

# Import your FastAPI app
from main import app  # Replace with the actual module name

# Define the test client
client = TestClient(app)

def test_process_wikipedia_data():
    # 1 Favourable test case
    payload = {"topic": "Sachin_Tendulkar", "word_count": 10}
    response = client.post("/api/v1/marvin/assignment/word-frequency-analysis", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "topic" in data
    assert "top_words" in data
   
    # Test case 2: Invalid topic 
    payload = {"topic": "", "word_count": 10}
    response = client.post("/api/v1/marvin/assignment/word-frequency-analysis", json=payload)
    data = response.json()
    assert response.status_code == 200
    assert data == None


    # Test case 3: Invalid request missing topic or word_count
    payload = {"word_count": 10}
    response = client.post("/api/v1/marvin/assignment/word-frequency-analysis", json=payload)
    assert response.status_code == 422  # 422 Unprocessable Entity

def test_get_history():
    # 1 Favourable test case, data is available
    response = client.get("/api/v1/marvin/assignment/search-history")
    assert response.status_code == 200
    data = response.json()
    assert "history" in data 

    