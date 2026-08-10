#!/usr/bin/env bash

# GitRadar Batch Analysis Shell Script
# Usage: ./examples/batch_analyze_ideas.sh

set -e

IDEAS=(
  "AI powered terminal code review tool"
  "Realtime CLI database monitoring dashboard"
  "Automated Git commit message generator using local LLM"
)

echo "📡 Starting GitRadar Batch Market Analysis..."
echo "------------------------------------------------"

for IDEA in "${IDEAS[@]}"; do
  echo "🔍 Analyzing: '$IDEA'"
  gitradar analyze "$IDEA" --limit 5
  echo "------------------------------------------------"
  sleep 2
done

echo "✅ Batch analysis completed!"
