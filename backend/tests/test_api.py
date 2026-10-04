from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_drift_endpoint():
    response = client.get("/api/drift")
    assert response.status_code == 200
    assert "features" in response.json()


def test_root_cause_endpoint():
    response = client.get("/api/root-cause")
    assert response.status_code == 200
    assert "fishbone" in response.json()
