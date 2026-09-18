"""Publish QA assessment documents from retained evidence, without product execution."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = Path("C:/Projects/DevForgeAI")
CANDIDATE = PROJECT / "devforgeai/experiments/codex-worker-probe-logging"
CORRECTED = PROJECT / "devforgeai/experiments/codex-worker-probe-logging-qa-fixes"


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    if name.endswith(".md"):
        for before, after in {
            "all67": "all 67", "all166": "all 166", "all15": "all 15",
            "All67": "All 67", "All24": "All 24", "All166": "All 166",
            "all24": "all 24", "only15": "only 15", "Only15": "Only 15",
            "the13": "the 13", "authored13": "authored 13", "of9": "of 9",
            "of8": "of 8", "of49": "of 49", "only152": "only 152",
            "full120": "full 120", "fixed120": "fixed 120",
            "unfiltered152": "unfiltered 152", "offline166": "offline 166",
            "in200.234seconds": "in 200.234 seconds", "in200.234": "in 200.234",
            "200.234seconds": "200.234 seconds", "12documents/49local": "12 documents / 49 local",
            "produces two OPEN": "produces two OPEN", "schema3": "schema 3",
            "Rust/Cargo1.97.1": "Rust/Cargo 1.97.1", "PowerShell7.6.6": "PowerShell 7.6.6",
            "rustfmt1.9.0": "rustfmt 1.9.0", "Clippy0.1.97": "Clippy 0.1.97",
            "cargo-llvm-cov0.8.4": "cargo-llvm-cov 0.8.4", "LLVM22.1.6": "LLVM 22.1.6",
            "Python3.10": "Python 3.10", "reported95.47%": "reported 95.47%",
            "complete120": "complete 120", "supplied153/153": "supplied 153/153",
            "as152": "as 152", "plus1": "plus 1", "then13": "then 13",
            "into9": "into 9", "of9": "of 9", "the116": "the 116",
        }.items():
            value = value.replace(before, after)
    with (ROOT / name).open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(value)


def write_json(name, value):
    write(name, json.dumps(value, indent=2, ensure_ascii=True) + "\n")


assert read("metrics.json")["verdict"] == "FAIL"
assert not read("final-identity-check.json")["problems"]
assert not read("documentation-review.json")["broken_links"]
assert not CORRECTED.exists()
candidate_hash = sha(ROOT / "candidate-manifest.json")
plan_hash = sha(ROOT / "plan.md")
input_hash = sha(ROOT / "input-manifest.json")
spec_names = {
    "logging-contract.md", "logging-design.md", "investigation-report.md",
    "codex-worker-feasibility-v1.md", "codex-worker-native-readiness-v1.md",
    "codex-worker-preflight-v1.md", "codex-worker-source-identity-v1.md",
    "diagnostic-contract.md",
}
specs = [item for item in read("candidate-manifest.json") + read("input-manifest.json") if Path(item["path"]).name in spec_names]
assert len(specs) == 8
write_json("specification-bindings.json", specs)

# Every grouped row retains the original source-qualified criteria from plan.md.
rows = [
    ("LG-01; LD-09", "Closed schema, literal config paths, <=4096 bytes, digest copy and final check", "PKG-070..072,079..081; QA-01,02", "Invalid intake never spawns; exact boundary and legacy composition work", "All predicates passed, including real junction denial and copied-byte digest", "PASS", "08-qa01,09-qa02,03-coverage"),
    ("LG-02; LD-01,02,05", "Mandatory ordered pre/post exit and joined-reader capture", "PKG-074,093,143; SUP-01; QA-03,04,09", "Complete temporal exit/capture evidence; inspector enforces it", "Real exits/readers passed; missing or contradictory post-stop evidence still inspects completed", "FAIL", "10-qa03,11-qa04,16-qa09,24-cli-confirm; QA-LOG-01,02"),
    ("LG-03; LD-03,04,06,11 capture slice", "Bounded independent pumps, full-byte hashes and explicit incomplete capture", "PKG-001..004,073,097,126; SUP-01; QA-04,05,09", "Exact hashes/limits; incomplete capture cannot qualify a complete observation", "Real pumping/limits passed; inspector accepts drain false/read error/overflow on completed evidence", "FAIL", "11-qa04,12-qa05,16-qa09,21-supplement; QA-LOG-01"),
    ("LG-04; LD-06,07,08,11 sink slice", "Four levels, closed data, fixed optional file and caps; mandatory failure precedence", "PKG-005,006,038..041,069,077; QA-06,07,08", "No canaries; optional failures nonauthoritative; required writes still fail and clean up", "All assertions passed, including real file and accounting failures", "PASS", "13-qa06,14-qa07,15-qa08,03-coverage"),
    ("LG-05; LD-01,02,08 classification slice", "Only two known startup Error patterns, explicit truncation", "PKG-001..004,074; QA-03..05", "Known patterns classify; lookalikes stay unclassified; exact byte accounting", "Positive/negative byte oracles passed; no inferred crash diagnosis", "PASS", "10-qa03,11-qa04,12-qa05"),
    ("LG-06; LD-12", "Bound current capture/status/log evidence; preserve legacy and interrupted prefixes", "PKG-006,075,076,084,092,144; QA-09,10", "Reject missing/inconsistent evidence; preserve sound historical interpretation", "6 of9 planned mutations falsely accepted;3 rejected; legacy/interrupted checks passed", "FAIL", "16-qa09,17-qa10,24-cli-confirm; QA-LOG-01,02"),
    ("LG-07", "Only15 policy key quote pairs change;116 argv positions/values and review binding", "PKG-045,067,068,078..081; QA-11", "Exact permitted byte differences and schema3/v2 composition", "Independent old/new vector comparison and denials passed without native launch", "PASS", "18-qa11,03-coverage"),
    ("LG-08", "Inherited and independent verification, real query_failed, floors, fmt/Clippy", "PKG-001..152; SUP-01; QA-01..13; BUILD/FMT/CLIPPY", "Every mandatory case and both numeric floors pass", "Numeric floors/static checks pass; mandatory QA-09 fails", "FAIL", "case-results.json,metrics.json,attempt-index.json"),
    ("DFF-WORKER-FEAS-01 sections3..7; WF-01..08; LD-10", "Strict wire subset, gates, correlation, single turn, independent oracle", "PKG-050,057..068,086,088..091,098..125; QA-08,11,12", "Only admitted/qualified work; exact trace and specification result", "All applicable offline trace/denial/oracle assertions passed", "PASS", "03-coverage,15-qa08,18-qa11,19-qa12"),
    ("WF-09..12; F-01/F-02 recovery regressions; base section7", "Exclusive persistence, intent before effect, no replay, honest inspection", "PKG-082,084,128..144,149; QA-09,10,12", "No mutation/replay; sound records inspect; inconsistent success rejected", "Inherited cases pass, but new capture/exit inconsistency is accepted", "FAIL", "03-coverage,16-qa09,17-qa10,24-cli-confirm"),
    ("WF-13..16", "Native Windows ownership, Ctrl+C/EOF/owner death, descendants and production watchdog", "PKG-085,093..097,132,133,135,137,142; QA-03..05", "Owned trees stop; pipes drain; fixed120-second watchdog fires", "Complete actual Windows campaign passed, including production watchdog", "PASS", "03-coverage,10-qa03,11-qa04,12-qa05"),
    ("WF-17..20", "Unsafe inputs, oracle mismatch, fixture mutation and evidence/cleanup precedence", "PKG-052..055,087,145,147..151; QA-01,02,07,12", "Closed rejection/explicit failure; no success from child claim alone", "Executed failure-path and preservation assertions passed", "PASS", "03-coverage,08-qa01,09-qa02,14-qa07,19-qa12"),
    ("NI-T01..10 offline; preflight companion", "Exact launcher junctions/digests, fixed policy, review and no-work preflight", "PKG-007..015,042..048,067,068,079..081,090..092,098..115,138; QA-11,12", "Synthetic identity/review denials and exact preflight gates", "Applicable offline assertions passed; no installed/native qualification inferred", "PASS", "03-coverage,18-qa11,19-qa12"),
    ("SI-T01..08", "Single allowed source junction, complete source inventory, freshness/final check", "PKG-016..035,042,044,046,049,152; QA-11,13", "Real synthetic Windows junctions; stale/malformed sources reject before spawn", "All selected assertions passed against synthetic roots", "PASS", "03-coverage,18-qa11,20-qa13"),
    ("SI-T09", "Existing source limits, credentials, identity/policy and WF/F-01/F-02 remain valid", "PKG-007..049,098,128..152; QA-09,11..13", "Inherited behavior remains valid including current inspection", "Source restrictions passed; expanded inspection semantics fail QA-09", "FAIL", "03-coverage,16-qa09; QA-LOG-01,02"),
    ("SI-T10 offline preservation slice; OUT-01", "Candidate, original, snapshot, bound inputs and console helper unchanged", "QA-13; PRESERVE", "All selected before/after bytes identical", "67 candidate,116 original/snapshot,37 inputs verified; no installed mapping mutation", "PASS", "20-qa13,final-identity-check.json"),
    ("Diagnostic v1 all stages; query_failed addendum", "Same held-job query/1-1 guard; null counts on error; no RPC/private fields; closed category order", "PKG-036..041,056,101..106; QA-08,12", "Real restricted handle fails actual API; closed observations/precedence", "Actual QueryInformationJobObject error5, null counts/no work and cleanup asserted", "PASS", "03-coverage,15-qa08,19-qa12; integrity.md"),
    ("Documentation review", "Factual native/authority boundaries, selected references and schema3 description", "QA-13; DOCS", "Local references resolve; no acceptance inferred from prose", "12documents/49local links reviewed; implementation completeness reduced by findings", "PASS", "documentation-review.json"),
    ("NI-T11,NI-T12; WN-01,WN-02; installed-profile qualification", "Separate native launch/installed source collection and operator evidence", "Excluded from selected offline166-case denominator", "No native launch in this invocation", "NOT_RUN; prerequisite independent offline QA has failed", "NOT_APPLICABLE", "plan.md; no native launch receipt"),
]
criteria = [dict(zip(["criterion", "requirement", "cases", "expected", "actual", "status", "evidence"], row)) for row in rows]
write_json("criterion-results.json", criteria)

prompt = f"""$dev In C:\\Projects\\DevForgeAI using native Windows PowerShell, remediate QA-LOG-01 and QA-LOG-02 only.

