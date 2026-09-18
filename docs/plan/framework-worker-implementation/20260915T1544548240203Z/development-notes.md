# Development observations and interpretation

- 001/002 established offline lockfile resolution and a compiling empty harness. Zero tests is setup, not behavioral qualification.
- 003/004 oracle: valid independent output failed against the compiling seam, then exact/invalid result tests passed after implementation.
- 005/007 admission: valid fixture failed against the compiling seam, then strict request tests passed. 006 is an implementation compilation error (SHA-256 formatter omitted finalize), retained separately and not Red.
- 008/010 recovery: required journal creation failed against the compiling seam, then four recovery tests passed. 009 exposed a test arithmetic typo: the literal partial tail has nine bytes, not eight. The assertion now measures the actual literal length. No product expectation was weakened.
- 011/012 process: atomic owned process creation failed against the seam, then a real Windows peer entered the job and teardown observed zero processes.
- 013/015 protocol: eight cases failed against the runner seam, then passed against the external peer. 014 exposed the peer's initialize-ID expectation (stage 0 versus request ID 1); this was a fixture defect. WF-04 was strengthened to require actual turn dispatch plus protocol_error, preventing a generic child failure from satisfying a protocol negative.
- 016 is mislabeled `red` in the execution invocation: its WF-18/19 failures came from missing external-peer stimuli. It is a retained fixture/setup error, not product Red. 017 added the missing peer stimuli and characterized the already implemented rejection behavior. WF-17 and WF-20 initially passed as characterization checks.
- 018/019 CLI: missing arguments incorrectly returned success from the empty main; implemented CLI now emits one JSON diagnostic with exit 2.
- 020 stdin cancellation: a real peer and descendant were observed through independently held live handles and both signalled after cancellation.
- 021: WF-13/14/15 passed; an output-limit variant reached the test-only 300ms RPC deadline before the byte stimulus completed. 022 selects production timing for output variants; the original attempt remains retained. This is a test-bound interaction, not evidence that the production limit failed.

Initial integration copies under 015..021 retain trace/journal bytes but reference original temporary paths. These copied artifacts are historical trace evidence; they do not demonstrate read-only recovery from a currently existing original fixture. The qualification campaign must retain test roots in place.

Documentation used for implementation context: [official Codex App Server](https://learn.chatgpt.com/docs/app-server), and [Microsoft atomic Job Object attachment](https://devblogs.microsoft.com/oldnewthing/20230209-00/?p=107812). Captured 0.154.0 schemas remain governing wire inputs. No schema regeneration or native Codex launch occurred.
# Later repair and measurement notes

- 031 full collection passed 20 mandatory plus 10 supplemental tests, correcting the earlier 31/11 prose count. Executed lines were 1061/1299 (81.67821401077752%): FAIL. Returning an ExitCode from main instead of process::exit allowed Windows LLVM profiles to flush normally; CLI lines remain in the denominator.
- 039 full collection passed its tests but measured 1243/1316 (94.45288753799392%): FAIL. No rounding, exclusions, or earlier pass claims qualify changed bytes.
- 040 exposed two behavioral defects: buffered completion hid a later conflicting buffered event; unknown token-usage fields were retained. 041 passed after draining all buffered observations and retaining only typed counters. The native path expectation in 040 instead exposed the captured launcher as a reparse path: a host prerequisite, not a valid Red for wrong fixture layout. No Codex process was launched. That source test conservatively checks the observed rejection; native path/profile qualification remains unperformed.
- 042 is a diagnostic subset without WF-13..16 and cannot qualify the final suite.
- 043 was a valid Red for home-boundary exclusion; 044 passed the repaired boundary and admission suite. The test uses synthetic home/temp paths under an owned fixture, never credential contents.
- 047 preserves another full candidate measurement. A subsequent contract review identified missing cooperative grace before turn IDs exist; it must be repaired and recollected rather than claiming this measurement qualifies later bytes.

- 048 valid Red: cancellation before IDs killed the cooperative peer with worker exit 1. 050 passed after EOF/cooperative grace, with bounded waits also applied to lost interrupt transport and startup evidence failure. 049's command filter executed WF-15 only; it is not a broad regression claim.
- 055 is a supplemental test compilation ERROR (closure parameter needed explicit `&serde_json::Value`), resolved before 057 Clippy passed. The prematurely named source-test-manifest.json remains an intermediate candidate. Select only final-source-test-manifest.json and the final delivery identity.
- 059 all tests passed but coverage 1305/1374 = 94.97816593886463% FAIL. 060's noninstrumented suite passed on the same candidate. Coverage was not rounded up.
- 061 added regression checks for exact/conflicting duplicate completion and valid output followed by nonzero worker exit. All passed without runtime edits. They address untested contract behavior, not a newly reproduced runtime defect. Runtime bytes remain unchanged from 059; final source/test identity changes because tests/peer changed.
- The fixture provenance audit initially assumed the captured schema-command.json receipt was in the 335-input manifests. It is not. The corrected audit separately compares its exact bytes to the original captured receipt and labels that origin accordingly. The task/prompt/output-schema/expected copies match manifest-pinned origins.
- Final normal and instrumented campaigns use separate build directories and disjoint fixture roots while overlapping in wall time. Earlier fixture and coverage attempts are retained. No native Codex process or live account capability was exercised.
