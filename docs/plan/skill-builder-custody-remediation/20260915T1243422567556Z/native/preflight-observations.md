# Native preflight and retained early attempts

## Environment

- Selected development source: `C:/Projects/DevForgeAI/src/agents/skills/skill-builder`.
- Windows Python: `C:/Program Files/Python310/python.exe`, 3.10.11. Codex: `C:/Users/bryan/AppData/Local/Programs/OpenAI/Codex/bin/codex.exe`, 0.154.0. Python platform API reported Windows build 10.0.26200. CIM OS caption access was denied, so no more specific edition claim is made.
- Ubuntu preflight: `pwd -P` returned `/tmp`; `uname -srm` returned `Linux 6.18.33.2-microsoft-standard-WSL2 x86_64`; Python `/usr/bin/python3`, 3.12.3; Codex `/home/bryan/.local/bin/codex`, 0.154.0. Discovery was performed in a login Bash shell, whereas direct WSL Python did not inherit its Codex PATH entry. Later harness arguments explicitly select that executable.
- The runner invokes Codex directly; Windows child command events show PowerShell 7. Windows fixtures are on the selected Windows filesystem. Linux fixture writes are planned under native `/tmp`, with source copied from `/mnt/c` and compared by per-file digest. Linux fixtures do not switch the selected checkout.

## Windows simple, repaired snapshot V1

`windows-simple` failed during Codex app-server initialization with Access denied, before task execution. Its exit code 1, stderr and manifests remain retained. This is a host/sandbox failure, not a skill defect.

The approved fresh host attempt `windows-simple-002` used the same 120-second ceiling. It read the selected builder, produced original requirement and design inputs, and invoked `begin`. Its first authored contract used a descriptive history value instead of the required `no_known_history`; the helper returned BLOCKED with no destination writes. The child retained that failed run, corrected its contract in a fresh linked run and reached a design-enabled stage including `stage-integrity.json`.

The parent runner then timed out at 120.547 seconds. `taskkill /T /F` returned 0 and recorded descendant termination. The destination package, publication receipt, successful baseline and manual handoff were absent. Therefore the full simple native workflow is **INCOMPLETE**, not PASS. The timeout is an execution ceiling, not a measured product performance requirement. No automatic retry is authorized/performed for that timeout.

The copied V1 input fixture remained byte-identical. The runner reports the source checkout changed because the parent performed its separately tracked V2 diagnostic correction while this frozen V1 trial was running. The V1 observation cannot qualify final V3 bytes.

## Linux initial setup and interrupted approval

The first `linux-simple` harness reached `subprocess.Popen` with a null executable because direct WSL invocation did not find `codex` in PATH. The tool returned a TypeError before starting Codex. This is a harness setup error. The runner now accepts an explicit `--codex` argument.

The requested `linux-simple-002` launch with `/home/bryan/.local/bin/codex` was interrupted while its tool/approval was pending, after 609 seconds, without a returned session ID or native attempt result. It is not counted as executed native testing. A subsequent approved read-only check found no matching harness/Codex-project processes and found the entire `/tmp/devforgeai-custody-native-20260915T1243422567556Z` directory absent. Its disappearance has no established cause. The setup error is retained in conversation tool evidence and described here; no surviving Linux file evidence is claimed for it.

The root agent owns fresh V3 Linux simple/branching and Windows branching launches, and immediate retention of Linux evidence. This note is a preflight/early-attempt record, not the final four-case assessment.
