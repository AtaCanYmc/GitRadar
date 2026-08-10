from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.markdown import Markdown
from rich.style import Style
from gitradar.models import ExpandedQueries, GapAnalysisReport, RepositoryInfo

console = Console()


def display_banner() -> None:
    """Print stylish GitRadar terminal banner."""
    banner_text = Text()
    banner_text.append("📡 ", style="bold cyan")
    banner_text.append("GitRadar", style="bold white on blue")
    banner_text.append("  CLI Market & Gap Analysis Tool  ", style="bold cyan")
    banner_text.append("[v0.1.0]", style="dim italic white")

    console.print()
    console.print(Panel(banner_text, border_style="cyan", expand=False))
    console.print()


def display_query_strategy(queries: ExpandedQueries) -> None:
    """Display the AI generated search query expansion strategy."""
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Key", style="bold yellow")
    table.add_column("Value", style="cyan")

    table.add_row("🔍 Anahtar Kelimeler:", ", ".join(queries.search_keywords))
    if queries.github_topics:
        table.add_row("🏷️ GitHub Konuları:", ", ".join(f"#{t}" for t in queries.github_topics))
    if queries.target_languages:
        table.add_row("💻 Önerilen Diller:", ", ".join(queries.target_languages))
    table.add_row("💡 Arama Stratejisi:", queries.search_explanation)

    console.print(
        Panel(
            table,
            title="[bold green]🧠 LLM Arama Stratejisi Türetildi[/bold green]",
            border_style="green",
            expand=True,
        )
    )
    console.print()


def display_repo_table(repositories: List[RepositoryInfo], title: str = "Taranan İlgili GitHub Repoları") -> None:
    """Display repositories in a Rich styled table."""
    if not repositories:
        console.print("[bold red]Hiç ilgili repository bulunamadı.[/bold red]")
        return

    table = Table(
        title=f"📊 {title} ({len(repositories)} Repo)",
        header_style="bold magenta",
        border_style="dim white",
        expand=True,
    )

    table.add_column("#", justify="center", style="dim", width=3)
    table.add_column("Repository", style="bold cyan", no_wrap=True)
    table.add_column("Yıldız ⭐", justify="right", style="bold yellow")
    table.add_column("Fork 🍴", justify="right", style="dim cyan")
    table.add_column("Dil 💻", style="green")
    table.add_column("Son Güncelleme 📅", justify="center", style="dim")
    table.add_column("Açıklama", style="white")

    for idx, repo in enumerate(repositories, 1):
        desc = repo.description or ""
        if len(desc) > 60:
            desc = desc[:57] + "..."

        table.add_row(
            str(idx),
            f"[{repo.html_url}]{repo.full_name}[/]",
            f"{repo.stars:,}",
            f"{repo.forks:,}",
            repo.language or "N/A",
            repo.updated_at or "N/A",
            desc,
        )

    console.print(table)
    console.print()


def display_gap_report(report: GapAnalysisReport) -> None:
    """Display comprehensive Market & Gap Analysis Report in terminal UI."""
    console.print()
    console.print("[bold cyan]════════════════════════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("  🎯 [bold white on blue] PAZAR & EKSİK NOKTA (GAP) ANALİZİ RAPORU [/bold white on blue]")
    console.print("[bold cyan]════════════════════════════════════════════════════════════════════════════════[/bold cyan]")
    console.print()

    # 1. Summary & Market Saturation Gauge
    sat_color = "green" if report.market_saturation == "Düşük" else ("yellow" if report.market_saturation == "Orta" else "red")
    
    summary_text = (
        f"[bold white]Proje Fikri Özeti:[/bold white] {report.idea_summary}\n\n"
        f"[bold white]Pazar Doluluk Oranı:[/bold white] [{sat_color}]{report.market_saturation}[/{sat_color}] "
        f"(Doluluk Skoru: [bold]{report.saturation_score}/100[/bold]) | "
        f"[bold white]Fırsat Potansiyeli:[/bold white] [bold green]{report.opportunity_score}/100 🚀[/bold green]\n\n"
        f"[bold white]Pazar Özeti:[/bold white]\n{report.market_summary}"
    )
    console.print(Panel(summary_text, title="[bold yellow]📌 Pazar Özeti & Doygunluk Derecesi[/bold yellow]", border_style=sat_color))
    console.print()

    # 2. Key Competitors
    if report.top_competitors:
        comp_table = Table(title="🏆 Öne Çıkan Rakipler & Analizleri", header_style="bold blue", expand=True)
        comp_table.add_column("Rakip Repo", style="bold cyan", width=25)
        comp_table.add_column("Güçlü Yönleri (Strengths)", style="green")
        comp_table.add_column("Zayıf Yönleri & Açıkları (Gaps)", style="red")

        for comp in report.top_competitors:
            strengths = "\n".join(f"• {s}" for s in comp.key_strengths)
            weaknesses = "\n".join(f"• {w}" for w in comp.weaknesses_or_gaps)
            comp_table.add_row(comp.repo_name, strengths, weaknesses)

        console.print(comp_table)
        console.print()

    # 3. Unmet Needs & Differentiators side-by-side or stacked
    unmet_md = "### 🚨 Mevcut Ekosistemdeki Eksiklikler (Unmet Needs / Gaps)\n"
    for gap in report.unmet_needs:
        unmet_md += f"- ❌ **{gap}**\n"

    diff_md = "### 💎 Projenizi Farklılaştıracak Noktalar (Differentiators)\n"
    for diff in report.differentiators:
        diff_md += f"- ✨ **{diff}**\n"

    console.print(
        Columns(
            [
                Panel(Markdown(unmet_md), border_style="red", title="[bold red]Açık Noktalar (Gaps)[/bold red]", expand=True),
                Panel(Markdown(diff_md), border_style="green", title="[bold green]Fark Yaratacak Fırsatlar[/bold green]", expand=True),
            ],
            equal=True,
        )
    )
    console.print()

    # 4. Actionable Recommendations
    rec_md = "### 💡 Geliştirici İçin Stratejik Tavsiyeler\n"
    for idx, rec in enumerate(report.actionable_recommendations, 1):
        rec_md += f"**{idx}.** {rec}\n"

    console.print(Panel(Markdown(rec_md), title="[bold cyan]🛠️ Aksiyon Planı & Tavsiyeler[/bold cyan]", border_style="cyan"))
    console.print()


def display_error(message: str) -> None:
    """Print an error panel."""
    console.print(Panel(f"[bold red]HATA:[/bold red] {message}", title="❌ İşlem Başarısız", border_style="red"))


def display_info(message: str) -> None:
    """Print an info callout."""
    console.print(f"[bold blue]ℹ️ {message}[/bold blue]")