Read current AGENTS.md and verify {ROOT / 'handoff-manifest.json'}, especially entries qa-report.md, qa-fix.md, specification-bindings.json, input-manifest.json and candidate-manifest.json. Those manifests bind the exact eight selected specifications and handoff bytes. The failed candidate is {CANDIDATE}; candidate-manifest.json SHA256 is {candidate_hash}. Report material drift before editing; do not restore older source.

Create the corrected candidate at {CORRECTED}, preserving the failed candidate, frozen original/snapshot, all prior evidence, unrelated changes and Start-CodexAppServerDiagnostic.ps1. Restore capture completeness and mandatory post-stop exit consistency for successful inspection, preserving legitimate failure/cancellation and historical-schema semantics. Follow red -> green -> refactor and applicable offline regression/QA checks with >=95% first-party executed-line coverage and required unit/project-suite pass rates. Retain real red evidence and independent positive/negative oracles.

Return corrected source/build identity, changed-file manifest, fresh evidence paths/raw metrics and a per-defect resolution map for separately selected independent QA retest. Do not self-close QA findings, issue framework acceptance, launch native Codex, change operational configuration, install/deploy, or auto-invoke QA."""
write("dev-prompt.txt", prompt + "\n")

spec_table = "\n".join(f"| `{item['path']}` | `{item['sha256']}` |" for item in specs)
criterion_table = "\n".join("| " + " | ".join(row) + " |" for row in rows)
report = f"""# Independent Rust logging QA report

