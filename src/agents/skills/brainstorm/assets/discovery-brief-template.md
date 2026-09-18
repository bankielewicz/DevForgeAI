---
format_version: brainstorm-brief-v1
brief_id: "{{safe-local-brief-id}}"
revision: {{positive-integer}}
updated_at_utc: "{{RFC3339-UTC-timestamp}}"
disposition: {{READY_FOR_PRD-or-NEEDS_INPUT-or-REUSE_EXISTING}}
supersedes: {{null-or-quoted-project-relative-previous-brief-path}}
---

# Discovery brief: {{selected topic}}

## Selected work and context

{{Attribute the selected request and decision source. State selected project/root when known, audience, greenfield/brownfield facts, persistence mode and permitted effects.}}

{{Source inventory: for inspected local sources, record ID, project-relative path, heading/stable locator and raw-byte SHA256. For external sources, record ID, actual URL, accessed date and supporting locator. Identify unavailable/uninspected sources honestly, including essentiality and affected claims. Attribute conversation inputs separately. State none when no documents were selected.}}

## Problem and outcomes

{{State the problem, relevant current behavior, intended users and desired observable outcomes with provenance. Separate supported quantitative targets from explicitly proposed targets; keep unknowns visible.}}

## Scope and exclusions

{{Distinguish selected and proposed MVP outcomes, exclusions and later ideas. Preserve the user's selected objective. Explicitly state empty applicable lists.}}

## Options and direction

{{Describe meaningful alternatives and benefits, costs, dependencies and uncertainty, including retaining current behavior when useful. Name the selected direction and actual decision origin; otherwise retain the unresolved choice. If no comparison is needed, explain why.}}

## Constraints and architecture questions

{{Reference governing requirements and established decisions. State relevant integration, quality and operational constraints; state ownership, interfaces, trust boundaries and deployment questions where they affect feasibility/scope. Give reasons for inapplicable categories and identify feasibility assumptions and decisions for later design.}}

## Evidence and experiments

{{Connect material claims to inventory sources and locators. Distinguish observations, hypotheses, proposed experiments, inspected results and unavailable evidence. State what an experimental result establishes and its limits; record proposed revisions without changing canonical policy. State “none selected” when no experiments are selected.}}

## Decisions and open questions

| Local ID | Decision or question | Origin or owner | Affected outcome | Blocking stage(s) or none |
| --- | --- | --- | --- | --- |
| {{ID}} | {{actual decision or unresolved question}} | {{actual decision source or question owner; unknown owner is a gap}} | {{outcome}} | {{discovery, PRD creation, PRD review, implementation, or none}} |

{{State explicitly when no open questions remain. Keep disputed choices, essential missing sources and unknown owners visible.}}

## Handoff

{{State the disposition and exact reason, next responsibility, reused artifact paths or none, open decisions transferred to that consumer and a plain-English suggested next request. Readiness for PRD does not establish implementation readiness or invoke that workflow.}}

## Follow-up and change notes

{{Record observed friction/product suggestions, evidence, proposed owners and selection state, or explicitly none. On resume identify changed/unavailable inputs, revised decisions, unchanged supported observations, the superseded revision and any explicitly superseded objective. For a first revision state that no prior brief is superseded.}}
