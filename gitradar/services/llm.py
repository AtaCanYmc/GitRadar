import json
import os
from typing import List
from litellm import completion
from gitradar.config import settings
from gitradar.models import ExpandedQueries, GapAnalysisReport, RepositoryInfo
from gitradar.prompts import render_prompt


class LLMService:
    """Service to interact with LiteLLM for query expansion and gap analysis."""

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.groq_api_key or os.environ.get("GROQ_API_KEY")
        self.model = model or settings.default_model

    def _ensure_api_key(self):
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found! "
                "Please configure your API key: `gitradar config --groq-api-key YOUR_KEY` "
                "or set the GROQ_API_KEY environment variable."
            )

    def expand_idea_to_queries(self, idea: str) -> ExpandedQueries:
        """Use LLM to generate search keywords and GitHub topics based on the project idea."""
        self._ensure_api_key()

        system_prompt = render_prompt("query_expansion_system")
        user_prompt = render_prompt("query_expansion_user", idea=idea)

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

        system_prompt = render_prompt("gap_analysis_system")
        user_prompt = render_prompt("gap_analysis_user", idea=idea, repositories=repositories)

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
