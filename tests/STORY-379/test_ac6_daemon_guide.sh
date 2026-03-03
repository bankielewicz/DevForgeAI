#!/bin/bash
# STORY-379 AC#6: Daemon Mode Usage Guide with Start, Stop, and Status Commands
# Tests verify the daemon mode section contains:
#   - Daemon purpose (persistent index, reduced latency, background re-indexing)
#   - Start daemon command
#   - Stop daemon command
#   - Status check command
#   - .treelint/ directory structure (index.db, config.toml, daemon.sock)
#   - Gitignore guidance referencing source-tree.md
#   - Recommendation threshold (1000+ files)
#
# TDD Red Phase: All tests MUST FAIL because docs/guides/treelint-integration-guide.md does not exist yet.

set -e

GUIDE="/mnt/c/Projects/DevForgeAI2/docs/guides/treelint-integration-guide.md"

echo "=== AC#6: Daemon Mode Usage Guide with Start, Stop, and Status Commands ==="

# Test 1: Guide file exists
echo -n "Test 1: Guide file exists... "
if [ -f "$GUIDE" ]; then
    echo "PASS"
else
    echo "FAIL - File does not exist"
    exit 1
fi

# Test 2: Daemon mode section header exists
echo -n "Test 2: Daemon mode section header exists... "
if grep -qi "## Daemon\|## Daemon Mode\|## Background Daemon" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Daemon mode section header not found"
    exit 1
fi

# Test 3: Daemon purpose documented (persistent index)
echo -n "Test 3: Daemon purpose documented... "
if grep -qi "persistent.*index\|background.*index\|re-index\|latency" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Daemon purpose (persistent index, latency) not documented"
    exit 1
fi

# Test 4: Start daemon command documented
echo -n "Test 4: Start daemon command documented... "
if grep -qi "start\|daemon.*start\|treelint.*daemon" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Start daemon command not documented"
    exit 1
fi

# Test 5: Stop daemon command documented
echo -n "Test 5: Stop daemon command documented... "
if grep -qi "stop\|daemon.*stop\|shutdown" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Stop daemon command not documented"
    exit 1
fi

# Test 6: Status check command documented
echo -n "Test 6: Status check command documented... "
if grep -qi "status\|daemon.*status" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Status check command not documented"
    exit 1
fi

# Test 7: .treelint/ directory structure - index.db
echo -n "Test 7: .treelint/index.db documented... "
if grep -q "index\.db" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - index.db not documented"
    exit 1
fi

# Test 8: .treelint/ directory structure - config.toml
echo -n "Test 8: .treelint/config.toml documented... "
if grep -q "config\.toml" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - config.toml not documented"
    exit 1
fi

# Test 9: .treelint/ directory structure - daemon.sock
echo -n "Test 9: .treelint/daemon.sock documented... "
if grep -q "daemon\.sock" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - daemon.sock not documented"
    exit 1
fi

# Test 10: Gitignore guidance present
echo -n "Test 10: Gitignore guidance present... "
if grep -qi "gitignore\|\.gitignore\|git.*ignore" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Gitignore guidance not found"
    exit 1
fi

# Test 11: source-tree.md referenced for gitignore patterns
echo -n "Test 11: source-tree.md referenced... "
if grep -q "source-tree\.md\|source-tree" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - source-tree.md reference not found"
    exit 1
fi

# Test 12: Recommendation threshold (1000+ files)
echo -n "Test 12: Recommendation threshold (1000+ files) stated... "
if grep -q "1000\|1,000" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - 1000+ files recommendation threshold not found"
    exit 1
fi

echo ""
echo "=== AC#6 All Tests Passed ==="
exit 0
