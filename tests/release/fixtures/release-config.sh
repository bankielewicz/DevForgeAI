#!/bin/bash
# Release Configuration (Test Fixture - STORY-070)

# Exclusion patterns for sync operations
CLAUDE_EXCLUDE_PATTERNS=(
  "*.backup*"
  "__pycache__/"
  "*.pyc"
  ".DS_Store"
)

DEVFORGEAI_EXCLUDE_PATTERNS=(
  "backups/"
  "qa/reports/"
  "feedback/sessions/"
  "*.log"
)

# Sensitive file patterns (must never be synced)
SENSITIVE_PATTERNS=(
  "*.env"
  "*.key"
  "secrets/"
  "credentials.json"
)

# NPM registry URL
NPM_REGISTRY="https://registry.npmjs.org"

# Checksum algorithm (SHA-256 only)
CHECKSUM_ALGORITHM="sha256"

# Minimum file count for validation
MIN_FILE_COUNT=50

# GitHub organization/user
GITHUB_ORG="devforgeai"
GITHUB_REPO="framework"

# NPM package name
NPM_PACKAGE="@devforgeai/framework"
