# PRD Claude-to-Codex import and SPEC-002 comparison

Date: 2026-09-29. This is a source import and author review, not independent behavioral
qualification. The PRD port is **authored**, its structural checks **PASS**, and the native
Codex catalog discovers it. PRD behavioral qualification remains **NOT_RUN** and owner
acceptance remains pending. The original approved specification is unchanged.

## Selected source and candidate

| Item | Identity |
|---|---|
| Worktree | `/home/bryan/Projects/DevForgeAI-prd-codex-port-20260929` |
| Branch | `codex/prd-codex-port-20260929` |
| Base | `073a2f2f498a5ebfc88dcf46d75a40bdee8e2216` |
| Baseline selection | Primary HEAD, local `origin/main` and remotely observed default `main` matched at selection |
| Claude input | `src/claude/DevForgeAI/skills/prd/`, SKL-002 v1, eight files |
| Original evaluation input | `src/claude/DevForgeAI/evals/prd/`, 20 cases, 157 files |
| Authority | Approved SPEC-002 v1 at `docs/specs/spec/SPEC-002.md` |
| Authority SHA-256 | `90b539a7a4ebdc57da1343c3e11099946872768d97bb66a50af6ab50e5e84e6c` |
| Codex skill | `skills/prd/`, SKL-002 v1 in the Codex provider, draft |
| Shared plugin | `devforgeai`, manifest 0.4.0, four skills |
| Combined runtime SHA-256 | `c46638c6881a99b3b29ac30e523bbe5e88f176ccb227292b19e2f40fd1947aef` |

The selected runtime has 49 files: the shared manifest and all four skills. Its complete
[file manifest](prd-import-evidence/candidate.json), frozen runtime copy, and
[source baseline](prd-import-evidence/source-baseline.json) bind these claims. The digest
is SHA-256 over sorted `relative-path NUL file-sha256 LF` records. It excludes tests,
reports and evidence. It does not identify an installed or accepted package.

