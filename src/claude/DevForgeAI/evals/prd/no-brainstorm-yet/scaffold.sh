#!/usr/bin/env bash
# Seeds the fixtures for SPEC-002 VER-33 (no-brainstorm-yet).
set -euo pipefail
cat > README.md <<'FIXTURE'
# Riverside Food Bank volunteer app

A web app where food bank volunteers see open warehouse shifts and sign up for them.
FIXTURE
