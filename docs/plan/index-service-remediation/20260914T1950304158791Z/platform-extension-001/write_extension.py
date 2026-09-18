import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
RUN = ROOT.parent
PROJECT = Path(r"C:\Projects\DevForgeAI\devforgeai")
def read(path): return json.loads(path.read_text(encoding="utf-8-sig"))
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
qa_inventory = read(Path(r"C:\Projects\DevForgeAI\docs\plan\index-service-qa\20260914T184442947070Z\executions\20260914T191133863776Z\executed-test-inventory.json"))
categories = {row["id"]:row["category"] for row in qa_inventory if row["platform"] == "windows"}
results = {}
build_rows = []
for host in ["linux", "wsl"]:
    directory = ROOT / host
    completion = read(directory / "completion.json")
    tests = re.findall(r"^test (\S+) \.\.\. (ok|FAILED|ignored)(?:, ([^\n]*))?$",(directory / "attempts/coverage/stdout.txt").read_text(),re.M)
    inventory = [{"id":name,"outcome":status,"reason":reason,"category":categories.get(name,"new regression")} for name,status,reason in tests]
    units = [row for row in inventory if row["category"] == "unit"]
    assert len(units) == 18 and all(row["outcome"] == "ok" for row in units)
    result = read(directory / "observed-metrics.json")
    result.update(original_declared_units={"passed":18,"required":18}, product_cases={"passed":75,"required":75},setup_cases={"passed":2,"required":2},source_manifest_sha256=digest(RUN / "source-manifest.json"),branch_coverage="NOT_RUN")
    (directory / "metrics.json").write_text(json.dumps(result,indent=2)+"\n")
    (directory / "test-inventory.json").write_text(json.dumps(inventory,indent=2)+"\n")
    assert not completion["remaining_owned_processes"]
    for row in completion["binaries"]:
        build_rows.append(f"| {host} | `{row['path']}` | `{row['sha256']}` |")
    results[host] = result
