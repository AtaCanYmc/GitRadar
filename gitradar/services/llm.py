import json
import os
import re
from typing import List, Optional
import httpx
from litellm import completion, NotFoundError, BadRequestError
from gitradar.config import settings
from gitradar.models import ExpandedQueries, GapAnalysisReport, RepositoryInfo
from gitradar.prompts import render_prompt

KNOWN_FALLBACKS = [
    "groq/openai/gpt-oss-120b",
    "groq/qwen/qwen3.6-27b",
    "groq/llama-3.3-70b-versatile",
    "groq/llama-3.1-8b-instant",
]


def extract_json(content: str) -> dict:
    """Extract and parse JSON object from LLM response text, handling markdown blocks or thought tags."""
    if not content:
        raise ValueError("Empty LLM response content received.")

    cleaned = content.strip()

    # Remove <think>...</think> block if present
    cleaned = re.sub(r"<think>.*?</think>", "", cleaned, flags=re.DOTALL).strip()

    # Extract ```json ... ``` block if present
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()
    else:
        # Fallback to finding first '{' and last '}'
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            cleaned = cleaned[start : end + 1].strip()

    return json.loads(cleaned)


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

    def _fetch_active_groq_models(self) -> List[str]:
        """Dynamically query Groq API for active text generation models available for this API key."""
        try:
            r = httpx.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5.0
            )
            if r.status_code == 200:
                data = r.json().get("data", [])
                models = [m["id"] for m in data]
                text_models = [
                    f"groq/{m}" for m in models
                    if not any(x in m for x in ["whisper", "guard", "orpheus"])
                ]
                return text_models
        except Exception:
            pass
        return []

    def _completion_with_fallback(self, messages: List[dict], temperature: float = 0.3) -> dict:
        """Try primary model, fallback dynamically to active Groq models and handle JSON mode errors."""
        dynamic_models = self._fetch_active_groq_models()
        candidates = [self.model] + dynamic_models + KNOWN_FALLBACKS

        models_to_try = []
        for m in candidates:
            if m and m not in models_to_try:
                models_to_try.append(m)

        last_exception = None

        for model_name in models_to_try:
            # 1. First attempt with response_format={"type": "json_object"}
            try:
                res = completion(
                    model=model_name,
                    messages=messages,
                    api_key=self.api_key,
                    temperature=temperature,
                    response_format={"type": "json_object"},
                )
                content = res.choices[0].message.content
                return extract_json(content)
            except Exception as e:
                err_str = str(e).lower()
                if "model_not_found" in err_str or "does not exist" in err_str or isinstance(e, NotFoundError):
                    last_exception = e
                    continue

            # 2. Second attempt without response_format if model supports standard text completion
            try:
                res = completion(
                    model=model_name,
                    messages=messages,
                    api_key=self.api_key,
                    temperature=temperature,
                )
                content = res.choices[0].message.content
                return extract_json(content)
            except Exception as e:
                last_exception = e
                continue

        raise last_exception or RuntimeError("All model fallback attempts failed.")

    def expand_idea_to_queries(self, idea: str) -> ExpandedQueries:
        """Use LLM to generate search keywords and GitHub topics based on the project idea."""
        self._ensure_api_key()

        system_prompt = render_prompt("query_expansion_system")
        user_prompt = render_prompt("query_expansion_user", idea=idea)

        data = self._completion_with_fallback(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )

        return ExpandedQueries(**data)

    def analyze_market_and_gaps(self, idea: str, repositories: List[RepositoryInfo]) -> GapAnalysisReport:
        """Analyze market saturation, identify gaps, differentiators, and produce an analysis report."""
        self._ensure_api_key()

        system_prompt = render_prompt("gap_analysis_system")
        user_prompt = render_prompt("gap_analysis_user", idea=idea, repositories=repositories)

        data = self._completion_with_fallback(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
        )

        return GapAnalysisReport(**data)
