# devforge-design — correction 1 (mechanical)

- **Package:** `providers/claude/plugins/devforgeai/skills/devforge-design` (SKILL-003, provider `claude`)
- **Worktree:** `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910`, branch `author/claude-devforge-design-scaffold-20260910`
- **Base commit for this correction:** `d4959c5f3564a951fe0a9c8b0f5ce3d2e30bde1e` (working tree clean, `HEAD == origin`, verified before writing)
- **Recorded at (observed UTC):** 2026-09-11T00:07:06Z
- **Authorization:** the coordinator's codex-review disposition of 2026-09-10. This is a bounded mechanical correction; no authoring judgement was re-opened.
- **Author model:** Opus 5 (1M context), model ID `claude-opus-5[1m]`. The system prompt states a 1M context window.

## Defect

`SKILL.md` line 3 carried the `description:` value as an **unquoted YAML plain scalar containing `: `** (colon followed by space), inside the fragment:

> `… "Design" here means the user experience: a database schema, an API surface …`

In a plain scalar a `: ` sequence opens a nested mapping, so the frontmatter is not loadable YAML. Observed against the bytes at `d4959c5`:

```text
$ python3 -c "import yaml; t=open('SKILL.md').read().split('---',2)[1]; yaml.safe_load(t)"
FAIL: ScannerError mapping values are not allowed here
$ python3 -c "import yaml; print(yaml.__version__)"
6.0.3
```

The Agent Skills specification requires YAML frontmatter, so the bytes were non-conforming. Severity is **MINOR, spec conformance — not a runtime failure**: the coordinator's probe observed Claude Code 2.1.268 loading this description in full. Nothing here is evidence about whether the skill activates or behaves correctly; that remains `NOT_EVALUATED`.

## Fix

One line changed, one byte added at each end of the value. The description text contains double quotes and no single quote, so the value was wrapped in **single quotes**, leaving all 950 characters of the text identical:

```diff
-description: Turn accepted requirements into a reviewable user experience - journeys, … is not this skill.
+description: 'Turn accepted requirements into a reviewable user experience - journeys, … is not this skill.'
```

No other byte of `SKILL.md` changed. File size went from 18109 to 18111 bytes; `git diff --numstat` for the file is `1	1`.

## Verification

The packet's verification command, run from the skill directory, verbatim output:

```text
$ cd /home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/providers/claude/plugins/devforgeai/skills/devforge-design
$ python3 -c "import yaml,sys; t=open('SKILL.md').read().split('---',2)[1]; d=yaml.safe_load(t); print(len(d['description']))"
950
```

950 equals the pre-correction unquoted length, so no character was folded, escaped or trimmed. A stronger check compared the parsed value against the captured pre-edit line byte for byte:

```text
name: 'devforge-design'
keys: ['description', 'name']
byte-exact match to pre-edit text: True
len: 950 expected: 950
```

Frontmatter keys remain exactly `name` and `description`, as the authoring contract requires.

What these commands establish: the frontmatter now parses under PyYAML 6.0.3 and the description text is unchanged. What they do not establish: anything about discovery, activation, installation, export or behaviour.

## Evaluation status (unchanged by this correction)

| Tier | Status |
| --- | --- |
| C (installed resources resolve) | `NOT_RUN` |
| B (output quality vs. baseline) | `NOT_RUN` |
| A (discovery and activation from the installed package) | `NOT_RUN` |
| Behavioural status | `NOT_EVALUATED` |

No skill was installed, exported, discovered, activated or run for this correction. A source edit closes no evaluation finding; an evaluator must evaluate the new bytes.

## Records touched, and records deliberately not touched

**Changed (inside the correction fence):**

| Path | Change |
| --- | --- |
| `providers/claude/plugins/devforgeai/skills/devforge-design/SKILL.md` | line 3 only; new sha256 `b92e932a364fdc073fb7b770583ebb4782520b1917b5ae5f119ceba2f0f936bc` (was `90698266b028a8abad3ba113eb8e14d85212e89b41c9b0e75e8c7cdd58d082a1`) |
| `…/authoring/file-manifest.json` | `files["SKILL.md"]` repointed to the new digest, and one sentence appended to `note` so the manifest does not claim every digest is post-repair-pass-1 bytes. New sha256 `02c7d6108ecc00f4f09a0f94076176959fac5cb4e9254babff2b03785804a9c3` (was `156ae87f934c21e42e46e41cdf5b8035dd5d71a2a6baa3066e60eae71dff41aa`) |
| `…/authoring/correction-1.md` | this file (new) |

**Checked and correctly left alone:**

- `providers/claude/plugins/devforgeai/skills/devforge-design/references/derivation.json` — **no update required.** Its only `SKILL.md` digest is the *upstream builder* (`devforge-project-expert-creator/SKILL.md`, `342b8292…` at commit `4999f310`), not this package's SKILL.md, and the file records no self-digest by design. The packet's conditional therefore does not fire. Its own digest in the manifest is unchanged and still correct.
- `…/validation/scaffold-review-recheck/` (`recheck-report.md`, `findings-recheck.json`, `commands.log`) — carries the pre-correction SKILL.md digest `90698266…`. This is frozen independent-evaluator evidence recording the bytes that were reviewed. It is outside the correction fence and was not modified; its digest reference is correct for the revision it evaluated.
- `…/authoring/handoff.md` (revision 3) — records `file-manifest.json` at `156ae87f…`, now stale. Its own stated invalidation condition already covers this ("any edit to the package (the manifest digests go stale immediately)"). Rewriting a frozen handoff revision in place was outside this correction's authorized scope, so it was left byte-identical. **Coordinator decision needed:** whether a handoff revision 4 is issued, or whether this correction record is sufficient for the evaluator to resolve the manifest digest.
- `…/authoring/authoring-notes.md`, `…/authoring/spec-mapping.md`, `…/authoring/design/` — unchanged.
- `file-manifest.json` fields `recorded_at_utc` (`2026-09-10T21:16:02Z`) and `candidate_revision` (`repair pass 1…`) still describe repair pass 1. Repointing them is a records decision beyond a mechanical digest update, so they were left as authored and flagged here and in the `note`.

## Deviation from the packet, disclosed

The packet supplied the trailer `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. The commit instead carries:

```
Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01UXvkMeZsS2zRyEBxgHfw62
```

Reason: this correction was authored by Opus 5 (1M context), and the session's harness-level attribution instruction — which states it replaces earlier attribution guidance — supplies that exact line. `Co-Authored-By` is a factual authorship claim, and recording a model that did not write these bytes would be a false record in the very commit whose purpose is record accuracy. Branch precedent matches: the previous author commit `b2827ce` used the Opus 5 (1M context) trailer, while `Claude Fable 5.1` appears on the coordinator's own commits (`d4959c5`, `60803e9`). The `Claude-Session` line is identical in both versions and was used unchanged. If the coordinator intended the Fable trailer as a literal requirement rather than a template default, this is the one point to correct.
