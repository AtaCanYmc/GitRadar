# Roadmap

This document tracks shipped milestones and planned engineering work for GitRadar by release tag.

## Table of Contents

- [v0.1.x (Shipped)](#v01x-shipped)
- [v0.2.0 (Planned: Export, Caching, and CLI Output Formats)](#v020-planned-export-caching-and-cli-output-formats)
- [v0.3.0 (Planned: Deep Repository Telemetry and Comparison)](#v030-planned-deep-repository-telemetry-and-comparison)

## v0.1.x (Shipped)

- **v0.1.0**: Initial CLI (`analyze`, `search`, `ui`, `config`, `version`), asynchronous GitHub REST API search and README snippet enrichment, Jinja2 prompt engine, and Rich terminal renderer.
- **v0.1.1 - v0.1.3**: Universal OpenAI-compatible provider routing (`OPENAI_API_KEY`, `OPENAI_BASE_URL`, automatic Groq `gsk_` endpoint detection, local Ollama/vLLM support), dynamic model fallback, and dual-mode JSON extraction.
- **v0.1.4**: LLM relevance evaluation stage (`evaluate_repository_relevance`) and logarithmic star-weighted hybrid ranking (`rank_and_sort_by_relevance`) with `--min-relevance` filtering.
- **v0.1.5**: Flask local web dashboard and standalone Vercel serverless demo (`demo/`) with dark/light theme synchronization, EN/TR UI localization, custom sort/limit controls, and Markdown/JSON report export.

## v0.2.0 (Planned: Export, Caching, and CLI Output Formats)

- **CLI Machine-Readable Output**: Add `--output json` and `--output markdown` flags to `gitradar analyze` and `gitradar search` for direct file export and CI pipeline consumption.
- **Local SQLite Response Cache**: Optional TTL cache in `~/.cache/gitradar/` for GitHub search responses and README fetches to reduce redundant REST API calls during iterative idea refinement.
- **Configurable Rate-Limit Retry Backoff**: Automatic retry-after header parsing and exponential backoff in `GitHubService` when secondary GitHub API rate limits trigger.

## v0.3.0 (Planned: Deep Repository Telemetry and Comparison)

- **Commit Velocity and Maintenance Signals**: Enrich candidate repositories with last commit timestamp, release cadence, and issue resolution ratio to distinguish active competitors from abandoned projects.
- **Multi-Provider Evaluation Benchmarks**: Deterministic fixture benchmark script comparing query expansion and gap analysis schema compliance across OpenAI, Groq, DeepSeek, and local Ollama models.
- **Batch Comparison Mode**: Native CLI subcommand to run comparative gap analysis across a YAML or JSON manifest of project concepts.
