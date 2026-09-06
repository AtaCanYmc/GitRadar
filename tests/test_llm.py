from unittest.mock import MagicMock, patch
import pytest
from gitradar.models import RepositoryInfo
from gitradar.services.llm import LLMService, extract_json


def test_extract_json_clean():
    raw = '{"search_keywords": ["foo", "bar"], "github_topics": ["git"]}'
    res = extract_json(raw)
    assert res["search_keywords"] == ["foo", "bar"]


def test_extract_json_markdown_and_think_tags():
    raw = """
    <think>
    Need to provide a JSON response.
    </think>
    ```json
    {
        "status": "ok",
        "count": 42,
    }
    ```
    """
    res = extract_json(raw)
    assert res["status"] == "ok"
    assert res["count"] == 42


def test_llm_service_initialization_openai():
    service = LLMService(api_key="sk-test-openai-key-12345")
    assert service.api_key == "sk-test-openai-key-12345"
    assert service.base_url is None
    assert service.model == "gpt-4o-mini"


def test_llm_service_groq_auto_detection():
    service = LLMService(api_key="gsk_1234567890abcdef")
    assert service.base_url == "https://api.groq.com/openai/v1"
    assert service.model == "llama-3.3-70b-versatile"


def test_llm_service_custom_base_url():
    service = LLMService(
        api_key="sk-deepseek-key",
        base_url="https://api.deepseek.com",
        model="deepseek-chat"
    )
    assert service.base_url == "https://api.deepseek.com"
    assert service.model == "deepseek-chat"


def test_llm_service_local_endpoint_dummy_key():
    service = LLMService(
        api_key="",
        base_url="http://localhost:11434/v1",
        model="llama3.2"
    )
    assert service.base_url == "http://localhost:11434/v1"
    client = service.client
    assert client.base_url.host == "localhost"
    assert service.api_key == "ollama"


def test_llm_service_strip_groq_prefix():
    service = LLMService(
        api_key="gsk_test_key",
        model="groq/llama-3.1-8b-instant"
    )
    assert service.model == "llama-3.1-8b-instant"


def test_llm_service_missing_key_raises():
    service = LLMService(api_key="")
    with pytest.raises(ValueError) as excinfo:
        service._ensure_api_key()
    assert "Missing AI API Key" in str(excinfo.value)


@patch("gitradar.services.llm.OpenAI")
def test_expand_idea_to_queries_mock(mock_openai_cls):
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    mock_choice = MagicMock()
    mock_choice.message.content = '{"search_keywords": ["ai git hook", "code review"], "github_topics": ["git", "ai"], "target_languages": ["python"], "search_explanation": "Test explanation"}'
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    service = LLMService(api_key="sk-mock-key")
    queries = service.expand_idea_to_queries("AI code reviewer")

    assert "ai git hook" in queries.search_keywords
    assert "git" in queries.github_topics
    assert queries.search_explanation == "Test explanation"


@patch("gitradar.services.llm.OpenAI")
def test_analyze_market_and_gaps_mock(mock_openai_cls):
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    mock_choice = MagicMock()
    mock_choice.message.content = '''{
        "idea_summary": "CLI tool for Git diff analysis",
        "market_saturation": "Moderate",
        "saturation_score": 45,
        "market_summary": "Growing market with high demand",
        "unmet_needs": ["Fast terminal UI"],
        "differentiators": ["Interactive reviews"],
        "actionable_recommendations": ["Release beta"],
        "opportunity_score": 85
    }'''
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    service = LLMService(api_key="sk-mock-key")
    report = service.analyze_market_and_gaps("CLI Git tool", repositories=[])

    assert report.idea_summary == "CLI tool for Git diff analysis"
    assert report.market_saturation == "Moderate"
    assert report.saturation_score == 45
    assert report.opportunity_score == 85
    assert "Fast terminal UI" in report.unmet_needs


@patch("gitradar.services.llm.OpenAI")
def test_evaluate_repository_relevance_mock(mock_openai_cls):
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    mock_choice = MagicMock()
    mock_choice.message.content = '''{
        "evaluations": [
            {
                "full_name": "owner/repo1",
                "relevance_score": 92,
                "is_direct_competitor": true,
                "relevance_reason": "Exact match for git terminal review"
            }
        ]
    }'''
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    repo = RepositoryInfo(
        full_name="owner/repo1",
        name="repo1",
        owner="owner",
        html_url="https://github.com/owner/repo1",
        stars=50,
    )

    service = LLMService(api_key="sk-mock-key")
    evaluated = service.evaluate_repository_relevance("git terminal review", [repo])

    assert len(evaluated) == 1
    assert evaluated[0].relevance_score == 92
    assert evaluated[0].is_direct_competitor is True
    assert "Exact match" in evaluated[0].relevance_reason
