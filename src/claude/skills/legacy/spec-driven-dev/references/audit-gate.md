# Audit Gate Behavior Reference

**Used by:** `spec-driven-dev` SKILL.md EXIT GATE step (5.a)
**Source of truth:** `audit-policy.yaml` (in this skill directory)
**ADR:** `devforgeai/specs/adrs/ADR-058-spec-driven-dev-audit-integration.md`
**Module README:** `src/claude/scripts/devforgeai_cli/audit/README.md`

---

## Section 1 — Behavior Matrix

The orchestration loop's EXIT GATE step calls:

```
devforgeai-validate audit-gate ${STORY_ID} --phase={phase_id}
```

The CLI's behavior is determined by 4 inputs in priority order:

| Input | Source | Effect |
|---|---|---|
| 1. Phase policy `audit:` | `audit-policy.yaml` | If `false` → exit 0, no audit fixture generated |
| 2. `REMEDIATION_MODE` env var | Set by skill when `/dev STORY-X --fix` | If `"true"` AND policy `respect_remediation_mode: true` → exit 0, audit skipped |
| 3. `DEVFORGEAI_AUDIT_BYPASS` env var | Operator-set escape valve | If `"1"` → exit 0, BYPASS logged to `bypasses.jsonl` |
| 4. Otherwise | — | Generate fixture, set `DEVFORGEAI_AUDIT_FAIL_MODE` env var, exit 0 (success) or 1 (fixture-gen failure) |

When the audit-gate exits 0 with a generated fixture, the next `phase-complete` Bash invocation triggers the audit hook (registered in `.claude/settings.json` PostToolUse). The hook:

* Reads the just-generated fixture from `devforgeai/audit/phases/<STORY_ID>-phase<NN>/`
* Reads `DEVFORGEAI_AUDIT_FAIL_MODE` (set by audit-gate). `"open"` → warn-only; anything else → fail-closed
* Calls the judge model (Anthropic Haiku by default; consensus mode if `consensus.yaml` present in fixture dir)
* Verifies citations against the actual filesystem (Layer 9 backstop)
* Returns 0 (approve) or 2 (reject) — `phase-complete` propagates this to the skill orchestration

---

## Section 2 — Per-Phase Decision Flow

```
ENTRY: phase {phase_id} reached step 5 (EXIT GATE)
       │
       ▼
   audit-gate ${STORY_ID} --phase={phase_id}
       │
       ├─ policy.audit == false?
       │      └─ YES → exit 0 ("not audited per policy")
       │
       ├─ REMEDIATION_MODE == "true"?
       │      └─ YES → exit 0 ("skipped — remediation mode")
       │
       ├─ DEVFORGEAI_AUDIT_BYPASS == "1"?
       │      └─ YES → log bypass; exit 0 ("BYPASSED")
       │
       └─ NO short-circuits fired:
              ├─ generate-audit-fixture STORY-NNN --phase=NN --force
              │      ├─ rc != 0 → exit 1 (HALT — fixture failed)
              │      └─ rc == 0 → set DEVFORGEAI_AUDIT_FAIL_MODE; exit 0
              │
              └─ phase-complete fires → audit hook runs against the fresh fixture
                                       → returns 0 (approve) or 2 (reject)
```

The audit hook itself (Plan D D4) further differentiates fixture states:

* No fixture directory → silent return 0 (legacy un-audited phase)
* Fixture dir exists but `requirements.json` missing → HALT exit 2 ("incomplete fixture")
* `requirements.json` empty `[]` or malformed → HALT exit 2 ("no-op fixture")
* `artifacts/` empty → HALT exit 2 ("nothing to verify")
* Otherwise → invoke judge

This eliminates the "audit theatre" failure mode where an empty fixture was indistinguishable from a successful audit.

---

## Section 3 — Failure Recovery

### Audit verdict = REJECT (judge found unsatisfied requirements)

`phase-complete` exit code 2. Skill HALTs. Recovery:

