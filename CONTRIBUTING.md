# Contributing to GitRadar

This document defines the development environment setup, validation requirements, and commit conventions for contributing to GitRadar.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Test and Verification Suite](#test-and-verification-suite)
- [Subsystem Extension Guides](#subsystem-extension-guides)
- [Conventional Commits](#conventional-commits)
- [Pull Request Checklist](#pull-request-checklist)

## Code of Conduct

All contributors must adhere to the [Code of Conduct](./CODE_OF_CONDUCT.md).

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/AtaCanYmc/GitRadar.git
cd GitRadar
```

### 2. Virtual Environment and Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Or use the `Makefile` target:

```bash
make venv
make install
```

## Test and Verification Suite

Run the unit and integration test suite before opening a pull request:

```bash
pytest -v
```

If you modify files under `gitradar/` or `gitradar/web/`, synchronize the Vercel serverless bundle in `demo/`:

```bash
make sync-demo
```

## Subsystem Extension Guides

### Prompt Templates (`gitradar/prompts/`)

Prompt logic is decoupled from Python orchestration using Jinja2 templates:

1. Create or update `.j2` template files in `gitradar/prompts/`.
2. Verify prompt interpolation and schema output in `tests/test_prompts.py`.

### Web Dashboard (`gitradar/web/` and `demo/`)

The local web interface and Vercel demo share core Flask endpoints and frontend assets:

1. Edit backend routes in `gitradar/web/app.py`.
2. Edit HTML templates in `gitradar/web/templates/index.html` and static assets in `gitradar/web/static/`.
3. Run `make sync-demo` to propagate changes into `demo/`.
4. Add or update route tests in `tests/test_web.py`.

## Conventional Commits

GitRadar uses Release Please for automated semantic versioning and PyPI publishing. Commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

| Prefix | Version Impact | Purpose |
| :--- | :--- | :--- |
| `feat(scope):` | Minor (`0.1.x` -> `0.2.0`) | New CLI command, API endpoint, or prompt pipeline stage |
| `fix(scope):` | Patch (`0.1.5` -> `0.1.6`) | Bug fix, error handling refinement, or schema correction |
| `docs(scope):` | None | Documentation and governance updates |
| `refactor(scope):` | None | Internal code restructuring with no behavior change |
| `test(scope):` | None | Test suite additions or fixture updates |
| `chore(scope):` | None | Build scripts, CI workflows, or dependency updates |

## Pull Request Checklist

1. Create a topic branch from `main` (`git checkout -b feat/short-description`).
2. Keep commits atomic and formatted according to Conventional Commits.
3. Run `pytest` and verify all test modules pass.
4. Run `make sync-demo` if core package or web assets changed.
5. Open a pull request against `main` with verification output attached.
