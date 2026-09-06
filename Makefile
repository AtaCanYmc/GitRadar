.DEFAULT_GOAL := help

# Python & virtual environment detection
VENV ?= .venv
ifeq ($(wildcard $(VENV)/bin/python),)
	PYTHON := python3
	PIP := pip3
	PYTEST := pytest
else
	PYTHON := $(VENV)/bin/python
	PIP := $(VENV)/bin/pip
	PYTEST := $(VENV)/bin/pytest
endif

.PHONY: help venv install test test-v run-ui cli config sync-demo clean

help: ## Display this help message
	@echo "📡 GitRadar Development Commands:"
	@echo ""
	@grep -E "^[a-zA-Z_-]+:.*?## .*$$" $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

venv: ## Create virtual environment (.venv)
	python3 -m venv $(VENV)
	@echo "Virtual environment created at $(VENV)."

install: ## Install package in editable mode with dev dependencies
	$(PIP) install -e ".[dev]"

test: ## Run test suite
	$(PYTEST) tests/

test-v: ## Run test suite with verbose output
	$(PYTEST) tests/ -v

run-ui: ## Launch the local web dashboard
	$(PYTHON) -m gitradar.cli ui

cli: ## Show CLI help and available commands
	$(PYTHON) -m gitradar.cli --help

config: ## Display active GitRadar configuration
	$(PYTHON) -m gitradar.cli config --show

sync-demo: ## Synchronize core package and assets to demo/ (Vercel)
	@echo "Syncing gitradar/ to demo/gitradar/..."
	rsync -av --exclude "__pycache__" --exclude "*.pyc" gitradar/ demo/gitradar/
	@echo "Syncing static assets to demo/public/..."
	cp gitradar/web/static/css/style.css demo/public/css/style.css
	cp gitradar/web/static/js/app.js demo/public/js/app.js
	python3 -c "with open('gitradar/web/templates/index.html') as f: c = f.read(); c = c.replace(\"{{ url_for('static', filename='css/style.css') }}\", 'css/style.css').replace(\"{{ url_for('static', filename='js/app.js') }}\", 'js/app.js').replace('href=\"/favicon', 'href=\"favicon').replace('href=\"/site.webmanifest\"', 'href=\"site.webmanifest\"').replace('href=\"/apple-touch-icon.png\"', 'href=\"apple-touch-icon.png\"'); open('demo/public/index.html', 'w').write(c)"
	@echo "✅ Demo directory synchronized successfully."

clean: ## Clean build artifacts, caches, and bytecode
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "🧹 Cleaned caches and build artifacts."
