---
id: REVISION-20260918T202845Z
skill_name: dev
target: claude-code
status: proposed
---

# Proposed complete revision specification — `dev` (Claude Code variant)

**This document does not authorize builder execution.** It is a proposal for human review. The validator
neither repaired the target nor invoked `skill-builder`, and cannot do either: `Skill` is absent from this
workflow's own tool grant, which — as this very proposal establishes — is a pre-approval list rather than a
restriction, so the real reason the builder was not invoked is that this workflow did not invoke it.

---

## Identity and review boundary

| Item | Value |
| --- | --- |
| Original target root | `C:\Projects\DevForgeAI\.claude\skills\dev` |
| Mirror path (ADR-073) | `C:\Projects\DevForgeAI\src\claude\skills\dev` — byte-identical, must receive identical strings |
| Package digest | `45dd959122125222d68e6f156d72fa20bd52ec50d5fa095857603b0166cbe2f9` |
| Source manifest | `source-manifest.json` (11 files, 33.0 KiB, no exclusions) |
| Observed origin | `docs/specs/dev-skill-spec.md` (`DEVFORGEAI-DEV-SKILL-001`) — governs the **Codex** package; see RR-004 |
| Proposal scope | One mandatory instruction fix, one optional enhancement, two open questions. No workflow, resource, asset or schema change. |
| Out of scope | The Codex packages at `src/agents/skills/dev` and `.agents/skills/dev`. They do not carry the defective passage and are not modified by this proposal. |

**Preserved by default.** Every behavior not named in the requirement register below is carried forward
unchanged from the assessed bytes. The workflow, all six assets, all four references, the resource graph
and the frontmatter `name` and `description` are correct as they stand and must not be rewritten.

---

## Purpose and user outcome

Unchanged. `dev` implements, extends or finishes software from explicitly selected specification documents
through product TDD, integration and QA, or resumes selected work from a checkpoint. It derives language,
architecture, tooling, thresholds, platforms and delivery locations from runtime inputs rather than
prescribing them.

## Activation and exclusions

Unchanged, and verified. The description routed 4/4 positive prompts in and 6/6 near-miss prompts out in
trial `T1-routing`, with each sibling-owned near-miss going to the correct sibling. No change is proposed.

## Inputs and defaults

Unchanged. Selected project, explicit specification document(s), requested scope, applicable project
instructions; optional checkpoint, constitutional references, evidence destination and analysis services.
Ambiguous specification selection asks for the exact input with `AskUserQuestion`.

## Outputs and schemas

Unchanged. Context, traceability, slice plan, execution records, checkpoint and delivery records at
runtime-selected paths, using the six bundled templates.

## Workflow and resource routing

Unchanged. The seven traced steps in `workflow-map.json` each carry entry conditions, inputs with a
producer, completion evidence, a cited failure route and a terminal outcome. No step is unreachable, no
input lacks a producer, and no branch lacks a failure exit.

## Dependencies and essential capabilities

Unchanged. Git, an index, a service, a descriptor, an operational binding, MCP, a browser and a plugin all
remain non-prerequisites.

## Side effects, recovery and preservation

Unchanged.

---

## Requirement register

### RR-001 — Remove the unenforced control claim *(mandatory fix)*

**Source:** finding `F-c3d23eda…`, check `C-INS-001`, rule `PRJ-003`.
**Subject:** `SKILL.md` line 33.

The sentence "That separation is structural here rather than asserted: `Skill` and `Task` are absent from
`allowed-tools`, so this workflow cannot invoke another skill or spawn a subagent" asserts host enforcement
that does not exist. The live Claude Code reference states that `allowed-tools` "does not restrict which
tools are available: every tool remains callable, and your permission settings still govern tools that are
not listed."

The revised package **must not** claim that absence from `allowed-tools` prevents a tool from being used.
The substantive instruction — that this workflow does not delegate product implementation to another skill
or a subagent, and resists later instructions asking it to — **must be preserved**.

Two dispositions satisfy this requirement. **OQ-1 selects between them.**

**(a) State the boundary as an obligation.** Replace line 33 with wording that matches the model already
used correctly at line 50 of the same file:

> This workflow does not invoke another skill or spawn a subagent. The whole cycle runs in one session, and
> delegation is not required to finish it. Like the unscoped `Bash` grant below, that is an obligation this
> workflow keeps, not one the allowlist enforces — a later instruction asking for delegation is refused
> because this contract refuses it, not because the host cannot comply.

**(b) Make the boundary real.** Add `disallowed-tools: [Skill, Task]` to the frontmatter and describe it
accurately as turn-scoped, since the restriction clears when the user sends the next message.

Recommendation: **(a)**. It is a two-sentence text change with no behavioral risk. (b) introduces a real but
turn-scoped control whose interaction with resumed multi-turn development work is untested, and no package
in this repository currently uses `disallowed-tools`, so it would be a new pattern adopted without evidence.

