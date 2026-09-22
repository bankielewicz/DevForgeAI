---
id: SPR-000
type: sprint
title: ""              # e.g. "Sprint 4 — Passwordless MVP"
status: planned        # planned | active | closed
version: 1
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: ""
authors: []
generated_by:
  tool: ""
  model: ""
  session: ""
reviewed_by: []
approved_by: ""
approved_on: null
upstream:              # sprints derive no requirements; only informed_by links (what the goal contributes to)
  - {id: EPIC-000, item: DW-01, relation: informed_by, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- sprint-specific ---
start: YYYY-MM-DD
end: YYYY-MM-DD
capacity: null
capacity_unit: points  # points | person-days
stories: []            # the ONLY record of sprint membership, e.g. [STORY-012, STORY-013]
stretch: []            # candidate stories, not committed
---

# SPR-000 — <sprint name>

<!-- A sprint is a scheduling artifact. It adds no requirements and no acceptance
     criteria. Story AC and the Definition of Done define "done".
     If new scope appears mid-sprint, write or change a story; do not describe it here. -->

## 1. Sprint goal

<!-- One sentence: the outcome this sprint commits to. -->

## 2. Committed stories

<!-- GENERATED from `stories:` plus each story's frontmatter: story, title, epic,
     estimate, owner, status, and the capacity check (committed vs capacity).
     Do not edit by hand. -->

## 3. Entry checks (Definition of Ready)

- [ ] Every committed story is `ready`, with no `[NEEDS CLARIFICATION]` markers and empty `blocked_by`
- [ ] Every committed story has AC items and a separate or embedded spec
- [ ] Dependencies outside the team are confirmed

## 4. Risks and dependencies

<!-- Prose: risk, impact, owner, mitigation. -->

## 5. Scope changes during sprint

<!-- Log every add or remove, and keep `stories:` in frontmatter in sync. -->

```yaml items
scope_changes:
  - date: YYYY-MM-DD
    change: added             # added | removed
    story: STORY-000
    reason: "<why>"
    approved_by: "<name>"
```

## 6. Review (fill at close)

```yaml items
review:
  - story: STORY-000
    outcome: done             # done | carried-over | dropped
    evidence: "<test run or demo link>"
```

**Sprint goal met?** yes / partially / no — <explanation>

## 7. Retrospective (fill at close)

- What went well:
- What didn't:
- Actions (owner, due):

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | YYYY-MM-DD | | Planned |
