import asyncio
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from gitradar.config import settings
from gitradar.services.github import GitHubService
from gitradar.services.llm import LLMService

BASE_DIR = Path(__file__).parent


def create_app() -> Flask:
    """Create and configure the Flask web application instance."""
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/config", methods=["GET"])
    def get_config():
        return jsonify({
            "groq_configured": bool(settings.groq_api_key),
            "github_configured": bool(settings.github_token),
            "default_model": settings.default_model,
            "max_repos_to_analyze": settings.max_repos_to_analyze,
        })

    @app.route("/api/analyze", methods=["POST"])
    def analyze_idea():
        data = request.get_json() or {}
        idea = data.get("idea", "").strip()
        limit = int(data.get("limit", 10))
        model = data.get("model") or settings.default_model

        if not idea:
            return jsonify({"error": "Project idea parameter is required."}), 400

        try:
            llm_service = LLMService(model=model)
            github_service = GitHubService()

            # 1. Expand Queries
            queries = llm_service.expand_idea_to_queries(idea)

            # 2. Search GitHub Repositories
            repos = asyncio.run(
                github_service.search_and_enrich(
                    keywords=queries.search_keywords,
                    topics=queries.github_topics,
                    limit=limit,
                )
            )

            # 3. Perform Gap Analysis
            report = llm_service.analyze_market_and_gaps(idea, repos)

            return jsonify({
                "queries": queries.model_dump(),
                "repositories": [r.model_dump() for r in repos],
                "report": report.model_dump(),
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/search", methods=["POST"])
    def search_repos():
        data = request.get_json() or {}
        query = data.get("query", "").strip()
        limit = int(data.get("limit", 10))

        if not query:
            return jsonify({"error": "Search query parameter is required."}), 400

        try:
            github_service = GitHubService()
            repos = asyncio.run(github_service.search_repositories(query, limit=limit))
            return jsonify({
                "repositories": [r.model_dump() for r in repos]
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app
