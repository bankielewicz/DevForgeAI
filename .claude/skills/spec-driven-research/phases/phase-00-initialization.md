# Phase 00: Initialization

Phase 00 is defined **inline** in SKILL.md (Steps 0.1-0.8).

This file exists as a placeholder for consistency with the phase file naming convention. The initialization phase runs inline because it creates the state that all other phases depend on.

**See:** `SKILL.md` > "Phase 00: Initialization [INLINE - Bootstraps State]"

---

## Why Inline?

Phase 00 must execute before the Phase Orchestration Loop begins. It:
1. Parses arguments to determine mode (new, resume, search, list)
2. Handles search/list mode early exits (no Phase 01-06 needed)
3. Generates the RESEARCH-ID used by all subsequent phases
4. Creates the checkpoint JSON that gates all phase transitions
5. Initializes CLI state tracking

Loading a separate file for this phase would add unnecessary indirection before the orchestration loop is established.