Worktree creation through the app failed with the already-recorded WSL ownership issue;
WSL Git created the new branch/worktree without changing global trust settings. No stale
PRD candidate was restored. The primary checkout had unrelated edits to templates and
untracked ADR-004, SPEC-009 and a handoff prompt; those were left in place. The dirty
primary templates were not silently copied into the selected base. During this task,
primary advanced independently to 1dacff87546230f400bb969e0bd5c1e2b43e7043 (PR #9),
committing those four documentation/template changes. Their bytes still match the
initial snapshot; the task worktree base and PRD authority/input bytes did not change.
The first final audit incorrectly required stable primary Git status; its failure and
helper are retained locally under prd-import-evidence/prior-attempts/; the failure summary
is tracked. The corrected audit distinguishes byte preservation from concurrent Git-history movement.

## Claude-to-Codex mapping

| Surface | Claude source / SPEC-002 | Codex port | Verification and limit |
|---|---|---|---|
| Invocation | `/devforgeai:prd`, `$ARGUMENTS`, `argument-hint` | `$devforgeai:prd BRN-NNN`, skill selection or natural language; ID parsed from the request/conversation; omit unsupported argument metadata | Native catalog found `devforgeai:prd`; implicit activation NOT_RUN |
| Read/search/write tools | Read, Glob, Grep, Write, Edit | Available file/patch tools and scoped shell/`rg` reads; no invented Claude Skill tool | Instruction/structure review only |
| Questions | Up to four questions, 2–4 options, AskUserQuestion | At most three questions per batch; permitted native tool only when it represents all choices; otherwise numbered plain text and wait | All original requirement/context choices retained; host mode and gate restrictions documented; interactive testing NOT_RUN |
| Interview budget | `interview.max_calls`, default 8, including gates | Same resolved call budget across tools and plain text; no reset or automatic increase | Policy/defaults match the existing Codex Architecture copies byte-for-byte |
| Resource lookup | `${CLAUDE_SKILL_DIR}` / plugin root | Resolve assets, references and sibling Architecture from the actual loaded skill directory | 17 relative Markdown links checked; sibling Architecture exists in the selected candidate |
| Local preference | `.claude/devforgeai.local.md` | `.codex/devforgeai.local.md`; same keys, precedence, ignore/report behavior | Provider adaptation, not a change to Codex configuration; no file created |
| Provenance | New records identify `claude-code`, current model/session | New records identify `codex`; use exact current metadata only when actually available; preserve historical authors/reviews | Missing values disclose `unknown` and remain validation errors; BEH-10/VER-09 not satisfied by non-empty placeholders |
| Downstream handoff | `/devforgeai:architecture PRD-NNN`, availability checked in selected plugin | `$devforgeai:architecture PRD-NNN`, same local existence check and final-paragraph rule | Catalog/file discovery PASS; produced-reply and absent-skill branch NOT_RUN |
| Evaluations | Claude `plugin eval`, Skill-call and slash-command assertions | Mechanical case conversion plus explicit `codex_skill_read` adapter contract | Original task bodies and scaffolds unchanged; no turnkey PRD native runner or behavioral result claimed |

The invocation and skill metadata mapping uses current [official Codex skill guidance](https://developers.openai.com/codex/skills).
The question mapping follows the actual host tool contracts, which vary by mode; it does
not assume that a request-user-input tool is always available. The local native catalog
check ran **codex-cli 0.159.0 on WSL**, from `/home/bryan/.local/bin/codex`, resolving to
`/home/bryan/.codex/packages/standalone/releases/0.159.0-x86_64-unknown-linux-musl/bin/codex`.
This identifies the tested CLI, not the desktop app or the model serving this authoring task.

## Discrepancies against the unchanged specification

These are source-level findings and host adaptations. A possible failure inferred from
instructions is not presented as an observed native failure. Exact source/spec/port lines
are retained in [comparison evidence](prd-import-evidence/comparison-evidence.json), and
[source correspondence](prd-import-evidence/source-correspondence.json) binds the source
and imported files. The generated complete diff remains local at
`prd-import-evidence/claude-to-codex.patch`; both source trees are tracked for comparison.

| ID | Original requirement / text | Claude source behavior | Imported behavior and evidence | Classification / disposition |
|---|---|---|---|---|
| D-01 | §5, BEH-01/05/10/11/13/18 name Claude invocation, tools, paths and author identity | Uses Claude-specific surfaces directly | Uses the mappings above; `references/codex.md`, agent metadata, shared manifest and catalog evidence | Intentional provider adaptations. Literal Claude-specific conformance is impossible for a truthful Codex port; no specification edits or provider acceptance implied |
| D-02 | BEH-10 requires the current model ID and session ID; VER-09 requires populated provenance | Uses the current model and `${CLAUDE_SESSION_ID}`; its regex mainly tests non-empty values | Port cannot verify exact authoring identity in this session. Runtime instructions require a supported production source and treat `unknown` as an unresolved validation error. No metadata adapter, config guess or evaluator injection was added | Unresolved host capability/conformance limitation. Exact runtime identity still needs behavioral proof; a regex pass is insufficient |
| D-03 | BEH-09: approved extension becomes `in-review` with approval cleared. ERR-06: leave status "as it was before this write". BEH-06: "Never set approved" | Step 8 changes approved to in-review; step 9 repeats the previous-status instruction | Both source instructions are retained, with a pre-write guard for approved extensions requiring an explicit failure disposition. No approved-extension run claimed | Specification conflict and guarded source deviation. Owner decision needed before that branch; do not label changed invalid content approved |
| D-04 | BEH-12: "Fix and check again, at most three attempts." ERR-06: "after three fix attempts" | Repeats both wordings; does not unambiguously define whether the initial check is an attempt | Port documents the ambiguity, bounds repairs to three, and requires actual initial-check/repair/readback evidence. Exhaustion NOT_RUN | Specification ambiguity. Resolve the exact counting contract before qualification; no fabricated repairs or no-op checks |
| D-05 | BEH-03 marks each required category "the user did not answer"; BEH-06 marks other unanswered gaps | Step 7 and self-check 11 instead require NFR coverage or a marker. Interview says every answer becomes an NFR, despite offering `none` and `no target yet` | Inherited rules retained. Explicit `none`, unanswered, partial answers and policy additions are separate NOT_RUN branches | Inherited semantic gap: an answered-none category can become a fake requirement or be mislabeled unanswered. A category-level NFR alone also does not prove every gap is settled. Resolve separately; no automatic waiver of a mandate |
| D-06 | BEH-09 leaves new/extend to the user; BEH-05 skips answered questions | General gate rule accepts an explicit choice in the request, but step 4 unconditionally says "ask" and wait | Step 4 now explicitly honors an already supplied destination, consistent with the source's gate rule. No runtime response yet tested | Narrow repair of contradictory source wording; it does not treat "proceed without questions" as choosing new/extend |
| D-07 | BEH-04 derives FRs from promoted ideas; BEH-07/16 permit user/policy constraints | Output contract says "every requirement cites a promoted idea", while BRN mapping correctly forbids invented NFR derivation; the template has similarly broad author comments | Main output contract now says every FR derives from a promoted idea and NFRs cite only actual sources. The unchanged asset retains its broad author comment, which generated output must delete | Narrow instruction repair with inherited template wording still reported. BRN mapping and output-rules are the precise link contract; never fabricate an IDEA link for a user or policy NFR |
| D-08 | BEH-10 says `reviewed_by` empty without an extension exception | Step 8 and output-rules preserve an extension's existing human review history | History-preserving source rule retained; original authors and old Change Log rows never relabeled | Source/specification ambiguity. Clarify new-document versus extension provenance separately; preservation is not claimed as literal compliance with every reading of BEH-10 |
| D-09 | BEH-17 R1 requires approved policy to validate "against the schema and SV-01 to SV-06" | Runtime policy checklist includes keys and selected types but omits parts of `policy.schema.json` / `common.schema.json`, such as date patterns and several frontmatter/link type constraints | Existing Codex policy copy has the same gap and is preserved; no new duplicate runtime validator or schema framework added | Inherited validation-coverage gap. The `max_calls=50` case does not prove full schema enforcement; add independently defined malformed-field cases before qualification |

Mandated platforms are unconditional R2 settings in v1; the source applies each effective
mandate even when the BRN does not name that capability. BEH-16's word "applicable" is not
permission to silently skip one. The port keeps this behavior, preserves each setting's
item-level citation, and lists unclear applicability as a supplemental decision/test branch.

## Coverage review

| Requirements | Static import result | Remaining evidence |
|---|---|---|
| BEH-01/02/04/08/11/14 | ID-only selection, promoted-only derivation, allocated output paths, all template sections and BRN immutability retained | Native cases and before/after source checks per trial |
| BEH-03/05/06/07 | User-owned null decisions, category floors, no design decisions, interview budget and choices retained | Interactive/manual coverage; D-05 explicit-none and partial-answer issue |
| BEH-09/15/16 | Scope/owner/lifecycle selection, stable item bytes/IDs, shared-constraint citations, bounded ADR context and NEEDS ADR markers retained | Extension/handoff/manual behavior; D-03/06/07 |
| BEH-10/12/13 | Truthful provider adaptation, readback self-check and conditional handoff represented | Current runtime provenance, validation exhaustion and final reply behavior; D-02/03/04/08 |
| BEH-17/18 | Same policy precedence, overrides, local ignore/report behavior and one-place citations | Full schema enforcement and policy/local manual branches; D-09 |
| ERR-01/02/03/04/05/07/08 | Original no-write gates, malformed-input errors, draft-save choice and fatal policy behavior retained | Native behavior NOT_RUN |
| ERR-06 | Original failure rule retained and conflict disclosed | Approved-extension branch guarded pending decision; exhaustion NOT_RUN |
| QR-01/02 | 354-line skill, 404-character description, valid metadata/provenance shapes, references separated | Structural PASS only; unknown provenance is not current identity |
| QR-03 / VER-01..23 | All 20 original automated cases and three manual VER groups retained; no threshold reduction | All 120 automated trials and 21 manual branches NOT_RUN; eight supplemental branches NOT_RUN |

The [frozen plan](prd-import-evidence/evaluation-plan.json) contains the original text and
coverage mapping for every BEH/ERR/QR/VER item, including obligations with no automated
case. It retains the **0.8** bar and **three repetitions**. Binary repetitions require
3/3 PASS. A percentage cannot waive a failed or unrun mandatory branch.

## Checks actually performed

| Check | Result | Evidence |
|---|---|---|
| Plugin Creator local plugin validator | PASS | `prd-import-evidence/plugin-validator.json` |
| Skill Creator validator | PASS | `prd-import-evidence/skill-validator.json` |
| Skill frontmatter/provenance schemas, metadata/version alignment, agent metadata, line/description limits | PASS | `prd-import-evidence/static-validation.json` |
| Relative resources and handoff target | PASS, 17 links | Same static report |
| Template and BRN mapping preservation | Byte-identical to selected Claude source | `prd-import-evidence/source-correspondence.json` |
| Codex shared policy/defaults | Byte-identical to existing Architecture copies | Static report |
| Original/adapted evaluation correspondence | PASS, 157 files, 29 mechanical changes | `evals/prd/provider-mapping.json` and correspondence result |
| Original scaffold syntax | PASS, 19 scripts | `prd-import-evidence/scaffold-syntax.json` |
| Existing combined-package regression tests | PASS, 44/44 | `prd-import-evidence/codex-regression-tests.json`; these test existing validators/evaluators, not PRD native behavior |
| Native catalog discovery | PASS, all four exact candidate skills | [Result summary](prd-import-evidence/catalog-preflight/result.json); raw catalog/protocol output remains local; no model turn was launched |
| New-file whitespace checks | PASS after retained control-verified helper correction | `prd-import-evidence/delivery-checks-v2.json` |
| Authority/source/primary preservation | Byte preservation PASS; concurrent primary Git movement recorded | `prd-import-evidence/final-preservation.json` |

Catalog discovery is not activation, a producing PRD run, a no-plugin behavioral baseline,
or verification of isolation. All behavioral trials remain NOT_RUN. There is no independent
semantic assessment in this import. The suite's custom Skill-read adapter is documented,
not falsely described as a built-in grader or a complete native execution harness.

## Files delivered and boundaries

- New runtime: `skills/prd/SKILL.md`, `provenance.yaml`, `agents/openai.yaml`,
  `assets/prd.md`, and six `references/*.md` files.
- Shared edits: `.codex-plugin/plugin.json` and `README.md` only. Existing default prompts,
  plugin identity and unrelated skill bytes are preserved.
- Development resources: `evals/prd/`, `tests/make_prd_evals.py`, this report,
  [unapproved proposals](PRD-SPEC-002-PROPOSALS.md), and `prd-import-evidence/`.
- Historical import hashes: `prd-import-evidence/delivery-manifest-v2.json`, captured before publication filtering.
- Current publication scope and hashes: [publication note](PRD-PUBLICATION.md) and
  [publication manifest](prd-import-evidence/publication-manifest.json).

All paths above are relative to `src/codex/devforgeai/` **inside the task worktree**.
Nothing was copied into the primary checkout or operational plugin directories. At the
original import capture, no commit, push or PR had been performed. The owner subsequently
authorized a draft PR with raw output retained locally; the publication note records that
scope. No marketplace entry, installation, cache update or merge is part of this delivery.

No production scripts, runtime dependencies, hooks or speculative metadata adapter were
introduced. Maintenance additions are one host-mapping reference, Codex metadata and the
mechanical evaluation generator. Policy/defaults duplication already exists in this package
and must stay synchronized with Architecture. Original authority and source files remain
read-only; proposed clarifications are expressly non-authoritative.

The next qualification step is to decide the failed-approved-extension lifecycle and
attempt-count wording, resolve exact provenance availability, and build/review the PRD
native runner against the frozen inventory. Then execute the matrix and manual branches
with independent semantic grading. Importing source or passing structural checks does not
complete that work or grant owner acceptance.
