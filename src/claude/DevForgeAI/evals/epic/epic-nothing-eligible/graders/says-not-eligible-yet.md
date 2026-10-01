---
type: llm
---

The workspace held PRD-001 and ARCH-001. ARCH-001 has an open question, DEC-08 (which hosting
provider runs the web app and the shift service), that cites FR-002, FR-003, FR-004, FR-012 and
NFR-001: every requirement that would otherwise be eligible for an epic. Every other requirement is
left out for its own reason. So no requirement is eligible for an epic yet, and no epic exists.

Judge only the final reply.
PASS if all of these hold:
- It says no epic was written because no requirement is eligible (or ready) for an epic yet, and
  names the open question DEC-08 as what blocks FR-002, FR-003, FR-004, FR-012 and NFR-001.
- It doesn't say that no requirement needs a new epic, or that everything is already covered.
- Its next step is to resolve the architecture question with /devforgeai:architecture PRD-001; it
  names no story step.
FAIL if any of these is missing, if it writes or proposes an epic, or if it tells the user to write
stories or run /devforgeai:story.
