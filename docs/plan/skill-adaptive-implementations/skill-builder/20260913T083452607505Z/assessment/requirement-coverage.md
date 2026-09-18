# BA implementation mapping

All fourteen requirements are authored and mapped below. Static delivery PASS is distinct from complete behavioral verification. See case-coverage.md for explicit gaps.

| Requirement | Delivered responsibility | Paths | Cases |
| --- | --- | --- | --- |
| BA-001 | Authoring-only/manual handoff | SKILL.md; references/adaptation.md; unchanged authoring.py | BAT-01, BAT-12 |
| BA-002 | Bounded discovery without project execution | references/adaptation.md; scripts/adaptive.py; runtime Capture | BAT-02, BAT-03 |
| BA-003 | Evidence-grounded roles and explicit gaps | references/adaptation.md; schemas/project-evidence-v1.schema.json; proposal schema; adaptive.py | BAT-04, BAT-05 |
| BA-004 | Source/operational identity separation | references/project-binding.md; adaptive descriptor and binding schemas; runtime | BAT-06, BAT-07 |
| BA-005 | Closed schemas, exact digests/references | schemas/* new families; scripts/adaptive.py | BAT-08, BAT-09 |
| BA-006 | Sequential selected sets and dependencies | references/adaptation.md; adaptive.py; selection/result/request schemas | BAT-10, BAT-11 |
| BA-007 | Core preservation and complete lineage | references/adaptive-contracts.md; adaptive.py | BAT-05, BAT-13 |
| BA-008 | Ground expertise and project conventions | references/adaptation.md; proposal semantics | BAT-04, BAT-14 |
| BA-009 | Portable descriptors and runtime template | assets/adaptive-runtime/check_project_binding.py; descriptor schema; project-binding.md | BAT-06, BAT-07, BAT-15 |
| BA-010 | Explicit update proposals, no automatic repair | references/adaptation.md; adaptive.py review branch | BAT-13, BAT-16 |
| BA-011 | Legacy history/schema/custody meanings | unchanged scripts/authoring.py, custody.py, build_evidence.py and legacy schemas | BAT-09, BAT-11, BAT-17 |
| BA-012 | Terminal-local capabilities and honest failure | references/adaptation.md; project-binding.md; runtime | BAT-03, BAT-15 |
| BA-013 | Discriminating routing and progressive resources | SKILL.md; three routed adaptive references | BAT-12, BAT-14 |
| BA-014 | Truthful authoring states, no quality/enforcement claims | references/adaptation.md; set schemas; adaptive.py reductions | BAT-10, BAT-12, BAT-17 |
