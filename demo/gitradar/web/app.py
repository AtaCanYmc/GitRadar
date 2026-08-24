import asyncio
import concurrent.futures
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from gitradar.config import settings
from gitradar.services.github import GitHubService
from gitradar.services.llm import LLMService

BASE_DIR = Path(__file__).parent


def safe_run_async(coro):
    """Run an async coroutine safely, handling cases where an asyncio event loop is already running (e.g. Vercel / ASGI)."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            return executor.submit(asyncio.run, coro).result()
    else:
        return asyncio.run(coro)


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

    @app.route("/<path:filename>")
    def serve_static_root(filename):
        target = BASE_DIR / "static" / filename
        if target.is_file():
            return send_from_directory(BASE_DIR / "static", filename)
        return jsonify({"error": "Not found"}), 404

    @app.route("/api/config", methods=["GET"])
    def get_config():
        return jsonify({
            "groq_configured": bool(settings.groq_api_key),
            "github_configured": bool(settings.github_token),
            "default_model": settings.default_model,
            "default_language": settings.default_language,
            "max_repos_to_analyze": settings.max_repos_to_analyze,
        })

    @app.route("/api/analyze", methods=["POST"])
    def analyze_idea():
        data = request.get_json() or {}
        idea = data.get("idea", "").strip()
        limit = int(data.get("limit", 10))
        model = data.get("model") or settings.default_model
        language = data.get("language") or settings.default_language

        def clean_key(v):
            if not v:
                return None
            cleaned = str(v).replace("\r", "").replace("\n", "").replace("\t", "").strip().strip("'\"")
            return cleaned if cleaned else None

        # Extract user credentials from headers or JSON payload
        groq_key = clean_key(
            request.headers.get("X-Groq-Api-Key")
            or data.get("groq_key")
            or data.get("groqKey")
            or settings.groq_api_key
        )
        github_token = clean_key(
            request.headers.get("X-Github-Token")
            or data.get("github_token")
            or data.get("githubToken")
            or settings.github_token
        )

        if not idea:
            return jsonify({"error": "Project idea parameter is required."}), 400

        try:
            llm_service = LLMService(api_key=groq_key, model=model, language=language)
            github_service = GitHubService(token=github_token)

            # 1. Expand Queries
            queries = llm_service.expand_idea_to_queries(idea, language=language)

            # 2. Search GitHub Repositories
            repos = safe_run_async(
                github_service.search_and_enrich(
                    keywords=queries.search_keywords,
                    topics=queries.github_topics,
                    limit=limit,
                )
            )

            # 3. Perform Gap Analysis
            report = llm_service.analyze_market_and_gaps(idea, repos, language=language)

            return jsonify({
                "queries": queries.model_dump(),
                "repositories": [r.model_dump() for r in repos],
                "report": report.model_dump(),
            })

        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            err_msg = str(e)
            if any(k in err_msg.lower() for k in ["invalid_api_key", "invalid api key", "groqexception"]):
                err_msg = "Invalid Groq API Key! Please click the Settings Modal (⚙️) in the top-right corner and enter a valid Groq API Key (gsk_...). Get a free key at https://console.groq.com"
            return jsonify({"error": err_msg}), 400

    @app.route("/api/search", methods=["POST"])
    def search_repos():
        data = request.get_json() or {}
        query = data.get("query", "").strip()
        limit = int(data.get("limit", 10))

        def clean_key(v):
            if not v:
                return None
            cleaned = str(v).replace("\r", "").replace("\n", "").replace("\t", "").strip().strip("'\"")
            return cleaned if cleaned else None

        github_token = clean_key(
            request.headers.get("X-Github-Token")
            or data.get("github_token")
            or data.get("githubToken")
            or settings.github_token
        )

        if not query:
            return jsonify({"error": "Search query parameter is required."}), 400

        try:
            github_service = GitHubService(token=github_token)
            repos = safe_run_async(github_service.search_repositories(query, limit=limit))
            return jsonify({
                "repositories": [r.model_dump() for r in repos]
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app
