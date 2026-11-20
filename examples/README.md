[← Back to Root Repository](../README.md)

# GitRadar Examples and Automation Recipes (`examples/`)

Runnable Python SDK scripts, shell batch pipelines, and sample output schemas for integrating GitRadar into local workflows or CI jobs.

## Contents

| File | Type | Description |
| :--- | :--- | :--- |
| [`python_sdk_usage.py`](./python_sdk_usage.py) | Python Script | Imports `GitHubService` and `LLMService` directly to run programmatic gap analysis. |
| [`batch_analyze_ideas.sh`](./batch_analyze_ideas.sh) | POSIX Shell | Sequentially analyzes an array of software project concepts via `gitradar analyze`. |
| [`ci_market_check.sh`](./ci_market_check.sh) | POSIX Shell | Executes automated repository search and market checks inside CI environments. |
| [`sample_gap_report.json`](./sample_gap_report.json) | JSON Artifact | Sample serialized `GapAnalysisReport` output payload. |

## Prerequisites

Install `gitradar` in editable mode from the repository root and configure an API key:

```bash
pip install -e ".[dev]"
gitradar config --openai-api-key "sk-your_api_key_here"
```

## Usage

### 1. Python SDK Script

```bash
python3 examples/python_sdk_usage.py
```

### 2. Batch Analysis Script

```bash
chmod +x examples/batch_analyze_ideas.sh
./examples/batch_analyze_ideas.sh
```

### 3. CI Market Check Script

```bash
chmod +x examples/ci_market_check.sh
./examples/ci_market_check.sh "AI git commit message linter"
```
