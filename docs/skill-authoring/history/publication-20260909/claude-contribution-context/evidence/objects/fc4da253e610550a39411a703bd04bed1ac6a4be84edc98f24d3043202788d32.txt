---
name: devforgeai-contribution-context
description: Recover the context for a DevForgeAI contribution and return the next permitted action, in two modes - orient/resume for a concise in-session readiness result, and checkpoint/transfer for a finalized handoff delivered with its full path and complete 64-character SHA-256. Use this whenever a session asks what contribution it is assigned, resumes assigned DevForgeAI work, needs a handoff, checkpoint, pause or work transfer, takes over as a replacement architect or worker, or has to reconstruct assignment, ownership, selected revisions, candidate identity and evidence state from shared records - including when those records turn out to be missing, inaccessible or contradictory. Not for ordinary implementation whose context is already complete, general application brainstorming, arbitrary code explanation, or final semantic review.
---

# DevForgeAI contribution context

## Outcome and scope

Identify the assigned task, resolve the records it selects, reconstruct the state from
evidence, and return the next permitted action. Two modes share that workflow and differ only
in what they deliver:

| Mode | Choose it when | Deliver |
| --- | --- | --- |
| Orient / resume | Starting a session, resuming the same assigned work, or checking whether the next action has its required context | A concise in-session readiness result. No new files. |
| Checkpoint / transfer | A handoff is explicitly requested, work is transferred, a pause needs durable recovery, ownership is released, or the governing workflow requires recorded delivery at completion | A finalized handoff, read back, with its full absolute path and complete 64-character SHA-256 delivered in your final response. |

Declare the mode from the request and the governing workflow **before** you start resolving
records. Deciding afterwards invites the two classic errors: writing a handoff nobody asked for
on a routine resume, and downgrading a requested checkpoint to "orientation" once you notice
the artifact would be awkward to produce.

This capability ends with recovery and the mode's output. It does not perform the underlying
code or skill repair, certify that repair, take over another assignment, integrate Git changes,
launch evaluations, or change external policy. Recovering context is also not a new permission:
if the calling session was already authorized to do the work, hand control back so it can
continue without another permission round.

Route elsewhere for: ordinary implementation whose context is already complete, general
application brainstorming, arbitrary code explanation, and final semantic review. Being in the
DevForgeAI repository does not make this capability mandatory.

## Required context

Ask the caller, or the project/session setup, for a bounded task, the selected authority roots
and the actual execution assignment. Checkpoint mode additionally needs one permitted output
location. An existing handoff is a useful optional input, never a prerequisite - a usable
assignment or a still-applicable prior authorization is enough to orient.

Resolve these facts when the selected task makes them applicable. Read
[references/source-selection.md](references/source-selection.md) before you start, and keep it
open while you work - it holds the interpretation rules that make these rows trustworthy.

| Fact | Where it comes from and how to treat it |
| --- | --- |
| Role, owner, authorization, assignment state | The actual selected session or authorization record. The runtime you are running on does not tell you your role. |
| Worktree, branch/base, write fence | The recorded assignment plus observations you are permitted to make. An old producer field does not establish a current owner. |
| Applicable decisions | The exact adopted decision, or a valid prior delegation with its scope. A still-applicable delegation does not have to be repeated in the current request to remain in force. |
| Governing rules and task excerpts | Selected revisions, digests and sections whose source bytes you can actually resolve. Newer text on a main branch is not an automatic replacement. |
| Required expertise | The needed capability, the selected package and any relevant evaluation. If none is installed, say so; do not invent a package. |
| Candidate and evidence state | Exact candidate, export or run identity, recorded checks, open findings and stated limits. A report's PASS is a claim to attribute to its author, not acceptance. |
| Current phase and continuation | Actual preserved observations and prerequisites. Gaps and contradictions stay visible. |

Follow references that are in scope for the task. Do not go looking for a more permissive
owner, policy or root because the selected one is inconvenient - that search is itself the
failure mode this capability exists to prevent.

## Decision guidance

**Provider is not role.** The client you run on, the role an assignment gives you, the source
package that assignment selects, and the permissions you hold are four separate facts. A Claude
session can hold a worker assignment, an architect assignment, or none. Read the role from the
record.

**Selected revision beats newer bytes.** When a record pins a revision and digest, resolve those
bytes. If the working copy now differs, you have made an observation about drift, not a
replacement: report the newer version, name the affected continuation, and leave the selection
to its owner.

**Blocked can be the correct answer.** Recovery succeeds when it truthfully reports that the
underlying contribution cannot proceed. It also succeeds when it reports that delegated work
may continue. Neither conclusion follows from the provider, the role name, or the absence of an
error message - only from the records.

**Separate the two states you are tracking.** Your recovery task can be complete while the
contribution it describes is blocked, and vice versa. Say which is which every time; collapsing
them is how a blocked contribution gets reported as ready.

**Attribute, do not certify.** When one record summarises PASS and a referenced finding records
a failure or a missing observation, keep both, name their sources, keep the candidate and run
identities intact, and route the unresolved question to its owner. Do not resolve it by
preferring the more confident record, and do not quietly restate someone's PASS as your own.

**Say what you could not read.** If a required record will not resolve inside your permitted
boundary, record its known expected identity and the failed resolution, and block only the
conclusion that depended on it. A similarly named file elsewhere is not a substitute, and a
digest you did not compute from bytes you actually read is not a verification.

