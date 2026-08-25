import asyncio
import webbrowser
from typing import Optional
import typer
from rich.console import Console
from rich.status import Status

from gitradar import __version__
from gitradar.config import settings, save_setting
from gitradar.services.github import GitHubService
from gitradar.services.llm import LLMService
from gitradar.utils import ui
from gitradar.web import create_app

app = typer.Typer(
    name="gitradar",
    help="📡 GitRadar: GitHub Market & Gap Analysis CLI tool driven by AI & GitHub REST API.",
    add_completion=False,
)
console = Console()


@app.command(name="analyze", help="💡 Analyze a project idea, scan candidate repos, and generate a Market & Gap Report.")
def analyze(
    idea: str = typer.Argument(..., help="Project idea to analyze (e.g. 'AI code review tool for git hooks')"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum repositories to fetch and evaluate"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Override LiteLLM model"),
    language: Optional[str] = typer.Option(None, "--lang", "--language", help="Output language for AI report (e.g. 'Turkish', 'English', 'Spanish')"),
):
    """Run full AI-driven market and gap analysis workflow on a project idea."""
    ui.display_banner()

    try:
        llm_service = LLMService(model=model, language=language)
        github_service = GitHubService()

        # Step 1: Query Expansion with LLM
        with Status("[bold cyan]🧠 Analyzing project idea with LLM & deriving search strategy...[/bold cyan]", spinner="dots"):
            queries = llm_service.expand_idea_to_queries(idea, language=language)
        
        ui.display_query_strategy(queries)

        # Step 2: GitHub Search & Enrichment
        with Status(f"[bold cyan]🔍 Scanning GitHub repositories via REST API (Max: {limit})...[/bold cyan]", spinner="earth"):
            candidate_repos = asyncio.run(
                github_service.search_and_enrich(
                    keywords=queries.search_keywords,
                    topics=queries.github_topics,
                    limit=max(limit * 2, 15),
                )
            )

        if not candidate_repos:
            ui.display_error("No relevant repositories found. Try phrasing your project idea with different terms.")
            raise typer.Exit(code=1)

        # Step 2b: Relevance Evaluation & Hybrid Ranking
        with Status("[bold cyan]⚖️ Evaluating relevance match & computing hybrid rankings...[/bold cyan]", spinner="dots"):
            evaluated_repos = llm_service.evaluate_repository_relevance(idea, candidate_repos, language=language)
            repos = github_service.rank_and_sort_by_relevance(evaluated_repos, limit=limit)

        ui.display_repo_table(repos, title=f"Repositories Related to '{idea}'")

        # Step 3: Semantic Gap Analysis with LLM
        with Status("[bold cyan]🎯 Semantically evaluating candidate repos & synthesizing Market & Gap Report...[/bold cyan]", spinner="bouncingBar"):
            report = llm_service.analyze_market_and_gaps(idea, repos, language=language)

        # Step 4: Display Final Report
        ui.display_gap_report(report)

    except ValueError as ve:
        ui.display_error(str(ve))
        raise typer.Exit(code=1)
    except Exception as e:
        ui.display_error(f"An unexpected error occurred: {str(e)}")
        raise typer.Exit(code=1)


@app.command(name="search", help="🔍 Perform a quick standalone GitHub repository search.")
def search(
    query: str = typer.Argument(..., help="Search query string or keywords"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum repositories to return"),
    sort: str = typer.Option("stars", "--sort", "-s", help="Sort field (stars, forks, updated)"),
):
    """Fast standalone repository search without LLM synthesis."""
    ui.display_banner()
    github_service = GitHubService()

    try:
        with Status(f"[bold cyan]🔍 Searching GitHub for '{query}'...[/bold cyan]", spinner="dots"):
            repos = asyncio.run(github_service.search_repositories(query, limit=limit, sort=sort))

        ui.display_repo_table(repos, title=f"Search Results: '{query}'")

    except Exception as e:
        ui.display_error(f"GitHub Search Failed: {str(e)}")
        raise typer.Exit(code=1)


@app.command(name="ui", help="🌐 Launches local GitRadar web dashboard in your browser.")
def ui_command(
    port: int = typer.Option(5000, "--port", "-p", help="Port to run the local web server on"),
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host address to bind the web server"),
    open_browser: bool = typer.Option(True, "--open/--no-open", help="Automatically open browser tab"),
):
    """Launch local Flask web application dashboard."""
    ui.display_banner()
    url = f"http://{host}:{port}"
    console.print(f"[bold green]🚀 Launching GitRadar Web Dashboard at:[/bold green] [bold cyan]{url}[/bold cyan]")

    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    flask_app = create_app()
    flask_app.run(host=host, port=port, debug=False)


@app.command(name="config", help="⚙️ View or configure GitRadar API credentials and preferences.")
def config_command(
    show: bool = typer.Option(False, "--show", help="Display current configuration"),
    groq_api_key: Optional[str] = typer.Option(None, "--groq-api-key", help="Save Groq API Key credential"),
    github_token: Optional[str] = typer.Option(None, "--github-token", help="Save GitHub Access Token credential"),
    default_model: Optional[str] = typer.Option(None, "--model", help="Save default LiteLLM model identifier"),
    default_language: Optional[str] = typer.Option(None, "--lang", "--language", help="Save default response language for AI reports"),
):
    """Manage GitRadar configuration."""
    ui.display_banner()

    updated = False
    if groq_api_key:
        save_setting("GROQ_API_KEY", groq_api_key)
        ui.display_info("GROQ_API_KEY successfully saved! 🔑")
        updated = True

    if github_token:
        save_setting("GITHUB_TOKEN", github_token)
        ui.display_info("GITHUB_TOKEN successfully saved! 🐙")
        updated = True

    if default_model:
        save_setting("DEFAULT_MODEL", default_model)
        ui.display_info(f"Default model saved as '{default_model}'! 🤖")
        updated = True

    if default_language:
        save_setting("DEFAULT_LANGUAGE", default_language)
        ui.display_info(f"Default language saved as '{default_language}'! 🌐")
        updated = True

    if show or not updated:
        curr_settings = settings
        grid = ui.Table(title="⚙️ Current GitRadar Configuration", header_style="bold yellow", expand=True)
        grid.add_column("Parameter", style="bold cyan")
        grid.add_column("Value", style="white")

        groq_val = curr_settings.groq_api_key
        masked_groq = f"{groq_val[:6]}...{groq_val[-4:]}" if groq_val and len(groq_val) > 10 else ("Configured" if groq_val else "[red]Not Configured[/red]")

        gh_val = curr_settings.github_token
        masked_gh = f"{gh_val[:4]}...{gh_val[-4:]}" if gh_val and len(gh_val) > 8 else ("Configured (Anonymous Mode)" if not gh_val else "Configured")

        grid.add_row("GROQ_API_KEY", masked_groq)
        grid.add_row("GITHUB_TOKEN", masked_gh)
        grid.add_row("DEFAULT_MODEL", curr_settings.default_model)
        grid.add_row("DEFAULT_LANGUAGE", curr_settings.default_language)
        grid.add_row("MAX_REPOS_TO_ANALYZE", str(curr_settings.max_repos_to_analyze))

        console.print(grid)


@app.command(name="version", help="ℹ️ Display GitRadar version information.")
def version():
    """Display CLI version."""
    ui.display_banner()
    console.print(f"[bold cyan]GitRadar CLI Version:[/bold cyan] [bold white]v{__version__}[/bold white]")


def main():
    app()


if __name__ == "__main__":
    main()
