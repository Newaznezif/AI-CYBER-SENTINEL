from fastapi.testclient import TestClient
from app.main import app

try:
    client = TestClient(app)
    response = client.get("/api/v1/system-health")
    print(f"Health status: {response.status_code}, json: {response.json()}")
    
    docs_response = client.get("/docs")
    print(f"Docs status: {docs_response.status_code}")
except Exception as e:
    print(f"Error starting app: {e}")
