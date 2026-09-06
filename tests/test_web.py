import pytest
from gitradar.web import create_app


@pytest.fixture
def app_client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_web_index_page(app_client):
    response = app_client.get("/")
    assert response.status_code == 200
    assert b"GitRadar" in response.data
    assert b"Developer Project Idea Analysis" in response.data


def test_web_config_endpoint(app_client):
    response = app_client.get("/api/config")
    assert response.status_code == 200
    data = response.get_json()
    assert "default_model" in data
    assert "max_repos_to_analyze" in data
    assert "openai_configured" in data


def test_web_analyze_missing_idea(app_client):
    response = app_client.post("/api/analyze", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "required" in data["error"].lower()


def test_web_analyze_invalid_key_error(app_client):
    response = app_client.post(
        "/api/analyze",
        headers={"X-OpenAI-Api-Key": "sk-invalid-fake-key-12345"},
        json={"idea": "Test idea"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

