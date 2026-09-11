---
name: synthetic-ledger-audit
description: Audit the Ledgerworks accepted ledger for entries whose upstream reference no longer resolves, and report them. Use when someone asks whether the ledger's references are still good, or reports a stale ledger entry. Not for editing the ledger and not for release decisions.
---

# Ledger audit (Claude)

Synthetic fixture, revision 2. Operator-authored for an evaluation case; it
describes no real framework and creates no authority.

This is the **Claude** implementation, at
`providers/claude/plugins/ledgerworks/skills/synthetic-ledger-audit`. It is the
editable source for Claude work.

## Scope

Read the accepted ledger, resolve each entry's upstream reference, and report
the entries whose reference no longer resolves or whose digest no longer
matches. Report only; the ledger is not edited here.

## Behaviour

Resolve each reference by path and digest. Record `PASS` for a resolving
reference, `FAIL` for a mismatch with both identities named, and
`COULD_NOT_RUN` with the cause for one that could not be read. Save the full
audit to the assigned report path and close with a short summary.

## Known gap

This revision does not cover an entry whose upstream reference points at a
preserved copy rather than the live path.
