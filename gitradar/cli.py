import asyncio
from typing import Optional
import typer
from rich.console import Console
from rich.status import Status

from gitradar import __version__
from gitradar.config import settings, save_setting
from gitradar.services.github import GitHubService
from gitradar.services.llm import LLMService
from gitradar.utils import ui

app = typer.Typer(
    name="gitradar",
    help="📡 GitRadar: GitHub Market & Gap Analysis CLI Tool driven by AI & GitHub REST API.",
    add_completion=False,
)
console = Console()


@app.command(name="analyze", help="💡 Bir proje fikrini analiz eder, ilgili repoları tarar ve Pazar & Gap Raporu oluşturur.")
def analyze(
    idea: str = typer.Argument(..., help="Analiz edilecek proje fikri (örn: 'AI tabanlı terminal kod inceleme aracı')"),
    limit: int = typer.Option(10, "--limit", "-l", help="Taranacak ve analize dahil edilecek maksimum repo sayısı"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Kullanılacak LiteLLM modeli (Varsayılan: groq/llama-3.3-70b-versatile)"),
):
    """Run full AI-driven market and gap analysis workflow on a project idea."""
    ui.display_banner()

    try:
        llm_service = LLMService(model=model)
        github_service = GitHubService()

        # Step 1: Query Expansion with LLM
        with Status("[bold cyan]🧠 Proje fikri LLM ile analiz ediliyor ve arama terimleri türetiliyor...[/bold cyan]", spinner="dots"):
            queries = llm_service.expand_idea_to_queries(idea)
        
        ui.display_query_strategy(queries)

        # Step 2: GitHub Search & Enrichment
        with Status(f"[bold cyan]🔍 GitHub API üzerinden repolar taranıyor (Maks: {limit})...[/bold cyan]", spinner="earth"):
            repos = asyncio.run(
                github_service.search_and_enrich(
                    keywords=queries.search_keywords,
                    topics=queries.github_topics,
                    limit=limit,
                )
            )

        if not repos:
            ui.display_error("Arama sonucunda hiç ilgili repository bulunamadı. Lütfen fikrinizi daha farklı terimlerle ifade etmeyi deneyin.")
            raise typer.Exit(code=1)

        ui.display_repo_table(repos, title=f"'{idea}' İle İlişkili Bulunan GitHub Repoları")

        # Step 3: Semantic Gap Analysis with LLM
        with Status("[bold cyan]🎯 Bulunan repolar semantik olarak puanlanıyor ve Pazar & Gap Analizi Raporu hazırlanıyor...[/bold cyan]", spinner="bouncingBar"):
            report = llm_service.analyze_market_and_gaps(idea, repos)

        # Step 4: Display Final Report
        ui.display_gap_report(report)

    except ValueError as ve:
        ui.display_error(str(ve))
        raise typer.Exit(code=1)
    except Exception as e:
        ui.display_error(f"Beklenmeyen bir hata oluştu: {str(e)}")
        raise typer.Exit(code=1)


@app.command(name="search", help="🔍 GitHub REST API üzerinden hızlı repository araması yapar.")
def search(
    query: str = typer.Argument(..., help="GitHub üzerinde aranacak terim veya sorgu"),
    limit: int = typer.Option(10, "--limit", "-l", help="Getirilecek sonuç sayısı"),
    sort: str = typer.Option("stars", "--sort", "-s", help="Sıralama ölçütü (stars, forks, updated)"),
):
    """Fast standalone repository search without LLM synthesis."""
    ui.display_banner()
    github_service = GitHubService()

    try:
        with Status(f"[bold cyan]🔍 GitHub'da '{query}' aranıyor...[/bold cyan]", spinner="dots"):
            repos = asyncio.run(github_service.search_repositories(query, limit=limit, sort=sort))

        ui.display_repo_table(repos, title=f"Arama Sonuçları: '{query}'")

    except Exception as e:
        ui.display_error(f"GitHub Araması Başarısız: {str(e)}")
        raise typer.Exit(code=1)


@app.command(name="config", help="⚙️ GitRadar API anahtarları ve tercihlerini görüntüler veya yapılandırır.")
def config_command(
    show: bool = typer.Option(False, "--show", help="Mevcut yapılandırmayı göster"),
    groq_api_key: Optional[str] = typer.Option(None, "--groq-api-key", help="Groq API Key değerini kaydet"),
    github_token: Optional[str] = typer.Option(None, "--github-token", help="GitHub Access Token değerini kaydet"),
    default_model: Optional[str] = typer.Option(None, "--model", help="Varsayılan LiteLLM modelini kaydet"),
):
    """Manage GitRadar configuration."""
    ui.display_banner()

    updated = False
    if groq_api_key:
        save_setting("GROQ_API_KEY", groq_api_key)
        ui.display_info("GROQ_API_KEY başarıyla kaydedildi! 🔑")
        updated = True

    if github_token:
        save_setting("GITHUB_TOKEN", github_token)
        ui.display_info("GITHUB_TOKEN başarıyla kaydedildi! 🐙")
        updated = True

    if default_model:
        save_setting("DEFAULT_MODEL", default_model)
        ui.display_info(f"Varsayılan model '{default_model}' olarak kaydedildi! 🤖")
        updated = True

    if show or not updated:
        # Load fresh settings
        curr_settings = settings
        grid = ui.Table(title="⚙️ Mevcut GitRadar Yapılandırması", header_style="bold yellow", expand=True)
        grid.add_column("Parametre", style="bold cyan")
        grid.add_column("Değer", style="white")

        groq_val = curr_settings.groq_api_key
        masked_groq = f"{groq_val[:6]}...{groq_val[-4:]}" if groq_val and len(groq_val) > 10 else ("Tanımlı" if groq_val else "[red]Tanımlanmamış[/red]")

        gh_val = curr_settings.github_token
        masked_gh = f"{gh_val[:4]}...{gh_val[-4:]}" if gh_val and len(gh_val) > 8 else ("Tanımlı (Anonim Mod)" if not gh_val else "Tanımlı")

        grid.add_row("GROQ_API_KEY", masked_groq)
        grid.add_row("GITHUB_TOKEN", masked_gh)
        grid.add_row("DEFAULT_MODEL", curr_settings.default_model)
        grid.add_row("MAX_REPOS_TO_ANALYZE", str(curr_settings.max_repos_to_analyze))

        console.print(grid)


@app.command(name="version", help="ℹ️ GitRadar sürüm bilgisini gösterir.")
def version():
    """Display CLI version."""
    ui.display_banner()
    console.print(f"[bold cyan]GitRadar CLI Sürümü:[/bold cyan] [bold white]v{__version__}[/bold white]")


def main():
    app()


if __name__ == "__main__":
    main()