QA verdict: **FAIL**. Execution: **COMPLETED**. The unchanged candidate passes the declared numeric floors but its inspector accepts six inconsistent successful-run records, producing two OPEN mandatory defects. These are diagnostic evidence-validation defects; no protected-authority decision or unauthorized dispatch was demonstrated.

## Identity and scope

- Run/mode: 20260917T023835Z-qa / run. Plan readiness READY; no blocked required offline cases remain.
- Project: `{PROJECT}`. Native Windows x64, OS reports Microsoft Windows 10.0.26200, native C: filesystem; PowerShell7.6.6 at `C:\\Program Files\\PowerShell\\7\\pwsh.exe`. No Git metadata.
- Candidate: `{CANDIDATE}`;67 files bound in [candidate-manifest.json](candidate-manifest.json), SHA256 `{candidate_hash}`. All match the delivered development candidate and final readback.
- Plan: `{ROOT / 'plan.md'}`, SHA256 `{plan_hash}`; [plan-binding.json](plan-binding.json). Initial plan/inventory remain historical NOT_STARTED/NOT_RUN records; final state is in checkpoint/case-results.
- Selected inputs: [input-manifest.json](input-manifest.json), SHA256 `{input_hash}`;37 paths. Governing current AGENTS.md and installed `.agents/skills/qa` are included. No relevant saved-memory claim was used.
- Build identity: [binary-manifest.json](binary-manifest.json). Main compiled probe SHA256 `a91bba376364cbba4cdbeb9cf84904e401ef89f476fc965f043dc6294abb9151`; independent test binary SHA256 `3860be55202ec3298d5e027bcd089e738e19848d6702506736c13b179cfc8d23` in [independent-binary-v2.json](independent-binary-v2.json).
- Development delivery: `{PROJECT / 'docs/plan/framework-worker-logging/20260917T014842Z-dev/delivery.md'}` and sibling qa-handoff.md; bound in input-manifest. The supplied153/153 claim was independently rerun as152 package cases plus1 supplemental case, then13 fresh acceptance cases were added before execution.
- Effects: isolated offline builds, instrumentation, real synthetic Windows child processes/junctions, independent fixtures and retained evidence only. No product/developer-test edits, native Codex, installed-profile collection, installation, operational changes, deployment, framework acceptance or release decision.

