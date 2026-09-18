---
name: github-incident-review
description: Independently review a GitHub incident or issue URL for factual merit, reproducibility, scope completeness, duplicate and related work, producer-consumer coupling, mirror and CI coverage, and linked implementation status. Use when asked to review, validate, triage, audit, assess merit, resolve a scope fork, or produce a provenance-backed ruling for a GitHub incident or issue URL. Do not use to create incidents or perform standalone pull request review.
---

# GitHub Incident Review

Produce a reproducible ruling that another reviewer can audit without access to the conversation.

## Non-negotiable boundaries

- Apply a **Read-only default** to GitHub and other external systems. Never create, edit, label, comment on, close, reopen, or otherwise mutate a GitHub artifact without a separate explicit authorization naming the mutation.
- **Local evidence writes are required**: write the evidence bundle, completed report, validation output, and hashes under a task-scoped local directory. "Read-only" never means skipping local review artifacts.
- Use an **isolated review worktree** or isolated clone for every live review. Keep any later source fix in a different feature worktree, branch, commit series, and pull request.
- HALT when the repository, incident identity, evidence boundary, requested mutation, or controlling acceptance criteria cannot be resolved from live sources.
- Classify evidence as `GROUNDED`, `DERIVED`, or `INCONCLUSIVE`. Never promote an inference to fact.
- Preserve exact commands, exit codes, URLs, timestamps, SHAs, and file hashes. Redact credentials and private data.
- Treat a review as incomplete until the rendered report passes `scripts/validate_review.py`.

## Required resources

1. Read `references/review-protocol.md` before classifying merit, coupling, duplication, or disposition.
2. Run `scripts/collect_incident_evidence.py` to capture read-only GitHub and repository evidence when the GitHub CLI and a checkout are available.
3. Copy `assets/github-incident-review-template.md` into the review evidence directory and replace every placeholder.
4. Run `scripts/validate_review.py` against the completed copy before presenting or posting it.

Both scripts are noninteractive and Python-standard-library only. Exit `0` means success, `1` means evidence or content failure, and argparse uses exit `2` for invalid usage. Structured data goes to stdout; diagnostics go to stderr.

## Workflow

### Phase 1: Resolve and isolate

1. Parse the GitHub issue URL or repository plus issue number.
2. Resolve the repository remote, default branch, base SHA, current head SHA, and tree status.
3. Create or select an isolated review worktree at the exact base or linked implementation head under review.
4. Record the review boundary. Do not reuse an implementation worktree as review evidence.

### Phase 2: Capture the incident record

Capture the live issue body, comments, labels, assignees, state, state reason, creation and update timestamps, ownership markers, linked pull requests, and referenced issues. Record collection time and the commands used.

### Phase 3: First duplicate search

Run the **First duplicate search** before investigating the proposed root cause. Search open and closed issues and pull requests by:

- exact and normalized title terms;
- component, workflow, file, function, hook, schema, and command names;
- exact error text, observable signature, and acceptance-criteria phrases.

Use at most eight high-signal queries per collector pass to remain below the GitHub Search API budget. Retain every query and candidate URL. Do not classify candidates from titles alone.

### Phase 4: Build the Claim ledger

Create one row for every material statement in the incident:

- assign a stable claim ID;
- quote or precisely paraphrase the claim;
- identify the evidence required to prove or refute it;
- classify the result as `GROUNDED`, `DERIVED`, or `INCONCLUSIVE`;
- cite the exact file, line, command output, GitHub URL, or captured artifact.

### Phase 5: Verify the implementation surface

Inspect exact live source, tests, schemas, hooks, workflow registration, mirrors, packaging rules, and CI collection. Trace the full coupling chain:

`producer -> validator -> consumer -> downstream enforcement`

Verify whether apparently identical predicates, payloads, handshakes, generated files, or mirror copies operate on the same contract. Expand scope only when the evidence proves the originally named fix would leave the same failure active elsewhere.

### Phase 6: Reproduce and discriminate

Run the smallest reproducible **positive path** that demonstrates the claim and a discriminating **negative path** or control that would pass if the proposed cause were wrong. Record command, environment, exact head SHA, exit code, and relevant output. Mark an unexecuted reproduction `INCONCLUSIVE`; never describe it as passing.

### Phase 7: Second duplicate search

Run the **Second duplicate search** after root cause and required remedy are known. Use at most eight high-signal queries in a separate collector pass. Search by the verified failure signature, predicate or contract, affected surface, and remedy. Compare each candidate using the taxonomy and four-part exact-duplicate test in the protocol.

### Phase 8: Verify linked implementation

When the incident has a linked pull request:

1. Resolve the linked pull request and **exact head SHA**.
2. Inspect files, commits, linked issues, required checks, check conclusions, and CI workflow identity.
3. Verify test collection rather than assuming a test path is executed.
4. Verify source/runtime and provider mirror status when mirrored assets are in scope.
5. Re-run focused acceptance and hostile negative-path checks at that exact head.

Use linked implementation dispositions `NOT_APPLICABLE`, `ACCEPT`, `CHANGES_REQUIRED`, or `HOLD_INCONCLUSIVE`.

### Phase 9: Classify merit and duplication

Use incident dispositions `VALID`, `VALID_WITH_AMENDMENTS`, `INVALID`, or `INCONCLUSIVE`.

Use duplicate classifications `EXACT_DUPLICATE`, `OVERLAP`, `RELATED`, `RECURRENCE`, `NONE`, or `INCONCLUSIVE`. Recommend duplicate closure only for `EXACT_DUPLICATE`, and only after identifying the canonical incident and unique evidence to migrate. A closed and fixed issue whose behavior reappears is `RECURRENCE`, not a duplicate.

### Phase 10: Render and validate

Complete every template section. Include provenance, claim ledger, reproduction, duplicate matrix, scope/coupling analysis, acceptance-criteria audit, linked implementation evidence, findings, exact amendments, recommended actions, and copy-ready postings.

Validate:

```bash
python3 scripts/validate_review.py path/to/completed-review.md --format json
```

Fix every validation error before issuing a ruling.

### Phase 11: Recommend or perform GitHub actions

By default, output actions and postings without publishing them.

For `EXACT_DUPLICATE`, produce:

1. a canonical incident posting that migrates unique evidence and cross-links the reviewed incident;
2. a reviewed incident posting that cites the canonical incident and exact-duplicate proof;
3. a recommendation to close the reviewed incident as not planned after both postings exist.

Never recommend duplicate closure for `OVERLAP`, `RELATED`, `RECURRENCE`, `NONE`, or `INCONCLUSIVE`.

If separately authorized to mutate GitHub, perform only the named actions in this order: post to the canonical incident, post to the reviewed incident, close as not planned when authorized, then re-fetch both incidents and record the resulting URLs, states, and timestamps.

## Completion gate

Finish only when:

- every material claim has a provenance classification and evidence pointer;
- both duplicate searches and candidate comparisons are recorded;
- coupling, mirrors, packaging, test collection, and linked implementation are resolved or explicitly `INCONCLUSIVE`;
- positive and negative paths include exact commands and exit codes or an explicit non-execution reason;
- the completed template has no placeholders and the validator exits `0`;
- no GitHub mutation occurred without separate explicit authorization.
