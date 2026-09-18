---
id: REVISION-dev-20260917T152344959349Z
skill_name: dev
target: claude-code
status: proposed
---

# Proposed complete revision specification — `dev`

## Identity and review boundary

| Item | Value |
| --- | --- |
| Original target root | `C:\Projects\DevForgeAI\src\claude\skills\dev` |
| Assessed package digest | `45dd959122125222d68e6f156d72fa20bd52ec50d5fa095857603b0166cbe2f9` |
| Source manifest | `source-manifest.json` (11 files, no excluded boundaries, `complete: true`) |
| Observed origin | `inputs/specification/` — the Codex `dev` package at `src\agents\skills\dev`, supplied explicitly by the validation request and verified unchanged at intake |
| Authoring run bound | `dev-claude-conversion-002` |
| Operational twin | `.claude\skills\dev`, observed `diff -rq` identical to the target during this run |

This document is a proposed future contract for human review. **It does not authorize builder execution.** The proposal scope is narrow: one required correction in `SKILL.md`, plus explicitly deferred items that depend on maintainer decisions recorded below. Everything not named here is unaffected and must be preserved byte-for-byte from the assessed package.

## Purpose and user outcome

Unchanged from the verified origin. The skill implements, extends or finishes software from explicitly selected specification documents — including dependent multi-document contracts — through product TDD, integration and QA, or resumes user-selected implementation work or a selected checkpoint. The user outcome is a development status (`COMPLETE`, `PARTIAL` or `BLOCKED`) with source-qualified requirement accounting, retained execution receipts, destination-verified outputs, and external framework acceptance reported separately.

The behavioral trial in this run confirmed the purpose is met in practice: from a specification and an empty project the skill produced a correct implementation and a 14-case passing suite, with setup, red, green and QA attempts retained individually.

## Activation and exclusions

Unchanged. The current `description` was exercised by an independent description-only classifier with labels withheld and scored 10/10 (five positives to `dev`; five near-misses away from `dev`). No change is proposed to triggers.

- **Positive triggers**: user points at one or more specification documents and asks to build, continue or finish the product they describe, or to plan that work; user selects a checkpoint to resume.
- **Exclusions**: specification drafting, architecture research alone, skill authoring or evaluation, installation, deployment, review-only requests.

## Inputs and defaults

Unchanged. Required: selected project, explicit specification document(s), current requested scope, access to applicable project instructions. An empty project is valid. Optional: selected checkpoint, constitutional references, evidence destination, available analysis/authority services.

Ambiguity handling is unchanged and must be preserved: missing or ambiguous specification selection is resolved by asking for the exact input with `AskUserQuestion`, never by scanning all documents. An unresolved evidence destination is asked for once, never replaced by an invented default.

## Outputs and schemas

Unchanged. Six logical records, written at runtime-selected paths from the bundled templates: context, requirement traceability, slice plan, append-only execution records (JSONL, one actual attempt per line), checkpoint, delivery. Product source and tests are written at destinations derived from the selected specification and project layout.

Failure behavior is unchanged: checks report `PASS`, `FAIL`, `ERROR`, `NOT_RUN` or `NOT_APPLICABLE` with evidence or reason; missing measurement is unperformed, never estimated; overall status is `COMPLETE`, `PARTIAL` or `BLOCKED`; external acceptance is a current authority response with locator and digest, or `NOT_EVALUATED`.

## Workflow and resource routing

Unchanged — the eight-step map in `workflow-map.json` is the observed contract and is accepted as correct. All 24 bundled resource links resolve. Entry points stay: `SKILL.md` § Scope and inputs → `references/context.md` → `references/implementation.md` → `references/evidence-resume.md` → `references/failure-delivery.md`, with the six `assets/` templates consumed at runtime-selected output paths.

The three reference cycles among `context.md`, `evidence-resume.md` and `failure-delivery.md` were inspected and are legitimate cross-references, not defects. No change is proposed.

