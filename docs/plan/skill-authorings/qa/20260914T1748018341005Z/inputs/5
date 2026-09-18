"""One-run content authoring and input capture; no evaluation or product execution."""
import hashlib
import json
from pathlib import Path
import re
import sys

PROJECT = Path(r"C:\Projects\DevForgeAI")
RUN_ID = "20260914T1748018341005Z"
INPUTS = Path(__file__).parent
RUN = INPUTS.parent / RUN_ID
SPEC = PROJECT / "docs/specs/qa-skill-spec.md"
BUILDER = PROJECT / ".agents/skills/skill-builder"


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = content.encode("utf-8") if isinstance(content, str) else content
    with path.open("xb") as stream:
        stream.write(data)
    if path.read_bytes() != data:
        raise RuntimeError("Write readback mismatch: " + str(path))


def reference(path):
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def segment(source, start, end):
    return source.split(start, 1)[1].split(end, 1)[0].strip()


def prepare():
    write(INPUTS / "user-request.txt", "$skill-builder C:\\Projects\\DevForgeAI\\docs\\specs\\qa-skill-spec.md\n")
    spec = SPEC.read_text(encoding="utf-8")
    mappings = {}
    for number in range(1, 27):
        paths = ["SKILL.md"]
        if number <= 9 or number == 12:
            paths += ["references/intake-planning.md", "assets/test-plan-template.md"]
        if number in (10, 11) or 13 <= number <= 17:
            paths += ["references/execution-integrity.md"]
        if number in (18, 19):
            paths += ["references/assessment.md"]
        if 20 <= number <= 25:
            paths += ["references/reporting-handoff.md"]
        if number == 20:
            paths += ["assets/qa-report-template.md"]
        if number in (21, 22, 24):
            paths += ["assets/qa-fix-template.md"]
        if number == 26:
            paths = ["validation-request.json (external authoring evidence)", "validator-request.md (external authoring evidence)"]
        mappings[number] = paths
    requirements = []
    for number, title, body in re.findall(r"\*\*QA-(\d{3}) — (.*?)\*\*(.*?)(?=\*\*QA-\d{3}|\Z)", spec, re.S):
        n = int(number)
        requirements.append({"id": "QA-" + number, "origin": "supplied specification", "outcome": title + body.split("\n\n", 1)[0], "artifacts": mappings[n], "source": "qa-skill-spec.md#QA-" + number})
    requirements.append({"origin": "inferred design default", "outcome": "Use instructions and three templates with four focused references; no runtime helper is needed. Preserve automatic invocation and supply minimal UI metadata.", "artifacts": ["SKILL.md", "agents/openai.yaml"]})
    files = ["SKILL.md", "agents/openai.yaml", "references/intake-planning.md", "references/execution-integrity.md", "references/assessment.md", "references/reporting-handoff.md", "assets/test-plan-template.md", "assets/qa-report-template.md", "assets/qa-fix-template.md"]
    inputs = [SPEC, INPUTS / "user-request.txt", PROJECT / "AGENTS.md", BUILDER / "SKILL.md", PROJECT / "docs/plan/devforgeai-codex-rust-enforcement-design.md", Path(__file__)]
    inputs += [BUILDER / "references" / name for name in ("authoring.md", "spec-build.md", "evidence-format.md", "validation-handoff.md", "scaffolding.md", "openai_yaml.md")]
    contract = {
        "schema_version": "authoring-contract-v1", "run_id": RUN_ID,
        "project_root": str(PROJECT), "target_root": str(PROJECT / "src/agents/skills/qa"),
        "target_name": "qa", "operation": "spec_build",
        "authorization": "User invoked $skill-builder with the explicit qa-skill-spec.md. Section 1.1 selects src/agents/skills/qa and section 13 authorizes development authoring, custody readback and manual validation handoff only.",
        "history_review": "no_known_history", "change_paths": sorted(files), "requirements": requirements,
        "purpose": "Portable independent product QA planning, authorized execution, assessment and manual remediation handoff to dev.",
        "activation": {"include": ["Independent product QA or test planning for explicit specifications/stories and scope"], "exclude": ["Product implementation/repair", "Skill-package validation", "Deployment/installation", "Standalone architecture research"]},
        "capabilities": ["Read selected project/specification/candidate bytes", "Author a test plan without test execution", "Execute a separately selected plan within authorization", "Inspect test integrity, calculate exact quality metrics and report evidence", "Return user-facing dev remediation and independent retest handoffs"],
        "expected_outputs": ["Nine-file development package", "QA-001 through QA-026 requirement mapping in contract.json", "authoring-v1 record and authoring-baseline-v1", "Digest-bound validation-request-v1 and manual validator prompt", "At runtime: plan, receipts, traceability, checkpoint, QA report and FAIL fix packet at resolved locations"],
        "dependencies": ["Runtime: Codex CLI terminal/file access and project-specific tools discovered at runtime", "Authoring custody: existing Python 3.10.11 and loaded builder helpers; no dependency installation", "Separate evaluated build: validator-owned Python JSONL runner, graders, fixtures/cases, expected results, schema, runtime/dependency declaration and bound manifests"],
        "operational_constraints": ["Development source only; no operational skill writes, installation, plugin, product QA or repair", "No builder test, grader, structural-checker or trial execution", "Portable runtime without concrete authoring paths or required framework binding", "QA assessment is not compiled-Rust framework acceptance"],
        "side_effects": ["Runtime plan: read-only product inspection and selected planning/evidence writes; host Plan mode has no file writes", "Runtime execute/retest: authorized independent QA tests, fixtures, logs and disposable product state, with candidate preservation", "No automatic repair, retest, installation or deployment"],
        "recovery": "Preserve prior evidence and partial attempts. Stop affected work on source drift or unavailable essential capabilities. Runtime checkpoints bind source/specification/plan, effects, owned state and next safe action; no blind replay or unobserved rollback claims.",
        "inputs": [reference(path) for path in inputs],
        "known_issues": ["QA-026 mandatory evaluated-build Python bundle has not been produced or executed; it belongs to the separately authorized validator task. Evaluated build remains incomplete; authoring can complete.", "Validation: NOT_PERFORMED. Testing: NOT_PERFORMED. Framework acceptance: NOT_EVALUATED."]
    }
    write(INPUTS / "authoring-contract.json", json.dumps(contract, ensure_ascii=False, indent=2) + "\n")
    write(INPUTS / "preflight.json", json.dumps({"target_absent": not (PROJECT / "src/agents/skills/qa").exists(), "qa_history_absent": not RUN.exists(), "git_metadata_present": (PROJECT / ".git").exists(), "source": reference(SPEC), "host": "Windows PowerShell; native filesystem", "python": sys.version, "scope": "Development authoring only; no recursion into backups or devforgeai_cli", "nested_instruction_search": "rg --files -g AGENTS.md under src, docs/specs and docs/plan/skill-authorings returned no nested files"}, indent=2) + "\n")
    print(json.dumps({"contract": str(INPUTS / "authoring-contract.json"), "run_root": str(RUN), "specification": reference(SPEC)}))