The selected contract amendments control schema3, policy v3 and logging. Exact specifications are also indexed by [specification-bindings.json](specification-bindings.json):

| Selected source | SHA256 |
| --- | --- |
{spec_table}

## Acceptance traceability

LD-01..12 are local locators for the logging design's numbered acceptance cases. Grouped criterion rows retain every selected ID; [criterion-results.json](criterion-results.json) is the machine-readable map and [case-results.json](case-results.json) contains all166 unique cases. PASS rows are bounded to their stated offline behavior. Broader native/authority deliverables were not selected.

| Criterion/source | Required behavior | Case IDs | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
{criterion_table}

LD-01..11's exercised runtime stimuli passed, including original exit1 cases and additional independent exit29 cases. The new failures are in interpreting completed historical evidence (LD-12/LG-06), not an observed live stream-pump failure. LG-02/03 and inherited inspection aggregates are reduced where their evidence invariants are not enforced.

## Test integrity

[integrity.md](integrity.md) records the bounded source/attribute/assertion inspection. All67 selected files and the supplemental harness were inventoried; detailed semantics concentrated on changed runtime/test paths, WF bodies and shared helpers. Inherited attribute/import/assertion locations were inspected. No confirmed first-party mocking decorator/attribute, ignored test, coverage exclusion or result gaming was found. Serialization derives and explicit private fault seams were distinguished from mocks. This is not an exhaustive repository security review.

The real query_failed test duplicates the held Job handle without query permission and invokes the production QueryInformationJobObject mapping; it does not substitute a canned error. The full120-second watchdog and actual Windows child/descendant tests ran. No native Codex qualification follows from them.

All supplied package/supplemental results were freshly executed. QA independently authored13 conjunctive cases and literal byte/hash oracles, reviewed/read back helpers before use, and retained negative controls. QA-09 starts nine fresh real successful runs, confirms each unmodified control, then applies one planned mutation. It retains all observations and fails once if any invalid observation is accepted. Six were accepted; missing capture, missing status and malformed log controls were correctly rejected. This prevents inherited green tests from hiding the defect.

One QA-only preparation error occurred in attempt06-qa01 (junction command returned exit1). Its raw output and old helper/binary remain under that attempt. The documented one-attempt correction changed only QA command selection; attempt08-qa01 passed after rebuilt-helper binding. [harness-gap-01.md](harness-gap-01.md) records QA-H01. Root cause of the initial command syntax failure was not established; it is not a product defect. The same case counts once, and no product failure was retried or removed. The latest helper bindings are qa-helper-manifest-v2.json and independent-binary-v2.json; earlier manifests bind the retained earlier helper versions.

## Metrics and environments

Windows is the only selected platform, so its exact integer ratios are also the overall ratios. Threshold decisions compare counts without rounding; displayed decimals below are expansions of the exact ratios.

| Platform | Metric | Numerator | Denominator | Exact ratio / decimal percent | Floor | Result | Raw evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Windows/overall | Executed-line coverage |3858|4041|100*3858/4041 =95.47141796585003711952487008...|95%|PASS|coverage.json, coverage-analysis.json|
| Windows/overall | Required unit cases |49|49|100%|95%|PASS|03-coverage/stdout.txt, package-results.json|
| Windows/overall | Declared project suite |165|166|100*165/166 =99.39759036144578313253012048...|95%|PASS numerical floor only|case-results.json, metrics.json|
| Windows/overall | Package integration |103|103|100%|Included in project suite|PASS|03-coverage/stdout.txt|
| Windows/overall | Supplemental integration |1|1|100%|Included in project suite|PASS|21-supplement/stdout.txt|
| Windows/overall | Independent acceptance |12|13|100*12/13 =92.30769230769230769230769231...|No separate category floor; every case mandatory|FAIL conformance|08..20 attempts; QA-09 FAIL|

Coverage denominator: all15 `src/*.rs` files declared before execution;14 have executable lines, declaration-only lib.rs has none. No executable first-party file was excluded. Test/support fixtures and dependencies are excluded. The complete unfiltered152-case package campaign alone contributes coverage; SUP-01 and the13 independent cases do not. Collection completed once with exit0, no skipped cases and usable LLVM JSON. Raw coverage SHA256 `610db5cec92d19f6f8e3571f9bcb45e86631c397345930bb1ad48241cf0c813d`. This reproduces the reported95.47% without treating it as acceptance.

Tools: native Rust/Cargo1.97.1, rustfmt1.9.0, Clippy0.1.97, cargo-llvm-cov0.8.4, LLVM22.1.6; Cargo/Rust at `C:\\Users\\bryan\\.cargo\\bin`; Python3.10 at `C:\\Program Files\\Python310\\python.exe`. Exact executable vectors, cwd, environment overrides, times and exits are in [attempt-index.json](attempt-index.json) and per-attempt receipts. Cargo used existing offline locked dependencies; no installation.

