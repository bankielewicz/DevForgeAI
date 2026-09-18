# Independent Codex QA audit of the enhanced skill-builder

Perform an independent, evidence-backed QA review and analysis of the enhanced **development-source skill-builder**. Determine whether its actual instructions, scripts, schemas, templates and observable behavior satisfy the governing specification, all BA requirements, all BAT acceptance cases, and preserved legacy behavior.

This is an audit of the implementation, not an implementation task. Do the authorized inspection and bounded tests, then deliver findings. Do not stop at a test plan or a capability statement. Do not repair either skill.

## Independence and tool boundaries

**Do not use `$skill-validator` to perform this audit.** If its skill card is attached, auto-suggested or present in the session, treat it as excluded context. Do not invoke its instructions, delegate this audit to it, execute/import its scripts, run its bundled tests/graders, or use its verdicts as your oracle. Another Codex session is separately auditing that skill.

Use your own source review and independently written terminal test harness. You may execute inspected **builder** helpers as systems under test in disposable fixtures. Do not use builder to assess or repair itself. A cold builder task may author synthetic test outputs; the independent auditor owns all checking. The normal builder task must still stop at authoring and manual handoff without executing quality checks.

The installed Skill Creator's `quick_validate.py` may be run directly as one limited structural observation, after inspecting it. This does not make Skill Creator or a structural checker the QA owner. Do not install a replacement checker or any missing skill.

Derive expected outcomes from the selected specifications and current user instructions before examining prior PASS/FAIL summaries. Establish your own requirement and test mapping, then inspect the implementation. Read prior assessment conclusions only afterward to compare coverage and challenge their claims. Prior tests, hashes, reports and implementation logs are evidence to verify, not authority that the implementation is correct. Do not assume agreement between helpers proves conformance.

## Exact scope and inputs

Project root:
`C:\Projects\DevForgeAI`

Only skill package under substantive audit:
`C:\Projects\DevForgeAI\src\agents\skills\skill-builder`

Governing specification — read completely:
`C:\Projects\DevForgeAI\docs\plan\skill-builder-adaptive-enhancement-spec.md`

Expected SHA-256:
`8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59`

Read-only companion **specification**, solely for shared interface and assessment-ownership requirements:
`C:\Projects\DevForgeAI\docs\plan\skill-validator-adaptive-enhancement-spec.md`

Expected SHA-256:
`f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42`

The companion specification may inform interface expectations; it does not authorize using or auditing the validator package. The selected builder specification governs builder behavior. If a material cross-document contradiction cannot be resolved by explicit scope or a more specific clause, retain both passages and block only the dependent conclusion rather than silently choosing an interpretation.

The last recorded delivered builder digest was:
`338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2`

That receipt described 43 permitted files. The pre-enhancement digest was:
`65e5513cdb531cbfb1d9ef3eb9a1665f4221b1993ea0e5fbd1eb8e20fa6cc680`

These are historical comparison points, not claims about bytes at your invocation. Recompute current identity independently. Do not substitute `.agents/skills/skill-builder`, an attached skill card, or an evidence snapshot for the actual `src/` target. Operational copies may differ or contain extra legacy files.

Read applicable AGENTS.md files. Inspect the full selected package and its actual routed custody, authoring, import, adoption, regeneration, schema and handoff resources. Follow explicit references to applicable older specifications where needed to verify preserved behavior; do not infer successful history from a missing pointer or from current files.

## Authorized effects and preservation

You may read selected inputs, create fresh QA evidence, write independent test code there, and run bounded synthetic trials. All audit writes belong under a fresh directory:

