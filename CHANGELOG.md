# Changelog

All notable changes to the **GitRadar** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.4](https://github.com/AtaCanYmc/GitRadar/compare/v0.1.3...v0.1.4) (2026-08-26)


### Features

* add minimum relevance threshold input and filtering for repository evaluation ([bfc56cb](https://github.com/AtaCanYmc/GitRadar/commit/bfc56cb49da96ea86961db98f669b90a2cad3820))
* add relevance scoring and display for discovered repositories ([e330512](https://github.com/AtaCanYmc/GitRadar/commit/e33051297b7c138a01135e530edd90bb1b79f0cc))
* implement relevance evaluation system for GitHub repositories ([70c0ffd](https://github.com/AtaCanYmc/GitRadar/commit/70c0ffdad09dcf4b54eab78f1e433277262b6414))
* increase maximum repositories to analyze and adjust sorting criteria for improved relevance evaluation ([adcd024](https://github.com/AtaCanYmc/GitRadar/commit/adcd0247139c0023ee7e9a90e6f941621709b282))
* synchronize AI response language with active UI language and update report generation instructions ([fa27a96](https://github.com/AtaCanYmc/GitRadar/commit/fa27a96cee35ae728577d575ee5933d902fca7f1))
* update input fields to textareas for improved user experience and add Enter key functionality ([8cef591](https://github.com/AtaCanYmc/GitRadar/commit/8cef5919f1494bdd9a6431fbce06fe19befa4cdf))
* update version to 0.1.3 and enhance mobile responsiveness with comprehensive media queries ([df97d6b](https://github.com/AtaCanYmc/GitRadar/commit/df97d6b40e40aef63d012fca3db8e353f9aec951))

## [0.1.3](https://github.com/AtaCanYmc/GitRadar/compare/v0.1.2...v0.1.3) (2026-08-24)


### Features

* add field validators for configuration settings to ensure defaults and handle empty values ([86debf6](https://github.com/AtaCanYmc/GitRadar/commit/86debf69d53ea62cc08e798d68f7df6efcfa69df))
* add sanitizeHeaderValue function to clean API keys and improve security ([6ed25f6](https://github.com/AtaCanYmc/GitRadar/commit/6ed25f6c5d6fbcc3d1994417ad64abaae73ec4d6))
* enhance JSON handling and default values in models for improved data integrity ([c6367f0](https://github.com/AtaCanYmc/GitRadar/commit/c6367f0336d6e2edfc6312cf4ab2bd929e81fe26))
* implement GitRadar web dashboard module with async GitHub API integration and market analysis features ([cf3bce3](https://github.com/AtaCanYmc/GitRadar/commit/cf3bce391c73ae58e53d1cb941a88d01726fc928))
* improve error handling for invalid Groq API keys and sync custom settings on load ([8104a7d](https://github.com/AtaCanYmc/GitRadar/commit/8104a7de64683c9c9bab3e107cf5b270964d0792))
* update page title for clarity in Vercel web demo ([1ee6c6a](https://github.com/AtaCanYmc/GitRadar/commit/1ee6c6aeb785e1dead560963b0edfdce69ef0ff2))

## [0.1.2](https://github.com/AtaCanYmc/GitRadar/compare/v0.1.1...v0.1.2) (2026-08-24)


### Features

* add export functionality for reports in Markdown and JSON formats with language selection support ([e870300](https://github.com/AtaCanYmc/GitRadar/commit/e87030028e5fc7b8ab2bbcca97a2cfd4fad9f917))
* add settings modal for user configuration with local storage support ([62a564c](https://github.com/AtaCanYmc/GitRadar/commit/62a564c05a015760483ee6b0e2d2d9e6dee75854))
* add static file serving and web app manifest for improved user experience ([1ef419b](https://github.com/AtaCanYmc/GitRadar/commit/1ef419ba6aac7cdc4ab46e0dd071b5fd587d5063))
* add Vercel deployment configuration and enhance web demo with language selection and report export features ([c17d9ed](https://github.com/AtaCanYmc/GitRadar/commit/c17d9edbf6fc7482eb7f7e7079fa5641b881cd35))
* enhance compatibility and add theme toggle with internationalization support ([b4f8695](https://github.com/AtaCanYmc/GitRadar/commit/b4f869595d4714b52339f28c849183e824070bc2))

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
