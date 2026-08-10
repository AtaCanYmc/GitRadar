from typing import Optional, List
from pydantic import BaseModel, Field


class RepositoryInfo(BaseModel):
    """Model representing a GitHub repository summary."""
    full_name: str
    name: str
    owner: str
    html_url: str
    description: Optional[str] = "Açıklama bulunmuyor"
    stars: int = 0
    forks: int = 0
    language: Optional[str] = "Belirtilmemiş"
    topics: List[str] = Field(default_factory=list)
    updated_at: Optional[str] = ""
    open_issues: int = 0
    readme_snippet: Optional[str] = None


class ExpandedQueries(BaseModel):
    """Model for LLM generated search strategy."""
    search_keywords: List[str] = Field(..., description="GitHub REST API araması için optimize edilmiş anahtar kelimeler")
    github_topics: List[str] = Field(default_factory=list, description="Fikirle ilişkili GitHub konuları/etiketleri")
    target_languages: List[str] = Field(default_factory=list, description="Önerilen veya hedef programlama dilleri")
    search_explanation: str = Field(..., description="Arama stratejisi açıklaması")


class CompetitorSummary(BaseModel):
    """Model for a key competitor identified in gap analysis."""
    repo_name: str
    key_strengths: List[str]
    weaknesses_or_gaps: List[str]


class GapAnalysisReport(BaseModel):
    """Model for LLM generated Market and Gap Analysis Report."""
    idea_summary: str = Field(..., description="Analiz edilen projenin özet tanımı")
    market_saturation: str = Field(..., description="Pazar Doluluk Oranı: Düşük, Orta veya Yüksek")
    saturation_score: int = Field(..., description="1-100 arası doluluk/rekabet puanı")
    market_summary: str = Field(..., description="Pazarın genel durumu ve mevcut ekosistem özeti")
    top_competitors: List[CompetitorSummary] = Field(default_factory=list, description="Öne çıkan rakipler ve incelemeleri")
    unmet_needs: List[str] = Field(..., description="Mevcut projelerde tespit edilen eksiklikler ve açıklar (Gaps)")
    differentiators: List[str] = Field(..., description="Projenizi öne çıkaracak farklılaşma stratejileri (Differentiators)")
    actionable_recommendations: List[str] = Field(..., description="Geliştirici için somut ve uygulanabilir tavsiyeler")
    opportunity_score: int = Field(..., description="1-100 arası Fırsat Potansiyeli Puanı")
