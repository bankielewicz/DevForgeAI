# Bounded inspection and evidence

## Contents

- When to use this
- Scope
- Project documents
- Inspecting code
- Leaving the scope
- Evidence items
- Classification
- Insufficient evidence

## When to use this

Read this before step 5 (inspect) and whenever you record an EVD item. Inspection is bounded, read-only
and recorded. Observed practice is never policy, and a missing answer is stated as unknown.

## Scope

- The **inspection scope** is exactly the components or directories the user names, for example
  `services/auth/` or "the billing service in `apps/billing`". Write them to `inspection_scope`, as the
  user named them.
- If the user names none, `inspection_scope: []` and you read no code at all. This isn't a gating
  question: don't stop to ask for a scope. Carry on, and record what couldn't be checked (Insufficient evidence).
- Never crawl or index the codebase, never list or search the whole repository, and never read code outside
  the scope "to get a feel for it".
- Never list the project root or any folder outside `docs/specs/` and the inspection scope. A one-level `ls` of
  the root, or of a scope's parent, counts as listing outside the scope. Forbidden examples: `ls` or `ls -la`
  at the root, `ls services` when the scope is `services/auth`, `find .`, `ls -R`, `grep -r .`. Without a
  Glob tool, find the project documents by these exact paths: `ls docs/specs/policy/ docs/specs/prd/
  docs/specs/adr/ docs/specs/arch/` and `test -e .claude/devforgeai.local.md`.

## Project documents

Always read these, whatever the scope. They are project documents read by contract, not code, so the scope
rule below doesn't apply to them:

- the input PRD, `docs/specs/prd/<PRD-ID>.md`;
- `docs/specs/policy/POL-*.md` (policy resolution);
- `docs/specs/adr/ADR-*.md`: every ADR, to know its status, `superseded_by` and what it decides;
- `docs/specs/arch/ARCH-*.md`: existing architecture descriptions;
- `.claude/devforgeai.local.md`, if it exists (policy resolution).

Framework files (this skill's instructions, references and templates) are not project evidence.
Never record them as EVD.

## Inspecting code

- Inspection is read-only, and **every path it reads, lists or searches is inside the scope**.
- Use Read, Glob and Grep when they are available. When they aren't (some interactive sessions have only Read),
  use read-only shell commands (`ls`, `find`, `grep`, `cat`, `head`) whose every path argument is inside the
  scope, for example `find services/auth -type f`, never `find .`. No redirection, no writes, and never run or
  build project code.
- Validation commands (`devforgeai check`, SKILL.md step 10) are not inspection and don't count against the scope.
- You may follow references (imports, configuration keys, file includes) only while the target is inside
  the scope.
- Look for what the architectural questions need: which component owns which data, how components
  talk to each other, what is deployed where, which platform or library provides a capability, and
  how a quality requirement is met today.
- Stop once each question has its evidence, or you know the scope doesn't contain it.

## Leaving the scope

When a reference leads outside the scope (ERR-03):

1. **Interactive:** ask before reading, naming the path and why it's needed. Read it only if the user
   agrees, and add it to `inspection_scope`.
2. **Not allowed, or no one to ask:** don't read it. Record the gap as an explicit unknown in ARCH §8:
   `[NEEDS CLARIFICATION: <what is unknown>; <path> is outside the inspection scope]`.

## Evidence items

Record **every project source consulted for architecture analysis** as one EVD item: each project document
above that you read, and each file or directory in the scope that informed a finding.

| Field | Rule |
|---|---|
| `id` | `EVD-01`, `EVD-02`, …; when amending, continue the numbering |
| `status` | `active` |
| `source` | the path, `ADR-NNN`, `POL-NNN#SET-NN` or `PRD-NNN`, followed by the version and status examined where the source has them, for example `"PRD-001 (version 3, approved)"` or `"ADR-002 (version 1, superseded by ADR-003)"` |
| `kind` | what the source **is**: `code` (code or configuration), `document` (any other document, including an ARCH or a README), `adr`, `policy` or `prd` |
| `finding` | what it shows, in one or two sentences, for the questions at hand |
| `classification` | what the finding **can establish** (Classification). Independent of `kind` |

- One EVD per ADR, one per policy setting consulted, and one per PRD or ARCH.
- Code: one EVD per file or small group of files that shows one finding.
- When amending, never change an existing EVD. If a source changed (for example, an ADR was superseded
  since), add a new EVD for it at its current version and status.

## Classification

| `classification` | Use for | Can establish |
|---|---|---|
| `observed` | Findings from code or configuration you **directly inspected inside the scope** | What the system does today. Not policy, not a decision |
| `policy` | An approved, active policy setting that applies to this run (effective after R2, or applicable after R4) | That the organization requires it |
| `decided` | An ADR with `status: accepted` and `superseded_by: null` | That the decision was made. It still resolves a DEC only by means 2 (`readiness.md`) |
| `context` | Every other consulted input or historical material: the input PRD (`kind: prd`); an existing ARCH (`kind: document`); a proposed, rejected, deprecated or superseded ADR; a policy document that isn't approved, or a setting that is deprecated or not applicable; documentation (a README, a design note) whose claims you didn't corroborate in the code | Neither implemented behavior nor an accepted decision |

- Classify by what the source can establish, never by how convincing it sounds.
- The PRD is the requirements authority through its links. Its EVD is `context`, because it establishes
  neither behavior nor a decision.
- A document inside the scope is `context` unless you confirmed its claim in the code. Then the code's
  EVD is `observed`.
- **No classification resolves a DEC by itself.** Only `readiness.md` (Resolve a question) does.
- An ignored policy document is also reported in the resolution line, and never linked.
- Knowledge that conflicts with policy (for example, the code uses a platform the policy doesn't mandate)
  isn't an error. Record it as `observed`, and state the conflict in the DEC's `notes`.

## Insufficient evidence

When the evidence can't answer something a question or the user's request depends on:

- Say so explicitly with a marker in ARCH §8, for example
  `[NEEDS CLARIFICATION: which system "our current auth service" is and what it provides; no inspection scope was named and no code was inspected]`.
- Never recommend reuse, or treat an existing system as the answer, on assumption. A request to "reuse X"
  where X wasn't inspected leaves the question open (`readiness.md`, What never resolves a question).
- The outcome can't be `reuse` on missing evidence.
