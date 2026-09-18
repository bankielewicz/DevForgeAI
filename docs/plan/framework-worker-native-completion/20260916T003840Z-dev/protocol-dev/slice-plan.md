# Protocol edge slice plan and execution lineage

## PE-01..09: observable pre-thread protocol edges

- Requirements: DFF-WORKER-FEAS-01 section 5 and DFF-WORKER-PREFLIGHT-01 Required pre-thread protocol items 3 and 8.
- Dependencies/build order: existing `Session`, `OwnedProcess`, `Journal`, test `Fixture`; root-added Cargo registration after the peer file existed.
- Consumed/provided contracts: consumes the public Session preflight API and closed JSONL wire behavior; provides only test evidence. Root remains the production/shared-manifest owner.
- Additions: `tests/protocol_edges.rs` drives the real Session; `tests/support/protocol_edges_peer.rs` independently validates outbound messages and supplies fixed responses.
- Allowed effects: the two new test files and protocol-dev evidence only. No production, original test, operational, configuration, native, installation or authority effects.
- Verification: nine labeled cases, real child process/pipes, mandatory traces/journals, no-work checks, fixture readback and stopped Job Object.
- Prerequisites/gaps: native Windows Rust toolchain and cached locked dependencies were available. Full coverage and independent retest remain root/QA work.
- Current state: VERIFIED for the bounded slice by `08-focused-integrity-green`, `09-focused-clippy-final`, and `10-owned-format-final`.

### Reuse assessment

| Search scope and limitation | Candidate source/tests | Decision | Evidence and reason |
| --- | --- | --- | --- |
| Existing preflight Session, profile test and peer; prior coverage used only to locate unexecuted behavior | `src/protocol.rs`, `tests/profile_protocol.rs`, `tests/support/profile_peer.rs` | Reuse Session/Fixture and add a distinct peer | Existing peer had a closed scenario set and was owned as historical evidence; adding cases there would overlap ownership. A separate peer preserves original bytes and exercises the real boundary. |
| Direct private-function/unit seam | private Session methods | Rejected | A public test bypass would weaken the real process/pipe integration and add product-only test surface. |

### Execution lineage

- Characterization: `01-focused-characterization`, 4 Rust functions covering 9 declared cases, passed initially. Existing required behavior was correct; no Red was fabricated.
- Formatting: `02-format-check` retained the expected pre-format diff plus a concurrent actor's file. `03-rustfmt-owned` formatted only owned files; `04-focused-post-format` passed.
- Static check: `05-focused-clippy` passed.
- Integrity refactor: mandatory reads, nonvacuous trace start, fixture readback and chunk-independent stderr byte accounting were added after review; `08-focused-integrity-green` passed the unchanged behavioral expectations.
- Final focused QA: `09-focused-clippy-final` and `10-owned-format-final` passed.
- Next action: root integrates disjoint slices and runs the complete developer campaign before freezing the candidate for independent QA.
