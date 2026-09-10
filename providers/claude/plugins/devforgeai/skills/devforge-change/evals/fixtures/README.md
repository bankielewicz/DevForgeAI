# Fixtures

**Every file under this directory is synthetic.** "Tidepool" is an invented project, its
decisions are invented, `tidepool-sync` is an invented package, and no artifact, session,
report or release note here describes anything real. They exist to give an evaluation case
a concrete, reproducible input set - nothing here is a DevForgeAI record and nothing here
is evidence about anything.

Fixtures are reproducible from this source tree. `evals/` is authored source and is omitted
from installed copies and runtime exports, so a fixture path is never a runtime resource of
this skill.

| Directory | Used by | What it holds |
| --- | --- | --- |
| `shared/` | most cases | The Tidepool artifact set: architecture contract, two stories, dependency pins, an expert package record, an evaluation report, a session assignment. |
| `b2/` | B2 | A synthetic upstream release note for a major version of an approved dependency. |
| `b3/` | B3 | A defect note about wording outside governed behaviour. |
| `b6/` | B6 | A second session assignment claiming the same worktree for a different owner. |
| `b7/` | B7 | A preserved prior revision of the architecture contract, and a candidate still citing it. |
| `b8/` | B8 | A change trigger whose affected revision cannot be recovered. |
| `b9/` | B9 | An operator note describing an environment with no usable CLI or policy. |

## Reference digests inside the fixtures

The fixture artifacts cite each other with **real SHA-256 values**, written in dependency
order so that every citation resolves to bytes that actually hash to it:
`b7/ARCH-002.r2.md`, then `shared/ARCH-002.md` (whose `supersedes` cites r2), then
`STORY-031`, `STORY-033` and `XPKG-tide-sync` (which cite ARCH-002), then `EVREPORT-007`
(which cites XPKG). A skill that resolves these references and checks the digests finds them
sound — which is what most of the cases need, because an accidentally broken edge everywhere
would drown the one case that is about a broken edge.

Two deliberate exceptions, and they are the point of their cases:

- **`ARCH-002` cites `PROD-002` with `sha256: null`.** PROD-002 is not in this fixture set.
  This is a deliberately unresolvable upstream edge: a correct assessment discloses it as a
  coverage limit rather than omitting it or inventing the dependency.
- **`b7/ARCH-002.r2.md` is a preserved superseded revision.** The B7 candidate cites
  revision 2 while revision 3 is current. Both files are real and both hash correctly; the
  case is about noticing which one the candidate is built against, not about a broken hash.

## Fixture digests used by assertions

Where a case asserts that a fixture is unchanged after a run, the expected SHA-256
is recorded in that assertion in `../cases.jsonl`. Editing a fixture invalidates those
assertions and they must be recomputed; that is the intended coupling, not a defect.
