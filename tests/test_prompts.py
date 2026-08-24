from gitradar.prompts import render_prompt
from gitradar.models import RepositoryInfo


def test_render_query_expansion_prompts():
    sys_prompt = render_prompt("query_expansion_system", language="Turkish")
    assert "Senior GitHub and Software Architect" in sys_prompt
    assert "Provide search_explanation text in Turkish" in sys_prompt

    user_prompt = render_prompt("query_expansion_user", idea="AI code reviewer")
    assert "Project Idea: AI code reviewer" in user_prompt


def test_render_gap_analysis_prompts():
    sys_prompt = render_prompt("gap_analysis_system", language="Turkish")
    assert "Market & Gap Analysis" in sys_prompt
    assert "Provide ALL report text contents (summaries, strengths, gaps, differentiators, recommendations, architecture) strictly in Turkish" in sys_prompt

    repos = [
        RepositoryInfo(
            full_name="owner/repo-one",
            name="repo-one",
            owner="owner",
            html_url="https://github.com/owner/repo-one",
            description="Test description",
            stars=500,
            forks=50,
            language="Python",
            topics=["cli", "ai"],
        )
    ]
    user_prompt = render_prompt("gap_analysis_user", idea="Test CLI", repositories=repos)
    assert "Developer Project Idea:" in user_prompt
    assert "Repo: owner/repo-one" in user_prompt
    assert "Stars: 500" in user_prompt

