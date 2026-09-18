# GitHub Incident Review

## Review snapshot
- Issue: <ISSUE_URL>
- State: <ISSUE_STATE>
- Updated at: <ISSUE_UPDATED_AT>
- Captured at: <CAPTURED_AT>
- Review boundary: <REVIEW_BOUNDARY>

## Disposition
- Incident: <VALID|VALID_WITH_AMENDMENTS|INVALID|INCONCLUSIVE>
- Linked implementation: <NOT_APPLICABLE|ACCEPT|CHANGES_REQUIRED|HOLD_INCONCLUSIVE>

## Executive ruling
<ONE_PARAGRAPH_EVIDENCE_BACKED_RULING>

## Provenance
- Repository remote: <REPOSITORY_REMOTE>
- Default branch: <DEFAULT_BRANCH>
- Base SHA: <BASE_SHA>
- Head SHA: <HEAD_SHA>
- Tree status: <TREE_STATUS>
- Evidence captured at: <CAPTURED_AT>
- Evidence manifest: <EVIDENCE_MANIFEST_PATH>
- Evidence SHA256: <EVIDENCE_MANIFEST_SHA256>

## Claim ledger
| ID | Claim | Class | Evidence | Verification |
|---|---|---|---|---|
| C-001 | <MATERIAL_CLAIM> | <GROUNDED|DERIVED|INCONCLUSIVE> | <FILE_LINE_URL_OR_ARTIFACT> | <COMMAND_OR_DERIVATION> |

## Reproduction and negative-path verification
| Path | Command | Exit | Result |
|---|---|---:|---|
| Positive | <COMMAND> | <EXIT_CODE> | <OBSERVED_RESULT> |
| Negative | <COMMAND> | <EXIT_CODE> | <CONTROL_RESULT> |

## Related and duplicate incidents
- First-pass queries: <QUERIES_AND_TIMESTAMPS>
- Second-pass queries: <QUERIES_AND_TIMESTAMPS>
- Classification: <EXACT_DUPLICATE|OVERLAP|RELATED|RECURRENCE|NONE|INCONCLUSIVE>
- Canonical incident: <URL_OR_NA>

| Candidate | Observable failure | Root cause | Contract/surface | Remedy | Classification | Evidence |
|---|---|---|---|---|---|---|
| <URL> | <SAME_DIFFERENT_UNKNOWN> | <SAME_DIFFERENT_UNKNOWN> | <SAME_DIFFERENT_UNKNOWN> | <SAME_DIFFERENT_UNKNOWN> | <CLASSIFICATION> | <CITATIONS> |

## Scope and coupling
- Producer: <PRODUCER_AND_EVIDENCE>
- Validator: <VALIDATOR_AND_EVIDENCE>
- Consumer: <CONSUMER_AND_EVIDENCE>
- Downstream enforcement: <DOWNSTREAM_AND_EVIDENCE>
- Mirrors and packaging: <MIRROR_PACKAGE_EVIDENCE>
- Scope ruling: <EXACT_FIX_SURFACE>

## Acceptance criteria audit
- [ ] <CRITERION_AND_EVIDENCE>

## Linked implementation and CI
- Linked PR: <URL_OR_NA>
- Reviewed head SHA: <SHA_OR_NA>
- Files and commits: <EVIDENCE_OR_NA>
- Required checks: <CHECK_IDENTITIES_CONCLUSIONS_URLS_OR_NA>
- Test collection: <WORKFLOW_AND_PATH_EVIDENCE_OR_NA>
- Mirror status: <SOURCE_RUNTIME_AND_PROVIDER_EVIDENCE_OR_NA>
- Exact-head verification: <COMMANDS_EXIT_CODES_OR_NA>

## Findings
- F-001 | <GROUNDED|DERIVED|INCONCLUSIVE> | <FINDING_WITH_EVIDENCE>

## Required amendments
<EXACT_AMENDMENTS_OR_NONE>

## Recommended GitHub actions
- <READ_ONLY_RECOMMENDATION_OR_EXPLICITLY_AUTHORIZED_ACTION>

## Copy-ready postings
### Reviewed incident
<COMPLETE_POSTING_OR_NA>

### Canonical incident
<COMPLETE_POSTING_OR_NA>

## Final ruling
<DISPOSITION_COLON_FINAL_SCOPE_AND_NEXT_ACTION>