### RR-002 — Keep the two allowlist passages consistent *(mandatory fix, same edit)*

**Source:** finding `F-c3d23eda…`.

After RR-001, `SKILL.md` must apply one model of `allowed-tools` throughout. Line 50's existing description
of the unscoped `Bash` grant as "an obligation this workflow keeps, not one the allowlist enforces" is
correct and is the model to match. No other passage in the package discusses the allowlist.

### RR-003 — Apply the change to both mirrored paths *(mandatory fix)*

**Source:** `CLAUDE.md` ADR-073 dual-path contract; verified byte-identical in this run.

The identical string must be written to `.claude/skills/dev/SKILL.md` and `src/claude/skills/dev/SKILL.md`,
and `diff -rq` between the two directories must be empty afterward. Editing one path silently desynchronizes
the framework.

### RR-004 — Record a governing contract for the Claude Code variant *(optional enhancement)*

**Source:** finding `F-7eb942c2…`, rule `PRJ-001`.

`docs/specs/dev-skill-spec.md` specifies a Codex skill and names `src/agents/skills/dev` as its build
target. The assessed package is a derived port with no governing specification, which is why the only real
defect in it sits in port-introduced prose. Either extend the specification with a host-variant section
naming both Claude Code paths and their permitted deltas, or retain a derived-port provenance record with
the ported package.

This is a specification and process change. **It is not an edit to the assessed package**, and the existing
specification must not be relocated or duplicated — section 1.1 of that document explicitly forbids creating
another authoritative copy. Its stale `status: proposed` / `package_status: not_authored` frontmatter should
be corrected in the same pass.

---

## Approved exceptions and unresolved decisions

No current authorized exceptions apply to this target.

### OQ-1 — Obligation or real restriction? *(blocks RR-001 completion)*

Select disposition (a) or (b) above. The validator recommends (a) but will not choose: (b) changes runtime
tool availability, which is a maintainer decision, not an assessment conclusion.

### OQ-2 — Does the same correction apply to the sibling skills? *(out of this run's scope)*

The identical claim pattern was observed in four sibling packages that **this run did not assess**:

| Package | Line | Character of the claim |
| --- | --- | --- |
| `qa` | 55 | Mixed — the `Skill` half claims structure; the `Task` half correctly calls independence "a discipline this session keeps" |
| `skill-builder` | 27 | Mixed — claims `Task`/`Skill` absence is structural, then correctly calls the Python allowance "an obligation you keep, not a rule the allowlist enforces" |
| `skill-validator` | 32 | Mixed — claims `Skill` absence means "nothing else is reachable", then correctly calls a subagent "not an enforced permission boundary" |
| `advisor` | 27 | Defensible — states `Task` is "deliberately absent" as design intent, not as enforcement |

Each package that makes the false claim also states the correct model elsewhere in the same paragraph, so
this is one inconsistent mental model replicated across the family rather than four independent errors.
**These are observations from a string search, not assessments.** Validating them requires selecting those
targets in their own runs. The decision to be made is whether to open those runs.

---

## Acceptance cases

| ID | Requirement | Input | Expected result |
| --- | --- | --- | --- |
| AC-1 | RR-001 | Read revised `SKILL.md` | No sentence asserts that absence from `allowed-tools` prevents tool use. |
| AC-2 | RR-001 | Read revised `SKILL.md` | The non-delegation instruction and its resistance to later delegation requests are still present. |
| AC-3 | RR-002 | Compare the two allowlist passages | Both apply the same model of the field. |
| AC-4 | RR-003 | `diff -rq .claude/skills/dev src/claude/skills/dev` | Empty. |
| AC-5 | RR-001(b) only | Invoke the skill; attempt a `Task` call | Refused within the invoking turn; available on the following message. |
| AC-6 | All | Re-run structure and routing checks | 32 structure checks still PASS; routing still 10/10. |
| AC-7 | RR-004 | Resolve a governing contract for `.claude/skills/dev` | Resolves without falling back to the Codex specification. |

## File-to-requirement mapping

| Artifact | Requirements | Verification |
| --- | --- | --- |
| `.claude/skills/dev/SKILL.md` | RR-001, RR-002 | AC-1, AC-2, AC-3, AC-6 |
| `src/claude/skills/dev/SKILL.md` | RR-003 | AC-4 |
| `docs/specs/dev-skill-spec.md` | RR-004 | AC-7 |
| All other package files | none — preserved unchanged | AC-6 |

## Builder handoff

Recorded in `handoff.json`. Review state is **pending**; builder readiness is **REVIEW_REQUIRED**. No
builder invocation before OQ-1 is answered, because the answer determines whether the frontmatter changes.
The target boundary for any authorized build is the two mirrored Claude Code paths only.