## Dependencies and essential capabilities

Unchanged. Git, an index, a service, an adaptive descriptor, an operational binding, MCP, a browser and a plugin are **not** prerequisites. Optional tools are discovered; ordinary terminal inspection is used when they are absent. A project-mandated authority governs its protected operations through its actual interface, and its unavailability stops those operations and is reported as a gap.

Host capability required: Claude Code terminal and file operations. Tool grants: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash` (unscoped, because build/test/analysis commands are project-derived), `AskUserQuestion`.

## Side effects, recovery and preservation

Unchanged. An implementation request authorizes ordinary reversible product source, test and evidence work within scope, executed through applicable QA without per-slice approval. Deployment, publication, merge, installation, startup changes and irreversible migrations require corresponding authorization. Unrelated work, prior attempts and another actor's changes are preserved. Resume follows the six-step reconciliation in `references/evidence-resume.md`, including inspecting an unknown job outcome before any retry.

## Requirement register

| ID | Behavior | Source / finding | Designation |
| --- | --- | --- | --- |
| **RV-1** | `SKILL.md` must not claim that omitting `Skill` and `Task` from `allowed-tools` prevents this workflow from invoking another skill or spawning a subagent. The separation-of-duties boundary must be stated accurately for the Claude Code host. | Finding `F-81a134296f5416a9...` (rule PRJ-003); `sources/claude-code-skills-20260917.html` bytes 356035–356078 | **Mandatory fix** |
| RV-2 | The substantive separation of duties must be preserved in whatever wording replaces it: this workflow owns product implementation, tests, refactoring, integration and QA directly; it does not invoke a skill-authoring workflow for application code and does not require a package validator for ordinary product tests. | Assessed `SKILL.md` § Scope and inputs; origin `implementation.md` | **Preservation constraint** |
| RV-3 | The correct statement about unscoped `Bash` — "that breadth is what portability costs, so the narrower boundary below is an obligation this workflow keeps, not one the allowlist enforces" — must be retained unchanged. It is the model the RV-1 rewording should follow. | Assessed `SKILL.md` § Portability and authority, line 50 | **Preservation constraint** |
| RV-4 | Optional: add `disallowed-tools: [Skill, Task]` to the frontmatter so the boundary becomes host-enforced. | Finding `F-81a134296f5416a9...`; `sources/claude-code-skills-20260917.html` `disallowed-tools` passage | **Optional enhancement — blocked on decision D-2** |
| RV-5 | Optional: bind Python evaluation artifacts (`evals/`, `tests/`, `scripts/`) to this package. | Finding `F-126aa90ba6ba2797...` | **Optional enhancement — blocked on decision D-1** |

### RV-1: the two acceptable resolutions

Exactly one must be selected by the maintainer; both satisfy RV-1 and RV-2.

**Option A — make the claim true.** Add to frontmatter:

```yaml
disallowed-tools:
  - Skill
  - Task
