from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


@patch("main.r")
def test_create_job(mock_redis):
    # Mock redis behavior
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data

    mock_redis.lpush.assert_called_once()
    mock_redis.hset.assert_called_once()


@patch("main.r")
def test_get_job_exists(mock_redis):
    # Mock redis behavior
    mock_redis.hget.return_value = b"queued"

    response = client.get("/jobs/test-id-123")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-id-123"
    assert data["status"] == "queued"

    mock_redis.hget.assert_called_once_with("job:test-id-123", "status")


@patch("main.r")
def test_get_job_not_found(mock_redis):
    # Mock redis behavior returning None
    mock_redis.hget.return_value = None

    response = client.get("/jobs/non-existent-id")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "not found"
