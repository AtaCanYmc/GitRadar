# Contributing to GitRadar 📡

Thank you for your interest in contributing to **GitRadar**! We welcome contributions from developers of all skill levels. Whether you are fixing a bug, adding new prompt templates, building Web UI components, or improving documentation, your efforts are appreciated.

---

## 📜 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](./CODE_OF_CONDUCT.md). Please ensure respectful and constructive communication in all interactions.

---

## 🛠️ Development Setup

### 1. Fork & Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/GitRadar.git
cd GitRadar
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Editable Package with Dev Dependencies

```bash
pip install -e ".[dev]"
```

---

## 🧪 Running Tests & Validation

Ensure all unit tests pass before submitting a Pull Request:

```bash
pytest
```

---

## 💡 Adding New Prompt Templates

GitRadar decouples LLM prompt logic into Jinja2 templates:
1. Add or edit `.j2` template files in `gitradar/prompts/`.
2. Add a corresponding test case in `tests/test_prompts.py` to verify template rendering.

---

## 🌐 Extending the Web Dashboard

The web dashboard is powered by Flask:
1. Backend routes are located in `gitradar/web/app.py`.
2. HTML templates are in `gitradar/web/templates/`.
3. Static CSS and JS assets are in `gitradar/web/static/`.
4. Add route tests in `tests/test_web.py`.

---

## 📝 Conventional Commit Format

GitRadar uses **Release Please** for automated release management. All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat(cli): add new interactive option` (Minor release bump `0.1.0` -> `0.2.0`)
- `fix(llm): resolve fallback model parsing error` (Patch release bump `0.1.0` -> `0.1.1`)
- `docs(readme): update architectural diagram`
- `chore(deps): update litellm dependency`

---

## 🔄 Pull Request Guidelines

1. Create a descriptive feature branch (`git checkout -b feature/your-feature-name`).
2. Keep commits atomic with conventional commit messages.
3. Verify test suite passes (`pytest`).
4. Submit your Pull Request targeting the `main` branch.

Happy Coding! 🚀
