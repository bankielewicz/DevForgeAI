---
id: DEVFORGEAI-DEV-CLAUDE-REVISION-002
skill_name: dev
host: claude-code
kind: proposed_revision_specification
status: proposed
review_state: pending
supersedes: null
origin_run: 20260918T202845Z
this_run: 20260919T021255Z
target_root: C:\Projects\DevForgeAI\src\claude\skills\dev
mirror_root: C:\Projects\DevForgeAI\.claude\skills\dev
baseline_package_digest: 8321da52e578ce1d72ce40b281882c756c03b260c75953820b4f209f90eb2d81
---

# Proposed revision — `dev` (Claude Code)

This is a **proposal for human review**, not an instruction to build. It does not replace the
origin specification (`docs/specs/dev-skill-spec.md`, digest `b9783ca0…`), which is preserved
unchanged and remains the Codex contract. Nothing here was applied to the target.

The scope is deliberately narrow. The prior revision proposal (`RR-001`–`RR-004`) has been
delivered for its mandatory items and verified resolved in run `20260919T021255Z`. What remains is
one mechanical fix to a side effect of that delivery, plus one enhancement carried forward
untouched.

## 1. What is already correct and must be preserved

The builder's delivered change is correct and this proposal does not reopen it. Preserve exactly:

- **The corrected scope-boundary paragraph**, character for character. Its wording is verified
  accurate against the live Claude Code reference and verified *operative* by trial `T1-boundary`,
  where a cold reader derived the right semantics and held the boundary against an embedded
  delegation instruction while delegation tooling was available. Any edit that reopens this
  paragraph invalidates that evidence and requires a fresh trial.
- **The consistent model across lines 33 and 50.** Both now read "an obligation this workflow
  keeps, not one the allowlist enforces." Do not reintroduce divergent phrasing.
- **The absence of `disallowed-tools`.** The prior run's `OQ-1` was answered in favour of stating
  the boundary as an obligation. Adding the field is a separate policy decision (`ENF-002`), not
  part of this revision.
- **All 10 non-entrypoint files**, byte-identical.
- **`name: dev`**, the `description` bytes, and the seven-entry YAML-list `allowed-tools`. The list
  form is valid on this host, re-confirmed live in this run. It is non-portable to a host
  implementing only the Agent Skills specification; that is a recorded divergence, not a defect,
  and must not be "fixed" by converting to a space-separated string.
- **The workflow**: six numbered items, seven mapped steps, four references, six assets, 24 links.

## 2. RR-101 — mandatory fix: restore LF line endings

**Finding:** `F-cb3c4b14057cb4b10bb307c16378de290042cdd156dd7f5d95b3b5e421a8d41b` (minor,
`standards_defect`, advisory rule PRJ-007).

**Contract.** `SKILL.md` must use LF line terminators on all 50 lines, matching the other 10 files
in the package, the 24 of 26 legacy `SKILL.md` files that use LF, and the Codex parent. The file's
character content must not change at all: this is a line-ending rewrite and nothing else.

**Why.** The builder's one-paragraph edit also converted the whole file from LF to CRLF — 5,479 to
5,809 bytes, every line terminator. `.gitattributes` declares `* -text` with the stated rationale
that "Retained manifests bind exact bytes," so a conversion moves the package digest for reasons
unrelated to content, and the review cost is measurable: `git diff --stat` reports 50 insertions
and 50 deletions for what `git diff --ignore-cr-at-eol --stat` shows is a 1-line change.

**Managed paths.** `SKILL.md` in **both** mirror roots. Per the ADR-073 dual-path contract the
identical bytes go to both, and `diff -rq` between them must be empty afterwards. Note that the
prior build wrote the `src/claude` copy outside its custody harness; a build executing this
revision should bring both paths inside the managed set rather than repeat that.

**Explicitly out of scope.** Every other file. The paragraph's text. The frontmatter. Any other
package.

**Acceptance cases.** All verifiable against the delivered bytes without any specification:

| ID | Case |
| --- | --- |
| AC-101 | `SKILL.md` contains 50 bare LF and 0 CRLF in both mirror roots. |
| AC-102 | The file's content with line endings normalised is byte-identical to the assessed bytes `212f99c3…` normalised the same way — i.e. no character changed. |
| AC-103 | The paragraph beginning "That separation is an obligation this workflow keeps" is present and character-identical. |
| AC-104 | `diff -rq .claude/skills/dev src/claude/skills/dev` is empty. |
| AC-105 | `git diff --stat` and `git diff --ignore-cr-at-eol --stat` report the same figures for `SKILL.md`. |
| AC-106 | All 11 files in the package share one line-ending convention. |
| AC-107 | `observe.py structure` still returns every required check PASS and 24 resolving links. |

