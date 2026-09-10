# Fixtures for devforge-design evaluation

**Every file in this directory is synthetic and operator-authored.** None of it describes a real project, a real user, a real decision, or a real approval. "Havenlist" is an invented neighbourhood tool-lending library that exists only here. The requirement IDs, session records, digests and approvals are fabricated for evaluation and must never be copied into a real project or cited as a precedent.

Fixtures are reproducible from this source directory. They are inputs to authored evaluation cases; they are not runtime resources and are excluded from installed copies and plugin exports.

| Path | Role in the cases |
| --- | --- |
| `shared/PROD-001.md` | A product-brief with stable requirement IDs. The upstream for the direct and indirect activation cases. |
| `shared/ARCH-001.md` | An architecture-contract declaring an approved UI stack and conventions. The scope-preservation case. |
| `backend-only/STORY-021.md` | An accepted story with no user-facing surface. The out-of-scope case. |
| `ownership-collision/SESSION-042.md` | An assignment record naming a different owner as the writer for the design directory. |
| `ownership-collision/sentinel/UX-004.md` | The other owner's in-progress design-spec. Its bytes must be unchanged after the run. |
| `stale/PROD-001.md` | The live product-brief, now at revision 3. |
| `stale/preserved/PROD-001.r2.md` | Revision 2's preserved bytes, still reachable. |
| `stale/UX-005.md` | A design-spec citing `PROD-001@2`, which no longer matches the live file. |
| `placeholder/UX-006.md` | A design-spec still holding `{{...}}` in required fields. |
| `blocked-check/UX-007.md` | A finished-looking design-spec, used when a requested external check has no implementation. |
| `unverified-inspection/UX-008.md` | A design-spec whose mockup row asserts a visual inspection with no evidence behind it. |
| `unverified-inspection/inspection-claim.json` | The same asserted outcome in field form - claim, tool, viewport, evidence - so a deterministic grader can address the claim and its evidence separately. |

Digests quoted inside a fixture are fabricated placeholders unless a case declares otherwise. Where a case asserts a real sha256 - the ownership sentinel - that value is computed from these exact bytes and is recorded in `evals/cases.jsonl`; editing the fixture invalidates the case until the case is updated with it.
