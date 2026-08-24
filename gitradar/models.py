from typing import Optional, List
from pydantic import BaseModel, Field


class RepositoryInfo(BaseModel):
    """Model representing a GitHub repository summary."""
    full_name: str
    name: str
    owner: str
    html_url: str
    description: Optional[str] = "No description provided"
    stars: int = 0
    forks: int = 0
    language: Optional[str] = "Unspecified"
    topics: List[str] = Field(default_factory=list)
    updated_at: Optional[str] = ""
    open_issues: int = 0
    readme_snippet: Optional[str] = None


class ExpandedQueries(BaseModel):
    """Model for LLM generated search strategy."""
    search_keywords: List[str] = Field(default_factory=list, description="Optimized search keywords for GitHub REST API")
    github_topics: List[str] = Field(default_factory=list, description="Relevant GitHub topics/tags")
    target_languages: List[str] = Field(default_factory=list, description="Suggested or target programming languages")
    search_explanation: str = Field(default="Search strategy generated.", description="Explanation of the search strategy")


class CompetitorSummary(BaseModel):
    """Model for a key competitor identified in gap analysis."""
    repo_name: str = Field(default="Unknown Repository")
    key_strengths: List[str] = Field(default_factory=list)
    weaknesses_or_gaps: List[str] = Field(default_factory=list)


class OpenSourceTool(BaseModel):
    """Model representing a recommended open-source library or tool to build the project."""
    name: str = Field(default="Open-Source Tool", description="Name of the open-source tool or library (e.g. Typer, Qdrant, Tree-sitter)")
    category: str = Field(default="General", description="Category (e.g. CLI Framework, Vector DB, LLM SDK, Parser)")
    description_and_usage: str = Field(default="", description="How to leverage this tool in building the project idea")
    repo_url: Optional[str] = Field(default=None, description="GitHub repository or URL link if applicable")


class ImplementationGuide(BaseModel):
    """Model for architecture and technical implementation guidance."""
    recommended_tech_stack: List[str] = Field(default_factory=list, description="Recommended technology stack (languages, frameworks, DBs)")
    architecture_overview: str = Field(default="", description="High-level architecture and how the system should be structured")
    open_source_building_blocks: List[OpenSourceTool] = Field(default_factory=list, description="Key open-source tools to use during development")


class GapAnalysisReport(BaseModel):
    """Model for LLM generated Market and Gap Analysis Report."""
    idea_summary: str = Field(default="Project Idea Summary", description="Summary of the analyzed project idea")
    market_saturation: str = Field(default="Moderate", description="Market Saturation level: Low, Moderate, or High")
    saturation_score: int = Field(default=50, description="Market saturation score from 1-100")
    market_summary: str = Field(default="Market analysis completed.", description="Overview of the current market and ecosystem")
    top_competitors: List[CompetitorSummary] = Field(default_factory=list, description="Top competitor repositories and analysis")
    unmet_needs: List[str] = Field(default_factory=list, description="Unmet needs and open gaps identified in existing repos")
    differentiators: List[str] = Field(default_factory=list, description="Key differentiators to make your project stand out")
    actionable_recommendations: List[str] = Field(default_factory=list, description="Actionable recommendations for the developer")
    opportunity_score: int = Field(default=80, description="Opportunity potential score from 1-100")
    implementation_guide: Optional[ImplementationGuide] = Field(default=None, description="Architecture, tech stack, and open source building blocks")

