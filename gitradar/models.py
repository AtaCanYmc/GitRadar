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
    search_keywords: List[str] = Field(..., description="Optimized search keywords for GitHub REST API")
    github_topics: List[str] = Field(default_factory=list, description="Relevant GitHub topics/tags")
    target_languages: List[str] = Field(default_factory=list, description="Suggested or target programming languages")
    search_explanation: str = Field(..., description="Explanation of the search strategy")


class CompetitorSummary(BaseModel):
    """Model for a key competitor identified in gap analysis."""
    repo_name: str
    key_strengths: List[str]
    weaknesses_or_gaps: List[str]


class GapAnalysisReport(BaseModel):
    """Model for LLM generated Market and Gap Analysis Report."""
    idea_summary: str = Field(..., description="Summary of the analyzed project idea")
    market_saturation: str = Field(..., description="Market Saturation level: Low, Moderate, or High")
    saturation_score: int = Field(..., description="Market saturation score from 1-100")
    market_summary: str = Field(..., description="Overview of the current market and ecosystem")
    top_competitors: List[CompetitorSummary] = Field(default_factory=list, description="Top competitor repositories and analysis")
    unmet_needs: List[str] = Field(..., description="Unmet needs and open gaps identified in existing repos")
    differentiators: List[str] = Field(..., description="Key differentiators to make your project stand out")
    actionable_recommendations: List[str] = Field(..., description="Actionable recommendations for the developer")
    opportunity_score: int = Field(..., description="Opportunity potential score from 1-100")
