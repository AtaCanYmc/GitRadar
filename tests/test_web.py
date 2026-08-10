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
