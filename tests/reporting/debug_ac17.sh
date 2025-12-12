#!/bin/bash
# Debug script for AC#1.7 - 50% boundary condition test

cd /mnt/c/Projects/DevForgeAI2

TEMP_DIR="/tmp/test_term_$$"
mkdir -p "$TEMP_DIR"

# Define ANSI codes
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
RED=$'\033[31m'

# Create mock epic with 4 features
cat > "$TEMP_DIR/EPIC-008.epic.md" << 'EOF'
---
id: EPIC-008
title: Boundary Epic
priority: High
---

## Features

### Feature 1.1: Feature A
### Feature 1.2: Feature B
### Feature 1.3: Feature C
### Feature 1.4: Feature D
EOF

# Create 2 stories (for 50% coverage: 2/4 features)
cat > "$TEMP_DIR/STORY-013.md" << 'EOF'
---
id: STORY-013
epic: EPIC-008
---
EOF

cat > "$TEMP_DIR/STORY-014.md" << 'EOF'
---
id: STORY-014
epic: EPIC-008
---
EOF

echo "=== FILES CREATED ==="
ls -la "$TEMP_DIR"
echo ""

# Run the report generator
output=$(bash .devforgeai/epic-coverage/generate-report.sh \
    --format=terminal \
    --epics-dir="$TEMP_DIR" \
    --stories-dir="$TEMP_DIR" \
    2>/dev/null)

# Show raw output with visible escape codes
echo "=== RAW OUTPUT (cat -v) ==="
echo "$output" | cat -v
echo ""

echo "=== NORMAL OUTPUT ==="
echo "$output"
echo ""

# Check for colors
echo "=== COLOR CHECKS ==="
if echo "$output" | grep -qF "$YELLOW"; then
    echo "YELLOW: FOUND ✓"
else
    echo "YELLOW: NOT FOUND ✗"
fi

if echo "$output" | grep -qF "$RED"; then
    echo "RED: FOUND (should NOT be present for 50%)"
else
    echo "RED: NOT FOUND ✓"
fi

echo ""
echo "=== TEST RESULT ==="
if echo "$output" | grep -qF "$YELLOW" && ! echo "$output" | grep -qF "$RED"; then
    echo "AC#1.7 PASS: 50% shows yellow, no red"
else
    echo "AC#1.7 FAIL: Boundary condition not met"
fi

# Cleanup
rm -rf "$TEMP_DIR"
