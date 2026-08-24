# Changelog

All notable changes to the **GitRadar** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.2] - 2026-08-24

### Added
- 🛠️ **Technical Implementation & Open-Source Roadmap**:
  - Introduced `ImplementationGuide` and `OpenSourceTool` Pydantic schemas.
  - Recommends architecture overviews, tech stacks, and relevant open-source libraries (`Typer`, `LiteLLM`, `Qdrant`, etc.) for every analyzed idea.
- 🌐 **AI Prompt Response Language Selection**:
  - Added `--lang` / `--language` CLI flag and `default_language` configuration setting.
  - Injects target response language (`English`, `Turkish`, `Spanish`, `German`, `French`, etc.) into Jinja2 prompt engine.
- 📥 **Web UI Report Export**:
  - Added Export Toolbar supporting **Markdown (`.md`)**, **JSON (`.json`)**, and **Copy to Clipboard**.
- 🚀 **Vercel Web Demo (`demo/`)**:
  - Added standalone `demo/` folder with 1-Click Vercel Deployment button (`vercel.json`, `api/index.py`, `public/`).
  - Supports client-side custom Groq API Key & GitHub Access Token authorization via `X-Groq-Api-Key` and `X-Github-Token` HTTP headers.
- ⚙️ **Web UI Configuration Modal**:
  - Added Settings Modal (⚙️) to configure LLM model, analysis limit, response language, custom Groq Key & GitHub Token directly in browser.
- 🎨 **Theme & Multi-Language Enhancements**:
  - Integrated Light / Dark mode theme toggle.
  - Added English & Turkish (EN / TR) client-side i18n translation switcher.
  - Installed RealFaviconGenerator cross-platform web favicons.
- 🐍 **Python < 3.11 Compatibility**:
  - Backported `NotRequired` and typing extensions to support Python 3.10 and earlier seamlessly.

---

## [0.1.1] - 2026-08-19

### Documentation
- Update architecture and contributing documentation for clarity and detail ([594974f](https://github.com/AtaCanYmc/GitRadar/commit/594974fe99ededbede3d1b06f4a18afc8456f9cb)).

---

## [0.1.0] - 2026-08-10

### Added
- 🚀 Initial release of **GitRadar CLI**.
- 💡 `gitradar analyze`: LLM-driven query expansion and semantic market/gap analysis workflow.
- 🔍 `gitradar search`: Fast standalone repository search via GitHub REST API (`httpx`).
- ⚙️ `gitradar config`: Persistent settings manager storing API keys (`GROQ_API_KEY`, `GITHUB_TOKEN`) in `~/.config/gitradar/config.env`.
- 🎨 Rich UI integration: Animated spinners, formatted repository tables, and markdown report panels.
- 🧪 Pytest test suite covering models and CLI interface commands.
- 📖 Complete developer documentation suite (`README.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `SECURITY.md`).
