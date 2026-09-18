# Contract Schema Reference

**Purpose:** Document the YAML contract file schema consumed by the
`validate-subagent-contract` CLI (`devforgeai-validate validate-subagent-contract`).

**Source:** `src/claude/scripts/devforgeai_cli/validators/subagent_contract.py`

---

## Contract Name Resolution (Three-Step Fallback)

The `contract_name` field in the JSON output is resolved in this order:

1. `contract.get('skill')` — preferred; the `skill:` key in the YAML contract
2. `contract.get('contract')` — alternative; the `contract:` key
3. `Path(contract_file).stem` — filesystem stem (last-resort fallback)

**Example:** A contract at `.claude/contracts/requirements-analyst-contract.yaml`
with no `skill:` or `contract:` key will be identified as `requirements-analyst-contract`
in the JSON output.

**Reference:** `src/claude/scripts/devforgeai_cli/validators/subagent_contract.py`
line 281 (three-step fallback order). See REC-STORY-646-L-004.

---

## Schema: YAML Contract File

```yaml
# Required fields
skill: "requirements-analyst"          # OR contract: "requirements-analyst"
subagent: "story-requirements-analyst"
contract_version: "1.0"

# Optional: constraints
constraints:
  no_file_creation:
    enabled: true

# Optional: prohibited patterns in NFR section
validation:
  check_no_file_paths:
    prohibited_patterns:
      - "Write\("
      - "Edit\("
  check_sections_present:
    required_sections:
      - "Acceptance Criteria"
      - "Technical Specification"
  check_ac_format:
    enabled: true
  check_nfr_measurability:
    enabled: true
    prohibited_terms:
      - "fast"
      - "efficient"
  check_size_limit:
    max_chars: 50000
```

---

## Security: Contract-Supplied Regex Patterns

**⚠️ ReDoS Warning:** Contract YAML files under `.claude/contracts/` MUST be
trusted author-controlled content. Regex patterns supplied via
`validation.check_no_file_paths.prohibited_patterns` and
`validation.check_nfr_measurability.prohibited_terms` are compiled as-is by
`re.search()`. Authors are responsible for avoiding catastrophic backtracking.

The `re.error` branch in the validator catches regex **syntax** errors and
continues silently. It does NOT protect against backtracking **timeouts**.

**Future hardening** (FRAMEWORK-REDOS-HARDENING, out of scope for STORY-646):
adopt the `regex` package which supports `timeout=N` and replace `re.search`
sites throughout the validators.

See: REC-STORY-646-L-005, `src/claude/scripts/devforgeai_cli/validators/subagent_contract.py`
lines 68-80.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Validation passed — no violations |
| `1` | Validation failed — at least one CRITICAL/HIGH/MEDIUM violation |
| `2` | IO/environment error — file not found, invalid YAML, path traversal |
| `127` | Shell-level — CLI not installed (used in phase-file fallback branches) |

---

## JSON Output Schema

```json
{
  "contract": "requirements-analyst",
  "subagent": "story-requirements-analyst",
  "contract_version": "1.0",
  "output_size": 12480,
  "violation_count": 2,
  "violations": [
    {
      "type": "MISSING_SECTION",
      "section": "## Technical Specification",
      "severity": "HIGH",
      "message": "Required section not found in output"
    }
  ],
  "valid": false
}
```