`C:\Projects\DevForgeAI\docs\plan\skill-independent-qa\skill-builder\<UTC-run-id>\`

Use `YYYYMMDDTHHMMSSffffffZ`; allocate a fresh name on collision. Keep source snapshots, fixtures, commands, outputs and reports disjoint. No writes to builder source, either validator package, operational/personal skill copies, specifications, old evidence, hooks, CI, plugin packaging or installation locations. No real project binding setup, production effects, remote publication or Rust implementation.

Enumerate before recursion. Honor applicable exclusions and no-follow rules; exclude backups, devforgeai_cli, repository metadata, dependency/generated trees, credentials, private keys, .env values and real operational binding contents before reading/hashing. Bound capture to 2,000 regular files and 32 MiB per declared capture scope, including the specification's aggregate limits. Count shared originals once. Reject links/junction traversal and special files. Report material omissions and never silently raise limits or truncate a complete claim.

Preserve actual package bytes, a complete permitted-file manifest, input hashes, current audit request, OS/shell/Python/tool identities and capture limitations. Follow the specification's digest algorithm: sorted relative-path rows with keys `path`, `bytes`, `sha256`; SHA-256 of compact UTF-8 JSON with unescaped Unicode. Sort row path strings as specified, not by native WindowsPath ordering. Do not include timestamps or absolute roots in the package digest or create a self-referential manifest.

Verify both specification hashes before dependent assessment. A mismatch stops spec-dependent conclusions; report actual hashes and continue only clearly independent observations. If builder bytes differ from the historical receipt, preserve current bytes and inspect the delta. Do not restore old bytes or discard another session's work. Audit compatible current changes with explicitly updated identity; material scope/contract ambiguity remains a concrete gap.

## Required review

Create a traceability matrix for **BA-001 through BA-014** and **every required behavior in the complete specification**, including obligations outside its summary register. Map each to exact source locations, test cases, independent expected results and evidence. Do not consider matching headings, keyword presence, schema equality or an implemented helper sufficient evidence of the complete workflow.

Inspect at least these connected behaviors:

- Authoring-only operation; normal create/edit/import/adopt/specification modes; portable destination selection; existing authorization reuse; manual validation-request-v1 handoff.
- Bounded project discovery without project-code execution; supported facts versus unknowns; preservation of existing skill coverage; grounded expertise and actual project conventions.
- Core preservation, distinct variants, complete parent requirement dispositions, authorized removals, explicit older-core inventories and missing/corrupt history.
- Strict closed record families and unchanged legacy fields/meanings; actual parser behavior, local references, digest calculations, identity, linked contracts and schema examples.
- Selection, capability/destination preflight, dependency closure, deterministic ordering, sequential authoring, independent continuation after failure, transitive blocking and truthful partial effects.
- Exact per-member custody/readback; authored versus retained results; full_set versus eligible_subset requests; complete member/handoff omissions and dependency closure.
- Portable descriptor/runtime helper behavior; source/operational identity separation; all specified binding reasons and exit codes; fresh checks after changes/resume; no product writes after non-MATCH.
- Update review of unchanged, byte-changed but semantically equivalent, materially changed and missing inputs; no automatic rebase, repair or carried-forward quality verdicts.
- Real terminal capabilities, safe argument vectors, missing-tool behavior, resource consumers, progressive routing, supported metadata and automatic invocation. Identify actual contradictions, unreachable branches and unsupported promises rather than treating verbosity or MUST wording as defects by themselves.

Review source-to-effect call sites. Distinguish deterministic checks from semantic judgments, editable evidence from authority, and implemented behavior from instructions that still require native execution to verify. A check that a requirement ID merely occurs in text cannot alone establish a valid disposition or authorization.

## Independent acceptance testing

Read and map **BAT-01 through BAT-17** from the governing specification without dropping compound subcases. Retain each test oracle, fixture inputs/digests, exact command or cold prompt, expected effects, timeout and permitted write root before execution.

Cover ordinary create/edit; monorepo discovery and exclusions; separate count/byte ceilings and missing capabilities; existing HTTP coverage plus justified storage responsibility; full lineage; relocation; the binding matrix; positive/negative record parsing; legacy compatibility; failed A/dependent B/independent C; cycles/collisions/user edits/drift; routing positives/near misses; update review; all four project-convention fixtures; hostile paths; resume; and all listed history modes. Read the specification for the full oracles, not just this shorthand.

Use independently constructed positive and negative fixtures, including boundary values and misleading-but-well-formed records. Test observable effects and rejection reasons, not just exit 0. Cross-check serialized records, publication/readback artifacts, applied paths and actual target bytes. Where feasible, test wrong role/parent bindings, incomplete lineage, stale source references, LF/CRLF inventories and resource-path variations directly against the builder's own stated contract.

Inspect new harness code and dependencies before running. Use `python -B -X utf8`. Discover relevant existing tests before selecting commands; do not assume builder/tests exists, and do not count empty discovery as success. Existing tests held in validator are excluded from execution in this audit: recreate necessary independent regression scenarios in your QA run. Historical test outputs may later be inspected as secondary evidence only.

Default to 120 seconds per command/cold attempt, including children. Preserve stdout, stderr, exit/timeout, actual command, timestamps, before/after effects and partial artifacts. A retry uses a fresh attempt; justify it and preserve the failure. Do not silently extend timeouts. Simulate a missing interpreter in a disposable child environment; do not uninstall or disrupt the host.

Use the installed Codex CLI for applicable cold workflow cases when available. Inspect its actual version/help and relevant inherited execution controls without exposing credentials. Use existing authentication/model and supported flags. No sandbox/approval bypass, hook-trust bypass, configuration edits, new provider, dependency installation or broad writable real-project roots. A required blocked host action uses the normal approval mechanism; unavailable coverage remains NOT_RUN.

Cold tasks receive only the selected builder entrypoint, minimum raw project inputs, requested outcome and authorized disposable scope. Keep expected answers, intended fixes and grader labels outside their prompts. Label explicit invocation separately from native implicit discovery. A scripted controller exercising authoring helpers is useful evidence but does not prove autonomous set orchestration. Author-generated artifacts must remain unchanged before independent checking.

Synthetic adaptive bindings may be created only inside disposable trial projects. Generate synthetic UUIDs during setup and keep them in the disposable operational binding records; do not copy actual project identity into generic evidence or source. Test no-product-write behavior around the runtime check, not only the helper's exit code.

Do not execute builder-to-validator integration in this audit, since validator use is explicitly excluded. Verify builder-emitted handoffs independently against the published interface. Mark actual enhanced-validator consumption outside this audit's scope; do not claim an integration PASS or attribute a companion-only defect to builder. This exclusion does not waive the builder's own handoff obligations.

## Prior evidence — examine after independent planning and first-pass review

Builder implementation and before/after evidence:
`C:\Projects\DevForgeAI\docs\plan\skill-adaptive-implementations\skill-builder\20260913T083452607505Z\`

Later compatibility investigation:
`C:\Projects\DevForgeAI\docs\plan\skill-set-validations\20260913T135752395202Z\`

These contain historical implementation claims, test harnesses, failed attempts and reports. Verify relevant referenced bytes before relying on them. Distinguish earlier observations from new executions and note which package each tested. Audit whether prior oracles, fixture construction, selected targets and result reductions support the claims. Do not copy old PASS labels into current coverage, treat previously known gaps as the only possible defects, or convert a prior timeout into proof that the implementation is defective.

## Deliverables and decision

Write a self-contained `qa-report.md`, requirement/BAT traceability matrix, findings ledger, independent test sources, exact command log, evidence index and final readback receipt in the fresh QA directory. Use simple audit-owned formats; do not require validator schemas or tools.

Each finding must state severity, affected BA/BAT/spec clause, exact source path and line/byte locator, expected versus actual behavior, minimal reproduction, retained raw evidence, impact, confidence and a concrete proposed correction. Separate implementation defects, documentation/contract ambiguities, evidence-quality defects and unperformed coverage. Report counterevidence and distinguish confirmed defects from hypotheses. Recommendations are proposed only; apply no fixes.

For each requirement and BAT subcase report PASS, FAIL, NOT_RUN or justified NOT_APPLICABLE with method, target digest and evidence. A requirement passes only when its required applicable subcases have adequate evidence. Overall FAIL takes precedence over INCOMPLETE, which takes precedence over PASS; preserve unperformed coverage even under FAIL. Separate audit completion from acceptance, and static/helper/semantic/native results from installation or future Rust qualification.

Recompute the original source package manifest and applicable specification hashes at the end. Compare exact file sets and bytes, recheck evidence references and all mappings, and confirm the audit did not modify the packages or old evidence. If source drifted, limit conclusions to the preserved snapshot and identify the required fresh readback/retest rather than silently updating the baseline.

Return the answer to: **Does this exact development-source skill-builder meet the complete selected acceptance contract, and what evidence or corrections are still needed?** Lead with that conclusion, then the most consequential findings, exact source digest, evaluated/unperformed coverage, artifact paths and specific remaining tests. Do not claim complete acceptance from structural success, previous reports, fixture-only integration or native timeouts. Stop after delivering the independent audit; do not repair, install or start another enhancement.
