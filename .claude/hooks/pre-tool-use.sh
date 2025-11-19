#!/bin/bash
# .claude/hooks/pre-tool-use.sh - DevForgeAI validation hook

TOOL_INPUT=$(cat)
COMMAND=$(echo "$TOOL_INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# Auto-approve safe DevForgeAI patterns
SAFE_PATTERNS=(
  "npm run test"
  "npm run build"
  "npm run lint"
  "pytest"
  "python -m pytest"
  "dotnet test"
  "dotnet build"
  "git status"
  "git diff"
  "git add"
  "git commit"
  "git log"
  "wc -"
  "bash tests/"
  "bash .claude/scripts/"
  "bash .devforgeai/"
  "echo "
  "cat tests/"
  "cat .devforgeai/"
  "grep -E"
  "head -"
  "tail -"
  "mkdir -p"
  "chmod +x"
  "dos2unix"
  "sed -i"
  "python3 -m json.tool"
)

for pattern in "${SAFE_PATTERNS[@]}"; do
  if [[ "$COMMAND" =~ ^${pattern} ]]; then
    exit 0  # Auto-approve
  fi
done

# Block anti-patterns
BLOCKED_PATTERNS=(
  "rm -rf"
  "sudo"
  "git push"
  "npm publish"
  "curl"
  "wget"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if [[ "$COMMAND" =~ ${pattern} ]]; then
    echo '{"decision": "block", "reason": "Dangerous operation: '"$COMMAND"'"}'
    exit 2
  fi
done

# For all others, ask user for approval
exit 1