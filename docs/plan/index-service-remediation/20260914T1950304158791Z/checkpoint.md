# Remediation checkpoint

Checkpoint recorded 2026-09-14T21:29:31.214848+00:00.

Selected project `C:\Projects\DevForgeAI\devforgeai`; native Windows QA-D01/QA-D02 remediation under the selected MVP spec and user-provided exact QA handoff. [context.md](context.md) and [inputs.json](inputs.json) preserve the intake and authorization boundaries. Overall multi-platform development status PARTIAL; Windows developer remediation checks pass and are ready for independently selected QA retest.

Original literal and resolved output root: `C:\Projects\DevForgeAI\docs\plan\index-service-remediation\20260914T1950304158791Z`. Selection source: this run's pre-write selection of a distinct docs/plan directory under the selected spec; original QA input directory remains immutable. Output map/readback: context.md, handoff-manifest.json and verification.json.

Last verified candidate: source-manifest.json SHA256 `cf3ee99015db0dcc1eb544fdac1bfdb0fcd2f10bfc8b749857d52740d8258094`. Release runtime manifest SHA256 `b1410d025148294ca577fce097ad12e8601de82f36163aa889f86d1ca8a668ac`. Retained source is candidate/, retained release binaries runtime/. Source manifests for coverage-final-002, release-build, fmt-final and clippy-final match exactly. tools.json binds native host/compiler/collector identities. changed-files.json and candidate.diff account for 27 owned application changes; prior source snapshot and QA artifacts retained unchanged.

Completed evidence: original two QA behavior failures reproduced, provenance repair and meaningful coverage tests added, final Windows 3314/3486 lines (95.06597819850832%), original declared units 18/18, product tests 90/90, release/fmt/Clippy pass. Native screenshot inspected. Full execution history and failures remain in executions.jsonl and attempts/. No tests need automatic replay merely to resume this handoff.

Pending: independent QA retest/closure for both findings; corrected-candidate Ubuntu/WSL verification; original QA-G01..05 qualification gaps. No remote synchronization, WSL invocation, installation or actual startup/systemd effects authorized by this checkpoint. The approved process-local volatile registry fixture restored HKCU and verified unchanged real startup bytes and fixture deletion. Branch coverage NOT_RUN; framework acceptance NOT_EVALUATED.

Owned processes: windows-process-readback.json contains an empty observed DevForgeAI process inventory after test cleanup. No known active owned daemon/job remains; unrelated processes were not stopped.

Resume procedure: reread current rules and selected spec; hash original QA inputs and corrected source/build/evidence; compare tool/platform, paths, permissions and process state. Report any drift without restoring source or overwriting old attempts. Invalidate only evidence dependent on changed bytes/platforms. Keep this run and use a fresh directory for independent retest. Next safe action is independent QA under the user's next selected scope; do not issue acceptance or self-close findings.
