# Author handoff — claude-brainstorm source publication

Prepared 2026-09-09 by the owning authoring session, under the handoff-only override:
**author handoff prepared; no publication worktree, commit, push or PR was created, and no
Git mutation of any kind was performed.** The coordinator owns those steps.

## Assignment match

| Field | Observed | Dispatch entry `prompts/20-claude-brainstorm.md` |
| --- | --- | --- |
| Worktree | `/home/bryan/Projects/DevForge/worktrees/claude-brainstorm` | identical |
| Repository | DevForgeAI (`framework/DevForgeAI/.git`) | identical |
| Branch | `author/claude-brainstorm-mvp` | identical |
| HEAD | `a006b3d91f39776cf3ac4cd06b174d5fa3ed688c` | identical |

Exact match on all four fields, so this is the correct assignment. Origin is
`https://github.com/bankielewicz/DevForgeAI.git`; the branch has **no upstream configured**.

Exclusive source scope: `providers/claude/plugins/devforgeai/skills/devforge-brainstorm/**`

## The delta the coordinator should publish

20 files in the owned package. **16 form the delta**; 4 are already correct at HEAD.

| Action | Count | Files |
| --- | --- | --- |
| update (tracked, modified) | 4 | `SKILL.md`, `assets/handoff.md`, `evals/evals.json`, `references/recording-rules.md` |
| add (untracked, new) | 12 | `references/derivation.json`, `references/managed-runtime.md`, `evals/reference-regressions.json`, `evals/triggers/trigger-queries.json`, and 8 fixtures under `evals/fixtures/{b6,b10,b12}/` |
| none (already at HEAD) | 4 | `assets/idea-ledger.md`, `evals/fixtures/IDEAS-001.md`, `evals/fixtures/STORY-014.md`, `scripts/check_artifact.py` |
| delete | 0 | `git diff --diff-filter=D` reports no deletions |

Per-file sha256, byte counts and HEAD blob ids are in `file-identity-inventory.json`.
Nothing is staged; the index is clean.

### Not mine — do not take these from this worktree

This worktree also carries two tracked modifications the coordinator owns:

- `docs/mvp/skill-authoring-contract.md`
- `docs/mvp/templates/shared/handoff.md`

Per the dispatch README these are published once on
`publish/devforgeai-shared-foundation-20260909`, and **this copy is stale** — it lacks the
newer committed manual-mode/local-baseline sections. Do not copy it over current main.
I have left both files untouched.

## Source state

Quiescent and safe to copy. Newest owned-file mtime is **2026-09-07T15:27:13Z**, roughly two
days before this handoff; no `.lock` and no `.git/index.lock` is present; no edit is in
progress. **No ongoing edits to flag.**

The recorded bytes match what the R11 authoring session independently verified on
2026-09-07 against its frozen packet selection: all twenty pins byte-exact, including
`references/derivation.json` at `eafe53ec3e02a7a4c6eda1138916bd34ccbd256ab88e88bd836ea3d8714e3bef`.

## Checks that exist, and what they do not cover

Carried forward from the R9/R10/R11 authoring sessions. These are custody and static-source
facts; **none of them is a behavioural result.**

| Check | Result | Scope limit |
| --- | --- | --- |
| Twenty owned pins byte-exact vs frozen selection | PASS (R11, re-verified today) | custody identity, not behaviour |
| Static source review R01–R10 on the current twenty | PASS, recorded by the packet's scoped review | the packet's finding, not an author claim |
| Derivation destination digests equal actual bytes | PASS (R10 CHG-022, re-verified today) | provenance record only |
| Manifest/readback/receipt custody for R9, R10, R11 | PASS | proves which bytes existed, not that they work |
| Validation | NOT_PERFORMED | no validator campaign was authorized |
| Native C / B / A | NOT_RUN | zero native calls authorized in R9–R11 |
| Root admission, hook activation, human acceptance | NOT_RUN | root-owned |
| Authored control/checker/suite code | NOT_RUN | execution forbidden in those allocations |

