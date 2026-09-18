---
id: DEVFORGEAI-ADVISOR-CLAUDE-CONVERSION-20260916
target: claude-code
status: observation
recorded: "2026-09-16"
---

# advisor — Codex to Claude Code conversion report

Complete source accounting for the conversion of `src/agents/skills/advisor` (22 files) into `src/claude/skills/advisor` (21 files). Produced alongside authoring run `advisor-claude-conversion-001`.

- Run root: `docs/plan/skill-authorings/advisor/20260917T025538Z-claude-conversion/`
- Operation: `import` · State: **AUTHORED** · 21 paths applied, no issues
- **Validation: NOT_PERFORMED · Testing: NOT_PERFORMED**

## File dispositions

| Source path | Disposition | Target path | Reason |
| --- | --- | --- | --- |
| `SKILL.md` | rewrite | `SKILL.md` | Host mapping: `$advisor` → `/advisor`; `allowed-tools` added; openai.yaml metadata folded into the description; Codex-as-caller reworded; contract path de-hardcoded. |
| `agents/openai.yaml` | **omit** | — | Claude Code has no separate UI metadata file. `display_name` and `short_description` folded into `description`. `default_prompt` has no Claude Code equivalent and its `$advisor` syntax is not substituted; recorded here as unreproduced source metadata. |
| `artifact-manifest.json` | rewrite | `artifact-manifest.json` | Digests regenerated for the converted package. `external_contract.path` replaced with an operator-configured token; its `sha256` carried forward unchanged as the contract version this package was authored against. |
| `references/execution.md` | rewrite | same | 7 replacements: absolute skill paths → `<skill>`; operator paths → resolution tokens; a new paragraph defining `<skill>` and stating the external contract is operator-supplied; Codex docs source → Claude skills. |
| `references/response-format.md` | rewrite | same | 4 replacements: "Codex" as the consuming agent → "the calling agent". Necessary here beyond cosmetics — the reviewer is also Claude, so naming the caller "Claude Code" would have made the response-interpretation rules ambiguous about which party assesses which. |
| `references/briefing-rules.md` | rewrite | same | 1 replacement, same reason. |
| `references/evaluation.md` | rewrite | same | 4 replacements: repo-relative skill paths → `<skill>`; "Codex skill routing" → "skill routing in the host". |
| `assets/briefing-template.md` | preserve | same | Host-neutral. |
| `assets/request.schema.json` | preserve | same | Host-neutral closed schema; unchanged so existing request files stay valid. |
| `scripts/advisor_run.py` | preserve | same | The execution model ports unchanged — it spawns the Claude CLI with `shell=False`, which behaves identically regardless of which agent calls it. |
| `scripts/advisor_stream.py` | preserve | same | As above. |
| `scripts/advisor.ps1` | preserve | same | Windows launcher, host-neutral. |
| `evals/` (4 files) | preserve | same | 38 eval cases, case schema, runner and coverage config. Verified free of host-specific content. |
| `tests/` (6 files) | preserve | same | Verified free of host-specific content. |

Verified: the only source file absent from the target is `agents/openai.yaml`; nothing was added that the source did not have.

## Design decisions worth review

**The external reviewer process was kept; it was not replaced with `Task`.** Claude Code offers fresh-context subagents, and mapping the reviewer onto one would have been the obvious "native" conversion. It was rejected: the skill's contract rests on a *separate process* with its own read-only tool set, its own `--max-budget-usd` cap, its own timeout, and an auth mode that manipulates only the child environment. A subagent shares the session's budget and authentication and offers no equivalent cap. Substituting it would have preserved the shape of the skill while quietly discarding the guarantees it documents.

Because that decision is load-bearing, `Task` is deliberately **absent** from `allowed-tools`, so the workflow cannot drift into using a subagent as a cheaper stand-in. `Skill` is absent for the same structural reason as in skill-builder — no chaining into other skills. Both omissions are enforcement, not prose.

**`allowed-tools` granted:** `Read`, `Glob`, `Grep` (evidence and citation verification), `Write`, `Edit` (briefing and request JSON in the intake directory), `AskUserQuestion` (only when materially different readings of the ask remain), `Bash(python:*)`/`Bash(python3:*)` (the helper), `Bash(pwsh:*)`/`Bash(powershell:*)` (the Windows launcher).

**`model` and `effort` omitted** from frontmatter, consistent with the source declaring neither. The skill's own `model=`/`effort=` request conventions select the *reviewer's* model, which is a different thing from the calling session's.

## Open question — maintainer decision required

**Q1 (recorded in the authoring design and carried into the handoff packet).** Where should a Claude Code deployment resolve the required external reviewer contract?

The Codex source hardcodes `C:/Users/bryan/.codex/advisor/contract.md` — one operator's path, under a Codex directory. That cannot travel into a portable package. The converted skill treats the path as operator-configured and resolved at preflight, and reports its absence as a dependency gap rather than creating one. No canonical default location for Claude Code installs has been selected.

Owner: maintainer. Affects behaviors `B2-preflight` and `B4-invoke-review`. The skill is complete and usable without this decision — the operator simply supplies the path — but a default would remove a setup step.

## Verification performed

| Check | Result |
| --- | --- |
| Design validated against `authoring-design-v1` | accepted by `authoring.py begin` (rejected once first, for a malformed helper contract) |
| Design capture bound | `design-capture.json` + `origin.design_capture_ref` + `stage-integrity.json`, source and snapshot digests equal |
| Portable files byte-identical | 15/15, no line-ending drift |
| Reference conversions | every replacement asserted to hit exactly once |
| Residual host/personal wiring in delivered package | none, including inside `evals/cases.jsonl` |
| Frontmatter parses as YAML | valid; `Task` absent, `Skill` absent |
| Internal link targets resolve | 0 missing |
| Delivered bytes vs candidate | identical |
| `artifact-manifest.json` self-consistency | 20 tracked, 0 mismatches, 0 untracked |
| Publication | `AUTHORED`, `publication-readback.json` present, no unresolved write issues |

These are build-integrity and write-custody observations. **No test suite, eval campaign, grader or reviewer call was executed**, per the authoring-only contract. The carried-over `tests/` and `evals/` remain unexecuted against the converted bytes.

## Next owner and action

Independent assessment. The handoff packet is at `<run>/validation-request.json` with the invocation in `<run>/validator-request.md`. It names the authored design, the 22 original requirement sources with digests, open question Q1, and unperformed helper-testing obligations for all three scripts.

Installation is a separate authorized act: the package is at `src/claude/skills/advisor/` and has not been copied to any operational skills directory.
