#!/bin/bash
# Audit commands for potential lean orchestration violations
# Story: STORY-410 - Create Automated Audit for Command/Skill Hybrid Violations
# Source: RCA-038 REC-4
#
# Usage: COMMANDS_DIR=.claude/commands bash audit-command-skill-overlap.sh
#
# Detects commands with excessive code blocks before Skill() invocation,
# which may indicate hybrid command/skill violations where manual workflow
# steps are documented in the command instead of delegating to the skill.
#
# Threshold: >4 code blocks (>8 triple-backtick lines) before Skill()
#
# Exit codes:
#   0 - All commands clean (no violations)
#   1 - One or more violations detected

# Strict mode (pipefail but not -e since grep returns 1 on no match)
set -uo pipefail

# Default to .claude/commands if COMMANDS_DIR not set
COMMANDS_DIR="${COMMANDS_DIR:-.claude/commands}"

# Validate directory exists
if [ ! -d "$COMMANDS_DIR" ]; then
  echo "ERROR: Directory not found: $COMMANDS_DIR" >&2
  exit 1
fi

# Threshold: more than 8 backtick lines = more than 4 code blocks = violation
BACKTICK_THRESHOLD=8

# Track violation count for exit code
violations=0

# Handle case where no .md files exist
shopt -s nullglob

for cmd in "$COMMANDS_DIR"/*.md; do
  filename=$(basename "$cmd")

  # Find first line containing Skill(command= pattern
  first_skill_line=$(grep -n "Skill(command=" "$cmd" 2>/dev/null | head -1 | cut -d: -f1)

  if [ -z "$first_skill_line" ]; then
    echo "⚠️ $filename: No Skill() invocation found"
    continue
  fi

  # Count triple-backtick lines before the Skill() line
  # Each code block has an opening ``` and closing ```, so count = 2 * num_blocks
  backtick_lines=$(head -n "$((first_skill_line - 1))" "$cmd" 2>/dev/null | grep -c '```')

  if [ "$backtick_lines" -gt "$BACKTICK_THRESHOLD" ]; then
    echo "❌ $filename: $backtick_lines code blocks before Skill() - potential hybrid violation"
    violations=$((violations + 1))
  else
    echo "✅ $filename: Clean ($backtick_lines code blocks before Skill())"
  fi
done

# Exit non-zero if any violations found
if [ "$violations" -gt 0 ]; then
  exit 1
fi

exit 0
