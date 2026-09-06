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


def test_web_search_missing_query(app_client):
    response = app_client.post("/api/search", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "query" in data["error"].lower()


def test_web_search_with_sort(app_client, monkeypatch):
    from unittest.mock import AsyncMock
    from gitradar.models import RepositoryInfo

    fake_repo = RepositoryInfo(
        name="test-repo",
        full_name="test-org/test-repo",
        owner="test-org",
        html_url="https://github.com/test-org/test-repo",
        description="A great repo",
        stargazers_count=100,
        forks_count=20,
        language="Rust",
    )
    mock_search = AsyncMock(return_value=[fake_repo])
    monkeypatch.setattr("gitradar.services.github.GitHubService.search_repositories", mock_search)

    response = app_client.post(
        "/api/search",
        json={"query": "rust cli", "limit": 5, "sort": "updated"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["repositories"]) == 1
    assert data["repositories"][0]["name"] == "test-repo"
    mock_search.assert_awaited_once_with("rust cli", limit=5, sort="updated")


