# Enforcement register — `dev`

Run `20260918T202845Z`. Target `C:\Projects\DevForgeAI\.claude\skills\dev`.

These are **candidates for later design**, not claims that a hook event, check or CLI command exists today.
Nothing here is an implemented acceptance gate. This register is the fifth descriptive dimension of the
assessment and does not contribute to PASS/FAIL.

---

## ENF-001 — Detect frontmatter-as-enforcement claims in skill packages

| Field | Value |
| --- | --- |
| Proposed destination | `ci_workflow`, with `claude_hook` as a lighter-weight variant |
| Trigger | Any change to a `SKILL.md` under `.claude/skills/`, `src/claude/skills/` |
| Invariant | A package must not claim that absence of a tool from `allowed-tools` prevents that tool from being used. |
| Inputs | The changed `SKILL.md` bytes; the `allowed-tools` and `disallowed-tools` frontmatter values |
| Intended observation | Flag prose matching the semantic pattern "X is absent from `allowed-tools`, so this workflow cannot Y" and the phrase "structural rather than asserted" when applied to an allowlist |
| Current evidence | F-001 in this run. The same string pattern was observed in four sibling packages (`qa`, `skill-builder`, `skill-validator`, `advisor`) that were **not** assessed by this run. |
| Failure behavior | Advisory comment on the change; not a merge block, because the classification is semantic and a correctly-worded discussion of the allowlist must pass. |
| Bypass and coverage limits | Keyword matching cannot establish the finding on its own — `rules.md` SV-007 requires semantic classification with context. A reworded claim with the same false meaning escapes a regex. Treat a hit as a review prompt, never as an automatic defect. |
| Dependencies | An agreed canonical statement of what `allowed-tools` does, sourced from the live Claude Code reference rather than restated locally. |
| Future verification scenario | Seed a fixture package asserting "`Task` is absent from `allowed-tools`, so this workflow cannot spawn a subagent" and confirm the check flags it; seed a second fixture asserting "the allowlist does not enforce this; it is an obligation this workflow keeps" and confirm the check stays silent. |

---

## ENF-002 — Enforce the real boundary with `disallowed-tools`

| Field | Value |
| --- | --- |
| Proposed destination | `guidance_only` today; `ci_workflow` once a policy decision exists |
| Trigger | A package states a tool-use boundary as part of its contract |
| Invariant | A boundary the package presents as structural is backed by `disallowed-tools`, or is stated as an obligation rather than a structural fact. |
| Inputs | Frontmatter `disallowed-tools`; the prose boundary claims |
| Intended observation | Where a package says it cannot use tool X, either `disallowed-tools` lists X, or the prose is phrased as a discipline. |
| Current evidence | The live Claude Code reference states `disallowed-tools` removes tools from the available pool while the skill is active — this is the field that actually restricts. No package in this repository currently uses it (`grep` over both skill trees returns only the validator's own documentation and test fixtures). |
| Failure behavior | Review prompt naming the specific tool and the two available remedies. |
| Bypass and coverage limits | `disallowed-tools` clears when the user sends the next message, so it bounds the invoking turn rather than the whole session. It is a real but **turn-scoped** control, and a register entry must not oversell it as a session-long guarantee. It also cannot remove `EndConversation` while other tools remain. |
| Dependencies | A maintainer decision on whether these skills actually want the restriction or only the obligation. That decision is recorded as OQ-2 in the revision specification and is not made here. |
| Future verification scenario | Add `disallowed-tools: [Skill, Task]` to a fixture skill, invoke it, and observe whether a `Task` call is refused within the invoking turn and available again on the next message. |

---

## ENF-003 — Keep the two mirrored Claude Code trees identical

| Field | Value |
| --- | --- |
| Proposed destination | `git_hook` (pre-commit) with a `ci_workflow` backstop |
| Trigger | A commit touching `.claude/skills/**` or `src/claude/skills/**` |
| Invariant | `diff -rq .claude/skills/<name> src/claude/skills/<name>` is empty for every skill present in both trees. |
| Inputs | Both trees |
| Intended observation | An empty diff. This run verified the pair for `dev` specifically and found it byte-identical. |
| Current evidence | The ADR-073 dual-path contract is documented in `CLAUDE.md`; this run confirmed compliance for `dev` only, not repository-wide. |
| Failure behavior | Block the commit locally and name the differing paths; CI re-checks because a local hook is bypassable with `--no-verify`. |
| Bypass and coverage limits | A local Git hook is advisory — it is not installed by cloning and is skippable. A GitHub-hosted check is the enforcing half. The two are different mechanisms and this register keeps them distinct. |
| Dependencies | None beyond Git. |
| Future verification scenario | Edit one path only, attempt a commit, confirm the hook names the mismatch; confirm CI independently fails the same change pushed with `--no-verify`. |

---

## ENF-004 — Bind a specification to each host variant of a ported skill

| Field | Value |
| --- | --- |
| Proposed destination | `guidance_only` |
| Trigger | A skill package is ported between hosts |
| Invariant | Every shipped host variant resolves to a governing specification, or records explicitly that it is a derived port with no separate contract. |
| Inputs | The package; the specification tree |
| Intended observation | A resolvable specification reference per variant. |
| Current evidence | F-002 in this run: `docs/specs/dev-skill-spec.md` specifies a **Codex** skill and names `src/agents/skills/dev` as its build target, so the assessed Claude Code package has no governing specification of its own. The port-introduced defect F-001 lives precisely in the prose that no specification covers. |
| Failure behavior | Review prompt at port time. |
| Bypass and coverage limits | This is an authoring-process recommendation. No mechanical check can tell a deliberate derived port from an unspecified one without a declared convention. |
| Dependencies | A convention for recording derived-port provenance — for example a builder authoring record retained with the ported package. None accompanied this port (ORG-U4). |
| Future verification scenario | Port a fixture skill without a variant specification and confirm the review prompt fires; add a derived-port provenance record and confirm it clears. |

---

## Not proposed

No enforcement candidate is recorded for the workflow's evidence, traceability, checkpoint or QA-metric
instructions. They are already expressed as observable obligations with concrete artifacts, and this run
found no gap between what they instruct and what they can deliver. Proposing a gate there would add
ceremony without a demonstrated failure to prevent.