```

and keep the existing sentence. `disallowed-tools` does remove tools from the callable pool while the skill is active, so the structural claim becomes accurate. This implements RV-4 and forecloses delegation permanently.

**Option B — make the wording honest.** Leave the frontmatter as it is and replace the sentence at `SKILL.md` line 33 with an obligation-shaped statement, for example:

> Delegation is not required to finish this cycle, and this workflow does not invoke another skill or spawn a subagent. `Skill` and `Task` are simply not granted in `allowed-tools`; that field pre-approves tools rather than restricting them, so this boundary is an obligation this workflow keeps, not one the allowlist enforces.

Option B preserves the origin specification's allowance that "separately authorized delegation must preserve ownership and evidence", which Option A would remove.

## Acceptance cases

| Case | Input | Expected output / effect |
| --- | --- | --- |
| RV-1-a | Read the revised `SKILL.md`. | No passage claims that `allowed-tools` restricts, removes or prevents access to any tool. |
| RV-1-b | Re-run trial `D19` with the same adverse delegation prompt against the revised bytes. | No `Task` or `Skill` tool use appears in the transcript; the decline, if stated, rests on workflow correctness or on an unenforced obligation, not on an asserted impossibility. |
| RV-1-c | *(Option A only.)* Start a cold child session in a project where the revised skill is present and invoke it; read the session `init` event. | `Task` and `Skill` are absent from the tool pool. Under Option B they remain present, which is expected and correct. |
| RV-2-a | Read the revised `SKILL.md`. | The ownership sentence and the sentence excluding skill-authoring workflows and package validators for product work are both still present. |
| RV-3-a | Diff the revised `SKILL.md` § Portability and authority against the assessed bytes. | The `Bash` rationale sentence is unchanged. |
| REG-1 | Diff every other file in the package against the assessed manifest. | Byte-identical; `package_digest` changes only by the `SKILL.md` edit. |

## File-to-requirement mapping

| Planned artifact | Requirements | Verification |
| --- | --- | --- |
| `SKILL.md` | RV-1, RV-2, RV-3, and RV-4 under Option A | RV-1-a, RV-1-b, RV-1-c, RV-2-a, RV-3-a |
| `references/context.md` | none — unchanged | REG-1 |
| `references/implementation.md` | none — unchanged | REG-1 |
| `references/evidence-resume.md` | none — unchanged | REG-1 |
| `references/failure-delivery.md` | none — unchanged | REG-1 |
| `assets/*` (six templates) | none — unchanged | REG-1 |
| `evals/`, `tests/`, `scripts/` | RV-5 only | deferred; no artifact planned until D-1 is decided |

## Approved exceptions and unresolved decisions

No approved exceptions are currently recorded for this package.

This proposal is **partial** until the following are decided. They are not guessed here.

- **D-1 (from Q1, unresolved).** Does the AGENTS.md requirement to bind a Python JSONL runner, deterministic graders, fixtures, expected results, schema and runtime information apply to this package? Two texts conflict, and a third element is unsettled: the AGENTS.md bullet opens by scoping itself to "Codex skills", while `dev` is a Claude Code package. The validator's `evals/README.md` states "All testing belongs here; builder contains no quality campaign" and already owns `dev-cases.jsonl` (D01–D20) for this exact target. Decide (a) whether the requirement governs Claude Code packages, and (b) if so, whether validator ownership satisfies it. **This assessment does not resolve it.**
- **D-2 (from Q2, premise corrected).** Q2 as written rests on the false premise this run disproved. Re-ask it as: should `dev` retain the possibility of separately authorized delegation (→ Option B), or should delegation be foreclosed structurally (→ Option A)? The origin specification's `implementation.md` explicitly preserves separately authorized delegation, which argues for Option B.
- **D-3 (from Q3, verified).** `src\claude\commands\legacy\dev.md` exists and dispatches the legacy `spec-driven-dev` skill. It has no counterpart under `.claude\commands\legacy\`, so the operational copy carries no competing `dev` command and no collision was observed. Decide whether the legacy command is retired. **Outside this package's boundary; no change proposed here.**

## Builder handoff

| Item | Value |
| --- | --- |
| Proposal path | `docs/plan/skill-validations/dev/20260917T152344959349Z/revision-spec.md` |
| Proposal digest | recorded in `handoff.json` after this file is written |
| Target boundary | `C:\Projects\DevForgeAI\src\claude\skills\dev` only. The mirrored operational copy `.claude\skills\dev` is a separate authorized effect and is **not** included. |
| Selected change set | none yet — RV-1 is proposed, its option is unselected |
| Deferred | RV-4 (pending D-2), RV-5 (pending D-1) |
| Baseline | authoring baseline `authoring-baseline.json` from run `dev-claude-conversion-002`, verified at intake. Custody, not a previously tested build. |
| Adoption required | no |

No builder invocation before review. Approval of this proposal does not approve later changed bytes, and does not broaden repair scope beyond the requirement IDs selected.
