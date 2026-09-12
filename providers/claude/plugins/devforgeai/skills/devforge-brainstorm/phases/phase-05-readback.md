# Phase 05: Read back and verify

**Classification:** A package-local step, **not** a runtime phase. [`references/managed-runtime.md`](../references/managed-runtime.md) names exactly four phases - Recover, Explore, Record, Focus - and this is not a fifth: never supply `05` or `readback` as a checkpoint `phase` value. It carries the write-ordering and read-back obligations of the Record and Focus writes, which used to sit inline in `SKILL.md` under "Before you call it done", in one place so that neither phase has to repeat them. The skill-authoring contract classifies no brainstorm phase. **Applies:** always, on every route that wrote anything - including a partial or blocked result that saved a record.

## Purpose

Make the references true. This is the verification work; it is retained evidence, not presentation, and it does not move into the summary or get shortened for it.

## Needed inputs

The artifacts [phase 03](phase-03-record.md) and [phase 04](phase-04-focus.md) saved, and the identity of the installed `SKILL.md` you are running from.

## Substantive work

No artifact carries its own digest, so the ordering of the writes is what keeps the
references true:

1. Write the ledger, then hash it.
2. Write the handoff, putting the ledger's digest in its output row - and, on the
   ordinary ledger-plus-handoff path, bind the completed ledger in the handoff's own
   `upstream` frontmatter: one unambiguous entry carrying that ledger's artifact ID, its
   revision, `store: project`, its selected path, that same digest, and the ledger
   headings you actually relied on. The output row and the upstream entry are separate
   claims, and a correct row does not supply the causal one - a managed runtime checks
   the frontmatter binding at Focus, against the ledger bytes it just read. A routed
   handoff-only task produces no ledger and carries no such entry.
   [`../references/recording-rules.md`](../references/recording-rules.md) has the exact fields.
3. Hash last. A digest computed before one more edit describes bytes that no longer
   exist, so if you touch a file again, hash it again. The handoff's own digest never
   goes inside the handoff, and a handoff does not list itself among its own outputs.
4. Then read your own references back, after the last write. Every `upstream`,
   `supersedes`, output row, resume line, invalidation condition and continuation note
   that names a revision, a path or a digest has to resolve, right now, to bytes that
   match at that locator. Digests get repeated - the same file typically appears in an
   output table, a custody line and an invalidation condition - and a stale copy in any
   one of those is the same defect as a wrong primary reference, just harder to notice.
   Check each occurrence rather than only the first.

A required field still holding a placeholder means the result is a draft and cannot be
presented as ready. A missing fact goes in `missing_inputs`, never into template filler.

`producer.skill_revision` is the SHA-256 of the installed `SKILL.md` file's bytes - one
file. It is not a digest of the package, and it is not the plugin version, which can be
identical across two different drafts and therefore identifies nothing about the bytes.
Name which one you actually have, in the artifact and not only in your message to the
user: a bare 64-character string tells a later reader nothing about what was hashed, and
they have no way to recover it. A short parenthetical is enough, on every artifact you
emit, not just the first. A managed runtime binds the installed resource identities
itself. Where nothing observable gives you the value, `unknown` is the honest entry; a
plausible-looking digest is not.

## Produced outputs

The saved artifacts, with every locator and digest in them read back and matching, and a record of what was and was not checked. That record is what [phase 06](phase-06-completion-summary.md) draws its one accuracy sentence from; it stays in the artifacts, where it remains retrievable, rather than being printed.

Structural conformance and semantic quality are separate observations, and passing the first is not evidence about the second - no available tool judges whether the ideas are any good, whether the attributions are faithful, or whether the ledger means what it says. If a runtime verified these artifacts it reports that result itself, with its own locator and digest; if none did, they are unverified drafts and must be described that way, with completion and any receipt left at `NOT_RUN`.

## Next phase

Continue to [phase 06, completion summary](phase-06-completion-summary.md). If a read-back does not resolve, fix the reference and hash again before going on - an unresolved locator is a defect in the artifact, not something for the summary to disclaim.
