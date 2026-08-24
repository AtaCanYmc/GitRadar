"""
Example script demonstrating programmatic usage of GitRadar Python SDK services.
"""

import asyncio
from gitradar.services.github import GitHubService
from gitradar.services.llm import LLMService
from gitradar.utils import ui


async def main():
    idea = "AI powered automated documentation generator for Python repositories"
    target_language = "Turkish"
    
    print(f"📡 Analyzing Project Idea via GitRadar SDK: '{idea}' (Language: {target_language})\n")

    # 1. Initialize Services with custom response language
    github_service = GitHubService()
    llm_service = LLMService(language=target_language)

    # 2. Expand Idea into Search Strategy
    print("1️⃣ Generating search queries with LLM...")
    queries = llm_service.expand_idea_to_queries(idea, language=target_language)
    print(f"   Keywords: {queries.search_keywords}")
    print(f"   Topics: {queries.github_topics}\n")

    # 3. Search & Enrich Repositories
    print("2️⃣ Fetching GitHub repositories asynchronously...")
    repos = await github_service.search_and_enrich(
        keywords=queries.search_keywords,
        topics=queries.github_topics,
        limit=5,
    )
    print(f"   Found {len(repos)} relevant repositories.\n")

    # 4. Perform Gap Analysis & Implementation Guidance
    print("3️⃣ Running Market & Gap Analysis...")
    report = llm_service.analyze_market_and_gaps(idea, repos, language=target_language)

    if report.implementation_guide:
        print(f"   Recommended Stack: {report.implementation_guide.recommended_tech_stack}")

    # 5. Display with GitRadar UI
    ui.display_gap_report(report)


if __name__ == "__main__":
    asyncio.run(main())
