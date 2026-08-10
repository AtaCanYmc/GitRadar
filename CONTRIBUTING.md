# Contributing to GitRadar 📡

Thank you for your interest in contributing to **GitRadar**! We welcome contributions from developers of all skill levels. Whether you are fixing a bug, improving documentation, adding new features, or optimizing LLM prompts, your efforts are appreciated.

---

## 📜 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](./CODE_OF_CONDUCT.md). Please ensure respectful and constructive communication in all interactions.

---

## 🛠️ Development Setup

To set up a local development environment for GitRadar:

### 1. Fork & Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/GitRadar.git
cd GitRadar
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install in Editable Mode with Dev Dependencies

```bash
pip install -e ".[dev]"
```

---

## 🧪 Running Tests

Ensure all unit tests pass before opening a Pull Request:

```bash
pytest
```

To run tests with detailed verbosity:

```bash
pytest -vv
```

---

## 🎨 Coding Standards & Guidelines

- **Python Version**: Write clean Python 3.10+ code.
- **Type Annotations**: Use type hints for function arguments and return values wherever applicable.
- **Style Conventions**: Follow [PEP 8](https://peps.python.org/pep-0008/) naming and formatting standards.
- **Data Models**: Use Pydantic `BaseModel` for structured data definitions.
- **Error Handling**: Gracefully catch network timeouts, API rate limits, and missing configuration settings, presenting user-friendly messages via `gitradar.utils.ui`.

---

## 🔄 Pull Request Guidelines

1. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Commit Your Changes**: Keep commits atomic and descriptive.
   ```bash
   git commit -m "feat(services): add fallback search mechanism"
   ```
3. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
4. **Open a Pull Request**: Provide a clear description of the problem solved or feature added. Reference any relevant GitHub issues.

---

## 💬 Getting Help

If you have questions or need guidance, feel free to open a [GitHub Discussion](https://github.com/username/GitRadar/discussions) or create an issue.

Happy Coding! 🚀
