# Final spawn source check: development evidence

The previous runner checked source qualification before argument construction, executable hashing and the `spawn_intent` journal callback, but did not check sources again immediately before `OwnedProcess::spawn`.

`02-runner-red` is a retained **harness setup failure**, not a Red: the new unit fixture initially used its own Rust test executable, whereas peer admission requires `protocol-peer.exe` in the package build directory. It failed with `input_missing` before any stimulus. The setup was corrected to use that required peer; `03-runner-peer-build` compiled it. This did not change product behavior or expected assertions.

`04-runner-red` is a valid behavioral Red. The private scaffold forwarded existing runner behavior unchanged and ignored a proposed final-check callback. The fixture first verified a real source digest, altered that source during the actual durable `spawn_intent` callback, and expected the final checker to run once and deny process creation. Actual final-check count was zero, and the runner reached the real compiled peer. The raw failing assertion and fixture observation are retained.

`05-runner-green` uses the same stimulus/assertions. The runner now executes the final check after all journal callbacks and argument work, then creates a process only if that check succeeds. The test observed one final check, exit 3/profile_unqualified, null worker exit, no server_started, and stopped tree. Public entry points always supply the compiled check; the injectable callback is a private unit-test seam, not a request/API option. Its digest checker isolates ordering; the source collector tests separately exercise full junction inventory freshness, and this test does not establish native Codex acceptance.

Production schema-2 final verification repeats review/inventory validation and pinned executable identity. A source denial retains a blocked terminal; invalid executable identity retains the existing exit-2 diagnostic behavior. All old source/identity checks remain. No further refactor is needed beyond isolating this final check and preserving the existing cleanup/error path.

The focused Green was captured while another agent had added test-only collector Red scaffolding, producing an expected temporary dead-code warning in that other slice. Final Clippy will run only on the integrated candidate. No passing static-analysis claim is made from this focused run.
