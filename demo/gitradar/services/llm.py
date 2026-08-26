import json
import os
import re
import sys
import typing
from typing import List, Optional

# Ensure typing backports are attached to typing module for Python < 3.11 before importing litellm
if sys.version_info < (3, 11):
    try:
        import typing_extensions

        for _name in ("NotRequired", "Required", "Self", "Never", "LiteralString", "TypeAlias", "Override", "dataclass_transform"):
            if not hasattr(typing, _name) and hasattr(typing_extensions, _name):
                setattr(typing, _name, getattr(typing_extensions, _name))
    except ImportError:
        pass

import httpx
import litellm
from litellm import completion, NotFoundError, BadRequestError
from gitradar.config import settings
from gitradar.models import ExpandedQueries, GapAnalysisReport, RepositoryInfo
from gitradar.prompts import render_prompt

# Suppress LiteLLM verbose logs and feedback prompts in terminal UI
litellm.suppress_debug_info = True
litellm.set_verbose = False

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

    # Remove markdown code blocks if wrapped in ```json ... ``` or ``` ... ```
    if "```" in cleaned:
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = cleaned.strip()

    # Find outer-most JSON bounds: first '{' and last '}'
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start : end + 1].strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Sanitize trailing commas: e.g. ", }" -> "}" or ", ]" -> "]"
        sanitized = re.sub(r",\s*([\}\]])", r"\1", cleaned)
        return json.loads(sanitized)


class LLMService:
    """Service to interact with LiteLLM for query expansion and gap analysis."""

    def __init__(self, api_key: str = None, model: str = None, language: str = None):
        raw_key = api_key or settings.groq_api_key or os.environ.get("GROQ_API_KEY") or ""
        self.api_key = raw_key.strip().strip("'\"")
        self.model = model or settings.default_model
        self.language = language or settings.default_language

    def _ensure_api_key(self):
        if not self.api_key or self.api_key.strip() in ("", "gsk_...", "gsk_your_groq_api_key_here"):
            raise ValueError(
                "Missing Groq API Key! Please open the Settings Modal (⚙️) and enter a valid Groq API key, "
                "or run `gitradar config --groq-api-key YOUR_KEY`. Get a free key at https://console.groq.com"
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
                if "invalid_api_key" in err_str or "invalid api key" in err_str or "authentication" in err_str:
                    raise ValueError(
                        "Invalid Groq API Key! Please enter a valid key in the Settings Modal (⚙️) "
                        "or run `gitradar config --groq-api-key YOUR_KEY`. Get a free key at https://console.groq.com"
                    ) from e
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
                err_str = str(e).lower()
                if "invalid_api_key" in err_str or "invalid api key" in err_str or "authentication" in err_str:
                    raise ValueError(
                        "Invalid Groq API Key! Please enter a valid key in the Settings Modal (⚙️) "
                        "or run `gitradar config --groq-api-key YOUR_KEY`. Get a free key at https://console.groq.com"
                    ) from e
                last_exception = e
                continue

        if last_exception:
            err_str = str(last_exception).lower()
            if "invalid_api_key" in err_str or "invalid api key" in err_str or "authentication" in err_str:
                raise ValueError(
                    "Invalid Groq API Key! Please enter a valid key in the Settings Modal (⚙️) "
                    "or run `gitradar config --groq-api-key YOUR_KEY`. Get a free key at https://console.groq.com"
                )

        raise last_exception or RuntimeError("All model fallback attempts failed.")

    def expand_idea_to_queries(self, idea: str, language: str = None) -> ExpandedQueries:
        """Use LLM to generate search keywords and GitHub topics based on the project idea."""
        self._ensure_api_key()
        lang = language or self.language or settings.default_language

        system_prompt = render_prompt("query_expansion_system", language=lang)
        user_prompt = render_prompt("query_expansion_user", idea=idea)

        data = self._completion_with_fallback(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
        )

        if not isinstance(data, dict):
            data = {}

        if "search_keywords" in data and not isinstance(data["search_keywords"], list):
            data["search_keywords"] = [str(data["search_keywords"])]
        if "github_topics" in data and not isinstance(data["github_topics"], list):
            data["github_topics"] = [str(data["github_topics"])]

        try:
            return ExpandedQueries(**data)
        except Exception:
            return ExpandedQueries(
                search_keywords=data.get("search_keywords") or [idea],
                github_topics=data.get("github_topics") or [],
                target_languages=data.get("target_languages") or [],
                search_explanation=str(data.get("search_explanation") or "Search strategy generated."),
            )

    def analyze_market_and_gaps(self, idea: str, repositories: List[RepositoryInfo], language: str = None) -> GapAnalysisReport:
        """Analyze market saturation, identify gaps, differentiators, and produce an analysis report."""
        self._ensure_api_key()
        lang = language or self.language or settings.default_language

        system_prompt = render_prompt("gap_analysis_system", language=lang)
        user_prompt = render_prompt("gap_analysis_user", idea=idea, repositories=repositories)

        data = self._completion_with_fallback(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
        )

        if not isinstance(data, dict):
            data = {}

        for score_key in ("saturation_score", "opportunity_score"):
            if score_key in data:
                try:
                    data[score_key] = int(data[score_key])
                except (ValueError, TypeError):
                    data[score_key] = 50

        try:
            return GapAnalysisReport(**data)
        except Exception:
            return GapAnalysisReport(
                idea_summary=str(data.get("idea_summary") or idea),
                market_saturation=str(data.get("market_saturation") or "Moderate"),
                saturation_score=int(data.get("saturation_score") or 50),
                market_summary=str(data.get("market_summary") or "Market analysis completed."),
                unmet_needs=list(data.get("unmet_needs") or []),
                differentiators=list(data.get("differentiators") or []),
                actionable_recommendations=list(data.get("actionable_recommendations") or []),
                opportunity_score=int(data.get("opportunity_score") or 80),
            )

    def evaluate_repository_relevance(
        self,
        idea: str,
        repositories: List[RepositoryInfo],
        language: str = None
    ) -> List[RepositoryInfo]:
        """Evaluate LLM relevance scores and fit reasons for a list of candidate repositories."""
        if not repositories:
            return repositories

        try:
            self._ensure_api_key()
            target_lang = language or self.language or settings.default_language

            sys_msg = render_prompt("relevance_evaluation_system", language=target_lang)
            user_msg = render_prompt("relevance_evaluation_user", idea=idea, repos=repositories)

            data = self._completion_with_fallback(
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.0,
            )

            if isinstance(data, dict):
                evals = data.get("evaluations", [])
                eval_map = {item.get("full_name"): item for item in evals if isinstance(item, dict)}

                for repo in repositories:
                    if repo.full_name in eval_map:
                        ev = eval_map[repo.full_name]
                        score = ev.get("relevance_score")
                        if isinstance(score, (int, float)):
                            repo.relevance_score = max(0, min(100, int(score)))
                        else:
                            repo.relevance_score = 50
                        repo.is_direct_competitor = bool(ev.get("is_direct_competitor", repo.relevance_score >= 60))
                        repo.relevance_reason = str(ev.get("relevance_reason") or "Evaluated fit against project idea.")
                    else:
                        repo.relevance_score = 50
                        repo.is_direct_competitor = True
                        repo.relevance_reason = "Search candidate."
        except Exception:
            for repo in repositories:
                if repo.relevance_score is None:
                    repo.relevance_score = 50
                repo.is_direct_competitor = True
                if not repo.relevance_reason:
                    repo.relevance_reason = "Keyword search match."

        return repositories

