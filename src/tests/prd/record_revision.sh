#!/usr/bin/env bash
# Binds an eval results folder to what it tested (SPEC-002 v2 verification plan §3, "Revision binding"):
# the commit, the plugin tree's digest and a copy of the tag's eval cases (prompts, scaffolds, graders).
# Run from the repository root, before `claude plugin eval`, with a new folder for every run:
#   bash src/tests/prd/record_revision.sh <results-dir> <tag>
# It refuses a dirty tree or an existing folder, so a rerun never replaces an earlier result.
set -euo pipefail
dir="${1:?usage: record_revision.sh <results-dir> <tag>}"
tag="${2:?usage: record_revision.sh <results-dir> <tag>}"
plugin=src/claude/DevForgeAI
[ -d "$plugin/evals/$tag" ] || { echo "no eval cases for tag '$tag'" >&2; exit 1; }
[ -z "$(git status --porcelain -- src docs)" ] || { echo "commit first: src/ or docs/ has changes" >&2; exit 1; }
[ ! -e "$dir" ] || { echo "$dir exists: use a new folder for every run" >&2; exit 1; }
mkdir -p "$dir"
git rev-parse HEAD > "$dir/REVISION"
find "$plugin" -path '*/evals/results' -prune -o -type f -print0 | sort -z | xargs -0 sha256sum \
  | sha256sum > "$dir/PLUGIN-DIGEST"
cp -r "$plugin/evals/$tag" "$dir/cases-$tag"
date -u +%Y-%m-%dT%H:%M:%SZ > "$dir/STARTED"
echo "bound $dir to $(cut -c1-12 "$dir/REVISION"), digest $(cut -c1-16 "$dir/PLUGIN-DIGEST")"
