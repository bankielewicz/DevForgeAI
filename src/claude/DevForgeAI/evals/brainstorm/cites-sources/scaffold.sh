#!/usr/bin/env bash
# Seeds the project file the prompt names as a source (VER-27).
set -euo pipefail
mkdir -p docs
cat > docs/contributor-survey.md <<'SURVEY'
# Contributor survey, October 2026

12 of 20 contributors said they gave up on an issue because nobody answered. fixture-survey-5b0c
3 of 20 said the labels helped them find an issue to work on.
SURVEY
