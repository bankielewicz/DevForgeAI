#!/bin/bash
# STORY-267 AC#2: All 6 Supported Languages Documented
# Test: Each language (Python, Node.js, .NET, Go, Java, Rust) has complete documentation
#
# Expected: FAIL (documentation not yet expanded to cover all 6 languages comprehensively)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/references/deep-validation-workflow.md"
STORY_ID="STORY-267"
AC_NUM="AC#2"

echo "================================================================"
echo "  ${STORY_ID} - ${AC_NUM}: All 6 Supported Languages Documented"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Define the 6 required languages per tech-stack.md lines 127-134
LANGUAGES=("Python" "Node.js" ".NET" "Go" "Java" "Rust")

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Check file exists
if [[ ! -f "${TARGET_FILE}" ]]; then
    echo "FAIL: Target file does not exist"
    exit 1
fi

# Extract the Runtime Smoke Test section (look in section 1.4 as per AC#1)
# Fallback to section 1.3 if 1.4 not found (current state)
SECTION_CONTENT=""
if grep -q "^### 1\.4 Runtime Smoke Test" "${TARGET_FILE}"; then
    SECTION_CONTENT=$(sed -n '/^### 1\.4 Runtime Smoke Test/,/^##[#]* [0-9]/p' "${TARGET_FILE}")
elif grep -q "^### 1\.3 Runtime Smoke Test" "${TARGET_FILE}"; then
    echo "Note: Section 1.4 not found, checking section 1.3 (current state)"
    SECTION_CONTENT=$(sed -n '/^### 1\.3 Runtime Smoke Test/,/^##[#]* [0-9]/p' "${TARGET_FILE}")
fi

echo "Testing for comprehensive documentation of each language..."
echo ""

for LANG in "${LANGUAGES[@]}"; do
    echo "Language: ${LANG}"
    echo "  Checking for required documentation elements..."

    LANG_CHECKS=0
    LANG_REQUIRED=5

    # Check 1: Language name mentioned
    if echo "${SECTION_CONTENT}" | grep -qi "${LANG}"; then
        echo "    [x] Language name mentioned"
        ((LANG_CHECKS++))
    else
        echo "    [ ] Language name mentioned"
    fi

    # Check 2: Detection pattern documented (how to identify the language)
    # Look for patterns like "detect", "detection", "identify" near language name
    if echo "${SECTION_CONTENT}" | grep -iE "(detect|detection|identify).*${LANG}|${LANG}.*(detect|detection|identify)" | grep -qi .; then
        echo "    [x] Detection pattern documented"
        ((LANG_CHECKS++))
    else
        echo "    [ ] Detection pattern documented"
    fi

    # Check 3: Smoke test command documented
    # Different patterns for each language
    case "${LANG}" in
        "Python")
            COMMAND_PATTERN="python|pytest|pip"
            ;;
        "Node.js")
            COMMAND_PATTERN="node|npm|npx"
            ;;
        ".NET")
            COMMAND_PATTERN="dotnet"
            ;;
        "Go")
            COMMAND_PATTERN="go run|go build|go test"
            ;;
        "Java")
            COMMAND_PATTERN="java|mvn|gradle"
            ;;
        "Rust")
            COMMAND_PATTERN="cargo|rustc"
            ;;
    esac

    if echo "${SECTION_CONTENT}" | grep -qiE "${COMMAND_PATTERN}"; then
        echo "    [x] Smoke test command documented"
        ((LANG_CHECKS++))
    else
        echo "    [ ] Smoke test command documented"
    fi

    # Check 4: Entry point source documented (where to find package/artifact name)
    # Look for config file references
    case "${LANG}" in
        "Python")
            CONFIG_PATTERN="pyproject.toml|setup.py|setup.cfg"
            ;;
        "Node.js")
            CONFIG_PATTERN="package.json"
            ;;
        ".NET")
            CONFIG_PATTERN="\.csproj|\.sln"
            ;;
        "Go")
            CONFIG_PATTERN="go.mod|main.go"
            ;;
        "Java")
            CONFIG_PATTERN="pom.xml|build.gradle"
            ;;
        "Rust")
            CONFIG_PATTERN="Cargo.toml"
            ;;
    esac

    if echo "${SECTION_CONTENT}" | grep -qiE "${CONFIG_PATTERN}"; then
        echo "    [x] Entry point source documented"
        ((LANG_CHECKS++))
    else
        echo "    [ ] Entry point source documented"
    fi

    # Check 5: Remediation guidance (at least language mentioned in context of failure/error)
    if echo "${SECTION_CONTENT}" | grep -iE "(remediation|failure|error|fix).*${LANG}|${LANG}.*(remediation|failure|error|fix)" | grep -qi .; then
        echo "    [x] Remediation guidance documented"
        ((LANG_CHECKS++))
    else
        echo "    [ ] Remediation guidance documented"
    fi

    # Determine pass/fail for this language
    if [[ ${LANG_CHECKS} -ge 4 ]]; then
        echo "  PASS: ${LANG} (${LANG_CHECKS}/${LANG_REQUIRED} elements)"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: ${LANG} (${LANG_CHECKS}/${LANG_REQUIRED} elements - need at least 4)"
        ((TESTS_FAILED++))
    fi
    echo ""
done

# Additional test: Language matrix/table exists for comparison
echo "Test: Language comparison table/matrix exists"
if echo "${SECTION_CONTENT}" | grep -qE "\|.*\|.*\|" | head -1; then
    # Check if table has multiple language entries
    TABLE_ROWS=$(echo "${SECTION_CONTENT}" | grep -E "\|.*\|.*\|" | wc -l)
    if [[ ${TABLE_ROWS} -ge 7 ]]; then
        echo "  PASS: Language comparison table found (${TABLE_ROWS} rows)"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: Table found but insufficient rows (${TABLE_ROWS}, expected >=7 for header + 6 languages)"
        ((TESTS_FAILED++))
    fi
else
    echo "  FAIL: No language comparison table found"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "================================================================"
echo "  SUMMARY: ${AC_NUM}"
echo "================================================================"
echo "  Languages with complete docs: ${TESTS_PASSED}/6"
echo "  Languages missing docs: ${TESTS_FAILED}"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
if [[ ${TESTS_FAILED} -eq 0 ]]; then
    echo "RESULT: PASSED (all 6 languages documented)"
    exit 0
else
    echo "RESULT: FAILED (${TESTS_FAILED} languages missing comprehensive documentation)"
    exit 1
fi