BUILD, FMT and Clippy all-targets with `-D warnings`: PASS (01,22,23). Full coverage command completed in200.234seconds according to its receipt, including the production watchdog. Branch coverage: NOT_RUN; discovered collector advertises unstable branch collection and no nightly toolchain is installed. Linux, native Codex and native rendered UI are unqualified/not selected. No partial measurement was used to trigger or avoid a stop; complete unit, line and project-suite floors pass.

## Defects and unresolved work

| ID | Requirement | Issue class / impact | Failure | Ownership | Evidence |
| --- | --- | --- | --- | --- | --- |
| QA-LOG-01 OPEN | LG-02/03/06, LD-12, base inspection | MANDATORY_PRODUCT_DEFECT; false complete diagnostic evidence | drain=false, missing EOF, reader error or byte overflow still returns completed | dev; capture.rs::Capture::validate and journal.rs::inspect |16-qa09,24-cli-confirm; qa-fix.md|
| QA-LOG-02 OPEN | LG-02/06, base exit/inspection | MANDATORY_PRODUCT_DEFECT; missing/contradictory mandatory exit accepted | absent process_exit.worker_exit_code or29 versus terminal0 still returns completed | dev; journal.rs::inspect |16-qa09,24-cli-confirm; qa-fix.md|
| QA-H01 resolved harness gap | QA fixture preparation | QA-owned setup ERROR, not product failure | initial junction creation syntax error; retained, corrected once and passed | QA helper only; already resolved |06-qa01,07-helper-rebuild,08-qa01; harness-gap-01.md|

No advisory repair scope or unresolved specification decision was added. No mandatory offline case remains NOT_RUN. Native NI-T11/12 and WN-01/02, installed-profile qualification and branch measurement remain explicitly unperformed outside this selected offline case inventory; independent offline QA must pass before downstream native qualification under the contract.

## Continuation, stopping and remaining obligations

Attempt03 finished complete metrics before independent cases. Attempt06 produced a local harness gap;07 rebuilt the QA helper and08 completed that case. Attempt16 (2026-09-17T02:56:51.415399Z to02:56:52.819452Z) confirmed both ordinary mandatory defects. The decision retained final FAIL and continued ready, safe independent QA-10..13, supplemental, formatting and Clippy checks. Attempt24 used only the already-built CLI's read-only inspect command and confirmed both findings, exit0/state completed, with unchanged run bytes.

There was no terminal integrity, metric, critical authorization/security/data-loss, identity or ownership stop. The inspector false-success result did not demonstrate protected framework acceptance, unauthorized dispatch or unintended mutation of preserved data. No issue was downgraded from a terminal class and no speculative authority capability was assumed. Remaining cases were safe, source-bound and independent of the failed consistency predicates.

All24 command/confirmation receipts are terminal and none timed out. Actual test-held handles, stopped-tree results and joined readers provide process cleanup evidence; no historical PID was killed. No live tool session or pending owned invocation remains. QA fixture/junction directories and all target outputs are intentionally retained under this evidence root, including failed attempts. No assertion of repository-wide process absence or unobserved cleanup is made. There are no partially collected mandatory metrics or blocked dependents.

## Disposition

Product QA outcome: **FAIL**, because QA-LOG-01/02 violate mandatory criteria despite passing numeric floors. Repair owner: **dev**. [qa-fix.md](qa-fix.md) is the bound correction/retest packet; its final SHA256 is the `qa-fix.md` entry in handoff-manifest.json. Only an explicitly selected independent retest can close these OPEN findings after a corrected candidate is supplied.

Final identity readback: all67 candidate files,116 original/snapshot files,37 input files and current helper/build identities match; see final-identity-check.json. PowerShell helper remains unchanged. External framework acceptance: **NOT_EVALUATED**. Release/deployment authorization: not granted.

## Artifact delivery

Original selection: `{PROJECT / 'docs/plan/framework-worker-logging'}`. Literal fresh destination: `{ROOT}`. Required artifacts are plan.md, qa-report.md, qa-fix.md, checkpoint.json, input/candidate/specification manifests, criterion-results.json, case-results.json, raw attempts and final external bindings. All are published at these paths; final publication readback is recorded by final-readback.json after hashing.

The external `{ROOT / 'handoff-manifest.json'}` records required and actual absolute paths, byte lengths and SHA256. Exact cross-reference entry keys include `qa-report.md`, `qa-fix.md`, `checkpoint.json`, `plan.md`, `candidate-manifest.json`, `input-manifest.json`, `specification-bindings.json`, `evidence-manifest.json` and `dev-prompt.txt`. It does not hash itself. evidence-manifest.json binds regular retained evidence while excluding Cargo target intermediates; produced binaries are separately bound. Junctions are recorded without traversing them. Any final write/readback error prevents a delivered claim and must be repaired only at this original destination; see final-readback.json for actual completion.

