# Future enforcement recommendations

These are **proposed designs, not installed controls**. Nothing below exists today, and none of it was exercised in this run. A recommendation here is a candidate for later design work requiring investigation; it is not a claim that a hook event, CI job or CLI subcommand exists. Actionable guidance in the target package must be preserved until an authorized replacement actually exists.

---

## E-1 — Detect prose that claims `allowed-tools` restricts the tool pool

| Field | Value |
| --- | --- |
| Finding reference | `F-81a134296f5416a9...` (rule PRJ-003) |
| Passage reference | `SKILL.md` line 33, assessed digest `ec47a6826276edc93675b0631d01aaa388f01d4fc0c68c71adf673e3ab27763f` |
| Proposed destination | `ci_workflow`, with `devforgeai_cli` as the eventual authority |
| Trigger | Any change to a `SKILL.md` under a skills root. |
| Invariant | No skill package asserts that `allowed-tools` restricts, removes, blocks or prevents access to a tool. `allowed-tools` pre-approves; `disallowed-tools` restricts. |
| Inputs | The changed `SKILL.md` bytes; a dated copy of the Claude Code skills reference passage (see `sources/`). |
| Intended observation / action | Flag co-occurrence of `allowed-tools` with restriction verbs ("cannot", "unable", "prevents", "removes", "structural", "not available") within a bounded window, for human review. Report only; do not edit. |
| Current evidence | This run: the defect existed in a package that passed both `observe.py structure` and the installed Skill Creator checker, and the same error is independently present in at least two other packages in this repository — `skill-validator/SKILL.md` and `skill-validator/references/handoff.md`. It is a repository-wide pattern, not a one-off. |
| Failure behavior | On unavailable source guidance, report `NOT_RUN` with the stale-snapshot reason rather than passing. |
| Bypass and coverage limits | Lexical proximity matching produces false positives on correct prose (the target's own accurate `Bash` sentence uses "enforces" near "allowlist" and would likely be flagged) and misses paraphrase. It is a review-location detector, never an acceptance gate. |
| Dependencies | A refreshed, digest-pinned copy of the official `allowed-tools` passage; a skills-root discovery convention. |
| Future verification scenario | Seed a fixture package carrying the exact defective sentence and a second carrying the corrected Option B wording; the check flags the first and not the second. |

---

## E-2 — Assert declared host-semantics claims against pinned official guidance

| Field | Value |
| --- | --- |
| Finding reference | `F-81a134296f5416a9...`, `F-4aafff1856bf34b2...` (Q2 premise) |
| Passage reference | `SKILL.md` line 33; `inputs/validation-request.json` `open_questions[1]` |
| Proposed destination | `devforgeai_cli` |
| Trigger | A builder authoring run that produces or edits a claim about host behavior, and any validation run that pins a rule set. |
| Invariant | A package statement about what the host does or prevents must cite a pinned source passage, and that passage must still carry the asserted meaning at the current digest. |
| Inputs | Package bytes; `sources.json`; `rule-set.json`; retained source snapshots. |
| Intended observation / action | Require a source binding for host-semantics claims; surface unbound claims as unresolved rather than passing them. |
| Current evidence | The bundled `assets/claude-frontmatter-guidance.md` documented the **shape** of `allowed-tools` but not its **enforcement semantics**, so the rule set as pinned could not have caught this. Only the live retrieval performed in this run closed the gap. |
| Failure behavior | Unbound claim → `NOT_RUN` / unresolved; never an automatic FAIL, since not every sentence is a host-semantics claim. |
| Bypass and coverage limits | Classifying which sentences are host-semantics claims is semantic and cannot be made fully deterministic. A compiled authority would gate on the presence of a binding, not on the correctness of the prose. |
| Dependencies | Rule-set source binding already exists; needs a claim-classification convention that does not yet exist. |
| Future verification scenario | A package asserting an unbound host behavior is reported unresolved; the same package with a pinned locator whose passage supports it is not. |

---

## E-3 — Keep `dev-cases.jsonl` coverage honest across runs

| Field | Value |
| --- | --- |
| Finding reference | `F-4a176fc9bdf39d29...` (rule PRJ-004) |
| Passage reference | `inputs/dev-cases.jsonl`, D01–D20, all `required: true` |
| Proposed destination | `devforgeai_cli` |
| Trigger | Completion of a validation run whose target has a bundled declarative case set. |
| Invariant | Every `required: true` case resolves to `PASS`, `FAIL`, `ERROR` or `NOT_RUN` with a reason; no required case is silently absent from the reduction, and static instruction coverage never promotes a case to `PASS`. |
| Inputs | The case set; `checks.jsonl`; the trial inventory. |
| Intended observation / action | Reconcile the case set against recorded checks and report unaccounted required cases. |
| Current evidence | This run accounted for all twenty cases by hand: 5 `PASS`, 15 `NOT_RUN` with per-case reasons. Nothing enforced that accounting — it was an obligation the assessor kept. |
| Failure behavior | Unaccounted required case → the run is incomplete. |
| Bypass and coverage limits | Deterministic accounting only. It cannot judge whether a `NOT_RUN` reason is honest or whether a `PASS` rests on adequate evidence. |
| Dependencies | A convention binding a case set to a target, which currently exists only by filename. |
| Future verification scenario | A run that omits one required case from `checks.jsonl` is reported incomplete; a run that records it `NOT_RUN` with a reason is not. |

---

## Not proposed

No enforcement candidate is offered for the ask-branch cases (D01, D05, D07, D08, D12). Those need an interactive executor because `AskUserQuestion` is unavailable to a host subagent; that is a host capability gap, and an enforcement control cannot close it.
