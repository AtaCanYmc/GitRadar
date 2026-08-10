import json
import os
from typing import List
from litellm import completion
from gitradar.config import settings
from gitradar.models import ExpandedQueries, GapAnalysisReport, RepositoryInfo, CompetitorSummary


class LLMService:
    """Service to interact with LiteLLM for query expansion and gap analysis."""

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.groq_api_key or os.environ.get("GROQ_API_KEY")
        self.model = model or settings.default_model

    def _ensure_api_key(self):
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY bulunamadı! "
                "Lütfen API anahtarınızı ayarlayın: `gitradar config --groq-api-key YOUR_KEY` "
                "veya GROQ_API_KEY environment değişkenini tanımlayın."
            )

    def expand_idea_to_queries(self, idea: str) -> ExpandedQueries:
        """Use LLM to generate search keywords and GitHub topics based on the project idea."""
        self._ensure_api_key()

        system_prompt = (
            "Sen kıdemli bir GitHub ve Yazılım Mimarısın. Kullanıcı sana bir proje fikri verecek.\n"
            "Senin görevin GitHub REST API üzerinde arama yapmak için en etkili arama terimlerini ve konularını (topics) türetmektir.\n"
            "Yanıtını YALNIZCA geçerli bir JSON formatında ver. Başka hiçbir açıklama yazma.\n\n"
            "İstenen JSON Yapısı:\n"
            "{\n"
            '  "search_keywords": ["keyword1", "keyword2", "keyword3"],\n'
            '  "github_topics": ["topic1", "topic2"],\n'
            '  "target_languages": ["Python", "Rust"],\n'
            '  "search_explanation": "Arama stratejisinin kısa açıklaması"\n'
            "}"
        )

        user_prompt = f"Proje Fikri: {idea}"

        response = completion(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            api_key=self.api_key,
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        data = json.loads(content)
        return ExpandedQueries(**data)

    def analyze_market_and_gaps(self, idea: str, repositories: List[RepositoryInfo]) -> GapAnalysisReport:
        """Analyze market saturation, identify gaps, differentiators, and produce an analysis report."""
        self._ensure_api_key()

        repos_text = ""
        for i, r in enumerate(repositories, 1):
            repos_text += (
                f"{i}. Repo: {r.full_name}\n"
                f"   Yıldız: {r.stars} | Fork: {r.forks} | Dili: {r.language}\n"
                f"   Açıklama: {r.description}\n"
                f"   Konular: {', '.join(r.topics)}\n"
            )
            if r.readme_snippet:
                repos_text += f"   README Özeti: {r.readme_snippet[:300]}...\n"
            repos_text += "\n"

        system_prompt = (
            "Sen yazılım projeleri için Pazar ve Eksik Nokta (Gap) Analizi uzmanısın.\n"
            "Sana bir geliştiricinin yeni proje fikri ve GitHub üzerinde bulunan en yakın mevcut açık kaynak projeler verilecek.\n"
            "Görevin bu projeleri semantic olarak analiz edip detaylı bir pazar raporu sunmaktır.\n"
            "Tüm metin içeriklerini Türkçe olarak hazırlar.\n"
            "Yanıtını YALNIZCA geçerli bir JSON formatında ver.\n\n"
            "İstenen JSON Formatı:\n"
            "{\n"
            '  "idea_summary": "Projenin kısa özeti",\n'
            '  "market_saturation": "Düşük | Orta | Yüksek",\n'
            '  "saturation_score": 45,\n'
            '  "market_summary": "Pazarın genel durumu...",\n'
            '  "top_competitors": [\n'
            "    {\n"
            '      "repo_name": "owner/repo",\n'
            '      "key_strengths": ["Güçlü yön 1", "Güçlü yön 2"],\n'
            '      "weaknesses_or_gaps": ["Eksik yön 1", "Açık 2"]\n'
            "    }\n"
            "  ],\n"
            '  "unmet_needs": ["Mevcut repolarda bulunmayan eksiklik 1", "Eksiklik 2"],\n'
            '  "differentiators": ["Fikri rakiplerinden farklılaştıracak özellik 1", "Özellik 2"],\n'
            '  "actionable_recommendations": ["Tavsiye 1", "Tavsiye 2"],\n'
            '  "opportunity_score": 85\n'
            "}"
        )

        user_prompt = (
            f"Geliştirici Proje Fikri:\n{idea}\n\n"
            f"GitHub'da Bulunan İlgili Mevcut Projeler ({len(repositories)} adet):\n"
            f"{repos_text if repos_text else 'Hiç doğrudan ilgili repo bulunamadı.'}"
        )

        response = completion(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            api_key=self.api_key,
            temperature=0.4,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        data = json.loads(content)
        return GapAnalysisReport(**data)
