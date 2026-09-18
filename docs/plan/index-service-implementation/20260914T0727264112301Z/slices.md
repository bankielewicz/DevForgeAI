# Dependency-ordered implementation slices

All source changes are owned under `devforgeai/`; evidence under the context-bound root. Current state: planned. No implementation or verification is claimed by this plan.

| Slice | Selected requirements | Observable result and verification |
| --- | --- | --- |
| S01 protocol and executable harness | DS-001, DS-022, DS-023, DS-024 | Strict typed operation registry, bounded framing, envelope and exit semantics; executable negative/positive fixtures, schema/examples. |
| S02 platform and local host | DS-003, DS-004, DS-007, DS-009 | Private identity/data/endpoint, exclusive ownership, authenticated IPC, idempotent start; native peer/root/duplicate-start checks. |
| S03 capture and extraction | DS-014, DS-015, DS-016, DS-017 | Exact immutable captures, exclusions/encodings, all adapters, cancellation and bounded work; independent synthetic expected ranges and failure fixtures. |
| S04 storage and scheduler | DS-002, DS-008, DS-010, DS-011, DS-012, DS-013, DS-018, DS-019, DS-020, DS-021 | Generation transactions, metadata recovery, registration, pause/resume/stop/jobs and dirty markers; crash/cancel/reader/recovery integration. |
| S05 management client and CLI | DS-009 through DS-013, DS-022 through DS-024 | Terminal lifecycle/project/index/job commands through shared client only; process-level JSON/exit/deadline/retry and source-immutability tests. |
| S06 WSL and tray | DS-005, DS-006, DS-025, DS-026 | Argument-vector bridge, no implicit wake, asynchronous native GUI and opt-in settings; Windows/WSL native and visual checks. |
| S07 delivery and qualification | DS-003, DS-A01 through DS-A19, sections 1.4, 9, 10 | Locked native builds, licenses, unit example, docs, three-repeat benchmark, coverage and platform acceptance accounting. |

Reuse assessment: directory listing of `devforgeai/` was empty; repository manifest/Rust search found no application Cargo manifest or source. No component exists to extend in the selected product scope. Build the new application units from selected contracts. Existing skill evaluators are neither application code nor acceptance authorities and are not reuse candidates. External parser/runtime/storage crates are dependencies, to be inspected and pinned.

S01 precedes host consumers. S03 and S04 supply published records to S05; S06 uses the same S05 client, never direct database access. Companion query commands are deferred until separately selected. Each behavioral slice requires executed red before implementation, same assertions green, justified refactor, and applicable QA. Execution lineage is appended as actual work occurs.


## Executed lineage and handoff

S01: protocol red 002, green 003. S02: platform red 011, native green 013; IPC red 017, native green 019. S03: capture red 006, green 007; worker/cancellation refinements 028–031; directory-link defect red 058, green 059/060. S04: storage red 008, green 010; service red 014, green 016; Resume defect 027→029; debounce 042→043; root failure 068/070→071; negative/reader QA 073. S05: CLI red 020, green 021; process failures 035/036/038 and fixes 039/040. S06: tray red 022, green 024; native harness corrections 050–053, native pass 054; readable status 061→062; WSL bridge 066. S07: final candidate tests/coverage 085/086, Windows Clippy 088, native release builds 087/089, WSL final checks 089; full qualification remains PARTIAL.

The user requested the HTML manual playbook and explicit WSL-tested/standalone-Linux-untested note. Playbook logic defect 075→076 is retained; live browser preview was policy-blocked. Further platform/manual results should be evaluated against the exact submitted candidate.
