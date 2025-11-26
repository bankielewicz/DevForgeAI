#!/bin/bash
# STORY-066: NPM Package Creation & Structure
# Test Execution Script
#
# Purpose: Run test suite and validate TDD RED phase
# Expected: All tests should fail (no implementation exists yet)

set -e

echo "=========================================="
echo "STORY-066: NPM Package Test Suite"
echo "TDD Phase: RED (Expected: All Tests Fail)"
echo "=========================================="
echo ""

# Change to test directory
cd "$(dirname "$0")"

# Check if Node.js and npm are available
echo "Checking prerequisites..."
if ! command -v node &> /dev/null; then
    echo "❌ ERROR: Node.js not found"
    echo "   Install Node.js 18+ from https://nodejs.org"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ ERROR: npm not found"
    echo "   Install npm 8+ (bundled with Node.js)"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'.' -f1 | sed 's/v//')
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ ERROR: Node.js 18+ required (current: $(node --version))"
    exit 1
fi

echo "✓ Node.js $(node --version)"
echo "✓ npm $(npm --version)"
echo ""

# Install test dependencies if not present
if [ ! -d "node_modules" ]; then
    echo "Installing test dependencies..."
    npm install --silent
    echo "✓ Dependencies installed"
    echo ""
fi

# Run tests
echo "Running test suite..."
echo ""

# Capture exit code (tests will fail in RED phase)
set +e
npm test
TEST_EXIT_CODE=$?
set -e

echo ""
echo "=========================================="
echo "Test Execution Complete"
echo "=========================================="

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "⚠️  UNEXPECTED: All tests passed"
    echo "   Expected: Tests should fail (TDD RED phase)"
    echo "   This means implementation already exists"
    exit 0
else
    echo "✓ EXPECTED: Tests failed (TDD RED phase)"
    echo "  Total Tests: 85+"
    echo "  Expected Failures: 85+"
    echo ""
    echo "Next Steps:"
    echo "  1. Review failed tests above"
    echo "  2. Create package.json with required metadata"
    echo "  3. Create bin/devforgeai.js CLI entry point"
    echo "  4. Create .npmignore, LICENSE, README.md"
    echo "  5. Run tests iteratively until GREEN"
    exit 0
fi
