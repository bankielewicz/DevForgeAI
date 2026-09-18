# Offline startup logging reproduction plan

## Scope and bindings

- Host: native Windows, workspace `C:\Projects\DevForgeAI`.
- Frozen candidate: `devforgeai/experiments/codex-worker-probe`.
- Candidate manifest: `docs/plan/framework-worker-diagnostics/20260916T181820Z-dev/candidate-v2-manifest.json`, SHA256 `419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540`.
- The harness compiles the frozen Rust modules through absolute source paths. It does not copy or edit production source.
- Only a local synthetic child is launched. Native Codex, credentials, user/system profiles, installed configuration, network access, full regression, and coverage are outside this run.

## Cases declared before execution

### SR-01: early exit before initialize

Launch a synthetic child through the unchanged `OwnedProcess`. The child writes one fixed harmless stderr block, flushes it, and exits with code 23 before reading stdin. Wait for the real held Job Object to report `(total, active) = (1, 0)`, then call the unchanged `Session::preflight`.

Required observations:

1. preflight returns `profile_unqualified` at the initialize `before_send` process guard;
2. the journal contains `unexpected_process_count`, total 1 and active 0;
3. the journal contains no stderr event;
4. the process receiver still contains stderr metadata with the exact fixed byte count and SHA256, demonstrating that the reader reduced the raw block to metadata but the guard returned before the receive loop journaled it;
5. child exit code is 23, teardown is bounded, and active count becomes 0.

### SR-02: receive-loop control

Launch the same synthetic child in a mode that writes the same stderr block, remains active, receives an initialize RPC, and returns a fixed local response. Invoke the unchanged private RPC path from an adjacent wrapper function without changing its implementation.

Required observations:

1. the held Job Object reports `(1, 1)` before the RPC;
2. initialize returns the fixed response;
3. the journal contains the same stderr byte count and SHA256 with `content: omitted`;
4. before-send and after-receive accounting both report `only_worker`, 1/1;
5. no thread or turn method is sent, teardown is bounded, and active count becomes 0.

## Interpretation

SR-01 plus SR-02 proves a startup observability blind spot only if all stated observations come from the unchanged candidate modules. It does not determine why the native Codex worker exited, qualify a product repair, repeat native execution, or establish framework acceptance. The wrapper has a different Cargo manifest directory and calls a private RPC through code lexically adjacent to the included module; path-sensitive public runner admission remains outside this reproduction.

## Commands

Run with cached dependencies and fresh output roots:

1. `cargo build --locked --offline --bins`
2. `cargo run --locked --offline --bin startup-repro`

Each command receives its own retained attempt directory with argv, cwd, stdout, stderr, exit status, timing, and candidate readback. A failed setup attempt remains retained and is not rewritten.
