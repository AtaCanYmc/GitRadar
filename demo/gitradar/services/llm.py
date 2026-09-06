import json
import os
import re
from typing import List, Optional
from openai import OpenAI, AuthenticationError, APIError, NotFoundError, BadRequestError
from gitradar.config import settings
from gitradar.models import ExpandedQueries, GapAnalysisReport, RepositoryInfo
from gitradar.prompts import render_prompt


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
    """Service to interact with OpenAI-compatible API endpoints for query expansion and gap analysis."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        language: Optional[str] = None,
    ):
        if api_key is not None:
            self.api_key = api_key.strip().strip("'\"")
        else:
            raw_key = (
                settings.openai_api_key
                or os.environ.get("OPENAI_API_KEY")
                or settings.groq_api_key
                or os.environ.get("GROQ_API_KEY")
                or ""
            )
            self.api_key = raw_key.strip().strip("'\"")

        if base_url is not None:
            raw_base_url = base_url
        else:
            raw_base_url = (
                settings.openai_base_url
                or os.environ.get("OPENAI_BASE_URL")
                or os.environ.get("OPENAI_API_BASE")
            )

        if raw_base_url:
            self.base_url = raw_base_url.strip().strip("'\"").rstrip("/")
        elif self.api_key.startswith("gsk_"):
            # Auto-detect Groq OpenAI-compatible endpoint for Groq keys
            self.base_url = "https://api.groq.com/openai/v1"
        elif api_key is None and not self.api_key and settings.groq_api_key:
            # Fallback to Groq if only groq is configured
            self.api_key = settings.groq_api_key.strip().strip("'\"")
            self.base_url = "https://api.groq.com/openai/v1"
        else:
            self.base_url = None

        # Local endpoints (Ollama, LM Studio, vLLM) may run without API keys
        if self.base_url and any(h in self.base_url for h in ["localhost", "127.0.0.1", "0.0.0.0"]):
            if not self.api_key:
                self.api_key = "ollama"

        raw_model = model or settings.default_model or "gpt-4o-mini"
        if raw_model.startswith("groq/"):
            raw_model = raw_model.replace("groq/", "", 1)

        # If routed to Groq and model is OpenAI default, default to Groq's high-capability model
        if self.base_url and "groq.com" in self.base_url and raw_model in ("gpt-4o-mini", "gpt-4o"):
            raw_model = "llama-3.3-70b-versatile"

        self.model = raw_model
        self.language = language or settings.default_language
        self._client: Optional[OpenAI] = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            self._ensure_api_key()
            effective_key = self.api_key or "no-key-required"
            self._client = OpenAI(
                api_key=effective_key,
                base_url=self.base_url,
                timeout=60.0,
            )
        return self._client

    def _ensure_api_key(self):
        # Local endpoints (Ollama, LM Studio, vLLM) may run without API keys
        if self.base_url and any(h in self.base_url for h in ["localhost", "127.0.0.1", "0.0.0.0"]):
            if not self.api_key:
                self.api_key = "ollama"
            return

        if not self.api_key or self.api_key.strip() in ("", "sk-...", "gsk_...", "gsk_your_groq_api_key_here"):
            raise ValueError(
                "Missing AI API Key! Please configure OPENAI_API_KEY (or GROQ_API_KEY) in Settings (⚙️), "
                "or run `gitradar config --openai-api-key YOUR_KEY`."
            )

    def _fetch_active_models(self) -> List[str]:
        """Dynamically query the OpenAI-compatible endpoint for available models."""
        try:
            res = self.client.models.list()
            models = [m.id for m in res.data]
            text_models = [
                m for m in models
                if not any(x in m.lower() for x in ["whisper", "tts", "embedding", "dall-e", "guard", "moderation"])
            ]
            return text_models
        except Exception:
            return []

    def _completion_with_fallback(self, messages: List[dict], temperature: float = 0.3) -> dict:
        """Try primary model, fallback models, and handle JSON mode variations."""
        candidates = [self.model]
        if self.base_url and "groq.com" in self.base_url:
            candidates.extend([
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "openai/gpt-oss-120b",
                "qwen/qwen3.6-27b",
            ])
        else:
            candidates.extend([
                "gpt-4o-mini",
                "gpt-4o",
                "gpt-3.5-turbo",
            ])

        models_to_try = []
        for m in candidates:
            if m and m not in models_to_try:
                models_to_try.append(m)

        last_exception = None

        for model_name in models_to_try:
            # 1. First attempt: JSON object response format
            try:
                res = self.client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=temperature,
                    response_format={"type": "json_object"},
                )
                content = res.choices[0].message.content
                return extract_json(content)
            except AuthenticationError as ae:
                raise ValueError(
                    f"Authentication Failed with AI Provider ({self.base_url or 'OpenAI'}): Invalid API Key. "
                    "Please update your key in Settings (⚙️) or via `gitradar config`."
                ) from ae
            except Exception as e:
                err_str = str(e).lower()
                if any(k in err_str for k in ["invalid_api_key", "incorrect api key", "unauthorized"]):
                    raise ValueError(
                        f"Authentication Failed with AI Provider ({self.base_url or 'OpenAI'}): Invalid API Key. "
                        "Please update your key in Settings (⚙️) or via `gitradar config`."
                    ) from e
                last_exception = e

            # 2. Second attempt: Plain text completion (fallback for providers without response_format support)
            try:
                res = self.client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=temperature,
                )
                content = res.choices[0].message.content
                return extract_json(content)
            except AuthenticationError as ae:
                raise ValueError(
                    f"Authentication Failed with AI Provider ({self.base_url or 'OpenAI'}): Invalid API Key. "
                    "Please update your key in Settings (⚙️) or via `gitradar config`."
                ) from ae
            except Exception as e:
                err_str = str(e).lower()
                if any(k in err_str for k in ["invalid_api_key", "incorrect api key", "unauthorized"]):
                    raise ValueError(
                        f"Authentication Failed with AI Provider ({self.base_url or 'OpenAI'}): Invalid API Key. "
                        "Please update your key in Settings (⚙️) or via `gitradar config`."
                    ) from e
                last_exception = e
                continue

        if last_exception:
            raise last_exception
        raise RuntimeError("All model fallback attempts failed.")

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