wsl_readback = read(ROOT / "wsl-final-readback.json")
assert wsl_readback["exit_code"] == 0
readback = json.loads(wsl_readback["stdout"])
assert not readback["source_drift"] and not readback["remaining_owned_processes"]
(ROOT / "wsl-fixture.json").write_text(json.dumps({"configured_executable":"/tmp/dfr-wsl-20260914T1950304158791Z/bin/examples/wsl_fixture", "observed_pretest_copy_hashes":[{"name":Path(row["path"]).name,"sha256":row["sha256"]} for row in readback["retained_builds"]], "post_test_readback":readback,"pretest_hash_source":"native copy command tool output; hashes match retained WSL release build manifest", "bridge_outcome":"1 passed, 1 failed; absent fixture in post-run readback; no automatic retry"},indent=2)+"\n")
rows = "\n".join(build_rows)
report = f"""# Linux and WSL coverage extension

**FAIL for both measured line-coverage floors and Unix Clippy.** All collected Linux unit/integration tests pass, including the repaired tray formatter assertions. The Windows-to-WSL bridge pause/identity test remains incomplete due to a fixture error. This is developer testing, not independent QA closure.

The user extended the active task with “test wsl & linux coverage” and supplied `me@192.168.245.128`. The corrected candidate is unchanged: parent [source-manifest.json](../source-manifest.json), SHA256 `{digest(RUN / 'source-manifest.json')}`. Selected spec SHA256 `52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4`. No product edits or remote checkout synchronization occurred during this test extension.

| Check | SSH Ubuntu 26.04.1 | WSL2 Ubuntu 24.04.5 |
| --- | --- | --- |
| Native source identity | 61 files match corrected candidate | 61 files match corrected candidate |
| Executed-line coverage | **2410/2830 = 85.15901060070671%, FAIL** | **2418/2830 = 85.4416961130742%, FAIL** |
| Cargo product cases | 75/75 PASS | 75/75 PASS |
| Original declared units (subset) | 18/18 PASS | 18/18 PASS |
| Setup cases, no product credit | 2/2 PASS | 2/2 PASS |
| Formatting | PASS, exit 0 | PASS, exit 0 |
| Clippy all targets, -D warnings | FAIL, exit 101 | FAIL, exit 101 |
| Release binaries and WSL example | PASS, exit 0 | PASS, exit 0 |
| Branch coverage | NOT_RUN | NOT_RUN |

All 77 collected cases ran on each Linux host; no ignored/failed Cargo cases. Native Windows-only test modules are not applicable inside Linux and are not claimed as Linux passes. Windows-to-WSL tests run separately on Windows. Counts are per unique case per host, not accumulated attempts. Full acceptance and integrity inventories remain incomplete.

Evidence: [Linux metrics](linux/metrics.json), [Linux raw coverage](linux/coverage.json), [Linux test output](linux/attempts/coverage/stdout.txt), [Linux completion/builds](linux/completion.json); [WSL metrics](wsl/metrics.json), [WSL raw coverage](wsl/coverage.json), [WSL test output](wsl/attempts/coverage/stdout.txt), [WSL completion/builds](wsl/completion.json). Each host has exact argv/cwd/environment/source-bound receipts under `attempts/`, native tool versions in `tools.json`, a unique test inventory, profile-manifest.json and retained raw/merged profiles. Source/build paths remain native Linux paths, not `/mnt/c` build trees.

## Observed gaps

QA-D02 still fails on Linux and WSL. The largest gaps are CLI (229 uncovered Linux, 227 WSL), tray shared support (48 each), platform support (42 Linux, 37 WSL), service (35 Linux, 34 WSL), and client (23 each). Coverage counts all 13 compiled first-party files including binaries. Original exclusions remain tests/examples/fixtures, dependencies and generated code; no first-party behavior is removed or suppressed. A successful test process does not waive the 95% floor.

Additional portability regression observed in developer tests: `tests/coverage_edges.rs:3` imports `platform` outside its Windows-only uses; WSL Clippy also reports `tests/platform.rs:48` importing `Path` outside its Windows-only block. These are strict unused-import failures, not Rust build or runtime failures. Both native Clippy receipts and stderr are retained. They require a focused developer correction and subsequent source-matched checks; no warning suppression or source mutation was used to make this testing result pass.

## Native Windows-to-WSL bridge

[bridge/receipt.json](bridge/receipt.json) records `cargo test --locked --offline --test wsl_bridge -- --ignored --test-threads=1`, Windows cwd and explicit `DEVFORGEAI_WSL_FIXTURE`, against the same candidate. Exit 101: `stopped_distribution_is_never_invoked_by_a_status_poll` PASS; `native_wsl_bridge_preserves_pause_and_environment_identity` FAIL before obtaining its initial handshake envelope (`WslCliMissing`, child exit 1). The passing probe uses a deliberately absent distribution, so it does not qualify the installed-but-stopped distribution lifecycle matrix.

The native fixture binaries were copied with matching SHA256 to a short isolated `/tmp` path before the test, to respect Unix socket path limits. [Post-run diagnostic readback](wsl-final-readback.json) found that directory and executable absent; the persistent build binaries and candidate still match. This supports an unresolved fixture/setup ERROR, not a confirmed product bridge defect. The cause and exact removal time were not established. No automatic retry occurred and no successful pause/identity claim is made. A later selected continuation should use a persistent short fixture location, verify it immediately before invocation, retain this attempt and run a new attempt.

## Identities and preservation

SSH isolated project: `/home/me/Projects/index-qualification.iIHbKX/DevForgeAI/dev-remediation/20260914T1950304158791Z/devforgeai`. Existing `/home/me/Projects/index-qualification.iIHbKX/DevForgeAI/devforgeai` was read, not modified; its 48 original entries had no drift and the complete before/after snapshot matches. Remote AGENTS.md was read; Git metadata absent and Git executable unavailable. Native Rust 1.93.1, cargo-llvm-cov 0.9.1, LLVM 21.1.8.

WSL isolated project: `/home/bryan/Projects/devforgeai-remediation-20260914T1950304158791Z/devforgeai`. The unrelated `/home/bryan/Projects/DevForgeAI` checkout was not selected or changed. Native Rust 1.98.1, cargo-llvm-cov 0.9.0 and its bundled LLVM. The installed Ubuntu distribution was started for user-requested tests; docker-desktop was not selected or changed.

[Transfer manifest](transfer-manifest.json) binds candidate archive SHA256 `30b2cd9d0ace40fef3109af5c7194408629f0c1f6f7ed76ea3f521d0b8088dbd`, checked before extraction on both hosts. Fetched evidence archive hashes were checked before safe local extraction: Linux `4ce12761fe4f1c5a52ae576825d133c8c171d7291586eb60671f832d91665744`; WSL `72a8832a7d1626af1c6c98218c188ec630a5b53aa0591d29b5a32dee116b486a`. These preserve native paths and raw receipts; local relocation does not imply execution on Windows.

| Host | Built artifact retained at native path | SHA256 |
| --- | --- | --- |
{rows}

The user-supplied credential was used only for SSH authentication and is absent from evidence files. No installation, deployment, dependency upgrade, startup/systemd changes, operational skill edits, or original checkout overwrite occurred. Remote completion and final WSL readback show no owned product process remaining. The SSH session was closed. Initial sandbox WSL enumeration AccessDenied was separately followed by approved native discovery; no setup error was counted as a behavioral pass.

Evidence root is exactly `{ROOT}`, as bound in [context.md](context.md) before native writes. [extension-manifest.json](extension-manifest.json) and parent verification.json provide path/hash readback. The earlier parent Windows-only draft report is historical scope; this report supersedes its Linux/WSL NOT_RUN statements with current measured failures.

Next owner: dev for Linux/WSL coverage gaps and Unix test-import correction, followed by independent QA retest of the corrected candidate. Bridge fixture continuation remains separate from product defect confirmation. QA-D01/D02 stay OPEN until independent QA; full qualification INCOMPLETE; framework acceptance NOT_EVALUATED.
"""
(ROOT / "extension-report.md").write_text(report,encoding="utf-8")
final = f"""# Development delivery after Linux/WSL testing

Overall development status **PARTIAL**. The Windows tray repair and Windows 95% line floor have current developer evidence; the extended Linux/WSL measurements fail 95%, Unix Clippy fails, and the bridge pause/identity scenario is incomplete due to the missing test fixture. No QA findings are self-closed and no framework acceptance is issued.

Selected scope: QA-D01/QA-D02 remediation under spec SHA256 `52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4`, initially native Windows, then the user's requested WSL/Linux coverage tests via the supplied SSH host. Source manifest SHA256 `{digest(RUN / 'source-manifest.json')}`; [runtime-artifacts.json](runtime-artifacts.json) SHA256 `{digest(RUN / 'runtime-artifacts.json')}`. All three measured hosts used these same 61 source/test/config/resource files by normalized path and hash. [Changed files](changed-files.json) and [candidate diff](candidate.diff) account for 14 modified and 13 added application files; 34 original files remain unchanged.

| Platform | Executed lines | Original declared units | Selected product cases | Result |
| --- | --- | --- | --- | --- |
| Windows | 3314/3486 = 95.065978% | 18/18 | 90/90 | Line floor, build, fmt, Clippy PASS |
| SSH Linux | 2410/2830 = 85.159011% | 18/18 | 75/75 | Coverage and Clippy FAIL |
| WSL Linux | 2418/2830 = 85.441696% | 18/18 | 75/75 | Coverage and Clippy FAIL |

Separate Windows-to-WSL bridge invocation: 1/2 passed; pause/identity test could not obtain an envelope, and subsequent inspection found its configured fixture absent. Retained as incomplete fixture evidence, not a confirmed product failure. Two setup cases on each platform receive no product credit. Branch coverage NOT_RUN. No full required-platform acceptance percentage is claimed.

QA-D01: actual generation/reconciliation fields rendered with honest unknown values; original independent oracles, developer cases and inspected native screenshot pass. QA-D02: Windows floor repaired; Linux and WSL floor still fail. New developer test portability issue: ungated Windows-only imports cause Unix Clippy failures. Prior QA-G02..05 remain unresolved; WSL Cargo coverage is now measured but QA-G01/DS-005/006 full native bridge/lifecycle qualification remains incomplete.

Detailed Windows red/green/refactor/QA evidence, production rationale, artifact hashes and screenshot: [Windows delivery](delivery.md). New host commands, integer metrics, profile/build identities, portability/fixture failures and preservation: [Linux/WSL extension report](platform-extension-001/extension-report.md). These reports are complementary; this final delivery governs overall status. [handoff-manifest.json](handoff-manifest.json) and [verification.json](verification.json) bind all promised outputs to the original selected root `{RUN}` and read back candidate, build, input and profile hashes.

Source and original QA oracles/evidence were preserved. No original remote checkout was overwritten, no installation/deployment/startup/systemd or operational changes were made. Owned processes were stopped/absent at recorded readback; SSH closed. Retain all old attempts and use a new evidence directory for corrections/retests. Next owner dev for remaining coverage/import/fixture work, then independent QA. Framework acceptance NOT_EVALUATED.
"""
(RUN / "final-delivery.md").write_text(final,encoding="utf-8")
(RUN / "final-checkpoint.md").write_text(f"""# Final checkpoint

Recorded {datetime.datetime.now(datetime.timezone.utc).isoformat()}. User-expanded scope is documented in platform-extension-001/context.md. Supersedes the earlier Windows-only checkpoint for platform status; source/build identity and ownership remain unchanged.

Candidate source-manifest SHA256 `{digest(RUN / 'source-manifest.json')}`; retained Windows source candidate/ and release binaries runtime/. All native Linux copies byte-match this candidate. Full delivery and defect map: final-delivery.md and platform-extension-001/extension-report.md; output binding/readback: context.md, handoff-manifest.json, verification.json.

Windows remediation tests and 95% line floor PASS. Linux 85.159011% and WSL 85.441696% coverage FAIL; all product Cargo cases pass. Both Unix Clippy runs FAIL on Windows-only test imports. Bridge 1 pass/1 fixture failure retained, no retry. Post-run configured fixture absent; persistent WSL builds and source match. No owned product process remained at recorded readbacks; SSH session closed.

No new product edits during the user-selected testing extension. Resume by hashing source/spec/rules and remote copies, reading failures and checking current process/fixture state. Do not overwrite old evidence, silently restore source, suppress uncovered first-party behavior, or treat fixture errors as product passes. Remaining implementation/testing work: Unix imports, meaningful Linux/WSL coverage additions, persistent bridge fixture continuation, then independent QA. Original broader qualification gaps remain; no QA closure or framework acceptance.
""",encoding="utf-8")
print(json.dumps({"final_delivery":str(RUN / "final-delivery.md"),"extension_report":str(ROOT / "extension-report.md"),"candidate":digest(RUN / "source-manifest.json")}))
