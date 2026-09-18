# Development delivery after Linux/WSL testing

Overall development status **PARTIAL**. The Windows tray repair and Windows 95% line floor have current developer evidence; the extended Linux/WSL measurements fail 95%, Unix Clippy fails, and the bridge pause/identity scenario is incomplete due to the missing test fixture. No QA findings are self-closed and no framework acceptance is issued.

Selected scope: QA-D01/QA-D02 remediation under spec SHA256 `52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4`, initially native Windows, then the user's requested WSL/Linux coverage tests via the supplied SSH host. Source manifest SHA256 `cf3ee99015db0dcc1eb544fdac1bfdb0fcd2f10bfc8b749857d52740d8258094`; [runtime-artifacts.json](runtime-artifacts.json) SHA256 `b1410d025148294ca577fce097ad12e8601de82f36163aa889f86d1ca8a668ac`. All three measured hosts used these same 61 source/test/config/resource files by normalized path and hash. [Changed files](changed-files.json) and [candidate diff](candidate.diff) account for 14 modified and 13 added application files; 34 original files remain unchanged.

| Platform | Executed lines | Original declared units | Selected product cases | Result |
| --- | --- | --- | --- | --- |
| Windows | 3314/3486 = 95.065978% | 18/18 | 90/90 | Line floor, build, fmt, Clippy PASS |
| SSH Linux | 2410/2830 = 85.159011% | 18/18 | 75/75 | Coverage and Clippy FAIL |
| WSL Linux | 2418/2830 = 85.441696% | 18/18 | 75/75 | Coverage and Clippy FAIL |

Separate Windows-to-WSL bridge invocation: 1/2 passed; pause/identity test could not obtain an envelope, and subsequent inspection found its configured fixture absent. Retained as incomplete fixture evidence, not a confirmed product failure. Two setup cases on each platform receive no product credit. Branch coverage NOT_RUN. No full required-platform acceptance percentage is claimed.

QA-D01: actual generation/reconciliation fields rendered with honest unknown values; original independent oracles, developer cases and inspected native screenshot pass. QA-D02: Windows floor repaired; Linux and WSL floor still fail. New developer test portability issue: ungated Windows-only imports cause Unix Clippy failures. Prior QA-G02..05 remain unresolved; WSL Cargo coverage is now measured but QA-G01/DS-005/006 full native bridge/lifecycle qualification remains incomplete.

Detailed Windows red/green/refactor/QA evidence, production rationale, artifact hashes and screenshot: [Windows delivery](delivery.md). New host commands, integer metrics, profile/build identities, portability/fixture failures and preservation: [Linux/WSL extension report](platform-extension-001/extension-report.md). These reports are complementary; this final delivery governs overall status. [handoff-manifest.json](handoff-manifest.json) and [verification.json](verification.json) bind all promised outputs to the original selected root `C:\Projects\DevForgeAI\docs\plan\index-service-remediation\20260914T1950304158791Z` and read back candidate, build, input and profile hashes.

Source and original QA oracles/evidence were preserved. No original remote checkout was overwritten, no installation/deployment/startup/systemd or operational changes were made. Owned processes were stopped/absent at recorded readback; SSH closed. Retain all old attempts and use a new evidence directory for corrections/retests. Next owner dev for remaining coverage/import/fixture work, then independent QA. Framework acceptance NOT_EVALUATED.
