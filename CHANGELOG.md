# Changelog

All notable changes to the **GitRadar** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.1](https://github.com/AtaCanYmc/GitRadar/compare/v0.1.0...v0.1.1) (2026-08-19)


### Documentation

* update architecture and contributing documentation for clarity and detail ([594974f](https://github.com/AtaCanYmc/GitRadar/commit/594974fe99ededbede3d1b06f4a18afc8456f9cb))

## [0.1.0] - 2026-08-10

### Added
- 🚀 Initial release of **GitRadar CLI**.
- 💡 `gitradar analyze`: LLM-driven query expansion and semantic market/gap analysis workflow.
- 🔍 `gitradar search`: Fast standalone repository search via GitHub REST API (`httpx`).
- ⚙️ `gitradar config`: Persistent settings manager storing API keys (`GROQ_API_KEY`, `GITHUB_TOKEN`) in `~/.config/gitradar/config.env`.
- 🎨 Rich UI integration: Animated spinners, formatted repository tables, and markdown report panels.
- 🧪 Pytest test suite covering models and CLI interface commands.
- 📖 Complete developer documentation suite (`README.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `SECURITY.md`).
