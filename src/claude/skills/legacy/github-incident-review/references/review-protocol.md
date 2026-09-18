# GitHub Incident Review Protocol

Use this protocol when the top-level workflow reaches evidence classification, duplication, scope, or disposition decisions.

## Contents

1. Evidence custody
2. Claim ledger
3. Merit and scope
4. Duplicate classification
5. Linked implementation
6. GitHub action protocol
7. Completion criteria

## Evidence custody

Capture the incident and repository as time-bound evidence. Record:

- issue URL, number, state, state reason, created time, updated time, and collection time;
- issue body, comments, labels, assignees, ownership markers, linked pull requests, and related issues;
- repository remote, default branch, base SHA, reviewed head SHA, and tree status;
- every duplicate query, candidate URL, query time, and state filter;
- reproduction and control commands, exit codes, relevant output, environment, and exact SHA;
- CI workflow, job, check name, conclusion, URL, and head SHA;
- evidence manifest path and SHA-256 for every captured file.

Use UTC RFC 3339 timestamps. Preserve raw values and add interpretation separately. Never store tokens, authentication headers, or unrelated private data.

## Claim ledger

Create one row per material issue assertion. Use these classifications:

| Class | Required basis |
|---|---|
| `GROUNDED` | Directly supported by live source, GitHub data, test output, schema, workflow, or explicit user instruction. |
| `DERIVED` | Inferred from grounded evidence; include a one-sentence derivation. |
| `INCONCLUSIVE` | The required evidence is unavailable, contradictory, stale, or not reproducible. |

Do not use confidence wording as a substitute for a classification. A missing check, dormant code path, or unexecuted test is not proof that behavior passes.

## Merit and scope

Assign one incident disposition:

- `VALID`: observable failure, root cause, affected contract, and requested remedy are supported without a material scope change.
- `VALID_WITH_AMENDMENTS`: the incident has merit but its cause, scope, acceptance criteria, severity, or remedy needs exact amendments.
- `INVALID`: discriminating evidence refutes the claimed failure or cause and no narrower valid incident remains.
- `INCONCLUSIVE`: evidence cannot distinguish valid from invalid.

Trace `producer -> validator -> consumer -> downstream enforcement`. Expand the fix surface only when two or more sites consume or enforce the same contract and leaving one unchanged preserves the reported failure. Distinguish:

- direct coupling: same payload, file, schema, handshake, or state transition;
- mirror coupling: authored source and installed/runtime copy;
- packaging coupling: source included by installer or release manifest;
- CI coupling: test exists and is or is not collected by a required job;
- dormant coupling: locally short-circuited but live in supported consumer configuration.

Record dormant coupling as grounded only when the enabling configuration and reachable path are verified.

## Duplicate classification

Classify every credible candidate as one of:

- `EXACT_DUPLICATE`: all four exact-duplicate conditions below are proven.
- `OVERLAP`: shares some failure or surface but needs a materially different remedy or has independent acceptance criteria.
- `RELATED`: informs the review but addresses a different failure or contract.
- `RECURRENCE`: a previously closed and fixed failure has reappeared.
- `NONE`: searched candidates do not meet another classification.
- `INCONCLUSIVE`: evidence cannot resolve the relationship.

### Four-part exact-duplicate test

Require all four conditions:

1. the same observable failure;
2. the same root cause;
3. the same affected contract or surface;
4. the same required remedy.

If any condition is false, classify `OVERLAP` or `RELATED`. If any condition lacks evidence, classify `INCONCLUSIVE`. Closed and fixed behavior that later reappears is `RECURRENCE`, not `EXACT_DUPLICATE`.

### Canonical selection

For `EXACT_DUPLICATE`, choose the canonical incident using this order:

1. the incident with active implementation or accepted ownership;
2. the incident with the more complete verified contract and evidence;
3. the earlier incident when completeness and activity are equal.

Identify unique evidence in the reviewed incident before recommending closure. Prepare a canonical incident posting that migrates that evidence and cross-links the reviewed incident. Prepare a reviewed incident posting that cites the canonical incident and the four-part proof. Recommend closing the reviewed incident as not planned only after both postings are published.

Never recommend duplicate closure for `OVERLAP`, `RELATED`, `RECURRENCE`, `NONE`, or `INCONCLUSIVE`.

## Linked implementation

Assign one linked implementation disposition:

- `NOT_APPLICABLE`: no linked implementation is part of the incident decision.
- `ACCEPT`: exact-head changes, tests, mirrors, collection, and required checks satisfy the verified incident.
- `CHANGES_REQUIRED`: a reproduced defect, missing acceptance criterion, uncollected test, mirror drift, or failing required check remains.
- `HOLD_INCONCLUSIVE`: the exact head, required checks, or necessary reproduction evidence cannot be verified.

Bind all findings to the pull request head SHA. A green check from another SHA is not evidence. Verify the workflow actually collects the cited test path. Treat zero checks as `N/A` only when the workflow path filter or event contract proves no check is expected.

## GitHub action protocol

Remain read-only unless the user separately authorizes exact mutations. A general request to review is not authorization to comment, edit, label, close, or reopen.

When authorized to close an exact duplicate:

1. post the evidence migration and cross-link to the canonical incident;
2. post the exact-duplicate ruling and canonical link to the reviewed incident;
3. close the reviewed incident as not planned;
4. Re-fetch both incidents;
5. record comment URLs, final states, state reasons, and timestamps in provenance.

HALT if authorization omits any requested mutation, the canonical incident is ambiguous, or unique evidence has not been migrated.

## Completion criteria

The review is complete only when the evidence manifest is hashed, all claims are classified, both duplicate searches are recorded, reproduction and control paths are recorded, linked implementation is exact-head verified or held inconclusive, the fixed template is complete, and the validator exits zero.