def stage():
    spec = (RUN / "inputs/0").read_text(encoding="utf-8")
    candidate = RUN / "candidate"
    entry = '''---
name: qa
description: Plan and execute independent product QA against explicitly selected specifications or stories and a development candidate. Use for iteration, sprint, or release-candidate testing, test-integrity review, evidence-backed assessment, and selected defect retests. Product repair, skill-package validation, authoring, installation, deployment, and standalone architecture research are separate tasks.
---

# Independent Specification-Driven QA

Assess the selected product against its requirements, independently of development completion claims. Work from explicit inputs in a cold Codex CLI session. Discover the actual language, project layout, tools, platforms and evidence destination; no installed framework, binding, index, plugin, browser or Git repository is intrinsically required.

## Select the mode and scope

Default to **plan** unless execution is explicit. Require the project, selected specifications/stories, scope and applicable rules. A sprint needs its selected story set or an unambiguous scope manifest. Read dependency references for context without selecting their deliverables. Ask only for missing decisions that affect the assessment.

Planning permits relevant read-only inspection and selected plan/evidence writes. Do not run product tests, build, generate executable harnesses, install dependencies or mutate product state. Under host Plan mode, provide the plan in conversation without file writes. Planning status is READY or NEEDS_INPUT, never product QA PASS.

**Execute** additionally requires a concrete selected plan and candidate and authorization for test effects. **Retest** requires a selected corrected candidate and defect set; it is a separate execution invocation. A pasted procedure or saved plan does not authorize execution. Do not automatically invoke dev or another QA session.

## Follow the selected workflow

1. Read [intake and planning](references/intake-planning.md). Bind exact input/candidate bytes and output paths, inventory every selected criterion, identify risks and missing decisions, and design independent oracles. Use [the test-plan template](assets/test-plan-template.md).
2. Read [execution and integrity](references/execution-integrity.md) and [assessment](references/assessment.md) while designing the plan. Inspect relevant test assertions and syntax within read-only planning limits. Include the actual required execution, integrity and metric procedures in the plan. In plan mode, publish/read back the plan and go directly to the final handoff.
3. In authorized execute/retest mode, reread the selected plan, rules and candidate; stop affected checks on drift. Follow execution/integrity instructions, preserve candidate bytes and prior attempts, and record exact case-bound observations. QA may author independent tests and fixtures in authorized QA locations; it must not repair product source or developer tests.
4. Apply assessment rules. Both first-party executed-line coverage and required **unit-test** pass rate must meet >=95%, or stricter project floors, per required platform and overall. Keep other test categories separate. Confirmed mandatory failures, prohibited mock decorators, gaming or unresolved confirmed regressions cause FAIL. Otherwise missing required evidence causes INCOMPLETE. PASS requires all mandatory obligations and both metrics with current evidence. Failure takes precedence over incompleteness.
5. Read [reporting, restart and user handoff](references/reporting-handoff.md). Fill [the QA report](assets/qa-report-template.md); on FAIL also fill [the qa-fix packet](assets/qa-fix-template.md). Read back actual artifacts at the originally resolved destination, then deliver the outcome-specific user handoff. Every mode ends with this step.

## Preserve evidence and ownership

Bind the literal selected evidence destination before writing. Keep input/plan/candidate identities, criterion/case maps, receipts, findings, report/fix paths and a checkpoint with owned process/fixture state and next safe action. On resume, reread identities, permissions, tools and state; invalidate affected evidence on drift and never blindly replay uncertain effects.

Any confirmed first-party mock decorator, including resolved aliases or analogous mocking attributes, is prohibited even when unused. Unresolved dynamic inspection is a gap. Search alone cannot establish absence. Confirm gaming from the source and claimed behavior, without inferring developer intent; legitimate setup is not automatically gaming and earns no product acceptance credit by itself.

Keep FAIL repair ownership with **dev**. Return a complete, resolved conversation prompt after verifying host skill availability and artifact identities. If dev is unavailable, retain the fix packet and report the discovery prerequisite. Never substitute QA as fixer, auto-send a handoff or install the missing skill. Only independent QA retest can establish QA defect closure.

Reports are QA assessments, not protected framework acceptance or release authorization. Respect any project-required external authority without simulating it. Do not install, deploy, change startup settings or broaden effects beyond current authorization. This skill's own package evaluation is a separate skill-validator task; authorized product QA execution remains this skill's responsibility.
'''
    write(candidate / "SKILL.md", entry)
    write(candidate / "agents/openai.yaml", '''interface:
  display_name: "Independent QA"
  short_description: "Plan and run independent specification-driven QA"
  default_prompt: "Use $qa to plan independent QA for the selected specifications and development candidate."
''')
    intake = "# Intake and planning\n\n" + segment(spec, "## 2. Activation, modes, and inputs", "## 6. Phase 4: Test-integrity audit")
    intake += "\n\n## Publish the testing plan\n\n" + segment(spec, "## 7. Phase 5: Publish the testing plan", "## 8. Phase 6: Execute the selected plan")
    intake += '''

## Resolve outputs before writing

Record the original `selected_evidence_value`, its selection source, resolved absolute evidence root, and a role-to-path map for the plan, source manifests, criterion/case maps, receipts, findings, report, fix packet, checkpoint and user handoff. Preserve all literal path components, spaces and Unicode. Do not shorten a supplied child destination to a nearby default. Allocate a fresh run/attempt location within the selected destination; preserve old runs and reject unintended input/candidate overlap. Resolve paths as data for the actual host; do not follow an unexpected link or change checkout identity silently.

Use [the test-plan template](../assets/test-plan-template.md). Fill every selected executable step with discovered procedures and specification-derived expectations. A missing tool, candidate, authorization or oracle stays an explicit affected-case prerequisite. Planned metrics are not measurements. Static findings may be confirmed during planning, but the plan remains READY or NEEDS_INPUT and any planning report uses NOT_EXECUTED.

Read the [integrity procedures](execution-integrity.md) and [assessment rules](assessment.md) before finalizing the plan. Record inspection performed versus inspection still planned. Follow [the final user handoff](reporting-handoff.md) after saving and reading back the plan. Under host Plan mode, return the unsaved plan in conversation and identify saving/binding as a prerequisite to a file-based execute handoff.
'''
    write(candidate / "references/intake-planning.md", intake + "\n")
    execution = "# Execution and test integrity\n\nIn plan mode, use these procedures for read-only inspection and test design only. Execution actions require the selected plan, candidate and permitted effects.\n\n"
    execution += segment(spec, "## 6. Phase 4: Test-integrity audit", "## 7. Phase 5: Publish the testing plan")
    execution += "\n\n## Execute the selected plan\n\n" + segment(spec, "## 8. Phase 6: Execute the selected plan", "## 9. Phase 7: Assess quality and decide the verdict")
    execution += '''

## Record a case and its attempts

Use the stable case ID from the plan and unique attempt IDs. Record category (unit, integration, acceptance, native or setup), required platform, execution provenance (developer-supplied, independent QA or manual native), candidate/plan/specification references, and status alongside the QA-017 receipt fields. Separate observed exit success from the expected behavioral assertions. Retain raw tool reports and capture their interpretation without rewriting them as passing evidence.

For uncertain timeouts/interruption, checkpoint the owned processes, fixtures, last observed state and next safe observation. Do not delete unrelated state or rerun a consumed action blindly. Track authorized retry budgets independently of case counts. A skipped or blocked required case uses NOT_RUN with its reason; it stays in the required inventory.

Before accepting an integrity absence claim, enumerate in-scope first-party files, inspect language-appropriate syntax/imports and follow resolvable aliases, re-exports, wrappers and factories. Record uninspectable/dynamic regions as omissions. Include QA-authored helpers in that inspection. If a suspected pattern is ordinary fixture setup, explain its limited claim rather than assigning product acceptance credit or alleging gaming. If confirmed, cite exact source and the assertion/boundary it fails to establish.

Feed valid raw evidence to [assessment](assessment.md), then use [reporting and handoff](reporting-handoff.md). QA source observations and evidence processing do not authorize protected phase transitions.
'''
    write(candidate / "references/execution-integrity.md", execution + "\n")
    assessment = "# Metrics and verdict\n\n" + segment(spec, "## 9. Phase 7: Assess quality and decide the verdict", "## 10. Phase 8: Publish the QA report and fix packet")
    assessment += '''

## Apply the decision to raw records

Before execution, declare eligible source inventory/exclusions and the unique required unit-case inventory for each platform. Preserve the plan's aggregate policy; identify cross-platform executions distinctly, and aggregate compatible line counts without treating a line executed on one platform as executed on another. Do not average rounded percentages or mix different candidate identities. If compatible overall evidence cannot be established, report that measurement unavailable. A later justified scope correction must be documented against requirements; never silently reduce the denominator to hide failures.

For every platform and overall scope, report integer numerator/denominator, the exact ratio and an unrounded decision. Apply thresholds by comparing the counts at full precision. A display-rounded value cannot qualify a result. For example, 9,499 of 10,000 eligible lines or required unit cases is 94.99% and fails independently of the other metric. Missing measurement has no estimated ratio. Required unit skips/errors/blocked/unexecuted cases remain nonpassing cases in the denominator; retries are attempts of the same case, never extra cases or erased evidence. Missing inventory completeness prevents PASS even if the observed suite passed.

Keep acceptance-criterion coverage, integrity inspection coverage and product metrics separate. Confirmed FAIL has priority while remaining gaps are still listed. An unresolved dynamic decorator investigation with no confirmed failure yields INCOMPLETE, not a clean inspection. A measured 99% cannot waive even one failed mandatory acceptance criterion. Use [the report template](../assets/qa-report-template.md) and route the result through [the user handoff](reporting-handoff.md).
'''
    write(candidate / "references/assessment.md", assessment + "\n")
    reporting = "# Reporting, restart and final user handoff\n\n" + segment(spec, "## 10. Phase 8: Publish the QA report and fix packet", "### 10.1 `assets/qa-report-template.md`")
    reporting += "\n\n" + "**QA-022" + segment(spec, "**QA-022", "## 12. Package design, resumption, and evaluation")
    reporting = reporting.replace("`assets/qa-report-template.md`", "[the QA report template](../assets/qa-report-template.md)").replace("`assets/qa-fix-template.md`", "[the qa-fix template](../assets/qa-fix-template.md)")
    reporting += '''

## Fill and bind artifacts (QA-025)

Use the [test plan](../assets/test-plan-template.md), [QA report](../assets/qa-report-template.md) and distinct [qa-fix packet](../assets/qa-fix-template.md) as the output contracts. Template brackets are authoring slots only: replace every slot with actual facts or a concrete unavailable/inapplicable reason. Explain omitted optional empty sections. Never present template slots as resolved runtime output.

Keep runtime records for input/plan/candidate identities, criterion/case maps, execution receipts, findings, report/fix locations, and a checkpoint with next safe action and owned processes/fixtures. Resolve locations at runtime using the original evidence selection. Preserve failed and interrupted attempts. On resume, reread source/specification/plan, verify evidence and permissions, rediscover tools and observe owned process state. Invalidate affected results on drift. Do not overwrite concurrent edits, replay uncertain mutations, delete old evidence or claim an unobserved rollback.

Publish the plan/report/fix at their bound output paths, read actual bytes back, and hash final versions. Record required-versus-actual artifact paths and hashes in a final external handoff manifest, then read that manifest back. Do not invent a hash for a future file or an artifact containing its own hash. When report and fix packet cross-reference each other, put their paths inside and use the final external manifest for their byte bindings; after publication the copyable user prompt can name that manifest and its hash. This keeps the required bindings complete without a circular hash dependency. Any write/readback failure remains explicit and no affected artifact is described as delivered.

The final prompt belongs in a fenced text block for the user's Codex conversation. For READY, select the actual saved plan, candidate, specification identities, evidence destination and intended test effects; this proposes a later execute invocation and does not authorize it itself. For FAIL, include all eight QA-024 fields and exact selected defects. Check the current host catalog or supported selection mechanism for the relevant skill. Missing dev discovery leaves its prompt pending and the fix packet intact. For INCOMPLETE or NEEDS_INPUT, give the exact unresolved input/evidence, affected cases and responsible owner. For PASS, use the project's defined downstream review; if none is defined, report that decision as unspecified without granting release permission.

For a selected retest, record OPEN -> FIX_REPORTED only when dev supplies the correction evidence. Independently rerun selected failures and affected regressions and reassess invalidated integrity/metrics before VERIFIED_FIXED. A persisting defect becomes REOPENED with the new case evidence. Never overwrite the original failure or close a defect solely on dev's report.
'''
    write(candidate / "references/reporting-handoff.md", reporting + "\n")
    for name, marker, next_marker in (("qa-report-template.md", "### 10.1 `assets/qa-report-template.md`", "### 10.2 `assets/qa-fix-template.md`"), ("qa-fix-template.md", "### 10.2 `assets/qa-fix-template.md`", "**QA-022")):
        section = segment(spec, marker, next_marker)
        template = segment(section, "```markdown\n", "```")
        write(candidate / "assets" / name, template + "\n")
    write(candidate / "assets/test-plan-template.md", '''# Independent QA Test Plan

Fill every field with actual values or a concrete missing/inapplicable reason. Repeat case sections as needed. READY execution steps have no unresolved slots. This is a plan, not an executed QA result.

## Identity, selection and authorization

- Plan/run identity and requested mode: [values]
- Planning status: [READY or NEEDS_INPUT and exact basis]
- Project identity, host, shell and filesystem: [actual values]
- Selected iteration/sprint/release-candidate scope: [explicit selection; story manifest if needed]
- Specification/story inputs: [literal paths, hashes, requirement locators]
- Candidate source identity: [commit plus dirty/untracked binding, or scoped first-party manifest; missing prerequisite if absent]
- Build/package identity and source correspondence: [artifact references/hashes or missing prerequisite]
- Dependencies/locks and available services: [versions, identities, state]
- Applicable instructions and architecture/stack/source/testing/data decisions: [references and decisions]
- Development handoff, baseline, known defects and claimed gaps: [references; distinguish claims from confirmed findings]
- Requested effects and existing authorization: [allowed scope; pending execution selection/effects]
- Explicit exclusions and dependency boundaries: [requirements-based reasons]

## Output and checkpoint binding

- selected_evidence_value and selection source: [literal supplied/policy/established selection]
- Resolved evidence root: [actual full host path]
- Fresh run/attempt destination: [actual path]
- Role-to-path map: [plan, source/build manifests, criterion/case maps, receipts, raw coverage/test reports, findings, QA report, qa-fix, checkpoint and final handoff manifest]
- Plan digest binding: [external manifest/path, completed after final plan readback; no self-hash]
- Checkpoint and next safe action: [input/plan/candidate bindings, completed/planned work, owned process/fixture state, remaining permissions]

## Acceptance inventory and risks

| Source-qualified criterion | Exact required behavior / source passage | Mandatory or advisory | Risks / priority | Cases | Independent oracle | Evidence required | Unresolved decisions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [ID and source identity] | [behavior] | [classification] | [risk] | [IDs] | [requirement-derived observation] | [artifacts] | [exact gap or none] |

- Inventory completeness: [all selected clauses including errors, state, recovery, concurrency, compatibility, platforms, documentation and nonfunctional obligations]
- No-ID/duplicate-ID handling: [source-bound local locators or qualified IDs]
- Ambiguous/conflicting requirements: [exact clauses, decision needed, affected cases and owner]
- Advisory improvements: [outside-scope items or none]

## Environment and capability matrix

| Required platform / host | Runtime/tools and discovered versions | Build/test/coverage capability | Services / permissions | Native or visual evidence needed | Readiness and missing prerequisite |
| --- | --- | --- | --- | --- | --- |
| [platform] | [values] | [actual discovery and command source] | [values] | [cases] | [ready or exact gap] |

## Required case inventory

| Stable case ID | Category | Criterion IDs | Required platforms | Provenance | Risk / priority | Applicable scope / exclusion reason |
| --- | --- | --- | --- | --- | --- | --- |
| [ID] | [unit/integration/acceptance/regression/native/setup] | [IDs] | [platforms] | [developer-provided/independent QA/manual native] | [priority] | [scope] |

### Case [stable ID]

- Criterion/source and assertion claim: [exact references and behavior]
- Required platform, category and priority: [values]
- Preconditions, entry conditions and environment: [versions, dependency/service state, permissions]
- Fixture/data identity: [inputs and hashes; safe synthetic data where appropriate]
- Isolation and side effects: [authorized QA/output paths, disposable state, candidate-preservation method]
- Procedure: [ordered exact discovered commands/actions, shell, working directory, timeouts and budgets]
- Command provenance: [inspected manifest/documentation and tool discovery; arguments quoted as data]
- Expected observations and independent oracle: [normal/negative/boundary outputs or state, requirement basis]
- Existing assertion limitations: [what developer tests establish and what remains to prove]
- Selected negative control / sensitivity check: [justification, deliberately incorrect behavior to detect, disposable-copy authorization; or justified not selected]
- Actual observations and case status: [NOT_RUN during planning; populated during execution]
- Evidence: [planned receipt/log/raw-report paths, case/attempt IDs and required hashes]
- Cleanup and uncertain-effect recovery: [owned state, safe cleanup, observation after timeout]
- Retry rules: [current authorization, bounded attempts, no duplicate case counting]

## Test-integrity inspection

- First-party implementation/test/QA-helper inventory and omissions: [bound scope]
- Language syntax/import/alias/re-export/wrapper/factory inspection: [performed findings versus planned work]
- Mock decorators or analogous attributes: [confirmed occurrences, bounded clean evidence or incomplete areas]
- Gaming checks: [assertion content, swallowed errors, skipped counts, fake boundaries, denominator/report manipulation, unjustified suppression]
- Legitimate setup/isolation distinctions: [claim limits; no setup-only acceptance credit]
- Unresolved dynamic behavior: [exact gap, owner and affected claims]

## Metrics and accounting declared before execution

- Executed-line source denominator and exclusions: [eligible first-party files/lines, tool, rules; no uncovered behavior removed]
- Per-platform source inventories and overall aggregation: [compatible counts and candidate bindings; no cross-platform substitution]
- Required unit-case denominator: [complete unique case/platform inventory including required skipped/blocked/unexecuted cases]
- Missing required unit tests: [gaps; inspected suite size alone is not completeness evidence]
- Effective coverage and unit pass floors: [each >=95% or stricter project requirement; record lower-policy mismatch]
- Calculation: 100 * executed eligible lines / all eligible executable lines; 100 * passing required unit cases / all required unit cases.
- Raw report locations and collector commands: [discovered commands and output bindings; unavailable if absent]
- Precision and attempts: [integer counts, unrounded threshold decision, retained attempts, each case counted once for final candidate]
- Separate branch coverage and acceptance/integration/regression/native accounting: [method and report paths]
- Current measurements: [NOT_RUN; no zero/unresolved denominator treated as 100%]

## Existing evidence proposed for reuse

| Evidence / hash | Candidate and tool/platform binding | Claimed criteria | Validity or drift assessment | Reuse reason / limitation |
| --- | --- | --- | --- | --- |
| [reference or none] | [binding] | [IDs] | [assessment] | [reason] |

## Entry, exit and final user handoff

- Execution entry conditions: [selected concrete plan/candidate, identity checks, allowed effects and prerequisites]
- Exit rules: FAIL for confirmed mandatory failure, measured subthreshold metric, prohibited mock decorator, gaming or unresolved confirmed regression; otherwise INCOMPLETE for required missing evidence; PASS only with all obligations and both floors satisfied per platform and overall.
- Remaining planning gaps and owner: [exact decisions/capabilities and affected cases]
- Source/plan drift and resume policy: [stop affected checks, invalidate affected evidence, preserve attempts]
- Publication/readback: [required-versus-actual literal paths and hashes; unsaved if host Plan mode]
- Open in Codex: [resolved project and correct host/environment]
- Next action/owner: [later QA execute or prerequisite resolution]
- Skill availability observation: [actual host catalog or supported selection mechanism]
- Copyable conversation prompt: [complete actual plan/candidate/specification selection and effects; for READY only, otherwise exact missing decisions]
- Product QA verdict: NOT_EXECUTED. Framework acceptance: NOT_EVALUATED. Release authorization: [separate supplied decision or not granted].
''')
    print(json.dumps({"state": "CONTENT_STAGED", "candidate": str(candidate), "quality_checks": "NOT_PERFORMED"}))


if __name__ == "__main__":
    {"prepare": prepare, "stage": stage}[sys.argv[1]]()
