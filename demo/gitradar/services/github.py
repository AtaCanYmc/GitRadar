import asyncio
from typing import List, Optional, Dict, Any
import httpx
from gitradar.config import settings
from gitradar.models import RepositoryInfo

GITHUB_API_BASE = "https://api.github.com"


class GitHubService:
    """Asynchronous client for interacting with the GitHub REST API."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.github_token
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitRadar-CLI/0.1.0",
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    async def search_repositories(
        self,
        query: str,
        limit: int = 10,
        sort: str = "stars",
        order: str = "desc"
    ) -> List[RepositoryInfo]:
        """Search GitHub repositories based on query string."""
        url = f"{GITHUB_API_BASE}/search/repositories"
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": min(limit, 100),
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, headers=self.headers, params=params)
            
            if response.status_code == 403:
                raise RuntimeError(
                    "GitHub API Rate Limit Exceeded. "
                    "Please configure a GITHUB_TOKEN (`gitradar config --github-token YOUR_TOKEN`)."
                )
            elif response.status_code != 200:
                raise RuntimeError(f"GitHub API Error ({response.status_code}): {response.text}")

            data = response.json()
            items = data.get("items", [])

            results: List[RepositoryInfo] = []
            for item in items[:limit]:
                repo = RepositoryInfo(
                    full_name=item.get("full_name", ""),
                    name=item.get("name", ""),
                    owner=item.get("owner", {}).get("login", ""),
                    html_url=item.get("html_url", ""),
                    description=item.get("description") or "No description provided",
                    stars=item.get("stargazers_count", 0),
                    forks=item.get("forks_count", 0),
                    language=item.get("language") or "Unspecified",
                    topics=item.get("topics", []),
                    updated_at=item.get("updated_at", "")[:10] if item.get("updated_at") else "",
                    open_issues=item.get("open_issues_count", 0),
                )
                results.append(repo)

            return results

    async def fetch_readme_snippet(self, owner: str, repo: str, max_chars: int = 800) -> Optional[str]:
        """Fetch README content snippet for a repository."""
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/readme"
        headers = {**self.headers, "Accept": "application/vnd.github.v3.raw"}

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, headers=headers)
                if response.status_code == 200:
                    text = response.text
                    cleaned = text.strip()
                    return cleaned[:max_chars] + "..." if len(cleaned) > max_chars else cleaned
            except Exception:
                pass
        return None

    async def search_and_enrich(
        self,
        keywords: List[str],
        topics: List[str] = None,
        limit: int = 10,
        fetch_readmes: bool = True
    ) -> List[RepositoryInfo]:
        """
        Execute smart combined search using keywords & topics, deduplicate results,
        and enrich top results with README snippets asynchronously.
        """
        all_repos: Dict[str, RepositoryInfo] = {}

        queries = []
        if keywords:
            for kw in keywords:
                kw_clean = kw.strip()
                if kw_clean and kw_clean not in queries:
                    queries.append(kw_clean)

        if topics:
            for topic in topics[:3]:
                topic_clean = topic.strip().replace(" ", "-").lower()
                if topic_clean and topic_clean not in ["python", "machine-learning", "deep-learning", "ai", "artificial-intelligence"]:
                    t_query = f"topic:{topic_clean}"
                    if t_query not in queries:
                        queries.append(t_query)

        tasks = [self.search_repositories(q, limit=limit) for q in queries]
        search_results = await asyncio.gather(*tasks, return_exceptions=True)

        for res in search_results:
            if isinstance(res, list):
                for repo in res:
                    if repo.full_name not in all_repos:
                        all_repos[repo.full_name] = repo

        sorted_repos = sorted(all_repos.values(), key=lambda r: (r.stars, r.forks, r.full_name), reverse=True)[:limit]

        if fetch_readmes and sorted_repos:
            readme_tasks = [
                self.fetch_readme_snippet(repo.owner, repo.name)
                for repo in sorted_repos[:5]
            ]
            readmes = await asyncio.gather(*readme_tasks, return_exceptions=True)
            
            for i, readme in enumerate(readmes):
                if isinstance(readme, str) and readme:
                    sorted_repos[i].readme_snippet = readme

        return sorted_repos

    def rank_and_sort_by_relevance(
        self,
        repos: List[RepositoryInfo],
        limit: int = 10,
        min_relevance: int = 50,
    ) -> List[RepositoryInfo]:
        """
        Calculate hybrid score for each repository, filter out repos below min_relevance threshold,
        and sort by hybrid score desc.
        Hybrid Score = (Relevance Score * 0.7) + (Normalized Star Score * 0.3)
        """
        if not repos:
            return repos

        import math
        max_stars = max((r.stars for r in repos), default=1)

        for r in repos:
            rel_score = r.relevance_score if r.relevance_score is not None else 50
            star_score = min(100.0, (math.log10(r.stars + 1) / math.log10(max(max_stars, 10) + 1)) * 100.0) if max_stars > 0 else 50.0
            r.hybrid_score = round((rel_score * 0.7) + (star_score * 0.3), 1)

        # Enforce minimum relevance threshold filtering
        filtered_repos = [
            r for r in repos
            if r.relevance_score is not None and r.relevance_score >= min_relevance
        ]

        if not filtered_repos:
            fallback_threshold = max(30, min_relevance - 20)
            filtered_repos = [
                r for r in repos
                if r.relevance_score is not None and r.relevance_score >= fallback_threshold
            ]

        sorted_repos = sorted(
            filtered_repos if filtered_repos else repos,
            key=lambda r: (r.hybrid_score, r.stars, r.forks, r.full_name),
            reverse=True
        )
        return sorted_repos[:limit]
