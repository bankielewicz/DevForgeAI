# Fixtures for devforge-define-product evaluation

**Every file in this tree is synthetic and operator-owned.** The projects ("Riverbend Running Club", "Northgate Tool Library", "Harbourside Allotments", "Kestrel Book Group"), their people, their ideas, their numbers and their decisions were invented for these cases. None of it is a real project decision, a real user, a real measurement or a real source. Do not cite anything here as evidence about anything outside these evaluations.

Fixtures are reproducible from this directory. They are authoring inputs, not runtime resources: `evals/` is excluded from installed copies and plugin exports.

| Directory | What it stages | Used by |
| --- | --- | --- |
| `new-product/` | `IDEAS-001` at revision 2 - four ideas, one adopted decision, open questions with consequences. | DP-B-001, DP-B-002, DP-B-003, DP-B-004, DP-B-009 |
| `new-product/preserved/` | `IDEAS-001.r1.md` - the exact bytes revision 2 supersedes. | staged with revision 2 so its `supersedes` reference resolves |
| `existing-product/` | `PROD-001` at revision 2 (accepted) and `CHANGE-011` (a scoped amendment). | DP-B-005, DP-B-010 |
| `existing-product/preserved/` | `PROD-001.r1.md` - the exact bytes revision 2 supersedes. | staged with revision 2 so its `supersedes` reference resolves |
| `stale/` | `PROD-002` citing `IDEAS-002@1`; `IDEAS-002` now on disk at revision 2. | DP-B-007 |
| `stale/preserved/` | `IDEAS-002.r1.md` - the exact bytes `PROD-002` cites. Staged **only** in the "preserved bytes available" variant; withheld in the "unavailable" variant. | DP-B-007 |
| `ownership/` | `SESSION-088`, an assignment naming a different writer, plus the contested brief that must not change. | DP-B-006 |
| `placeholder/` | `PROD-005`, a draft whose required fields still hold `{{template}}` placeholders. | DP-B-008 |

## Every digest in these fixtures is real

No fixture carries filler in an `upstream` or `supersedes` digest. Each value below is the SHA-256 of the exact bytes at the named path in this directory, and each reference resolves when the case's staging list places the referenced file in the consuming project. This is deliberate: the skill instructs a worker to read the bytes at each recorded path and hash them, and it forbids "a digest with no reachable bytes behind it". A fixture that modelled the forbidden shape, unlabelled, would make a correct worker emit a staleness report that no case anticipated.

| File | SHA-256 | Referenced by |
| --- | --- | --- |
| `new-product/preserved/IDEAS-001.r1.md` | `4dbe2259ecd3378c6993b2b088bfb9771db3d13bfd9a5532f8e2709637e971ac` | `new-product/IDEAS-001.md` `supersedes`; `existing-product/preserved/PROD-001.r1.md` `upstream` |
| `new-product/IDEAS-001.md` | `8a0b193eb62be9cb2d07ae22658895c9fdf23fbdca4d5be86422addbba2e6ec0` | `existing-product/PROD-001.md` `upstream` |
| `existing-product/preserved/PROD-001.r1.md` | `f6c8f64fef8ffdf259df50bcd6618fdc4fd66c3627baaff382351d9ba687666c` | `existing-product/PROD-001.md` `supersedes` |
| `existing-product/PROD-001.md` | `f7396e407445c4f401e494cca71916464a342ce5895d1c2830f13fc847987179` | `existing-product/CHANGE-011.md` `upstream` |
| `stale/preserved/IDEAS-002.r1.md` | `03b523dea859ed3442d833eed9653ec6bc57cf995a14716d478e0a64959b0098` | `stale/PROD-002.md` `upstream`; `stale/IDEAS-002.md` `supersedes`; `cases.jsonl` DP-B-007 sentinel |
| `stale/IDEAS-002.md` | `569d1dd38129b0745f77a07005d48241559efcfe130875b356f01c85185cdcc8` | `cases.jsonl` DP-B-007 sentinel; quoted in `evals.json` DP-B-007's expected output |
| `ownership/contested/PROD-004.md` | `6d25b414245faad27a66242072cfe408578fa2da6f0469318f8326aa513d8ea5` | `cases.jsonl` DP-B-006, as the declared sentinel |

The one reference that is **deliberately unresolvable at its recorded path** is `stale/PROD-002.md`'s `upstream`: it cites `IDEAS-002` revision 1 at the ledger's live path, and the bytes now at that path are revision 2. That mismatch is DP-B-007's whole subject. The revision-1 bytes still exist, at `stale/preserved/`, and whether they are reachable in-project is exactly what the case's two staging variants differ on.

Digests of the remaining fixtures - `stale/PROD-002.md`, `ownership/SESSION-088.md`, `placeholder/PROD-005.md` and this README - live in the authoring evidence's `file-manifest.json`, outside this package. This file does not carry its own digest.

## Staging note

A fixture manifest for a run must distinguish two lists that are not the same: the **source inventory** (everything in this directory, and everything a case's `files[]` array names) and the **worker-visible set** (what was actually staged into the disposable consuming project for that case). `evals.json` `fixture_staging` is the authority for worker visibility; `cases.jsonl` `files[]` is source inventory only, and two entries are deliberately never staged for the worker - `stale/preserved/IDEAS-002.r1.md` in DP-B-007's unavailable variant, and `existing-product/PROD-001.md` in DP-B-008, where it is the grader-only positive control. A file appearing in a source inventory is not evidence that any worker consumed it.
