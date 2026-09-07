
## Worktree environment enhancement — 2026-09-07

This amendment records the user's requested alternative testing environment and supersedes only conflicting environment-setup statements above. The original design remains preserved in history/skill-validator-worktree-2026-09-07/design-before.md. This is an ordinary enhancement, not a disposition of findings from the historical skill-builder evaluation.

### Purpose, scope and results (sections 1–3)

Keep skill-validator's identity, activation and evaluate-and-hand-off role. When no test environment exists, offer **Create Git worktrees for validation**, **Use an existing validation environment**, and **Continue with static review only**. A selected creation option directs the validator to provision and prepare alternative local test workspaces; it must not merely recommend that the user find an environment.

“GitHub worktree” is interpreted as a local Git worktree of the chosen repository. Repository hosting adds no requirement. No worktree is created by this authoring task.

Inputs for future setup: explicit environment selection, consuming repository and resolved base commit, bounded workspace/common-directory write assignment, independent attempt paths, frozen skill/baseline bytes, runtime/auth arrangement and test budget. Infer routine values from the assignment; ask only for unresolved consequential inputs. An earlier “no existing environment” answer does not select static-only.

Deliverables during validation: the frozen plan's environment allocation; a separate environment-setup.json observation record; prepared workspaces when selected and available; per-run setup evidence references; verification results and handoff that distinguish workspace preparation from native observations. A setup failure preserves partial work and exact missing prerequisites.

### Accepted requirements and existing workflow (sections 4–5)

| ID | Requirement | Existing task / classification |
| --- | --- | --- |
| SV-WT-01 | Offer the alternative after “no environment”; reuse explicit selection and never infer it from silence. | T01 / Enforced |
| SV-WT-02 | Freeze repository/common-directory, commit, write scope and separate attempt/arm allocations. | T02 / Enforced |
| SV-WT-03 | Carry out selected bounded creation and continue runtime preparation; existing/static-only choices create no worktrees. | T05 / Enforced |
| SV-WT-04 | Keep original checkout and exact candidate/baseline bytes; preserve dirty candidates through snapshots rather than commits or stashes. | T02/T05 / Enforced |
| SV-WT-05 | Keep preparation and observed readiness distinct; continue C/B/A only with their actual prerequisites. | T05–T08 / Enforced |
| SV-WT-06 | Retain setup evidence, paths, unavailable observations and continuation in results/handoff. | T10–T12 / Enforced |

The user already explicitly enforced the workflow, all six phases and every named task. Worktree generation is a selected branch inside those tasks, not a new phase/task classification. Existing H1/H2 proposals cover frozen setup choice/allocation and native readiness; missing or stale assignment, preparation or boundary evidence prevents dependent admission. External runtime/operator owns mechanical admission and transitions. No extra model completion marker or phase command is introduced.

Git setup permits only assigned new destinations plus necessary shared administrative writes. Detached checkout at the observed base is the routine default. Preserve concurrent work, prior attempts, source-only expectations and independent client history. No automatic cleanup, force reuse, branch resets, remote changes or credential copying.

### Resources and proposed enforcement (section 6)

New runtime reference: references/worktree-environment.md, with selection, concrete Git add/list command shapes, preparation, failure handling and continuation.
New template: assets/environment-setup.json, a local observation record rather than a registered admission schema.
Updated resources: SKILL.md, references/native-evaluation.md, references/enforcement-design.md, assets/validation-plan.json, assets/run-manifest.json, references/sources.md and references/derivation.json.

Git command semantics use the official Git worktree manual consulted 2026-09-07. Native support is determined by the selected actual runtime and observed boundary. This focused enhancement retains the validator's selected shared contract revisions; it does not migrate the legacy hook proposals or supply a generic native supervisor. H1/H2 feasibility remains Partial. Hook status: Design only; not installed, activated, executed, or validated.

### Future examples (section 7)

Source-only SV-018–SV-023 cover offering creation, performing selected setup, honoring existing/static-only choices, collision/unavailable Git, created workspaces with missing authentication/containment, and an uncommitted candidate distinct from the project base. Existing SV-001–SV-017 remain. All cases are authored, not executed.

### Placement, selection and provenance (sections 8–10)

Enhance the named canonical Codex skill; it already owns environment intake and native evaluation. The exposed skill catalog and selected builder/validator sources establish this ownership; no new skill or global uniqueness claim is needed. skill-builder authors; skill-validator evaluates.

Canonical path: providers/codex/plugins/devforgeai/skills/skill-validator in this framework. Generated project path: /home/bryan/Projects/DevForge/.agents/skills/skill-validator. Root performs the scoped generation from canonical bytes with collision preservation; evals remain source-only. Shared integration, companion DevForge, other skills/providers and historical evaluation reports are outside the change.

The selected current builder design/handoff templates and prior source/design/runtime bytes are retained under history/skill-validator-worktree-2026-09-07. The accompanying source-before/source-after manifests and authoring-record.json record actual identities. No commit, assignment ID or runtime receipt is invented. The selected validator contract pins remain unchanged.

### Intake and authoring disposition (sections 11–12)

CHG-WT-01: applied user-authorized enhancement; requirements SV-WT-01–06; no finding ID.
This request does not authorize rerunning the old skill-builder campaign or changing its results.
The complete candidate manifest is source-after-manifest.json in this amendment's history directory. This specification never contains its own digest; its saved identity is recorded externally after authoring.

Prepared continuation: skill-validator-worktree-handoff.md in docs/skill-authoring. Next workflow owner is skill-validator under a separate allocated evaluation; no receiving invocation occurs here. Native runtime, authentication, test budget and isolated environment are prerequisites of that later run, not authoring prerequisites.

Validation status: Not performed. Behavioral status: NOT_EVALUATED. Hook status: Design only.
