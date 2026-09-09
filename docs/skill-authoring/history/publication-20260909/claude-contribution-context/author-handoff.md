# Author source-publication handoff — Claude contribution-context

Prepared 2026-09-09 by the retained Claude contribution-context author (`SESSION-004@2`) for the
DevForgeAI publication coordinator. Dispatch entry: `prompts/21-claude-contribution-context.md`.

This invocation was narrowed to **prepare the author handoff only**. No worktree was created, no
files were staged, committed or pushed, and no PR was opened. No Git mutation of any kind was
performed. The coordinator owns those steps.

## Identity

| Fact | Value |
| --- | --- |
| Worktree | `/home/bryan/Projects/DevForge/worktrees/claude-contribution-context` |
| Repository | DevForgeAI (common Git dir `/home/bryan/Projects/DevForge/framework/DevForgeAI/.git`) |
| Origin | `https://github.com/bankielewicz/DevForgeAI.git` |
| Branch | `author/claude-contribution-context-poc` |
| HEAD | `c9298bd34ebb73bf598deec6253068d7f8b0ed59` |
| Dispatch snapshot HEAD | identical — no drift |
| Commits by this session | 0 |

HEAD is an ancestor of local main (`d29430b`). Publishing this scope therefore exposes **no new
commit history**; every commit reachable from HEAD is already reachable from the baseline the
coordinator seeds. The delta is working-tree files only.

## Assigned source scope

`project-experts/claude/devforgeai-contribution-context/**` — **78 files, all untracked, zero
deletions.** Six are runtime-distributed (`SKILL.md`, one asset, three references, one script);
72 are authored evaluation inputs, excluded from any runtime export per the skill authoring
contract. Nothing else under `project-experts/` exists in this worktree, so the fence is exact.

Per-file paths, sizes, SHA-256 digests, categories and release flags: [`source-inventory.json`](source-inventory.json).

## Excluded — coordinator-owned, left untouched

Seven working-tree items are present here but belong to `publish/devforgeai-shared-foundation-20260909`:

- `docs/mvp/skill-authoring-contract.md` (modified) — **stale**; lacks main's newer manual-mode
  and local-baseline sections. Digest `1bfe5c1c…` vs the coordinator's `37146238…`. Must not be
  published from this worktree.
- `docs/mvp/templates/shared/handoff.md` (modified) — `abc7f8e0…`, **byte-identical** to the
  coordinator's pending working copy.
- The five untracked `docs/coordination/20260905-contributor-*` documents.

I have not modified, reverted or staged any of them.

## The one dependency

`assets/handoff-template.md` (`abc7f8e0…`) is a byte-identical derived copy of the shared
`docs/mvp/templates/shared/handoff.md`, recorded in `references/derivation.json`. That governing
revision is **pending, not committed**: main holds `0b7056c6…`, while the coordinator's working
tree holds the matching `abc7f8e0…`.

So this package should be based on remote `main` only once the shared foundation is merged;
otherwise base it on `publish/devforgeai-shared-foundation-20260909` and link that dependency.
Publishing the package against a base lacking the pending handoff change leaves its derivation
record citing a governing revision that is not publicly resolvable.

**Remote state observed 2026-09-09T13:20Z:** `git ls-remote --heads origin` exits 0 and
advertises **zero refs**. Remote main is not seeded and the shared branch does not exist yet.
Per the prompt's step 2 that is the single dependency to report; I did not invent a substitute
contract.

Do not "fix" `derivation.json`'s `preserved_locator` to point at a durable path. That would
change frozen candidate bytes and invalidate the review below. The mapping is recorded here instead.

## Existing checks and evidence

Reusable exact-byte evidence exists and covers **exactly these 78 files**:

- **r2 integration review**, 2026-09-06 —
  `/home/bryan/Projects/DevForge/framework/DevForge/.poc/integration-reviews/claude-contributor-context-r2-20260906T023244923666Z/INTEGRATION-REVIEW.md`
  `9e39e88250dc40f9bbfb675d2808eafa59f5aa05d3bbcb322f8b81d9d9c12666`.
  Its frozen `run/inventories/source-manifest.json`
  (`7c1b3d896607bd73446900c0f080ac83888d48c79ed67bb88881da730548794e`) records package revision 2,
  base `c9298bd`, `file_count: 78`. I re-verified all 78 digests against current disk bytes today:
  **78 match, 0 drift, 0 missing.** Verdict: all six findings CCTX-IR-001…006 **CLOSED**; nine
  author checks PASS; custody preserved.