**Not run here, and available to the coordinator:** the structural validator
`python3 scripts/validate_framework.py --framework <this-worktree>` from
`framework/DevForge`. I did not run it — the override narrows this invocation to handoff
preparation — so treat the selected delta as **structurally unvalidated in this session**.

Zero findings from the R9/R10/R11 reviews are closed. Source publication here is distinct
from test success, native qualification, acceptance and installation.

## Required evidence, and what I cannot release

All authoring evidence lives under `.poc/`, which is **gitignored** (`.gitignore:1`). None of
it is publishable by a plain `git add`, and it must not be bulk-added.

**Public-safe candidates** (authoring-only: no transcripts, no client state, no credential
files) — 9 runs, ~4.5 MB, the ones that actually reconstruct this candidate:
`SESSION-001-r7`, `r8`, `r9-source-exec-authoring`, `SESSION-001-r10`, `SESSION-001-r11`,
`SESSION-001-prep2`, plus `b7-fixture`, `b7-report`, `isolation-probe`.

**Excluded — sensitive.** The four 2026-09-05 native campaign runs
(`SESSION-001-run-20260905T{0152,0832,1500,1832}Z`, ~45 MB) hold **119 raw client
transcript stores** and **86 `.credentials.json` files**. Every credential file is 0 bytes —
the isolation launcher strips API keys — but they are credential-named client-state
artifacts and are excluded on principle. **Their contents were never read or copied**, and
nothing from these runs appears in this handoff.

**Review required.** `SESSION-001-prep-20260906T1506Z` has no transcripts and no credential
files but carries 14 `clientstate/` directories holding only `settings.json`, from no-model
test scaffolding. Shape-wise it is client state; content-wise it is benign. Coordinator's call.

### Two limits I cannot resolve from here

1. **Cross-repository authority evidence.** `references/derivation.json` cites 23 unique
   authority-store paths rooted at `/home/bryan/Projects/DevForge/framework/DevForge/.poc` —
   the **other** repository's ignored tree. 22 resolve and hash-match. The 23rd,
   `authoring-assignments-20260905/SESSION-001.md`, differs, and that difference is
   **expected, not drift**: derivation records `SESSION-001@10` (`0b5d5fec…`) as a historical
   locator, root issued `@11` (`bfea50f8…`) on 2026-09-07, and the issued @10 copy under
   `runtime-repairs/brainstorm-authoring-r10-.../authority/SESSION-001-r10-DRAFT.md` still
   hashes to `0b5d5fec…`. This material is outside my exclusive scope and in a different
   repository; I flag it rather than copy it.
2. **Nine project-store references become unresolvable from a public clone.**
   `derivation.json` cites nine `.poc` paths for superseded package bytes. All nine resolve
   locally, but publishing `derivation.json` without them leaves those references dangling.
   Two of the nine sit inside EXCLUDE_SENSITIVE runs — but only those two specific files are
   needed, not their surrounding runs, so they can be lifted individually.

No private off-machine backup destination is known to me. The `.poc` evidence, the
excluded transcripts and the workspace-root private material remain **local-only and
unbacked**; I am not inventing a destination.

## What the coordinator still needs to decide

- Base selection: remote main if the shared foundation is merged, otherwise
  `publish/devforgeai-shared-foundation-20260909` as base plus a linked dependency. I could
  not verify remote state — no push, fetch or authenticated remote read was performed here.
- Which public-safe evidence to copy into
  `docs/skill-authoring/history/publication-20260909/claude-brainstorm/`, with the
  old-path/new-path/hash map the README asks for.
- Whether to run the structural validator on the delta before opening the draft PR.

## Release

I release the exact bytes recorded in `file-identity-inventory.json` — the 16-file delta at
the sha256 values listed there — to the publication coordinator. The source is not moving.
Re-verify the hashes at copy time; if any differs, stop and ask, because nothing in this
session will change them.

Publication of these bytes claims no test success, no native qualification, no acceptance
and no installation readiness.
