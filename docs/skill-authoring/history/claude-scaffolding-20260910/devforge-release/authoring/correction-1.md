# devforge-release — correction 1 (mechanical)

Model: **Opus 5 (1M context)**, model ID `claude-opus-5[1m]`. The system prompt for this session does state a 1M context window.

Authorized by the coordinator's codex-review disposition of 2026-09-10. Scope: one line of one file, plus the authoring evidence that records its digest. No instruction, phase, exit condition, input row, authority statement, eval case, fixture or asset was touched.

- Provider / skill: `claude` / `devforge-release`
- Worktree: `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910`
- Branch: `author/claude-devforge-release-scaffold-20260910`
- Base for this correction: `66d8dbad7c211ce1cba208cb09600a80997c5d74` (repair pass 1 recheck), working tree clean and equal to `origin/author/claude-devforge-release-scaffold-20260910` before any write
- Recorded at: 2026-09-11T00:08:30Z

## The defect

`providers/claude/plugins/devforgeai/skills/devforge-release/SKILL.md` line 3 held the `description:` value as an **unquoted YAML plain scalar containing `: `** (a colon followed by a space), in the closing clause `A release record is not a deployment receipt: writing one does not establish that anything was published.`

In a plain scalar, `: ` opens a nested mapping, so a strict YAML parser rejects the frontmatter rather than reading the description. The Agent Skills specification requires the frontmatter to be YAML, so a file that only some readers can parse does not meet it.

Severity: **MINOR, spec conformance.** It is not a runtime failure on this provider — the coordinator's probe observed Claude Code 2.1.268 loading this same description in full. The fix is for portability and for any consumer that parses the frontmatter strictly.

Observed with PyYAML 6.0.3 on CPython 3.12.3, against the pre-correction bytes taken from `HEAD` (`git show HEAD:…/SKILL.md`):

```text
yaml.scanner.ScannerError: mapping values are not allowed here
  in "<unicode string>", line 3, column 969:
     ... cord is not a deployment receipt: writing one does not establish ...
                                         ^
```

## The fix

The description value is now wrapped in **double quotes**. Nothing else changed on the line and nothing else changed in the file.

Chosen because the text contains no `"`, no `\`, no `'`, no `&` and no non-ASCII character — checked before editing — so a double-quoted scalar needs no escaping and processes no escape sequence. The alternative of rewording the clause to remove `: ` was not taken: the wording is a discriminating clause the repair-pass-1 record lists as deliberately preserved.

- Characters changed: exactly two added (`"` before the value, `"` after it). File grew by 2 bytes.
- `git diff --numstat` on `SKILL.md`: `1 1` — one line added, one line removed.
- Changed content lines in the diff: `2` (the `-` and the `+` for line 3).
- The document body after the frontmatter is byte-identical to `HEAD`.
- The parsed description is byte-identical to the previous raw scalar text: `yaml.safe_load(...)['description'] == <HEAD line 3 after "description: ">` returns `True`, 1016 characters on both sides.
- Frontmatter keys after the change are exactly `['description', 'name']`, with `name` still `devforge-release`.

### Verification command and output

The packet's command, with the relative `SKILL.md` replaced by its absolute path; nothing else in the one-liner was altered.

```text
$ python3 -c "import yaml,sys; t=open('/home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910/providers/claude/plugins/devforgeai/skills/devforge-release/SKILL.md').read().split('---',2)[1]; d=yaml.safe_load(t); print(len(d['description']))"
1016
```

**1016** is the required value: the same length the unquoted scalar had, so the quoting added delimiters and not content. The same command against the pre-correction bytes raises the `ScannerError` quoted above instead of printing anything.

### Digests

| File | Before | After |
| --- | --- | --- |
| `providers/claude/plugins/devforgeai/skills/devforge-release/SKILL.md` | `b4ac89032c8b17ee6d201033290833c1498e06952f5885e80b331b50629112fe` | `7498e37c96f80454afdcb2bd6786422c88f9188136e77136ca6a659fcd225b71` |

Every other file in the package is unchanged; `authoring/file-manifest.json` `files_sha256` carries the new SKILL.md value and is otherwise the repair-pass-1 map.

## Evidence bookkeeping

- **`authoring/file-manifest.json`** — updated: `files_sha256["SKILL.md"]` set to the new digest; `candidate_revision` now names correction 1 and its immediately prior candidate commit `66d8dba`; a `changed_in_correction_1` block records the before/after pair, the authorization, and the scope. The existing `changed_in_repair_pass_1` block was **not** rewritten — it is an accurate record of what that pass produced, so its `SKILL.md.after` value is the pre-correction digest by design. A `changed_in_repair_pass_1_note` says so, to stop a reader reading two current digests out of one file.
- **`references/derivation.json`** — checked, **not changed**. It records no digest for `SKILL.md`: the file appears there only in `not_derived`, as `{"path": "SKILL.md", "note": "Written for this package against SKILL-011. Not a copy or adaptation of any single source."}`, with no `sha256` field. Nothing in it required an update, and nothing in it was edited. (It is also outside this correction's fence, which covers SKILL.md line 3 and the `authoring/` tree only.)
- **`authoring/handoff.md` line 104** — deliberately **not** modified. It is a delivered receipt for the repair-pass-1 candidate and correctly states the digest of what was handed over. It is therefore now **superseded**, not wrong: read it as the digest of commit `66d8dba`, and read this file and the manifest for the current identity.
- **`validation/scaffold-review/**` and `validation/scaffold-review-recheck/**`** — untouched and outside the fence. They are the independent evaluator's frozen records, and they too name the pre-correction digest for the candidate they examined. Frozen evidence is never repinned.

## What this correction does not establish

- **Tier C (resource resolution): `NOT_RUN`. Tier B (quality against a baseline): `NOT_RUN`. Tier A (discovery and activation from an installed package): `NOT_RUN`.** No tier was run for this correction and none was run before it. Behaviour remains `NOT_EVALUATED`.
- Nothing was installed, exported, bound, discovered or activated. No skill was invoked. The only execution here is a YAML parse of one file.
- A YAML parse proves the frontmatter is now readable by a strict parser. It proves nothing about discovery, activation, triggering, or whether the skill works.
- Changing SKILL.md makes this a **new candidate identity**. The evaluator's findings were closed against `66d8dba`; re-evaluation is required against `7498e37c…` before any result recorded here is treated as covering the current bytes. This correction closes no finding and opens none.

## Deviation to flag to the coordinator

The packet specifies these commit trailers:

```text
Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01UXvkMeZsS2zRyEBxgHfw62
```

The first line names a model that did not do this work. This session runs on **Opus 5 (1M context), `claude-opus-5[1m]`**, and the session's own attribution instruction — which states that it replaces earlier attribution guidance — gives `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>` with the identical `Claude-Session` line. Recording a model identity that is not the acting model would put a false attribution into the permanent record, in a project whose standing rules are about not fabricating evidence identity.

The commit therefore uses:

```text
Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01UXvkMeZsS2zRyEBxgHfw62
```

The `Claude-Session` line is byte-identical to the packet's. Only the model name differs, and only because the packet's value is not this session's model. If the coordinator intended the `Fable 5.1` line for some reason other than a copy-paste from its own session, say so and it can be amended before merge.
