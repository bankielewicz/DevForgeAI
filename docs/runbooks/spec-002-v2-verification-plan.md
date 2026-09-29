# SPEC-002 v2: verification plan

Approved by Bryan with SPEC-002 v2 on 2026-09-29.

**Scope.** SPEC-002 v2 changes shared rules (D-03 to D-09) and moves provider identity into §5's adaptations
table. After approval, both prd skills change against the same contract, and so do both architecture skills,
because the policy validation script and schema copies are shared (D-09). Each provider is evaluated
independently, with the existing thresholds (≥ 0.8 per case over 3 runs, against the no-plugin baseline;
three binary runs need 3/3) and every manual obligation. Nothing here has run yet.

## 1. What each provider changes

| | Claude (`src/claude/DevForgeAI/`) | Codex (`src/codex/devforgeai/`) |
|---|---|---|
| prd skill | SKL-002 v1 → v2: SKILL.md steps 4 (D-06), 6 (D-07, line 313's "every requirement cites a promoted idea"), 7 and the interview (D-05), 8 (D-08), 9 (D-03, D-04); `references/output-rules.md`, `interview.md`, `brn-mapping.md`; the template's author comment (D-07); provenance implements SPEC-002 v2 | The same shared rules in its prd skill; keep its identity adaptation (D-01, D-02) as §5 describes; provenance implements SPEC-002 v2 |
| Policy validation (D-09) | New `scripts/validate_policy.py` and `references/schemas/{policy,common}.schema.json` (unchanged copies) in **prd and architecture**, byte-identical; `references/policy.md` R1 calls the script | The same files in its prd and architecture skills, byte-identical to the Claude copies where the host allows |
| Architecture skill | SKL-003 v2 → v3: the shared policy files only | Its architecture skill: the shared policy files only |
| Specs relinked (mechanical) | SPEC-003 and SPEC-004 link SPEC-002 v1 → v2 (their consumed §5 contract is unchanged) | — |

## 2. Structural checks (both providers)

- SPEC-002 v2 against `spec.schema.json` (PASS on 2026-09-29: 61 items, every BEH, ERR and QR covered by a VER).
- Each skill's frontmatter and provenance; `metadata.devforgeai-version` equals `provenance.yaml`'s version.
- Byte-identity: `policy.md`, `defaults.md`, `validate_policy.py` and the schema copies, across prd and
  architecture in each provider, and the schema copies against `src/schemas/`.
- **`validate_policy.py` unit tests, with independent negative fixtures:**
  - a malformed date (`2026-13-45`);
  - `authors` as a string;
  - a link record with no `relation`;
  - a wrongly typed value (`interview.max_calls: "eight"`);
  - SV-01 to SV-06;
  - a valid policy that passes;
  - behaviour when `jsonschema` is missing: a distinct exit that the skill turns into ERR-08.

## 3. Automated evaluation matrix (per provider, run independently)

| Group | Cases | Note |
|---|---|---|
| Unchanged cases | VER-01 to VER-06, VER-08, VER-13 to VER-22 (17) | Rerun on the v2 skill; the original grader definitions stay |
| Changed obligation | VER-09 (provenance, D-08 and identity), VER-10 (no BRN link on constraint NFRs, D-07) | Grader additions only; the old graders stay unless a defect is shown with controls |
| Changed since the last run | VER-07 (`hands-off-to-architecture`, changed in `acce5a2`) | First run of the current case |
| New cases | VER-24 to VER-32 (9) | D-05 ×2, D-06, D-03 and D-04, D-09 ×4, D-08 |
| **Total** | **29 cases × 3 runs × 2 arms = 174 trials per provider** | |

- **Claude cost estimate:** the last 20-case prd run cost $41.51 on Claude Code 2.1.283, so about $60 for
  29 cases. The architecture tag run (the shared policy files) is about $35, going by the last 14-case
  architecture suite. **Total: about $95, before any rerun.** Codex runs on its own harness and budget.
- **Claude command** (plain terminal, repository root):

  ```
  claude plugin eval src/claude/DevForgeAI --tag prd --allow-tools Write Edit Bash --scaffold --threshold 0.8
  ```

- **Revision binding (fixes the gap in v1's record):** run from a committed, clean tree. For each run,
  record `git rev-parse HEAD` and the plugin tree's digest in the results folder, and keep the grader
  files, so every result names the source and graders it tested.
- **Record every run separately.** A rerun with changed graders is a new run; it never replaces an earlier
  result.

## 4. Manual obligations (per provider)

- **VER-11 (interactive interview):** as before, plus a partial answer to one category (D-05).
- **VER-12 (extension, approved PRD, shared constraint, unknown or malformed BRN):** as before.
- **VER-23 (local preferences and SV rules):** as before, with each provider's local preference path (§5).
- **Codex only:**
  - the question-tool and plain-text branches;
  - the `unavailable` identity disclosure (BEH-10). A disclosed gap keeps BEH-10 open in Codex's
    qualification.
- **Claude only:** the session ID comes from `${CLAUDE_SESSION_ID}`, checked against the transcript.

## 5. Order after approval

1. Record approval: SPEC-002 v2 `approved`, and SPEC-003 and SPEC-004 relinked (done by the SPEC-002 v2 PR).
2. Claude: SKL-002 v2 and the shared policy files in SKL-003 v3, on a branch, with the structural checks.
3. Codex: the same contract, through a Plugin Creator prompt modelled on the architecture-kinds one.
4. Evaluate each provider independently (sections 3 and 4), with revision binding.
5. Record the results in SPEC-002 §9 and each provider's report, then ask for skill approval.

## 6. SPEC-003 v3 (approved by Bryan on 2026-09-29, installed with SPEC-002 v2)

SPEC-003 v3 brings Architecture Definition in line with SPEC-002 v2 (SHA-256
`8a3f93d127fca7358250dfb6770da5c9f1408b95c866ea4eb76ac9a05a8ce681`).
- **ERR-05:** content that failed validation is never left approved or accepted. An approved ARCH whose
  amendment or review record fails stays in-review with its approval cleared, and an ADR accepted in that
  run becomes proposed. This is D-03's rule.
- **BEH-14 and ERR-05:** one initial check plus at most three repair cycles (D-04).
- **BEH-03, ERR-02, §3 and §5:** policy is validated through the shared script (D-09), and VER-12 (f)
  checks its byte-identity.
- **New cases:** VER-17 `policy-bad-date` and VER-18 `failed-amendment-stays-in-review`.

**Per provider:**
- The architecture skill implements v3, as SKL-003 v3 in Claude. It ships the shared policy files, and the
  ERR-05 and BEH-14 changes.
- The architecture eval runs 16 cases × 3 runs × 2 arms: the 14 existing plus VER-17 and VER-18. The Claude
  estimate is about $40, replacing section 3's $35. VER-12 (f) and (i) are manual.
- The `failed-amendment-stays-in-review` fixture has an existing component with a value the self-check
  rejects, which the amendment must leave unchanged.