1. Read the audit log: `devforgeai/audit/log/<STORY_ID>-phase<NN>_*.json` (most recent timestamp).
2. Identify which `verdicts[]` entries have `status: "missing_evidence"` or `"fabricated"`.
3. Address the gap in the implementation (NOT by editing the fixture — that's the bias the audit catches).
4. Re-run the phase: the orchestration loop re-fires audit-gate → fresh fixture → fresh audit.

### Fixture generation failed (`audit-gate` exit 1)

Causes:
* Story file missing `## Acceptance Criteria` section
* Git base ref unresolvable (`git merge-base HEAD main` failed — likely on a fresh branch)
* Story-declared paths reference non-existent files

Recovery:

1. Check stderr for the specific error.
2. Fix the story file or pass an explicit `--base=<ref>` to fixture-gen if it's a git issue.
3. Re-run the phase.

### Audit infrastructure error (judge API timeout, malformed response)

`phase-complete` returns exit 2 with stderr indicating infrastructure failure. Two recovery paths:

* **Wait and retry** — transient API issues usually clear within 60s.
* **Bypass with audit trail** — `export DEVFORGEAI_AUDIT_BYPASS=1`, re-run phase, then `unset DEVFORGEAI_AUDIT_BYPASS`. The bypass is logged to `devforgeai/audit/log/bypasses.jsonl` for compliance review.

NEVER use `--no-verify`-style bypasses that don't leave an audit trail.

---

## Section 4 — Bypass Procedure (Detailed)

The `DEVFORGEAI_AUDIT_BYPASS` escape valve exists for one purpose: continuing development when the judge API is unreachable but you have high confidence in the code. Every bypass is logged with timestamp, story_id, phase, and invoking command in `devforgeai/audit/log/bypasses.jsonl`.

### When to use

* Anthropic API is returning 5xx for >5 minutes
* You're on a flight / no internet / CI environment without API key
* You're exercising the dev workflow against a story you're confident about (e.g., trivial follow-up to a fully-audited story)

### When NOT to use

* You hit a real audit failure and want to ignore it (this is the bias the audit catches)
* You want to skip audits for cost reasons (use `audit: false` in policy YAML instead, code-reviewed)
* You want to disable Layer 9 framework-wide (talk to the project owner; this requires a new ADR)

### Procedure

```bash
export DEVFORGEAI_AUDIT_BYPASS=1
# Run the dev workflow as normal:
/dev STORY-XXX
# When done, unset:
unset DEVFORGEAI_AUDIT_BYPASS
```

The bypass log entries look like:

```json
{"timestamp":"2026-05-01T14:23:00Z","story_id":"STORY-672","phase":"03","reason":"DEVFORGEAI_AUDIT_BYPASS=1","command":"audit-gate STORY-672 --phase=03"}
```

Review with `tail devforgeai/audit/log/bypasses.jsonl` periodically.

---

## Section 5 — Cross-References

| Topic | Path |
|---|---|
| Per-phase policy | `src/claude/skills/spec-driven-dev/audit-policy.yaml` |
| ADR for this integration | `devforgeai/specs/adrs/ADR-058-spec-driven-dev-audit-integration.md` |
| Audit module README | `src/claude/scripts/devforgeai_cli/audit/README.md` |
| Audit hook source | `src/claude/scripts/devforgeai_cli/audit/hook.py` |
| Audit-gate CLI source | `src/claude/scripts/devforgeai_cli/commands/audit_gate.py` |
| Policy loader | `src/claude/scripts/devforgeai_cli/audit/_phase_policy.py` |
| Plan B execution report (Layer 9 module integration) | `devforgeai/audit/results/REPORT-STORY-658-audit-test.md` |
| Plan C3 fixture-generator | `src/claude/scripts/devforgeai_cli/commands/generate_audit_fixture.py` |

### Glossary

| Term | Meaning |
|---|---|
| **Layer 5** | The 5th anti-skip enforcement layer added to `spec-driven-dev` per ADR-058 |
| **Layer 9** | The audit module itself (`devforgeai_cli/audit/`) — broader framework taxonomy from the architectural review session |
| **Audit fixture** | A `devforgeai/audit/phases/<phase_id>/` directory containing `requirements.json` + `sources.json` + `artifacts/` |
| **Audit gate** | The `audit-gate` CLI invocation in SKILL.md EXIT GATE step 5.a |
| **Single mode** | One judge runs (Anthropic Haiku) |
| **Consensus mode** | Multiple judges run in parallel; `rule: all` requires all approve |
| **`consensus_when_available`** | Use consensus if `consensus.yaml` exists in fixture dir; otherwise fall back to single |
| **Fail-closed** | Audit failure blocks phase advancement (`fail_mode: closed`) |
| **Fail-open** | Audit failure produces a warning but doesn't block (`fail_mode: open`) |
