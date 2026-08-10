# 📡 GitRadar

> **Smart GitHub Market & Gap Analysis CLI Tool**  
> AI-powered CLI tool that expands developer project ideas into GitHub search queries, scans existing repositories via GitHub REST API, semantically scores them, and generates an executive **Market & Gap Analysis** report directly in your terminal.

---

## 🌟 Key Features

- 🧠 **AI Query Expansion**: Uses LiteLLM (Groq / Llama 3) to translate raw ideas into optimized search keywords and GitHub topic tags.
- ⚡ **Async GitHub Scanning**: Concurrently searches repositories, evaluates star/fork ratios, and enriches top candidates with README summaries.
- 📊 **Semantic Gap Analysis**: Evaluates market saturation, identifies key competitors, unmet market needs, and unique differentiators.
- 🎨 **Rich Terminal UX**: Renders vibrant tables, color-coded status badges, and Markdown panels using `rich`.
- 🔑 **Flexible Configuration**: Store API keys safely in `~/.config/gitradar/config.env` or local `.env` files.

---

## 🛠️ Architecture Overview

```text
gitradar/
├── gitradar/
│   ├── __init__.py
│   ├── cli.py             # Typer CLI commands (analyze, search, config, version)
│   ├── config.py          # Pydantic settings & env manager
│   ├── models.py          # Data models (RepositoryInfo, GapAnalysisReport)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm.py         # LiteLLM client for Groq / Llama 3
│   │   └── github.py      # Async GitHub REST API client (httpx)
│   └── utils/
│       ├── __init__.py
│       └── ui.py          # Rich UI visualizer (Tables, Panels, Status)
├── pyproject.toml
├── README.md
└── .env.example
```

---

## 🚀 Quick Start

### 1. Installation

Install GitRadar locally in editable mode:

```bash
pip install -e .
```

### 2. Configure API Keys

GitRadar uses **Groq** for high-speed LLM inference. Set your Groq API key:

```bash
gitradar config --groq-api-key "gsk_your_groq_api_key"
```

*(Optional)* Provide a GitHub token to increase API rate limits (from 60 req/hr to 5,000 req/hr):

```bash
gitradar config --github-token "ghp_your_github_token"
```

Check your configuration at any time:

```bash
gitradar config --show
```

---

## 💻 Usage

### 💡 1. Analyze a Project Idea (`analyze`)

Run the full end-to-end AI analysis workflow:

```bash
gitradar analyze "AI tabanlı terminal kod inceleme ve refactoring aracı"
```

Options:
- `--limit` / `-l`: Max repositories to fetch and analyze (default: 10)
- `--model` / `-m`: Override LiteLLM model (default: `groq/llama-3.3-70b-versatile`)

### 🔍 2. Quick Repository Search (`search`)

Perform a fast standalone search on GitHub without LLM synthesis:

```bash
gitradar search "cli tool developer experience" --limit 5 --sort stars
```

### ℹ️ 3. Version Check (`version`)

```bash
gitradar version
```

---

## 📄 License

MIT License. Developed with ❤️ for developers worldwide.
