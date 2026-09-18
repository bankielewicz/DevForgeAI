---
id: SBP-REVISION-20260914T2131571597777Z
skill_name: skill-builder
target: codex
status: proposed
---

# Complete proposed skill-builder revision contract

## Identity and review boundary

Target: `C:/Projects/DevForgeAI/src/agents/skills/skill-builder`.
Assessed package digest: `ecb01ece2c38443e58fe7a5b307e9d0de22a1fa9b9ec1f726b79cfa328cb9c9e`.
The exact original package is [source](source/SKILL.md), bound by [source-manifest.json](source-manifest.json).
The governing post-MVP contract is retained byte-for-byte at [inputs/skill-builder-postmvp-spec.md](inputs/skill-builder-postmvp-spec.md).
This proposal authorizes no edits, installations, adoption or evaluation retries. It proposes one mandatory custody correction, retaining all other selected behavior.

## Purpose, activation and exclusions

Create and edit portable Codex development skills from conversational requirements or selected Markdown, convert selected Claude skills without executing imported instructions, record explicitly requested custody adoption, propose project-specific skills, author exact selected adaptive sets, and review variant updates. Validation/testing, standalone specification writing, installation, deployment, operational skills, hooks, CI and Rust implementation remain separate responsibilities.

Positive triggers include creating a reusable transformation skill, editing an existing skill, importing a Claude skill, reviewing a changed variant, or authoring explicitly selected members. Requests merely to validate, install, run product tests or write a standalone specification do not activate authoring.

## Inputs and defaults

The current request selects project, skill identity, requirements, permitted effects and destination. Reuse supplied answers; ask for a destination only when absent, recommending the resolved project `src/agents/skills` parent. Inspect existing bytes and known provenance before choosing an observed first edit, authored prior, legacy generated history or explicit adoption. Conflicting known history blocks dependent work.

Preserve the exact closed `authoring-contract-v1`, `authoring-design-v1`, `validation-request-v1`, authored/legacy baseline families and adaptive v1 interfaces in the captured schemas. Relative CLI arguments resolve from the actual working directory; references bind raw bytes and actual absolute locators. Package paths stay relative, without traversal, links, special files or operational destinations. Capture ceilings remain 2,000 files and 32 MiB. Selected inputs, destinations and evidence roots stay disjoint.

New create/edit/import/specification-build operations prepare the external design before staging, record observable behavior and requirement-derived challenges, include original sources and the design in contract inputs, and supply `begin --design`. Each authored adaptive member has its own design. Legacy no-design calls, including those carrying design-shaped JSON as ordinary input, remain supported. Adoption-only, proposals and update reviews do not acquire a mandatory design.

## Outputs and schema compatibility

Preserve candidate, before/baseline/delivered manifests, supplied/effective contract capture, path-resolution records, exact design input snapshot, `design-capture.json`, authoring record/baseline, manual validator packet/prompt and publication/failure records. Keep design out of generated runtime packages by default. Quality stays NOT_PERFORMED without separately selected, current-byte external evidence. Source action, authoring state and evaluated-build completion remain distinct.

Add a small **internal stage-integrity receipt** outside candidate/runtime output, written after origin capture/readback and before STAGED is returned. Its closed fields are `schema_version: "authoring-stage-integrity-v1"`, `run_id`, `target_name`, `origin_ref: {path, sha256}` and `design_capture_requested: boolean`. `origin_ref` binds the exact observed `origin.json` bytes, including the existing design capture reference and mode. This receipt is a local consistency check, not protected authority. No existing contract, validator packet, baseline or design schema receives new fields.

## Workflow and resource routing

1. Resolve the authorized task through SKILL.md. Load authoring.md for ordinary work; spec-build.md for explicit documents; conversion-rules.md for imports; regeneration.md for existing packages; adoption.md for custody-only work; adaptation.md plus adaptive-contracts.md/project-binding.md for selected adaptive operations.
2. Capture original requirements, resolve material decisions and fill workflow-design.md's template before selected authoring. Define completion, literal delivery, failure/recovery, resource loading conditions, justified helper contracts and supplied timeout provenance. Missing decisions block only dependent work.
3. Run `authoring.py begin` with selected inputs. Validate custody shape/identity, capture raw bytes, write origin/design records, then write/read back the new stage-integrity receipt. Return STAGED only after these writes complete.
4. Author the candidate. Load branch resources when needed. Initializer and metadata tools remain optional authoring aids, never run on an occupied existing package. Do not execute candidate helpers, tests, graders, checkers or automatic validation.
5. At publication, read and validate stage integrity **before selecting the legacy/design branch or performing destination writes**. For new stages carrying the existing `design_capture_requested` marker, require the receipt and exact run/name/mode/origin binding. Missing, changed, malformed or mismatched evidence blocks publication. An altered false marker must not bypass the origin digest comparison.
6. Continue all existing B/C/N comparisons, pre-write/per-path input checks, design rechecks, destination readback and baseline ordering. Recheck stage integrity alongside design evidence at publication boundaries. Keep actual applied changes and failure records; never claim rollback or publish a successful next baseline after failure.
7. Return delivered source, source action, authoring state, custody references, unresolved issues and manual validator handoff. Stop at authoring. The validator independently constructs fixtures/oracles from original requirements and exercises generated skills under separate authorization.