**Expected delivered digests.** Not predicted here. A build must report the digests it actually
produced; a revalidation run recomputes them. Naming an expected hash in advance would invite a
build to be judged against a number rather than against the cases above.

## 3. RR-102 — optional enhancement: a governing contract for the Claude Code variant

**Finding:** `F-7eb942c2a0129bdb66fe75c4883354235fa7493d94da2bd298fe875f0a14a606` (minor,
`input_evidence_limitation`). Carried unchanged from the prior run's `RR-004`; the builder declined
it correctly as outside a skill edit's charter.

**Contract.** Record a governing contract for the Claude Code variant, either as a section of the
existing specification or as a sibling document citing it as parent. It should state: the host; the
two mirrored install paths; the frontmatter decisions, including the deliberate absence of
`disallowed-tools` and the reason; the LF line-ending convention that RR-101 restores; and the
derived-port provenance. Correct the stale `status: proposed` / `package_status: not_authored`
frontmatter in the same change.

**Constraints.** `docs/specs/dev-skill-spec.md` must not be relocated or duplicated — its section
1.1 forbids another authoritative copy. The Codex packages at `src/agents/skills/dev` and
`.agents/skills/dev` stay out of scope.

**Why optional.** RR-101 is verifiable against the package itself, so this is not a prerequisite.
It remains worth doing: without it, a reviewer cannot distinguish an intended host-specific
decision from drift, which is exactly how the now-resolved allowlist defect entered — in prose no
specification covered.

**This is a specification and process change, not a skill edit.** It does not belong in a
skill-builder run against the package.

## 4. Decisions required before a build

| ID | Question | Recommendation | Owner |
| --- | --- | --- | --- |
| OQ-101 | Apply RR-101 as a pure line-ending rewrite of `SKILL.md`, with a verified guarantee that no character changes? | **Yes.** The alternative — leaving the file CRLF — leaves the package internally inconsistent and every future diff noisy, for no benefit. The risk is that a careless rewrite also reflows text, which AC-102 exists to catch. | maintainer |
| OQ-102 | Should `qa/SKILL.md` (also CRLF, already committed) and the surviving allowlist claim in `qa`, `skill-builder` and `skill-validator` be opened as their own validation targets? | Out of scope here and not blocking. Recorded so the family pattern is not lost. Each needs selecting as a target; editing them under this proposal would reset validation state bound to their current bytes. Carried from the prior run's `OQ-2`. | maintainer |
| OQ-103 | Should the LF convention be written down rather than left statistically observable? | Recommended, as part of RR-102 or in `.gitattributes`. Until it is, PRJ-007 can only flag that a conversion happened, not assert a direction — see `ENF-005`. | maintainer |

## 5. What a build must not do

- Do not change the corrected paragraph's wording.
- Do not add `disallowed-tools`, change `allowed-tools`, or alter `name` or `description`.
- Do not touch the 10 other files, the Codex packages, or any other skill.
- Do not modify `docs/specs/dev-skill-spec.md` under RR-101; that is RR-102's scope and a separate
  authorization.
- Do not treat this document as authorization. It is a reviewable proposal; approval must be bound
  to this proposal's digest and to the target.
- Do not overwrite or amend any existing evidence run under `docs/plan/`. Both
  `20260918T202845Z` and `20260919T021255Z` are append-only history.

## 6. Post-build verification

A fresh validation run over the actual delivered bytes. It should classify `F-cb3c4b14…` resolved
or persistent against AC-101 through AC-107, confirm `F-7eb942c2…` unchanged unless RR-102 was also
done, and re-exercise the standards and workflow dimensions. `C-BEH-002` and `C-BEH-003` will
remain NOT_RUN for the same structural reason as in this run and the prior one; a build cannot
clear them, and a future run should not be expected to.

Because RR-101 changes no characters, the instruction and behavioural conclusions of this run —
including trial `T1-boundary` — carry forward to the revised bytes provided AC-102 holds. If AC-102
fails, they do not, and the paragraph needs a fresh cold trial.
