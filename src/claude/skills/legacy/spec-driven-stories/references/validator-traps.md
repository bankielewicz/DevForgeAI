# Validator Traps Reference (Phase 02 + Phase 07 awareness)

**Created:** 2026-04-26 — /create-story remediation Tier 1 File 4
**Purpose:** Document validator behaviors that are technically correct but produce false positives in legitimate use cases. Pre-loaded in Phase 02 (`Reference Loading [MANDATORY]` section) so the orchestrator can pre-emptively avoid the traps BEFORE Phase 07 fires regression-slot-consuming HALTs.

**Origin:** STORY-655 / STORY-656 framework friction observations. STORY-656 successfully avoided these traps by front-loading awareness; this reference encodes that awareness as framework structure.

---

## Trap A: `<quote>` triggers duplicate-user-story detection

**Validator:** `.claude/scripts/devforgeai_cli/validators/user_story.py` lines 47-51 (`USER_STORY_PATTERN` regex), `_scan()` line 55 (no preprocessing).

**Trigger:** Any `As a ... I want ... so that ...` pattern anywhere in the story file is matched, including inside:
- `<quote>...</quote>` XML tags (typical when documenting verbatim stakeholder text)
- `<provenance>...</provenance>` blocks (typical when the provenance block quotes a requirements doc)
- Fenced code blocks ` ``` ... ``` ` containing example user stories
- HTML comments `<!-- ... -->`

The validator counts each match as a separate canonical user story. A story file with one canonical user story PLUS a verbatim-quoted user story inside `<quote>` is flagged with `user_story_count == 2` and HALTs Phase 02 Step 2.3.5 (or Phase 07 self-validation).

**Workaround (use until permanent fix ships):** When quoting a stakeholder's verbatim user-story text from a requirements doc, paraphrase to break the canonical pattern while preserving the source location. Example:

```xml
<!-- AVOID — triggers duplicate detection -->
<quote>As a Framework Maintainer, I want X, so that Y</quote>

<!-- USE — preserves intent without triggering duplicate detection -->
<quote>The Framework Maintainer needs X to achieve Y. Verbatim text preserved at the source location below.</quote>
<source>devforgeai/specs/requirements/foo-requirements.md, FR-NNN user_story (line NNN)</source>
```

**Permanent fix:** Tier 2 File 5 of /create-story remediation (deferred) — add `_strip_quoted_blocks()` preprocessing to `_scan()` mirroring the pattern in `validators/aspirational_language.py:80-114`.

---

## Trap B: DataModel type requires `table` + `fields`

**Validator:** `.claude/scripts/devforgeai_cli/validators/tech_spec/_component_validator.py` lines 27-37 (`COMPONENT_REQUIRED_FIELDS` schema), enforcement at lines 107-112.

**Trigger:** A `components[].type: "DataModel"` entry without both `table_name` and `fields[]` keys produces a CRITICAL validation error.

**The full enum at line 37:**
```python
VALID_COMPONENT_TYPES = ["Service", "Worker", "Configuration", "Logging", "Repository", "API", "DataModel"]
```

There is no `InMemoryDataModel`, `EphemeralDataModel`, or `kind: "in_memory"` discriminator. In-memory dict-literal schemas, in-process configuration objects, and ephemeral data structures cannot use `type: "DataModel"`.

**Workaround (use until permanent fix ships):** Use `type: "Configuration"` for in-memory schemas. Document the choice explicitly in the component description so reviewers understand the semantic intent. Example:

```yaml
- id: "COMP-002"
  type: "Configuration"
  name: "AuditReportSchema"
  file_path: "src/scripts/verify_adr_056.py"
  description: "In-memory JSON schema (Python dict literal) for the audit report. Embedded inline within the verification script — no external schema file references. Treated as a Configuration component (in-process schema definition, not a database entity)."
  required_keys:
    - key: "story_id"
      type: "string"
      ...
```

**Permanent fix:** Deferred (out of scope for current remediation). Requires schema redesign to add `kind: "in_memory" | "persisted"` discriminator to DataModel type, OR introduction of a separate `MemoryDataModel` type. Tracked as known limitation; revisit if multiple stories surface the friction.

---

## Trap C: NFR Auditability not in whitelist (FIXED 2026-04-26)

**Validator:** `.claude/scripts/devforgeai_cli/validators/tech_spec/_nfr_validator.py` lines 20-22 (`VALID_NFR_CATEGORIES`).

