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
                    "GitHub API Oran Sınırı (Rate Limit) Aşıldı. "
                    "Lütfen GITHUB_TOKEN ayarlayın (`gitradar config --github-token YOUR_TOKEN`)."
                )
            elif response.status_code != 200:
                raise RuntimeError(f"GitHub API Hatası ({response.status_code}): {response.text}")

            data = response.json()
            items = data.get("items", [])

            results: List[RepositoryInfo] = []
            for item in items[:limit]:
                repo = RepositoryInfo(
                    full_name=item.get("full_name", ""),
                    name=item.get("name", ""),
                    owner=item.get("owner", {}).get("login", ""),
                    html_url=item.get("html_url", ""),
                    description=item.get("description") or "Açıklama bulunmuyor",
                    stars=item.get("stargazers_count", 0),
                    forks=item.get("forks_count", 0),
                    language=item.get("language") or "Belirtilmemiş",
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
                    # Clean markdown code blocks / trim text
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

        # 1. Build queries
        queries = []
        if keywords:
            # Combined keyword query
            queries.append(" ".join(keywords[:4]))
            # Individual key phrases
            for kw in keywords[:3]:
                if kw not in queries:
                    queries.append(kw)

        if topics:
            for topic in topics[:2]:
                queries.append(f"topic:{topic}")

        # 2. Run searches concurrently
        tasks = [self.search_repositories(q, limit=limit) for q in queries]
        search_results = await asyncio.gather(*tasks, return_exceptions=True)

        for res in search_results:
            if isinstance(res, list):
                for repo in res:
                    if repo.full_name not in all_repos:
                        all_repos[repo.full_name] = repo

        # 3. Sort by star count descending
        sorted_repos = sorted(all_repos.values(), key=lambda r: r.stars, reverse=True)[:limit]

        # 4. Fetch README snippets concurrently for top repos if requested
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
