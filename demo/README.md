[← Back to Root Repository](../README.md)

# GitRadar Serverless Web Demo (`demo/`)

Standalone Vercel serverless deployment bundle for the GitRadar web dashboard.

## Table of Contents

- [Architecture and Credential Flow](#architecture-and-credential-flow)
- [Directory Structure](#directory-structure)
- [Synchronizing with Root Package](#synchronizing-with-root-package)
- [Local Verification with Vercel CLI](#local-verification-with-vercel-cli)
- [Deploying to Vercel](#deploying-to-vercel)

---

## Architecture and Credential Flow

The demo bundle runs statelessly on Vercel Python Serverless Functions (`@vercel/python`). No provider API keys are stored on the server:

1. Users open the Settings modal in the browser UI and enter an OpenAI-compatible API key (`sk-...` or `gsk_...`), optional custom base URL, and optional GitHub Personal Access Token (`ghp_...`).
2. Credentials are saved exclusively in browser `localStorage`.
3. Each request to `/api/analyze` or `/api/search` transmits keys via HTTPS request headers:

| Header | Target Service | Purpose |
| :--- | :--- | :--- |
| `X-OpenAI-Api-Key` | `LLMService` | Primary OpenAI-compatible API key |
| `X-OpenAI-Base-Url` | `LLMService` | Custom OpenAI-compatible base endpoint URL |
| `X-Groq-Api-Key` | `LLMService` | Legacy Groq API key header (auto-routes to Groq endpoint) |
| `X-Github-Token` | `GitHubService` | Per-request GitHub REST API bearer token |

---

## Directory Structure

```text
demo/
├── README.md                # Scoped Vercel demo documentation
├── api/
│   └── index.py             # Vercel WSGI entrypoint mounting gitradar.web.create_app()
├── gitradar/                # Synchronized copy of root gitradar package for Vercel bundling
├── public/                  # Static frontend assets served by Vercel CDN
│   ├── css/style.css        # Dashboard stylesheet
│   ├── js/app.js            # Frontend state, i18n, theme, and API client
│   ├── index.html           # Dashboard HTML entrypoint
│   └── site.webmanifest     # Web app manifest and favicons
├── requirements.txt         # Python runtime dependencies for Vercel builder
└── vercel.json              # Vercel rewrite rules routing /api/* to api/index.py
```

---

## Synchronizing with Root Package

Whenever files in the root `gitradar/` directory are modified, run the synchronization target from the repository root before deploying or committing:

```bash
make sync-demo
```

This copies `gitradar/` into `demo/gitradar/` and updates static asset paths in `demo/public/`.

---

## Local Verification with Vercel CLI

```bash
npm install -g vercel
cd demo
vercel dev
```

The local serverless preview listens on `http://localhost:3000`.

---

## Deploying to Vercel

Deploy directly from the `demo` root directory using the Vercel CLI or the Vercel GitHub integration:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FAtaCanYmc%2FGitRadar&root-directory=demo)
