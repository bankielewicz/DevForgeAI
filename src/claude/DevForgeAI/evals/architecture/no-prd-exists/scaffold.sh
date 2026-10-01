#!/usr/bin/env bash
# Seeds the fixtures for SPEC-003 VER-23 (no-prd-exists).
set -euo pipefail
mkdir -p docs/specs/prd
cat > docs/specs/prd/.gitkeep <<'FIXTURE'
FIXTURE