## End-user handoff

Open `{PROJECT}` in Codex on native Windows. Next owner/action: dev repairs the two selected defects in a fresh sibling candidate, then returns a candidate for separately selected QA retest. Current host skill catalog exposes `dev` at `{PROJECT / '.agents/skills/dev/SKILL.md'}`; it was not invoked or installed by QA. No additional approval or skill-installation prerequisite blocks the manual handoff.

Paste into the Codex conversation input (not PowerShell); final conversation also supplies the external manifest's SHA256:

```text
{prompt}
```
"""
write("qa-report.md", report)

fix = f"""# QA remediation handoff to dev

## Selected candidate and authority

QA run: 20260917T023835Z-qa, verdict **FAIL**, execution COMPLETED. Report: `{ROOT / 'qa-report.md'}`; SHA256 is the exact `qa-report.md` entry in `{ROOT / 'handoff-manifest.json'}`. This packet's digest is its `qa-fix.md` entry. Repair is a manual next invocation; QA has not changed product source or invoked dev.

Failed candidate: `{CANDIDATE}`,67 files; candidate-manifest.json SHA256 `{candidate_hash}`. Main compiled executable in `{ROOT / 'build-target/debug/devforgeai-codex-worker-probe.exe'}` has SHA256 `a91bba376364cbba4cdbeb9cf84904e401ef89f476fc965f043dc6294abb9151`. Plan SHA256 `{plan_hash}`. Exact original specification paths/hashes are in specification-bindings.json (8 contracts/clarifications), input-manifest.json (37 selected inputs; SHA256 `{input_hash}`), and the report table.

Project/environment: `{PROJECT}`, native Windows x64 / PowerShell7.6.6 / native C: filesystem; Rust/Cargo1.97.1, locked offline dependencies. Evidence destination: `{ROOT}`. Current AGENTS.md and applicable development skill govern any future implementation. Mandatory first-party executed-line and required unit/project-suite floors remain independently >=95%; failed mandatory behavior cannot be waived by the percentages.

Remediation owner: **dev**. Selected defects: **QA-LOG-01, QA-LOG-02**, both OPEN. Proposed manual repair output: `{CORRECTED}` (verified absent during QA handoff preparation). Preserve the failed candidate in place; create fresh corrected source/evidence without resetting, installing or overwriting existing attempts. Scope is Rust capture/inspection consistency and specification-aligned regression tests; expand only as necessary for these two demonstrated defects. No native Codex, operational configuration, PowerShell helper edits, installation, deployment, protected acceptance or automatic retest is selected.

## Shared reproduction and evidence

QA-09 is implemented at qa-harness/independent.rs:217. For each of9 planned mutations it creates a fresh schema3/debug successful WF-01 run, observes exit0 with stopped tree and unchanged fixture, verifies the original inspector returns completed, preserves journal-before.jsonl, changes one capture/exit/status/log condition, and records mutation-result.json. Six invalid variants return Ok/completed. The other three controls (missing capture, missing status, malformed log) correctly reject. The final test assertion fails once; it does not retry the product or inflate case counts.

Original full command/environment: attempts/16-qa09/receipt.json; raw assertion: attempts/16-qa09/stdout.txt; Cargo exit101. All records are externally bound by evidence-manifest.json. A future fresh execution must allocate its own fixture/attempt path and verify current identities first; do not rerun the existing exclusive recorder attempt.

The retained binary can reproduce the false inspector observations without any worker launch. From `{PROJECT}` in PowerShell, the following exact commands were independently exercised in attempt24:

```powershell
& '{ROOT / 'build-target/debug/devforgeai-codex-worker-probe.exe'}' inspect --run-dir '{ROOT / 'attempts/16-qa09/fixtures/qa09rE4EEf/run'}' --after 0 --limit 100
& '{ROOT / 'build-target/debug/devforgeai-codex-worker-probe.exe'}' inspect --run-dir '{ROOT / 'attempts/16-qa09/fixtures/qa09cCNcpd/run'}' --after 0 --limit 100
```

Both exit0 with state completed. attempts/24-cli-confirm/receipt.json records executable hash, exact argv/cwd, elapsed time and unchanged=true for each run. This is confirmation through the compiled public CLI, not only a library assertion. Fixtures retain absolute bindings to the selected peer, source and fixture directories; preserve those bytes and paths when inspecting historical evidence.

## Defect QA-LOG-01

