#!/usr/bin/env bash

# GitRadar CI Market Check Script
# Usage: ./examples/ci_market_check.sh "Your Project Idea"

set -e

PROJECT_IDEA="${1:-"CLI Developer Tool"}"

echo "📡 Running GitRadar Market Scan for: '$PROJECT_IDEA'"

# Run search via CLI
gitradar search "$PROJECT_IDEA" --limit 5

echo "------------------------------------------------"
echo "✅ Market scan complete!"
