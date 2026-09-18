# Repository-owner standalone platform override

Authorization: user stated, "I'm the repo owner. ubuntu 26.04.1 validation overrides Ubuntu 24.04" on 2026-09-14.

Effective target: standalone Ubuntu 26.04.1 LTS x64 replaces standalone Ubuntu 24.04 x64 in DS-003. Windows 11 x64 and Ubuntu 24.04 WSL2 are unchanged. Numeric quality floors, no-mock-decorator and anti-gaming requirements, and mandatory acceptance scenarios remain in force. This is an owner-authorized requirement revision, not an acceptance waiver.

The received VMware campaign now matches the required standalone release. The revised [evaluation](../evaluation-20260914T163707306677Z/evaluation.md) still records coverage FAIL: 2066/2786 = 74.1564967695621%. All 36 raw regression cases passed; one trivial setup assertion has no product credit. Full manual specification checks and independent test-integrity QA remain incomplete.

Specification before SHA-256: b1886c7bf237f823b2f83a8b37c1288ca26880ecfc58771568b38750e8855897
Specification after SHA-256: 52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4
Updated HTML SHA-256: b33e1defb2cf28ed6c2c886086d3397dfb5c4ff3f9079406ddb4e97ce1fd93d4

Original specification/page snapshots are retained here. Original transfer archive, checksums, raw VM files, old evaluation and all historical implementation receipts remain unchanged. The VM's source candidate still matches all 48 application files; the only contract change is the standalone platform revision. No software was rebuilt or requalified by this documentation change. The already-downloaded playbook remains historical; its JSON/raw evidence can be evaluated with this explicit override. The updated HTML uses a separate storage key and new specification hash, preserving historical browser results without silently relabeling them.

Verification: revised evaluator exit 0; playbook Node syntax/logic/export checks exit 0. Browser visual QA was not performed. The earlier evaluator attempt failed a filename-glob assertion (benchmark build log also matched); the selector was narrowed and the successful evaluation retained separately. This was an evidence-review helper error, not a product test failure.