- State/class: OPEN, MANDATORY_PRODUCT_DEFECT, nonterminal. Mandatory conformance failure with false successful evidence; no demonstrated protected-authority or data-loss impact. Safe independent checks continued after attempt16; final verdict stayed FAIL.
- Requirements: logging-contract.md LG-02 (mandatory capture), LG-03 (digest complete only with EOF and no capture-preventing error/overflow), LG-06 (valid current completed observations), logging-design.md acceptance12; base contract inspection consistency.
- Ownership/artifact: application Rust, `{CANDIDATE / 'src/capture.rs'}` Capture::validate lines80..100 and `{CANDIDATE / 'src/journal.rs'}` inspect lines363..380,406..485. QA-created fixtures are the stimulus, not the defective artifact.
- Verified source mechanism: Capture::validate rejects EOF/read errors only when drain_complete is true, and does not reject byte_overflow in a claimed successful completion. inspect validates the capture shape then retains only exit_summary=true, so successful terminal checks do not enforce the required complete-capture condition. This verified explanation is limited to the demonstrated paths, not an exhaustive cause analysis.
- Preconditions: bound schema3 inputs, debug diagnostics, valid successful peer/control, preserved binary/fixture paths; native Windows. No native Codex or external credentials.

| Fixture under attempts/16-qa09/fixtures | Changed process_exit field(s) | Expected | Observed |
| --- | --- | --- | --- |
|qa09rE4EEf|capture.drain_complete=false|Reject inconsistent completed evidence|Ok/state completed|
|qa09LmAQen|capture.stdout.eof=false and drain_complete=false|Reject incomplete capture claiming completion|Ok/state completed|
|qa09pPRBRh|capture.stdout.read_error=pipe_read_failed and drain_complete=false|Reject reader failure claiming completion|Ok/state completed|
|qa09W3tEW5|capture.stdout.byte_overflow=true|Reject overflow claiming complete capture|Ok/state completed|

Each directory has journal-before.jsonl, run/journal.jsonl, result.json and mutation-result.json. Original terminal outcome, worker code0, valid optional log/status and successful control remain otherwise unchanged. The first variant is also reproduced through CLI as above. Evidence reproduction is **CONFIRMED**; optional sink/hash checks did not catch these semantic contradictions.

Required correction: inspection must enforce completion semantics for current capture-bearing records and reject inconsistent successful completion. Retain the typed capture state through the terminal decision or use another sound equivalent. Do not merely set drain_complete/EOF true, erase error/overflow fields, suppress failed tests, or accept a byte hash as proof of complete capture. No particular speculative algorithm is required.

Compatibility: legitimate historical schemas must remain inspectable. A failed/cancelled/timed-out/cleanup-uncertain run may truthfully report incomplete capture; do not globally reject every explicit failure observation as malformed. Off still requires mandatory capture/status but no optional file. Optional diagnostics incompleteness remains nonauthoritative. Pre-stop exit remains a temporal observation, not proof of self-exit or crash.

Required regressions: preserve each independently mutated success/control pair above, include both streams and valid historical/failure controls, assert the public inspect result/code is appropriate and leaves bytes unchanged. Preserve actual reader-budget/EOF/error tests and no worker launch on inspection. Recheck affected integration, fmt/Clippy, integrity, and complete source/metric collections for the corrected bytes.

Retest condition: explicitly select the corrected candidate and this defect for independent QA; rerun the failure predicates against fresh completed evidence plus affected regressions. Only independent QA can mark VERIFIED_FIXED. No tests were stopped; QA-09's original FAIL remains. Owned child cleanup completed before evidence mutation; all test invocations ended. Dependencies: shares current capture-bearing terminal validation with QA-LOG-02; neither requires resolving a missing specification decision.

## Defect QA-LOG-02

- State/class: OPEN, MANDATORY_PRODUCT_DEFECT, nonterminal. A required exit observation is missing or conflicts with the successful terminal while inspect still reports completed. No demonstrated runtime authorization or protected framework acceptance.
- Requirements: logging-contract.md LG-02 mandatory post-stop code and LG-06 valid current completed evidence; base contract sections4/7 exit/inspection consistency.
- Ownership/artifact: application `{CANDIDATE / 'src/journal.rs'}` inspect lines363..380 (deserialization/presence handling),432..483 (success checks). Source citations were numbered/read immediately before handoff.
- Verified mechanism: process_exit.worker_exit_code is indexed into serde_json::Value and deserialized as Option<u32>; an absent key becomes Null/None. Unlike pre_stop_exit_code, its key presence is not checked. The parsed post-stop value is discarded and never compared with terminal.worker_exit_code; successful terminal validation checks only its own zero code.
- Preconditions: same real successful schema3/debug control and native Windows retained fixtures as above.

| Fixture under attempts/16-qa09/fixtures | Mutation | Expected | Observed |
| --- | --- | --- | --- |
|qa09cCNcpd|process_exit.worker_exit_code=29; terminal.worker_exit_code stays0|Reject contradictory mandatory exit evidence|Ok/state completed|
|qa09j98aey|Delete process_exit.worker_exit_code|Reject absent mandatory post-stop observation|Ok/state completed|

