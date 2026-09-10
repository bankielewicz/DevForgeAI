# Fixtures for devforge-define-product evaluation

**Every file in this tree is synthetic and operator-owned.** The project ("Riverbend Running Club"), its people, its ideas, its numbers and its decisions were invented for these cases. None of it is a real project decision, a real user, a real measurement or a real source. Do not cite anything here as evidence about anything outside these evaluations.

Fixtures are reproducible from this directory. They are authoring inputs, not runtime resources: `evals/` is excluded from installed copies and plugin exports.

| Directory | What it stages | Used by |
| --- | --- | --- |
| `new-product/` | `IDEAS-001` at revision 2 - four ideas, one adopted decision, open questions with consequences. | DP-B-001, DP-B-002, DP-B-003, DP-B-004 |
| `existing-product/` | `PROD-001` at revision 2 (accepted) and `CHANGE-011` (a scoped amendment). | DP-B-005, DP-B-010 |
| `stale/` | `PROD-002` citing `IDEAS-002@1`; `IDEAS-002` now on disk at revision 2. | DP-B-007 |
| `stale/preserved/` | `IDEAS-002.r1.md` - the exact bytes `PROD-002` cites. Staged **only** in the "preserved bytes available" variant; withheld in the "unavailable" variant. | DP-B-007 |
| `ownership/` | `SESSION-088`, an assignment naming a different writer, plus the contested brief that must not change. | DP-B-006 |
| `placeholder/` | `PROD-005`, a draft whose required fields still hold `{{template}}` placeholders. | DP-B-008 |

## Digests of the fixtures other fixtures or cases refer to

These are recorded here so a run can verify the staging it actually used. They are hashes of the exact bytes in this directory, and the same values appear in the places named in the last column. This file does not carry its own digest.

| File | SHA-256 | Also recorded in |
| --- | --- | --- |
| `stale/preserved/IDEAS-002.r1.md` | `03b523dea859ed3442d833eed9653ec6bc57cf995a14716d478e0a64959b0098` | `PROD-002`'s `upstream` entry; `IDEAS-002`'s `supersedes` entry; `cases.jsonl` DP-B-007 |
| `stale/IDEAS-002.md` | `300f1c7872ce1f8121f2554e4a3daf0b60754f3ee3e79bea24db20c8778c4e1d` | `cases.jsonl` DP-B-007; quoted in `evals.json` DP-B-007's expected output |
| `ownership/contested/PROD-004.md` | `6d25b414245faad27a66242072cfe408578fa2da6f0469318f8326aa513d8ea5` | `cases.jsonl` DP-B-006, as the declared sentinel |

The other fixtures carry no cross-reference; their digests live in the authoring evidence's `file-manifest.json`, outside this package.

## Staging note

A fixture manifest for a run must distinguish two lists that are not the same: the **source inventory** (everything in this directory) and the **worker-visible set** (what was actually staged into the disposable consuming project for that case). `stale/preserved/IDEAS-002.r1.md` exists in the inventory for both variants of DP-B-007 and is staged for only one of them. A file appearing in a source inventory is not evidence that any worker consumed it.