**Trigger (was):** `non_functional_requirements[].category: "Auditability"` produced a validator warning. Stories shoehorned audit-trail NFRs into "Security" or "Maintainability" with semantic loss.

**Status:** **FIXED** in /create-story remediation Tier 1 File 3. Both `Auditability` AND `Observability` are now in the whitelist. The full enum is:

```python
VALID_NFR_CATEGORIES = [
    "Performance", "Security", "Scalability", "Reliability",
    "Usability", "Maintainability", "Auditability", "Observability"
]
```

**Action required:** None. Use `category: "Auditability"` for audit-trail / non-repudiation / forensic-capability NFRs. Use `category: "Observability"` for logging / tracing / metrics NFRs.

---

## Issue D: Phase 07 self-validation findings consume regression slots

**Hook:** `.claude/hooks/phase-gate-write.sh` lines 222-230 (Phase 07 src/test write block — correctly enforced; story files are NOT blocked here).

**CLI:** `.claude/scripts/devforgeai_cli/commands/phase_commands.py` lines 1329 (`MAX_REGRESSIONS_PER_STORY = 2`), 1357-1361 (slot-limit enforcement), 1374 (default reason="regression"), 1443-1447 (exit 3 on slot exhaustion).

**The trap:** Phase 07 Step 7.x finds a fixable issue (e.g., a duplicate user-story trigger from Trap A, an NFR vague-term flagged by the whitelist, an `implements` consistency mismatch). The only recovery path documented in the hook error message is `phase-reset --to=02` (or earlier). Phase-reset defaults to `reason="regression"` and consumes one of the 2 regression slots per story. STORY-655 burned both slots before completing.

**Workaround (use unconditionally — documented as standard practice from STORY-656 onward):** Two complementary tactics:

1. **Front-load validator awareness in Phase 02** — make the subagent pre-emptively avoid the traps so Phase 07 has nothing to find. This is the entire purpose of the present reference file.

2. **When phase-reset IS necessary for a Phase 07 self-validation finding (NOT a test-infrastructure failure), pass `--reason=remediation-cycle` explicitly:**

```bash
# WRONG (consumes regression slot)
devforgeai-validate phase-reset $STORY_ID --to=02

# RIGHT (regression slot preserved for genuine test infra failures)
devforgeai-validate phase-reset $STORY_ID --to=02 --reason=remediation-cycle
```

The `remediation-cycle` reason is unrestricted (no slot accounting). It signals that the reset is for self-validation finding remediation, NOT a test-infrastructure regression that the 2-slot budget was designed to bound.

**Permanent fix:** Deferred (out of scope for current remediation). Risk of changing `phase_commands.py` regression-slot semantics affects the broader `/dev` and `/qa` workflows. Track as known limitation; revisit if the workaround proves insufficient.

---

## Cross-Trap Pattern: Pre-emptive Avoidance > Post-hoc Detection

All four issues above (Traps A/B/C + Issue D) share a common pattern: **the validator detects a real issue, but the workflow has no upstream pre-emption**. The framework's response to "validator triggered" is currently `phase-reset` (slot-consuming) rather than "Phase 02 already accounted for this trap."

**The remediation philosophy** (encoded by this reference file's existence): **shift validator awareness left** from Phase 07 to Phase 02. The orchestrator pre-loads this reference, knows the traps, and instructs the subagent (story-requirements-analyst) to produce output that doesn't trigger them. Phase 07 then runs cleanly because the inputs are pre-validated.

When new traps surface in future stories, **add them to this file** rather than expanding Phase 07's recovery surface.

---

## References

- **Origin observations:** STORY-655 framework friction report (3 validator traps + Issue D + epic_format=no-table parser, the latter fixed separately in `story_preflight.py`)
- **Sibling success case:** STORY-656 (front-loaded validator-trap awareness; completed without phase-reset)
- **Methodological guidance:** `.claude/rules/core/epistemic-integrity.md` (provenance classification; trap workarounds are DERIVED workarounds)
- **Operational safety:** `.claude/rules/workflow/operational-safety.md` Rule 3 (sanctioned operational edits when `src/` mirror absent)
- **Permanent-fix tracking:** Plan file `1-plan-mode-steady-sparrow.md` Section 11 (Out of Scope) — Trap B and Issue D listed as deferred follow-ups
