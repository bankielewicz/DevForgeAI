#!/bin/bash
# Test Runner: STORY-440 - Rename Architecture Skill to designing-systems
# Generated: 2026-02-18
#
# Usage: bash tests/STORY-440/run_all_tests.sh
#   or:  pytest tests/STORY-440/ -v

set -e
cd "$(dirname "$0")/../.."
pytest tests/STORY-440/ -v --tb=short
