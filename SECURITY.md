# Security Policy

## Supported Versions

Security patches are applied to the latest minor release track on the `main` branch.

| Version | Supported | Status |
| :--- | :---: | :--- |
| `0.1.x` | Yes | Active maintenance |
| `< 0.1.0` | No | End of life |

## Reporting a Vulnerability

Do not open a public GitHub issue for security vulnerabilities such as credential exposure, injection flaws, or unsafe dependencies.

1. Submit a private report via [GitHub Security Advisories](https://github.com/AtaCanYmc/GitRadar/security/advisories/new) or email `atacanymc@gmail.com`.
2. Include reproduction commands, affected file paths, environment configuration, and proof-of-concept logs.
3. Allow maintainers to remediate the defect before public disclosure.

## Response SLA

| Milestone | Target SLA |
| :--- | :--- |
| Initial acknowledgment | Within 48 hours |
| Triage and severity assessment | Within 7 business days |
| Patch release and coordinated advisory | Upon verification of fix |

## Credential Handling Architecture

- **Local CLI and Web Server**: Credentials persisted via `gitradar config` are written only to `~/.config/gitradar/config.env` outside the repository tree.
- **Serverless Web Demo (`demo/`)**: User API keys are stored in browser `localStorage` and forwarded per request via HTTPS headers (`X-OpenAI-Api-Key`, `X-Groq-Api-Key`, `X-Github-Token`). Keys are never logged or persisted server-side.
