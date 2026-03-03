# STORY-180 Test Suite

**Story:** Pass Context File Summaries to Subagents
**Status:** TDD Red Phase (tests written, implementation pending)

## Test Coverage

| AC | Description | Tests | Status |
|----|-------------|-------|--------|
| AC-1 | Context Summary Format Defined | 6 | FAILING |
| AC-2 | Anti-Pattern Scanner Accepts Summary | 6 | FAILING |
| AC-3 | Subagent Documentation Updated | 6 | FAILING |
| AC-4 | QA Skill Passes Summaries | 8 | FAILING |
| AC-5 | Token Reduction Measurable | 8 | FAILING |
| **Total** | | **34** | **TDD Red** |

## Running Tests

### Run All Tests
```bash
bash tests/STORY-180/run-all-tests.sh
```

### Run Individual AC Tests
```bash
# AC-1: Context Summary Format
bash tests/STORY-180/test-ac1-context-summary-format.sh

# AC-2: Anti-Pattern Scanner Accepts Summary
bash tests/STORY-180/test-ac2-anti-pattern-scanner-accepts-summary.sh

# AC-3: Subagent Documentation Updated
bash tests/STORY-180/test-ac3-subagent-documentation-updated.sh

# AC-4: QA Skill Passes Summaries
bash tests/STORY-180/test-ac4-qa-skill-passes-summaries.sh

# AC-5: Token Reduction Measurable
bash tests/STORY-180/test-ac5-token-reduction-measurable.sh
```

## Files Under Test

### Primary Target Files
- `.claude/agents/anti-pattern-scanner.md` - Subagent specification
- `.claude/skills/devforgeai-qa/references/parallel-validation.md` - QA parallel validation

### Expected Changes for Green Phase

**AC-1: Context Summary Format Defined**
- Add `## Context Summary Format` section to anti-pattern-scanner.md
- Include template: `**Context Summary (do not re-read files):**`
- Document summary line format for each context file

**AC-2: Anti-Pattern Scanner Accepts Summary**
- Add `context_summary` field to Input Contract
- Document workflow accepting Context Summary in prompt
- Add conditional for pre-provided summaries in Phase 1

**AC-3: Subagent Documentation Updated**
- Add `IF context_files_in_prompt: Use provided summaries` conditional
- Update Guardrail #2 with summary exception
- Document explicit no-reload behavior

**AC-4: QA Skill Passes Summaries**
- Add Context Summary section to parallel-validation.md
- Update Task invocations to include context_summary
- Add summary generation step before Task calls

**AC-5: Token Reduction Measurable**
- Add Token Efficiency section
- Document summary size vs full context size
- Reference token savings in parallel-validation.md

## Test Framework

Tests use Bash shell scripts with:
- `grep` for content verification
- Pattern matching for structural validation
- Exit code 1 on any failure (TDD Red expected)
- Color-coded output for readability

## Token Efficiency Target

Story requires **-3K tokens per subagent call** through:
- Context summaries instead of full context file reading
- Summary format: 3-5 lines per context file
- Full context files: ~3-4K tokens
- Summary format: ~200-300 tokens
