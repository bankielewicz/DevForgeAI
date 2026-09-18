# Discovery workflow documentation review

This is the authoring session's factual, requirement and consistency review, not independent skill validation, product QA or framework acceptance. The selected task is documentation only. User-selected naming is brainstorm -> prd-create -> prd-review; saved project and operational package bytes outside the selected framework documents are not implementation targets.

## Scope and evidence

- Workspace: `C:\Projects\DevForgeAI`; native PowerShell 7.6.6 and Python 3.10.11 were used for the recorded documentation observations. Use the actual version fields in the execution receipts if host versions change later.
- The [before manifest](inputs-before.json) binds 35 inputs. Nine selected existing documents have byte-preserving before snapshots under `before/`; the other 26 bound inputs are checked for unchanged bytes.
- [Phase 1](../../../specs/framework/workflows/phase-1-brainstorm-spec.md) is the only new framework specification. Nine existing capability/index/decision documents are revised. No numbered phase 0 or phase 1 occurred in the pre-edit framework Markdown, as checked against retained before content and unchanged inputs.
- [Final documentation observations](verification.json) cover local links/heading anchors, metadata/table structure, requirement/case inventory, selected naming and bounded preservation. [Changed-file manifest](changed-file-manifest.json) gives before/after identities.
- Check 001 passed structural/documentation observations. Its output, execution receipt and report copies remain retained. Subsequent review made the user quote exact, explicitly classified unavailable essential sources, and clarified destination containment/readback and the associated negative case. Check 002 applies to the final documents. The first failed multi-file patch matched a nonexistent heading and wrote no changes; its corrected application used the actual heading context.

## Discussion-to-document map

| Discussed idea | Canonical disposition and reviewed locator |
| --- | --- |
| Phase 0 versus phase 1 | DFF-02, Discovery route and workflow names; DFF-WF-01 section 1. No mandatory setup phase 0 is invented. |
| Preferred workflow names | DFF-02 route; DFF-WF-01 provenance/section 8; DEC-22. User selected PRD names, not spec-create/spec-review. |
| Setup, work and discovery intake | DFF-02, Intake and entry selection; DFF-11, Setup intake. One conversation can reuse answers while preserving effect ownership. |
| Greenfield and brownfield entry | DFF-02 route; BR-004/005; BV-01/02/03. Project age does not force a route or an installation. |
| Interview, alternatives and source-grounded decisions | BR-006/007/008 and BV-05/06/07/09. Missing answers do not become approval. |
| PRD/architecture/prototype iteration | DFF-02 route, DFF-04 architecture/provenance section, BR-009 and BV-10/11. Evidence motivates selected revision rather than silently changing requirements. |
| Constitution documents | DFF-04, Architecture, document ownership and provenance; BR-002/006. Useful/user-selected names are allowed; no mandatory pack is imposed. |
| Provenance through derived artifacts | DFF-04 canonical ownership; DFF-03 clause ownership; BR-006/011/013. Claims, user decisions and experiments have distinct origins. |
| Story readiness and AI probability | DFF-03, Readiness, parallel work and sprint grouping; DEC-25. Named blockers cannot be waived by a rubric; a calibrated probability remains unspecified. |
| Epics, dependencies and sprint grouping | DFF-03 decomposition and sprint paragraphs. Six query groups remain illustrations; no story set or execution order is selected here. |
| Parallel agents/worktrees | DFF-03 shared-contract/resource ownership; DFF-11 root/binding compatibility; AMB-20. A ready producer story and separate filenames do not supply an implementation dependency. |
| Planned versus actual worktree facts | DFF-03 references the current story contract. `worktree_path` remains null until an actual delivery fact exists. |
| Setup bootstrap and binding writer | DFF-11 setup sections; AMB-13/20/21. Existing project-binding-v1 fields remain canonical, operations unimplemented and deterministic framework ownership Rust. |
| Core versus standalone packaging | DFF-05 packaging; BR-001/002; DEC-24. The first brainstorm skill is specified standalone without mutating adaptive schemas or current dev/story-create. |
| Anti-gaming and existing QA policy | DFF-08 independent oracles and existing-policy paragraphs; MIG-01/02. No mock-decorator or threshold rule is weakened or exported silently to other products. |
| Combined candidate, UI evidence and delivery | DFF-08 added integration section. Clicks alone do not prove persistence; branch passes do not prove combined behavior; QA PASS does not create merge rights. |
| Lessons during work and later ideas | DFF-09 feedback section and BR-010/BV-20. Route the evidenced issue to its owner; proposed product work remains unselected. |
| First skill's implementable boundary | BR-001..014 cover activation, inputs, behavior, output, failures and handoff. BV-01..20 map all requirements; those are future cases, not executed outcomes. |

## Conclusions and limits

The specification is ready as a bounded input for separately selected skill authoring. Full PRD creation/review specifications, installed skills, operational activation, automated routing, multi-worktree binding, protected delivery and native qualification are not established. AMB-04 is narrowed for the discovery handoff only; AMB-12/13 and MIG-01/02/03 remain open, with new AMB-20/21 recording concrete compatibility/bootstrap questions.

No runtime tests or coverage were needed for these prose changes. Future skill builds retain their bound Python evaluation requirements and applicable 95% floors; none of those future cases are claimed as executed by this review. External URLs were not fetched: their existing upstream claims were not the subject of this documentation change. Preservation observations cover the declared inputs, not an invented repository-wide audit.
