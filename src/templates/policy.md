---
id: POL-000
type: policy
title: ""
status: draft          # draft | in-review | approved | superseded | deprecated (only approved policy binds)
version: 1
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: ""              # accountable for this policy
authors: []
generated_by:
  tool: ""
  model: ""
  session: ""
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- policy-specific ---
scope: project         # organization (vendored copy of the organization-wide policy) | project
source: null           # organization scope only: {repository: "<org policy repo>", ref: "<tag or commit>"}
---

# POL-000 — <organization or project> policy

<!-- A policy document holds organizational policy and interaction defaults as citable settings,
     following configuration contract v1 (ADR-003). v1 allows at most one approved policy
     document per scope in docs/specs/policy/. Workflows cite the settings they applied with
     upstream links, so changing a setting marks dependent documents as suspect.
     Framework requirements and document contracts are NOT settings; they can't be configured here. -->

## 1. Scope and ownership

<!-- Who owns this policy, which projects it covers, and how changes are approved. -->

## 2. Settings

<!-- Supported keys in v1:
     - quality.required_categories (organizational_policy): NFR categories that must be asked,
       in addition to the framework floor, when applies_when matches. Additive only.
     - interview.max_calls (interaction_default): integer 1–20.
     - architecture.mandated_platforms (organizational_policy): one setting per mandated platform.
     - testing.method: test-after, tdd, atdd, bdd or spike-and-stabilize.
     - testing.coverage_metric: line or branch.
     - testing.coverage_threshold: a number from 0 to 100.
     - testing.coverage_scope: a list of repository-relative folders, each ending in /; at least one.
     - testing.coverage_exclusions: a list of repository-relative paths (a folder ends in /); no globs.
     - testing.exception_approvers: a list of people, written as in owner fields; at least one.
     testing.* (organizational_policy, ADR-005): project may override only if allowed; never local.
     overridable_by lists which lower layers may override: project, local (local only for
     interaction_default). Omit a setting to inherit the framework default. -->

```yaml items
settings:
  - id: SET-01
    status: active
    key: interview.max_calls
    class: interaction_default
    value: 8
    overridable_by:
      - project
      - local
    rationale: "<why this value>"
```

## Change Log

| Version | Date | Author | Change | Settings affected |
|---|---|---|---|---|
| 1 | YYYY-MM-DD | | Initial draft | all |
