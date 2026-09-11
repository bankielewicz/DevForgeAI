# Checkpoint and transfer: producing and delivering the handoff

Read this when the declared mode is checkpoint/transfer. Orient/resume does not use it, and
file or receipt checks are NOT_APPLICABLE to that mode by the declaration you made before
resolving records - not because an artifact happened to be missing.

## Contents

- [Before you write anything](#before-you-write-anything)
- [Write order, so the digests stay honest](#write-order-so-the-digests-stay-honest)
- [What the handoff has to make recoverable](#what-the-handoff-has-to-make-recoverable)
- [Delivering the receipt](#delivering-the-receipt)
- [When there is no writable delivery path](#when-there-is-no-writable-delivery-path)
- [Failure modes this procedure exists to prevent](#failure-modes-this-procedure-exists-to-prevent)

## Before you write anything

Confirm three things, and say so in your result:

1. **A checkpoint trigger actually applies** - explicit request, transfer, a pause needing
   durable recovery, ownership release, or a governing workflow that requires recorded delivery
   at completion. A routine resume is not one.
2. **You have exactly one independently authorized output location.** Its authority is separate
   from the state of the contribution being described; a blocked inner task does not revoke it.
3. **The facts have changed, or a new checkpoint was requested.** Reuse current records rather
   than emitting successive handoffs that restate unchanged state. A user asking for a fresh
   checkpoint is still honored - they are allowed to want one.

## Write order, so the digests stay honest

An artifact never contains its own complete-byte digest. The only way to keep that true is to
finish each file before anything hashes it:

1. Finish every task output you intend to list. Hash each one only after its bytes are complete.
2. Write the handoff, embedding those digests in its inputs/outputs table.
3. Read the handoff back from disk and compute its digest from the bytes you just read.
4. Deliver that digest **outside** the handoff - in your final response, and in an external
   receipt if your assignment provides one.

Never insert step 4's digest into the document, and never edit the document afterwards to record
its own receipt. If the handoff has to change, that is a new revision with a new digest: preserve
the previous bytes rather than mutating a document whose digest has already been delivered.

`<selected devforge executable> receipt check` performs the mechanical part of step 3, and helps
you inspect step 4. Invoke it through the absolute path of the DevForge executable your assignment
selected; nothing puts it on `PATH`. It has two commands, because they establish different things
and merging them would overstate what you know. [scripts/check_receipt.py](../scripts/check_receipt.py)
remains in this package unchanged as the legacy baseline, and is no longer the instructed path;
its retirement is a later owner decision.

**Command 1, verify the receipt.** This is the one the workflow depends on:

```bash
/absolute/path/to/devforge receipt check \
  --file /absolute/path/to/HANDOFF.md \
  --expected-sha256 <the 64-character digest you are about to deliver>
```

Exit 0 means the digest is well-formed 64-lowercase-hex and recomputing the file's bytes
reproduces it. Exit 2 means a check failed. Exit 3 means the file could not be read, which is
COULD_NOT_RUN rather than FAIL. Exit 4 means the invocation asserted nothing.

**Command 2, list digests for your own inspection.** This is a listing, not a verdict:

```bash
/absolute/path/to/devforge receipt check \
  --file /absolute/path/to/HANDOFF.md --self-receipt-inspection
```

Inspection lists recognized standalone 64-hex tokens. Exit 0 means the scan found no recognized
token; it does not establish that the document contains no self-receipt. Unicode-adjacent or split
representations may escape the listing. Manually inspect the document regardless of the listing
outcome. It fails if the file literally contains its own final digest, though that predicate cannot
be made to fail by construction and is not a tested guarantee. Other recognized tokens are reported
as COULD_NOT_RUN with a line number, exit 5, because it cannot tell a legitimate reference to
another file from a receipt for this one.

A normal handoff lists many digests in its inputs table, so exit 5 is the expected result there.
That is not a failure; it is the command telling you which lines you must read. **You** confirm
that none of them is a receipt for this document. Two things that commonly look alike:

| Line | Verdict |
| --- | --- |
| `input \| prior/HANDOFF.md \| <digest>` - same basename, different path, an earlier file | Legitimate. A historical reference is not a self-receipt. |
| `This document (HANDOFF.md) sha256: <digest>` - or the same claim spread over a "file:" line and a "sha256:" line | A self-receipt. Remove it; the digest belongs outside the document. |

The compiled command, like the script it replaces, proves byte identity and receipt format. It does not know whether the handoff is
correct, authorized or accepted, it does not establish that the document is free of a
self-receipt, and no exit code from it may be reported as semantic acceptance.

## What the handoff has to make recoverable

Use `assets/handoff-template.md`, the package-local copy of the shared template. Its inputs
table is the recovered-context inventory; the original records stay authoritative. Fill required
fields with real values - a placeholder left in a required field means the result is still a
draft and cannot be presented as ready.

The reader must be able to recover, without the conversation that produced it:

1. **Two task states, kept apart.** The recovery task and the underlying contribution task. One
   can be complete while the other is blocked.
2. **Who and where.** Role, runtime provider, owner, assignment reference, worktree, base,
   write fence, and the authorization carried forward with its scope.
3. **What was verified, and what was not.** Required input, package, candidate and evidence
   identities; the verification you actually performed; and the facts explicitly unavailable,
   with their expected identities preserved.
4. **What is unresolved.** Open finding identities, conflicting observations between records,
   and the continuation each affects.
5. **One next task.** With prerequisites, owner (or the unresolved-owner gap), output
   destination, and the checks that would evidence completion. Name only real installed skills
   or a plain-language request; a command that does not exist is not a continuation.
6. **Custody.** Ownership disposition, the observed checks with their exact outcome labels, and
   the changes that would invalidate this recovered view.

Use exactly PASS, FAIL, NOT_RUN, COULD_NOT_RUN, NOT_APPLICABLE for check outcomes. Preserve
historical omissions and outcomes as they were recorded - a later successful check does not
retroactively repair a frozen earlier trial, and rewriting one to look better destroys the
evidence trail the handoff exists to carry.

## Delivering the receipt

Delivery means the reader can find and verify the file:

- the **full absolute path**, and
- the **complete 64-character SHA-256**, lowercase hex.

Deliver both in your final response. An earlier tool output that happened to print a hash is not
delivery - the terminal result is what the recipient reads. An abbreviated digest, a digest of a
different path, or a digest computed before the last edit are each a failed delivery, not a
minor formatting problem. Hashing a file in a trace without stating the result is not delivery
either.

## When there is no writable delivery path

Report that specific limitation through the terminal channel you are permitted to use, and say
what would unblock it. Do not invent a substitute outbox, write outside your fence, or quietly
convert the request into an orientation answer. The correct result is an honest report that the
checkpoint could not be persisted, with the recovered context still delivered in-session so the
work is not lost.

## Failure modes this procedure exists to prevent

| Failure | What it looks like |
| --- | --- |
| Record churn | A new handoff on a routine resume, restating unchanged facts. |
| Missing delivery | The handoff is written but its path and full digest never reach the final response. |
| Abbreviated or wrong receipt | A shortened digest, a digest of the wrong path, or one computed before the final edit. |
| Trace-only hashing | A hash appears in tool output and is never stated as the delivered receipt. |
| Self-digest loop | The document carries a receipt for itself, so the value can never be correct. The helper lists digest lines; you decide. |
| Retroactive repair | A frozen failed trial or historical omission edited to look better. |
| Invented outbox | Writing somewhere unauthorized because the permitted path was unavailable. |
