# GitRadar Technical Architecture 🏛️

This document outlines the software architecture, component relationships, data flow pipelines, and resiliency strategies of **GitRadar**.

---

## 📐 High-Level Architectural Pattern

GitRadar adopts a modular, layer-decoupled architecture separating **Presentation** (Terminal CLI, Local Web UI, & Vercel Serverless Demo), **Domain Services** (GitHub REST API & LLM Orchestration), **Prompt Engine** (Jinja2 Templates), and **Persistence** (Pydantic Settings & LocalStorage).

```mermaid
graph TD
    subgraph PresentationLayer["Presentation Layer"]
        CLI["Typer CLI (gitradar.cli)"]
        WebUI["Flask Web App (gitradar.web)"]
        VercelDemo["Vercel Web Demo (demo/)"]
        RichUI["Rich Terminal Renderer (gitradar.utils.ui)"]
    end

    subgraph ServiceLayer["Service Layer"]
        LLM["LLM Service (gitradar.services.llm)"]
        GH["GitHub Service (gitradar.services.github)"]
    end

    subgraph DataLayer["Data & Prompt Layer"]
        Prompts["Jinja2 Prompt Engine (gitradar.prompts)"]
        Models["Pydantic Schemas (gitradar.models)"]
        Config["Config Manager (gitradar.config)"]
    end

    subgraph ExternalAPIs["External APIs"]
        GroqAPI["Groq REST API (LLM Inference)"]
        GitHubAPI["GitHub REST API (v3)"]
    end

    CLI --> LLM
    CLI --> GH
    CLI --> RichUI
    
    WebUI --> LLM
    WebUI --> GH

    VercelDemo --> LLM
    VercelDemo --> GH

    LLM --> Prompts
    LLM --> GroqAPI
    LLM --> Models

    GH --> GitHubAPI
    GH --> Models

    Config --> CLI
    Config --> WebUI
    Config --> LLM
    Config --> GH
```

---

## 📦 Component Details

### 1. Presentation Layer
- **CLI (`gitradar/cli.py`)**: Built on `typer`. Defines commands (`analyze`, `ui`, `search`, `config`, `version`), manages options/arguments (including `--lang` / `--language`), handles async runtime execution via `asyncio.run()`, and controls terminal status spinners.
- **Local Web UI (`gitradar/web/`)**: Built on `flask`. Hosts a single-page web dashboard (`/`), JSON REST endpoints (`/api/analyze`, `/api/search`, `/api/config`), serves static assets, and supports full report exporting (`.md`, `.json`, clipboard).
- **Vercel Web Demo (`demo/`)**: Standalone, Vercel-ready serverless environment (`demo/api/index.py` & `@vercel/python`). Accepts user-provided Groq API keys (`X-Groq-Api-Key`) and GitHub Access Tokens (`X-Github-Token`) via HTTPS headers for zero-server-state hosting.
- **Rich UI (`gitradar/utils/ui.py`)**: Renders stylized terminal banners, query strategy panels, repository tables, gap report panels, and technical implementation roadmaps.

### 2. Service Layer & Resiliency
- **GitHub Service (`gitradar/services/github.py`)**: Asynchronous HTTP client built with `httpx`. Executes concurrent keyword/topic searches via `asyncio.gather`, deduplicates repositories, handles rate limiting (HTTP 403), and enriches top candidates with README snippets. Accepts per-request user GitHub tokens.
- **LLM Service (`gitradar/services/llm.py`)**: Integrates LiteLLM with Groq models. Features:
  - **Prompt Response Language Resolution**: Injects requested target language (`English`, `Turkish`, `Spanish`, etc.) into prompt templates.
  - **Dynamic Groq Model Discovery**: Interrogates `https://api.groq.com/openai/v1/models` to discover active text models available for the user's API key.
  - **Fallback Execution**: Automatically tries primary model -> discovered active Groq models -> known fallback models.
  - **Dual Mode JSON Handling**: Tries `response_format={"type": "json_object"}` first; if rejected by provider server-side validation, retries in standard completion mode and parses content using `extract_json()`.
  - **Noise Suppression**: Sets `litellm.suppress_debug_info = True` and `litellm.set_verbose = False` to prevent log pollution.

### 3. Data Models (`gitradar/models.py`)
- **`RepositoryInfo`**: Summary schema for GitHub repositories.
- **`ExpandedQueries`**: LLM-derived search strategy.
- **`CompetitorSummary`**: Competitor strengths and gap profiles.
- **`OpenSourceTool`**: Recommended open-source library/tool (`name`, `category`, `description_and_usage`, `repo_url`).
- **`ImplementationGuide`**: Architecture overview, recommended tech stack, and open-source building blocks.
- **`GapAnalysisReport`**: Full executive gap report schema containing market saturation, opportunity score, unmet needs, differentiators, recommendations, and implementation roadmap.

### 4. Prompt Engine (`gitradar/prompts/`)
- Uses `jinja2.Environment` and `FileSystemLoader`.
- Decouples prompt engineering from Python code.
- Templates:
  - `query_expansion_system.j2` / `query_expansion_user.j2`
  - `gap_analysis_system.j2` / `gap_analysis_user.j2`

---

## 🔄 End-to-End Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant App as CLI / Web UI / Vercel
    participant LLM as LLMService
    participant GH as GitHubService
    participant Groq as Groq API
    participant GHREST as GitHub REST API

    User->>App: Input idea prompt & language choice
    App->>LLM: expand_idea_to_queries(idea, language)
    LLM->>Groq: Render Jinja2 prompt with language & query LLM
    Groq-->>LLM: JSON (keywords, topics, strategy explanation)
    LLM-->>App: ExpandedQueries object
    
    App->>GH: search_and_enrich(keywords, topics)
    GH->>GHREST: GET /search/repositories (Parallel)
    GHREST-->>GH: Raw repo metadata
    GH->>GHREST: GET /repos/{owner}/{repo}/readme
    GHREST-->>GH: README snippets
    GH-->>App: Enriched RepositoryInfo list
    
    App->>LLM: analyze_market_and_gaps(idea, repos, language)
    LLM->>Groq: Render Jinja2 gap template with language & query LLM
    Groq-->>LLM: JSON Gap Report (with Implementation Guide)
    LLM-->>App: GapAnalysisReport object
    App-->>User: Render Rich Terminal / Web Dashboard / Export (.md, .json)
```

---

## 🛡️ Error & Exception Matrix

| Failure Mode | Component | Handling & Fallback Strategy |
| --- | --- | --- |
| Missing `GROQ_API_KEY` | `LLMService` | Friendly `ValueError` guiding user to `gitradar config --groq-api-key` or browser Settings modal. |
| GitHub API Rate Limit (HTTP 403) | `GitHubService` | Catches status code and prompts user to set `GITHUB_TOKEN`. |
| Groq Model Not Found | `LLMService` | Dynamically queries `/v1/models` and falls back to active alternative models. |
| Server-side JSON Validate Failed | `LLMService` | Retries without `response_format` constraint and uses robust `extract_json()` regex parser. |