- **Independent helper reproduction** (within that review) — 19/19 predeclared outcomes observed.
- **Dispatch inventory cross-check** — all 85 working files recorded in the coordinator's
  `inventory.json` match current bytes: **0 drift**.

Full absolute paths and freshly computed 64-character digests for every evidence record are in the
`evidence` array of [`source-inventory.json`](source-inventory.json); those digests were computed
from the files today, not copied from their own receipts.

Preparation-stage context, **not** exact-byte evidence for these 78 files: the authoring store's
`/home/bryan/Projects/DevForge/framework/DevForge/.poc/contributor-context-authoring-20260905/CHECKS.json`
(2026-09-05T20:22Z) records all PASS with `models_launched: 0`, but its `candidate_state` is
`ABSENT` — it predates this candidate and certifies nothing about it.

Three nonblocking notes (CCTX-R2-N01 finding-category counts, N02 an inherited wrong prose
locator, N03 absence-of-token wording) are recorded as **annotations, deliberately not repaired**.
Repairing them would create a new candidate identity and invalidate this review.

### Limitations — publication is not qualification

- Evaluation status **NOT_RUN**: 0 model calls, 0 cases, 0 trigger queries, 0 arms executed.
- Behavioral status **NOT_EVALUATED**; native C/B/A, installation and acceptance all NOT_RUN.
- The r2 review scope is **static and structural**. A digest proves byte identity only.
- No repository test suite applies to this documentation/skill-source delta; I ran no new checks
  beyond the read-only digest verification above, per the "handoff only" narrowing.

## Public suitability

Scanned all 78 files for home paths, credentials, tokens, keys and client state: **no matches**.
No `/home/bryan` occurrences — `derivation.json`'s promise to keep the operator's home directory
out of a runtime resource holds. All files are text; no binaries. Fixtures are synthetic, use
session IDs in a fictional 9xx range and a fictional `/srv/devforgeai-fixture/` root.

`evals/withheld/ccx-06-DECISION-950.md` is **safe to publish**. Its held-out property is enforced
by each case's `files` array in `evals.json`, not by filesystem secrecy; it is synthetic and
documented in `evals/README.md`.

## Evidence I cannot make public

The authority store
`/home/bryan/Projects/DevForge/framework/DevForge/.poc/contributor-context-authoring-20260905/`
is readable locally and I verified its preserved input
`inputs/framework/docs/mvp/templates/shared/handoff.md` still hashes to
`abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206`, agreeing with both the package
copy and the coordinator's pending copy.

It lives under the `.poc` directory of the companion **DevForge** repository (that is
`framework/DevForge`, not this `framework/DevForgeAI` repository) and is **not publicly
resolvable**. It is out of my ownership and out of scope for this PR, and `.poc` must not be bulk
-added. `derivation.json` cites it by relative locator only, deliberately omitting the
operator-held absolute root. **This remains an unbacked private-evidence gap**; I have not
invented an off-machine destination and did not delete or move any original.

## Ongoing edits

**None. This is not a moving candidate.** Newest mtime in the owned scope is 2026-09-05 22:03
EDT; nothing has been touched in over 72 hours, and all 78 digests match both the r2 reviewed
manifest and today's dispatch inventory.

The only change this session makes to the worktree is adding this directory
(`docs/skill-authoring/history/publication-20260909/claude-contribution-context/`) with this file
and `source-inventory.json`. The worktree therefore goes from 85 to 87 untracked/modified paths.
Read that as the handoff, not as candidate drift.

## Release

**I release the exact recorded bytes of all 78 files under
`project-experts/claude/devforgeai-contribution-context/**` to the publication coordinator**, as
identified by the SHA-256 digests in `source-inventory.json`.

Conditions: publish on a base that contains the pending shared handoff change; exclude the seven
coordinator-owned paths; carry the package bytes unchanged; and describe the result as source
preservation, not evaluation, qualification or acceptance.
