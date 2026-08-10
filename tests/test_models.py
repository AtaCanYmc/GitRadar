import pytest
from gitradar.models import RepositoryInfo, ExpandedQueries, GapAnalysisReport, CompetitorSummary


def test_repository_info_model():
    repo = RepositoryInfo(
        full_name="owner/test-repo",
        name="test-repo",
        owner="owner",
        html_url="https://github.com/owner/test-repo",
        description="A test repository",
        stars=150,
        forks=20,
        language="Python",
        topics=["cli", "ai"],
        updated_at="2026-08-10",
        open_issues=5,
    )
    assert repo.full_name == "owner/test-repo"
    assert repo.stars == 150
    assert repo.topics == ["cli", "ai"]


def test_expanded_queries_model():
    eq = ExpandedQueries(
        search_keywords=["terminal", "ai review"],
        github_topics=["cli", "llm"],
        target_languages=["Python", "Rust"],
        search_explanation="Testing search strategy",
    )
    assert len(eq.search_keywords) == 2
    assert "cli" in eq.github_topics


def test_gap_analysis_report_model():
    report = GapAnalysisReport(
        idea_summary="Test AI CLI tool",
        market_saturation="Orta",
        saturation_score=50,
        market_summary="Market is moderately active",
        top_competitors=[
            CompetitorSummary(
                repo_name="owner/competitor",
                key_strengths=["Fast", "Popular"],
                weaknesses_or_gaps=["No AI support"],
            )
        ],
        unmet_needs=["Lack of real-time LLM feedback"],
        differentiators=["Groq integration"],
        actionable_recommendations=["Focus on CLI UX"],
        opportunity_score=80,
    )
    assert report.market_saturation == "Orta"
    assert report.opportunity_score == 80
    assert len(report.top_competitors) == 1
