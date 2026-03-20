# Result Formatting Guide

**Purpose:** Define the display template for conversion results shown to the user at the end of Phase 07.

---

## Result Display Template

```
═══════════════════════════════════════
     MCP Conversion Complete
═══════════════════════════════════════

ID:          ${CONVERT_ID}
Source:      ${MCP_SOURCE} (${SOURCE_TYPE})
Pattern:     ${detected_pattern} (confidence: ${confidence})

─── Generated Files ───
CLI:         ${OUTPUT_DIR}/cli.py
Adapter:     ${OUTPUT_DIR}/adapters/${pattern}_adapter.py
Skill:       ${OUTPUT_DIR}/skill/SKILL.md
Tests:       ${OUTPUT_DIR}/tests/test_cli.py
Total:       ${file_count} files

─── Validation ───
CLI Help:    ✓ / ✗
Smoke Test:  ✓ / ✗ / Skipped
Alignment:   ${alignment_score}%
Tests:       ${passed}/${total} passed

─── Registration ───
Registered:  Yes → .claude/skills/${cli_name}/ | No
Dependencies: Installed / Pending

─── Next Steps ───
1. Run:    python ${OUTPUT_DIR}/cli.py --help
2. Review: ${OUTPUT_DIR}/skill/SKILL.md
3. Test:   pytest ${OUTPUT_DIR}/tests/

Report: devforgeai/workflows/${CONVERT_ID}-conversion-report.md
═══════════════════════════════════════
```

---

## Conversion Report Template (Markdown)

Written to `devforgeai/workflows/${CONVERT_ID}-conversion-report.md`:

```markdown
# MCP Conversion Report

**ID:** ${CONVERT_ID}
**Date:** ${completed_at}
**Duration:** ${duration}

## Source

- **MCP:** ${MCP_SOURCE}
- **Source Type:** ${SOURCE_TYPE}
- **Tools Extracted:** ${tool_count}

## Pattern Detection

- **Pattern:** ${detected_pattern}
- **Confidence:** ${confidence}
- **Override:** ${pattern_override || "None (auto-detected)"}

## Generated Files

| File | Path | Description |
|------|------|-------------|
| CLI Entry Point | ${OUTPUT_DIR}/cli.py | Main CLI with argparse |
| Adapter | ${OUTPUT_DIR}/adapters/${pattern}_adapter.py | Pattern-specific logic |
| Error Handler | ${OUTPUT_DIR}/utils/error_handler.py | Exit code mapping |
| Output Formatter | ${OUTPUT_DIR}/utils/output_formatter.py | JSON/text/base64 |
| SKILL.md | ${OUTPUT_DIR}/skill/SKILL.md | Claude skill documentation |
| CLI Reference | ${OUTPUT_DIR}/skill/references/cli_reference.md | Detailed commands |
| Examples | ${OUTPUT_DIR}/skill/references/usage_examples.md | Usage patterns |
| Tests | ${OUTPUT_DIR}/tests/test_cli.py | Test stubs |

## Validation Results

| Check | Result |
|-------|--------|
| CLI Help | ${cli_help_ok} |
| Smoke Test | ${smoke_test_passed} |
| Interface Alignment | ${alignment_score}% |
| Test Suite | ${test_results} |
| **Overall** | **${overall_status}** |

## Registration

- **Registered:** ${registered}
- **Skill Path:** ${skill_path}
- **Dependencies:** ${dependencies_installed}

## Recommendations

${conversion_recommendations}
```

---

## Status Indicators

| Status | Display |
|--------|---------|
| Success | ✓ |
| Failure | ✗ |
| Skipped | — |
| Pending | ○ |

---

## Error Display

If any phase failed, include error context:

```
⚠ Phase ${N} encountered issues:
  ${error_message}
  Resolution: ${suggested_fix}
```