## Legacy stages and bounded recovery

Historical canonical stages without the mode marker and without the new receipt follow existing legacy handling. A newly staged ordinary no-design call writes a false-mode receipt and remains publishable, even with design-shaped JSON among ordinary inputs. Existing completed baseline readers retain their exact prior semantics.

Already-staged pre-revision records containing the mode marker but no new receipt cannot prove the stronger consistency property; preserve them and require a fresh linked authoring run instead of manufacturing a receipt after the fact. This compatibility migration must be explained in evidence-format.md and regeneration.md. It does not alter published historical baselines.

The receipt detects the reproduced inconsistent-stage modification; it does not prevent an actor from coherently rewriting every editable artifact. No cryptographic trust anchor or hostile-writer enforcement is claimed. Protected validation remains compiled Rust. A killed child is not assumed to have cleaned up. Retain parent-owned recovery receipts and distinguish execution ceilings from specified performance requirements.

## Requirements and acceptance

| ID | Required behavior | Independent acceptance |
| --- | --- | --- |
| REV-001 | Validate the original stage mode and origin bytes before legacy/design dispatch. | Stage with --design; flip mode to false, remove its binding and capture record, change captured design; publication must not be AUTHORED, must not write target or successful baseline, and must name the inconsistent evidence. Reproduce on Windows and Linux. |
| REV-002 | Preserve local corruption detection and actual failure effects. | Mutate/delete origin, receipt, capture record and original/captured design individually; corrupt receipt identity/hash/mode; inject changes after first write. Observe BLOCKED before effects, PARTIAL with accurate deltas afterward, and no successful publication readback. |
| REV-003 | Preserve documented legacy behavior and packet shape. | Fresh no-design calls with ordinary design-shaped input still publish. Historical no-marker canonical stages and published baselines remain readable. Pre-revision staged marker/no-receipt records report the explicit fresh-run migration. The unchanged validator accepts current valid packets and rejects stale ones. |
| REV-004 | Preserve authoring-only behavior and portable output. | Cold simple/branching authoring produces actual packages and manual handoffs without candidate execution; independently run both generated skills, including literal spaces/Unicode paths, failure delivery and interruption. Preserve all SBPV-01–18 obligations and prior failed attempts. |
| REV-005 | Bind delivery and evidence without overstating qualification. | Update only required development files and manifest; retain exact before/after changes. Execute focused red/green/refactor and regression evidence with Python JSONL runner, deterministic graders, fixtures, expectations, schema and runtime/digests. Measure declared first-party executed-line coverage and required-case pass rate >=95% independently per required platform, without hiding failed mandatory cases. |

## File-to-requirement mapping

`scripts/authoring.py`: REV-001–003. `references/evidence-format.md`, `references/regeneration.md`, `references/workflow-design.md`, `references/authoring.md`, and necessary SKILL.md routing: REV-001–004. `package-manifest.json`: REV-005. External maintenance/evaluation evidence: REV-001–005. Reuse `record_schema.py` only if its existing vocabulary suffices; add no dependency/service/package initializer. No unrelated source files are selected for repair.

## Dependencies, effects and preservation

Existing Python 3.10+ custody runtime; installed PyYAML only where current metadata tools need it; Codex terminal for cold evaluation. No MCP, GUI, network service or future CLI is required. Preserve operational copies, validator implementation, existing generated skills, project specification bytes and historical evidence. Stage/file observations are editable evidence only.

## Review decisions and handoff

Review the one proposed custody correction and its explicit pre-revision staged-run migration. Selection is pending; no optional enhancements are bundled. A repair task must bind this proposal and fresh target digest, confirm the maintenance basis and narrowly authorized changed paths, then use skill-creator for implementation and a fresh skill-validator run for independent evaluation. The current run does not assert a generated/adopted baseline or authorize re-adoption. No runtime performance requirement is proposed from the two timeouts.
