from gitradar.models import RepositoryInfo
from gitradar.services.github import GitHubService
from gitradar.services.llm import LLMService


def test_repository_info_relevance_fields():
    repo = RepositoryInfo(
        full_name="owner/repo-test",
        name="repo-test",
        owner="owner",
        html_url="https://github.com/owner/repo-test",
        description="A terminal code review tool",
        stars=120,
        relevance_score=95,
        is_direct_competitor=True,
        relevance_reason="Direct match for terminal code review tool",
    )
    assert repo.relevance_score == 95
    assert repo.is_direct_competitor is True
    assert "Direct match" in repo.relevance_reason


def test_hybrid_ranking_algorithm():
    github_service = GitHubService()

    repo_niche = RepositoryInfo(
        full_name="niche/terminal-code-reviewer",
        name="terminal-code-reviewer",
        owner="niche",
        html_url="https://github.com/niche/terminal-code-reviewer",
        stars=200,
        relevance_score=95,
    )
    repo_generic = RepositoryInfo(
        full_name="generic/git-tool",
        name="git-tool",
        owner="generic",
        html_url="https://github.com/generic/git-tool",
        stars=50000,
        relevance_score=20,
    )

    repos = [repo_generic, repo_niche]
    sorted_repos = github_service.rank_and_sort_by_relevance(repos, limit=10)

    # The 95% relevant niche repo should outrank the 20% relevant generic high-star repo
    assert sorted_repos[0].full_name == "niche/terminal-code-reviewer"
    assert sorted_repos[0].hybrid_score > sorted_repos[1].hybrid_score