**Scope what you say about a peer, but read what you were assigned.** Include only what the task
needs for dependencies and collision detection. An unassigned peer source stays protected; a peer
candidate or evidence input your own assignment names, with its locator and digest, is an input
to resolve rather than a boundary to refuse - [references/source-selection.md](references/source-selection.md)
draws the line. Either way, another contributor's private deliberation is not yours to relay,
resolving a record is not authority to edit it or to do the work it describes, and a new role
label does not make you an independent reviewer of your own work.

## Workflow

1. **Establish the recovery task.** Name the actual task, the declared mode, your role, the
   runtime provider, the owner, the selected assignment, and - in checkpoint mode - the
   permitted output location. State plainly what you do not know. If mode, assignment or output
   authority is genuinely ambiguous, ask before resolving records rather than guessing.

2. **Resolve the selected context.** Read the accessible required records. Match identities,
   locators, digests and sections against what the assignment selected, and keep selected older
   revisions distinct from anything newer you happen to observe. Take only what this task needs;
   unrelated project history and another author's deliberation are out of scope.

3. **Carry authority forward with its scope.** Record the applicable authorization and what it
   does and does not cover. Accepted-looking labels, stale producer metadata and a previous
   handoff's suggested next steps are not grants of authority. Absence of a record is not
   ownership either.

4. **Reconstruct state from evidence.** Separate recovery progress, the underlying contribution
   state, recorded check outcomes and actual acceptance. Attribute unverified claims to whoever
   made them, name contradictions between records, and stop any dependent target action whose
   prerequisite is missing or contested - while continuing the recovery and reporting work you
   were independently authorized to do.

5. **Return one continuation, in the declared mode.** Give the next action, its owner (or the
   unresolved-owner gap), prerequisites, output destination and completion evidence.
   - *Orient/resume:* answer in-session and stop. Do not write files, do not restate records
     that have not changed, and do not manufacture ownership or completion state. Pointing at an
     already pinned manifest beats dumping every digest.
   - *Checkpoint/transfer:* follow
     [references/checkpoint-transfer.md](references/checkpoint-transfer.md) exactly. The receipt
     discipline there is where this mode usually fails.

## Verification and missing information

Use exactly these outcome labels, and no synonyms: **PASS**, **FAIL**, **NOT_RUN**,
**COULD_NOT_RUN**, **NOT_APPLICABLE**. Readiness for an identified next action is a separate
assessment - it is neither acceptance nor certification.

Label with care, because the interesting cases are the ones that tempt a wrong label:

- A recovery check can PASS *because* it honestly reported that a required input was
  unavailable. The unavailable underlying check keeps its own COULD_NOT_RUN.
- NOT_APPLICABLE needs a stated scope rule. File and receipt checks are NOT_APPLICABLE to
  orient/resume by the mode you declared - never because an artifact turned out to be missing.
- An unrecognised required record is not inapplicable. Say you could not resolve it.
- NOT_RUN means planned and unattempted. COULD_NOT_RUN means attempted, with a recorded cause.

Check the validity of the references you consume and deliver, and name any obvious contradiction
between referenced records. Regrading transcripts, deciding whether an implementation meets its
specification, and repairing a validator belong to separately assigned work.

Never copy credentials or another session's private client state into anything you produce.

## Deliverable and handoff

**Orient/resume** returns: the identified task and role, the selected record references,
readiness for the specific next action, and material gaps. Nothing else, and nothing written to
disk. Invoked again with unchanged facts, it says the same thing again rather than generating a
fresh record.

**Checkpoint/transfer** produces one handoff from
[assets/handoff-template.md](assets/handoff-template.md), the package-local copy of the shared
template. Its inputs table is the recovered-context inventory. The original records stay
authoritative - the handoff is a derived view, not a replacement registry. Make these directly
recoverable from it:

1. The recovery task and the underlying contribution task, with their states distinguished.
2. Role, provider, owner, assignment reference, worktree/base/fence and applicable authorization.
3. Required input, package, candidate and evidence identities, the verification actually
   performed, and the facts explicitly unavailable.
4. Relevant open finding identities, conflicting observations and the affected continuation.
5. One next task with prerequisites, owner, output destination and completion checks.
6. Ownership disposition, actual observed checks, and the changes that would invalidate this
   recovered view.

Then finalize, read back, and deliver the receipt as described in
[references/checkpoint-transfer.md](references/checkpoint-transfer.md). The handoff must not
contain its own digest. If no authorized writable delivery path exists, report that specific
limitation in the terminal channel you are permitted to use - do not invent a substitute outbox.

Name only real installed skills or plain-language requests in a next-session prompt. A command
that does not exist is not a continuation.

## Supporting resources

- [references/source-selection.md](references/source-selection.md) - how to select, resolve and
  interpret the records: authority, revisions versus newer bytes, evidence versus acceptance,
  and the boundaries around peers and companion repositories. Read it at step 2.
- [references/checkpoint-transfer.md](references/checkpoint-transfer.md) - the checkpoint
  procedure and receipt discipline. Read it when the declared mode is checkpoint/transfer.
- [assets/handoff-template.md](assets/handoff-template.md) - package-local copy of the shared
  handoff template, used for checkpoint output.
- [scripts/check_receipt.py](scripts/check_receipt.py) - two deterministic commands, run with
  `python3` and an absolute path. `--expected-sha256` verifies the receipt: full 64-hex format
  and recompute-and-compare. `--self-receipt-inspection` lists the document's digest lines for
  you to read, because whether a digest is a receipt for this document or a legitimate reference
  to another file is a judgement the script cannot make. It proves byte identity and receipt
  format only; it says nothing about whether the content is correct, authorized or accepted.
- [references/derivation.json](references/derivation.json) - provenance for the copied template:
  source locator, revision, digests, transformation and refresh triggers. Read it when
  maintaining or refreshing this package.
