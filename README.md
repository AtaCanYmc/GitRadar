# 📡 GitRadar

<p align="center">
  <img src="https://raw.githubusercontent.com/username/GitRadar/main/assets/gitradar-banner.png" alt="GitRadar Banner" width="700"/>
</p>

<p align="center">
  <b>Smart GitHub Market & Gap Analysis CLI Tool Driven by AI & GitHub REST API</b>
</p>

<p align="center">
  <a href="https://github.com/username/GitRadar/actions"><img src="https://img.shields.io/github/actions/workflow/status/username/GitRadar/ci.yml?branch=main&style=flat-square&logo=github" alt="CI Status"></a>
  <a href="https://pypi.org/project/gitradar/"><img src="https://img.shields.io/pypi/v/gitradar?style=flat-square&color=blue&logo=pypi" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/gitradar/"><img src="https://img.shields.io/pypi/pyversions/gitradar?style=flat-square&logo=python" alt="Python Versions"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/username/GitRadar?style=flat-square" alt="License"></a>
</p>

---

## 💡 What is GitRadar?

**GitRadar** is an open-source Command Line Interface (CLI) tool designed for software developers, founders, and open-source creators. 

Before spending weeks building a new side-project or open-source tool, **GitRadar** analyzes your idea directly from your terminal. It expands your prompt into intelligent GitHub search queries, scans existing repositories via the GitHub REST API, semantically evaluates competitor repos using **LiteLLM** (Groq / Llama 3), and renders an executive **Market & Gap Analysis Report** right inside your terminal.

---

## ✨ Key Features

- 🧠 **AI Query Expansion**: Translates raw developer project ideas into optimized GitHub search queries, keywords, and topic tags (`#cli`, `#ai`, `#devtools`).
- ⚡ **Async GitHub Repository Scanning**: Concurrently fetches repository metadata, star/fork counts, topic tags, and README snippets via `httpx`.
- 🎯 **Semantic Gap Analysis**: Synthesizes market saturation levels, top competitor strengths/weaknesses, unmet developer needs, and unique differentiators.
- 🎨 **Rich Visual UX**: Renders color-coded status gauges, styled tables, Markdown panels, and progress spinners using `rich`.
- ⚙️ **Simple API Management**: Easily set and save your `GROQ_API_KEY` and optional `GITHUB_TOKEN` using `gitradar config`.

---

## 🛠️ System Architecture

```text
                                  +-----------------------+
                                  |   User Project Idea   |
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------------------+
                                  | LLM Query Expansion   | (LiteLLM / Groq)
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------------------+
                                  | GitHub Async Scanner  | (httpx REST API)
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------------------+
                                  | LLM Gap & Opportunity | (Semantic Analysis)
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------------------+
                                  |  Rich Terminal UX     | (Panels, Tables, Gauges)
                                  +-----------------------+
```

---

## 🚀 Quick Start

### Installation

Install GitRadar directly from PyPI (or locally in editable mode):

```bash
pip install gitradar
```

Or install from source:

```bash
git clone https://github.com/username/GitRadar.git
cd GitRadar
pip install -e .
```

---

## 🔑 Configuration

GitRadar requires a free **Groq API Key** for fast LLM inference (Llama 3.3 70B).

1. Set your Groq API Key:
   ```bash
   gitradar config --groq-api-key "gsk_your_groq_api_key_here"
   ```

2. *(Optional)* Add a GitHub Personal Access Token to boost rate limits from 60 to 5,000 requests/hour:
   ```bash
   gitradar config --github-token "ghp_your_github_token_here"
   ```

3. View your active configuration:
   ```bash
   gitradar config --show
   ```

---

## 💻 CLI Commands & Usage

### 💡 `gitradar analyze <IDEA>`

Runs full AI-driven market and gap analysis workflow on a project idea.

```bash
gitradar analyze "AI powered code review tool for terminal and git hooks"
```

**Options:**
- `--limit` / `-l`: Maximum repositories to evaluate (Default: `10`)
- `--model` / `-m`: Override default LiteLLM model (Default: `groq/llama-3.3-70b-versatile`)

**Sample Terminal Output Preview:**

```text
╭───────────────────────────────────────────────────────╮
│ 📡 GitRadar  CLI Market & Gap Analysis Tool  [v0.1.0] │
╰───────────────────────────────────────────────────────╯

🧠 LLM Search Strategy Generated:
  • Keywords: code review, git hooks, ai code review
  • Topics: #code-review, #git-hooks, #llm
  • Languages: Python, Rust

📊 Relevant Repositories Found (Top 5):
  1. owner/ai-reviewer (⭐ 4,200) - AI git hook reviewer
  2. dev/git-check    (⭐ 1,850) - Automated PR inspector

🎯 MARKET & GAP ANALYSIS REPORT
  • Market Saturation: Moderate (Saturation Score: 45/100)
  • Opportunity Score: 85/100 🚀
  • Unmet Needs: Lack of offline local LLM fallback, high latency on large diffs
  • Differentiators: Real-time interactive terminal UI, instant Groq inference
```

---

### 🔍 `gitradar search <QUERY>`

Performs a fast, direct GitHub repository search without LLM synthesis:

```bash
gitradar search "terminal devtools" --limit 5 --sort stars
```

---

### ⚙️ `gitradar config`

View or update CLI settings and credentials:

```bash
gitradar config --show
```

---

### ℹ️ `gitradar version`

Prints the current version of GitRadar:

```bash
gitradar version
```

---

## 🧪 Running Tests

GitRadar uses `pytest` for testing:

```bash
pip install -e ".[dev]"
pytest
```

---

## 🤝 Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](./CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) for guidelines on submitting pull requests, reporting issues, and setup instructions.

---

## 🛡️ Security

If you discover a security vulnerability within GitRadar, please consult our [SECURITY.md](./SECURITY.md) policy for disclosure procedures.

---

## 📄 License

GitRadar is open-source software licensed under the [MIT License](./LICENSE).
