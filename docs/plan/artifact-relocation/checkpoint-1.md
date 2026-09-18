# Checkpoint 1: inventory baseline

Observed on native Windows / PowerShell 7.6.6 at C:\Projects\DevForgeAI; authoring checkout: worktrees/git/artifact-inventory.
Base commit: 164b652572cbb349e2c44eb3270f4d653bac05e5. Migration reviewer: Bryan.

## Results

- 64 non-Git collections; 482,456 regular files; 40,073,689,838 logical bytes (37.32 GiB).
- 37 reparse points in 10 collections skipped; zero directory-read errors. No reparse target was followed.
- Two pre-existing linked Git worktrees remain separate from the inventory; this checkpoint adds its own authoring worktree.
- 14 collections initially held; the others await dependency/process admission. No collection has been moved or declared disposable.
- Expanded current-documents scan: 98 broken link occurrences to 76 distinct existing local files. The earlier framework-only scan was 26 occurrences / 15 targets.
- Seven literal location references in tracked runtime/configuration files were found and attributed in the inventory.
- File lengths are logical sizes, not allocated disk or guaranteed reclaimable space. Full content hashing belongs to relocation admission.

## Method and limitations

Native PowerShell used System.IO.DirectoryInfo enumeration with an explicit stack, 15-minute deadline and no-follow reparse handling; metadata enumeration completed in 6.73 seconds. No snapshots were copied. The source root was explicitly C:\Projects\DevForgeAI\worktrees, excluding git.
Current tracked .ps1/.py/.rs/.json/.toml/.yml/.yaml files were searched for literal original/current collection locations; current docs Markdown links were resolved against their actual document roots. Dynamic paths, external sessions and nonliteral dependencies require later admission review.
The initial local summary accidentally counted a null expansion as one read error; reconciliation against every collection shows zero. The initial observation remains local alongside the corrected summary.
Raw metadata observations: tmp/artifact-relocation-inventory-001 in this checkpoint worktree. The compact inventory and broken-link list are published here; no payload files are published.

## Verification

Counts and byte totals were recomputed from all inventory entries; all source collection directories and all 76 unique referenced local files exist. The two pilot reports match their pre-deletion Git blobs (verified during planning); a complete pilot file manifest remains pending.
Changed-file review, JSON parsing and exact-byte manifest readback apply to this documentation checkpoint. TDD, runtime coverage, independent QA and framework acceptance are NOT_RUN / NOT_EVALUATED as applicable.

## Collection accounting

| Collection | Files | Logical bytes | Initial disposition |
| --- | ---: | ---: | --- |
| advisor-auth-fix | 57 | 357839 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| advisor-build | 131 | 628682 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| advisor-claude-conversion | 3 | 35978 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| advisor-guidance | 3 | 19611 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| advisor-runs | 97 | 1004696 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| advisor-streaming-dev | 80 | 209094 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| dev-claude-conversion | 4 | 47372 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| dev-qa-remediation | 492 | 3084026 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-discovery-planning | 23 | 199219 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-foundation | 6 | 23083 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-mvp-planning | 20 | 135096 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-native-readiness | 48 | 809543 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-prd-planning | 10 | 71810 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-prd-review-planning | 9 | 83355 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-config-fix | 17 | 18169 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-console-helper | 35 | 102741 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-contract | 322 | 3658731 | HOLD |
| framework-worker-diagnostics | 23533 | 2981328333 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-diagnostics-qa | 13219 | 2139542942 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-implementation | 9634 | 35833738 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-logging | 69298 | 11563683614 | HOLD |
| framework-worker-native-completion | 27268 | 4748957020 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-native-completion-qa | 20036 | 3242582900 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-native-continuation | 104 | 638972 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-native-diagnostics | 63 | 4204051 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-native-implementation | 8075 | 1195110673 | HOLD |
| framework-worker-native-qa | 7618 | 1350103513 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-qa | 21206 | 3574602593 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-source-identity | 18986 | 2661699886 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-source-identity-qa | 16007 | 3898197610 | HOLD |
| framework-worker-startup-investigation | 1111 | 276091355 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| framework-worker-trials | 778 | 10054689 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| index-service-implementation | 311 | 20463551 | HOLD |
| index-service-qa | 277 | 8493481 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| index-service-remediation | 918 | 94437557 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| qa-claude-conversion | 5 | 75669 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| root-cause-analyses | 53 | 822230 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-adaptive-implementations | 16053 | 185577648 | HOLD |
| skill-adoptions | 537 | 5245738 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-authoring-enhancement | 105040 | 778590480 | HOLD |
| skill-authorings | 2352 | 20322318 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-builder-adoption-verification-20260912 | 793 | 1749707 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-builder-adoption-verification-20260912-independent-adoption-trial | 399 | 685592 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-builder-adoption-verification-20260912-independent-adoption-trial-final | 384 | 1537079 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-builder-adoption-verification-20260912-independent-adoption-trial-final2 | 676 | 2155906 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-builder-adoption-verification-20260912-independent-build-trials | 567 | 1062771 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-builder-adoption-verification-20260912-independent-build-trials-final | 564 | 1057404 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-builder-adoption-verification-20260912-independent-build-trials-final2 | 564 | 1057383 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-builder-adoption-verification-20260912-independent-failure-trials | 816 | 931428 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-builder-custody-remediation | 17862 | 196474275 | HOLD |
| skill-builder-enhancement-evidence | 689 | 4091730 | HOLD |
| skill-builder-evaluation | 6 | 247939 | HOLD |
| skill-builder-postmvp-maintenance | 7198 | 103568405 | HOLD |
| skill-builder-remediation | 16326 | 119234638 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-builder-review-20260916 | 4 | 45969 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-builds | 10580 | 128722175 | HOLD |
| skill-creator-reviews | 218 | 355014 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-independent-qa | 27556 | 378461094 | HOLD |
| skill-set-validations | 611 | 2772924 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-validations | 29347 | 242749549 | HOLD |
| skill-validator-claude-conversion | 1 | 22205 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| skill-validator-postmvp-maintenance | 3279 | 77058925 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| specification-reviews | 2 | 7808 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
| ubuntu-results-20260914-123258 | 175 | 2490312 | PENDING_DEPENDENCY_AND_PROCESS_REVIEW |
