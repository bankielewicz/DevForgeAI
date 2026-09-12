---
name: synthetic-release-check
description: Compare a candidate manifest against the accepted Ledgerworks ledger and report the differences. Use when someone asks whether a candidate matches the accepted ledger, or asks for a release check before a handoff. Not for editing the ledger and not for deciding a release.
---

# Release check

Synthetic fixture, revision 1. Operator-authored for an evaluation case; it
describes no real framework and creates no authority. Its workflow is written
inline on purpose, so that a refactor has something to move.

## Scope

You read. You do not edit the accepted ledger, the candidate manifest, or the
release decision. Reporting a difference is the deliverable; resolving it is
someone else's.

## 1. Resolve the inputs

Find the accepted ledger at the path the assignment gives, and the candidate
manifest at the path the request gives. Record both identities - path and
digest - before reading anything else. **LC-1: if the accepted ledger cannot be
resolved, stop and report it. Do not substitute a newer ledger, and do not
proceed against an unidentified one.**

## 2. Compare

Compare entry by entry: present in both and identical, present in both and
different, present only in the ledger, present only in the candidate. **LC-2:
an entry you could not read is `COULD_NOT_RUN` with the cause recorded, never
an absent entry.**

## 3. Classify each difference

Every difference gets one of `PASS`, `FAIL`, `NOT_RUN`, `COULD_NOT_RUN`,
`NOT_APPLICABLE`. **LC-3: never blend them into a count, a percentage or a
score - the vocabulary is fixed, and a blended result hides the failures.**

## 4. Save the report, then report

Write the full comparison to the assigned report path. **LC-4: the closing
response stays short - the outcome, where the report is, and the one thing that
needs a decision. The inventory belongs in the saved report, not in the
message.**

## What this skill cannot do

It grants no tool permission and blocks nothing. A requirement that must
actually prevent a release is recorded and routed to the integration owner, who
owns the compiled check. **LC-5: do not write a command sequence here that
pretends to gate a release.**

## When something is missing

Say which input, what it blocks, and who owns it. An absent error is not a
pass.