Reproduction is **CONFIRMED** by the independent mutation case; the contradictory value also reproduces through the compiled CLI command above. The same four retained artifact names apply. Exact hashes are in evidence-manifest.json; original successful result/control and unchanged diagnostic file remain available.

Required correction: enforce schema-dependent mandatory field presence and valid typed post-stop observations, then reconcile current success terminal codes with the corresponding process_exit record. A successful observation requires the independently observed successful exit that its terminal claims. Preserve appropriate nullable observations for legitimate failed cleanup/query situations rather than inventing an exit code. Do not conflate pre-stop/post-stop timing or merely copy the terminal code into missing evidence.

Required regressions: missing key versus explicit null where semantically permitted, nonzero/zero contradictions, matching successful zero and legitimate nonzero failed outcomes, both completed and preflight_checked success branches where applicable, historical-schema compatibility, read-only CLI behavior and no replay. Keep native-profile test controls synthetic; no native Codex launch is required for this repair. Run affected and full declared offline regressions/metrics with unchanged denominator policy.

Retest condition: separately select corrected identity and QA-LOG-02 for independent failure/compatibility checks; development's repair claim becomes FIX_REPORTED only, not closure. No tests remain stopped or unexecuted from this run. Cleanup is the same verified stopped child/control state; no historical PID action occurred. Dependency: QA-LOG-01 shares journal validation, so coordinated focused correction is reasonable without widening scope.

## Return contract from dev

Return a fresh corrected candidate/build identity and changed-file manifest, per-defect correction/evidence references and state FIX_REPORTED, actual red/green/refactor results, raw required-unit/project-suite counts and complete first-party line coverage, compatibility/negative-path results, and exact paths/environment for independently selected retest. Preserve all original failure records and the unchanged failed candidate. No model/Python report may issue protected framework acceptance.

## Pending prerequisites or specification decisions

None blocks scoped offline repair. QA-H01 was a resolved QA-only setup gap, not a selected dev defect. Branch coverage remains NOT_RUN with the current stable collector capability; no tool installation is implied. Native Codex/installed-profile qualification remains separately selected after offline QA passes. Current findings do not establish a need for native execution or operational changes.

## End-user remediation invocation

Open `{PROJECT}` using native Windows PowerShell in Codex. The current host skill catalog exposes dev at `{PROJECT / '.agents/skills/dev/SKILL.md'}`. Paste this into the Codex conversation input; QA does not send it or initiate the repair:

```text
{prompt}
```
"""
write("qa-fix.md", fix)

# Preserve the original checkpoint before updating the current restart record.
write("checkpoint-before-execution.json", (ROOT / "checkpoint.json").read_text(encoding="utf-8-sig"))
checkpoint = {
    "intent": "run", "plan_readiness": "READY", "execution_status": "COMPLETED", "verdict": "FAIL",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "candidate_manifest": "candidate-manifest.json",
    "input_manifest": "input-manifest.json", "specification_manifest": "specification-bindings.json",
    "plan_binding": "plan-binding.json", "case_results": "case-results.json", "criterion_results": "criterion-results.json",
    "attempts": "attempt-index.json", "completed_command_receipts": 24, "stop_trigger": None,
    "findings": [{"id": "QA-LOG-01", "state": "OPEN", "class": "MANDATORY_PRODUCT_DEFECT", "terminal_stop": False}, {"id": "QA-LOG-02", "state": "OPEN", "class": "MANDATORY_PRODUCT_DEFECT", "terminal_stop": False}],
    "owned_processes": [], "owned_process_basis": "All24 invocation/confirmation receipts ended without timeout; real test-held handles and successful stopped-tree checks provide bounded child cleanup evidence. No repository-wide PID absence claim.",
    "retained_fixtures": "attempts/*/fixtures and QA-owned Cargo targets remain preserved; no automatic replay or deletion",
    "remaining_required_offline_cases": [], "native_codex": "NOT_RUN", "branch_coverage": "NOT_RUN", "framework_acceptance": "NOT_EVALUATED",
    "next_owner": "dev", "next_safe_action": "Manual dev remediation for QA-LOG-01 and QA-LOG-02; no automatic repair/retest. Verify current rules and all bound identities first; report drift.",
    "report": str(ROOT / "qa-report.md"), "fix": str(ROOT / "qa-fix.md"), "handoff_manifest": str(ROOT / "handoff-manifest.json"),
}
(ROOT / "checkpoint.json").write_text(json.dumps(checkpoint, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"published": ["specification-bindings.json", "criterion-results.json", "qa-report.md", "qa-fix.md", "dev-prompt.txt", "checkpoint.json"], "verdict": "FAIL", "findings": ["QA-LOG-01", "QA-LOG-02"]}, indent=2))
