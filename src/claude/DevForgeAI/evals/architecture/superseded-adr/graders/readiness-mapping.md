---
type: llm
---

Context: the fixture PRD has three requirements, FR-001, FR-002 and NFR-001. In the amended ARCH, DEC-01 (which identity provider; it cites only FR-001) is open again because its resolver ADR-002 was superseded, and DEC-02 (session revocation; it cites FR-001 and NFR-001) stays resolved by the accepted ADR-001. An amendment may add new questions, numbered DEC-03 or higher.

PASS only if every one of these holds in the reply:
1. It gives a status (ready or blocked) for each of FR-001, FR-002 and NFR-001.
2. FR-001 is blocked, with DEC-01 among its blockers.
3. FR-002 and NFR-001 are each reported ready, or blocked only by a new question numbered DEC-03 or higher that the reply says cites that requirement.
4. No requirement other than FR-001 is said to be blocked by DEC-01, and no requirement is said to be blocked by DEC-02.
5. No summary sentence contradicts the per-requirement statuses, for example "nothing is ready" while FR-002 or NFR-001 is reported ready, or the reverse.

FAIL if any of these fails, including when a requirement is left out.
