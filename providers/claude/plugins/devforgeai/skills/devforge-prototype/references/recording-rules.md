# Recording rules for the experiment artifacts

Read this when you fill an XPLAN, an XREPORT or a handoff, and whenever any of these come up: no session record exists, an upstream input no longer matches the revision you referenced, a check you planned could not run, or you are about to overwrite bytes you have already cited.

## The envelope

Both output templates and the handoff carry a `devforge.artifact/v1` YAML envelope. The fields whose meaning matters when filling one in:

| Field | Meaning for an experiment artifact |
| --- | --- |
| `schema_version` | `devforge.artifact/v1`. A proposed schema for these documents, not the CLI's policy schema. |
| `artifact_id` | `XPLAN-<n>` for the plan, `XREPORT-<n>` for the report, `HANDOFF-<n>` for the handoff. Allocate the next unused number only when no identity was selected for you. |
| `artifact_type` | `experiment-plan`, `prototype-report`, `handoff`. |
| `revision` / `status` | Positive integer; `draft`, `in_review`, `accepted`, `superseded` or `retired`. A report stays `draft` until someone with the authority to accept it does so - producing it is not accepting it. |
| `created_at_utc` | The actual UTC creation time for this revision. Not a plausible-looking one. |
| `producer` | `devforge-prototype`, and the exact loaded skill revision or digest. |
| `execution_ref` | The authority-selected session record and revision. Use `null` plus an entry in `missing_inputs` when no session record exists; its absence does not establish ownership. |
| `upstream` | The causal inputs: `artifact_id`, `revision`, `store`, `path`, `sha256`, and the stable section IDs you actually relied on. The XREPORT's upstream includes its own XPLAN. |
| `evidence` | Locators for the raw observations, command output and environment records the report cites. |
| `supersedes` | Prior artifact ID, revision and digest, or `null`. Retain the prior bytes. |
| `decision_ref` | The user's actual adoption of the disposition, or previously delegated authority; `null` while none exists. A report you wrote does not adopt itself. |
| `missing_inputs` | Explicit unresolved required information - an absent threshold, an unavailable runtime, an unresolvable upstream revision. |

## Upstream references

An experiment is only as meaningful as the requirement it was aimed at, so the reference has to be exact.

Cite the artifact ID, its revision, its store and path, its `sha256`, and the stable section IDs you relied on. Record whether that source is **draft** or **accepted**, because it changes what the finding can do: a proposed source can motivate an experiment and support exploration, and it cannot become an accepted production constraint by being copied into your report. If your report reads as though a draft were settled, a later reader will treat it as settled.

For an established project, reuse the valid current artifacts rather than replaying earlier phases to regenerate them.

When the upstream has moved on while you were working, two separate things follow and running them together is how a report gains a commitment nobody made:

- **Repairing a broken reference** is mechanical. If the revision you cite is archived somewhere reachable, find it, confirm it hashes to the digest you cite, and point the locator at the archive. That fixes a path and changes nothing about what has been adopted.
- **Adopting the newer revision** is a decision needing the user's actual authorisation covering this change. The newer document's own `accepted` status and its own `decision_ref` are decisions recorded about that document; neither is the user adopting it into your experiment. Where it changes what should have been measured, that is a finding to surface and a plan revision to propose, not a threshold to silently re-aim.

## Digests, and the order of the writes

No artifact carries its own complete-byte digest. The ordering of the writes is what keeps the references true:

1. Write the XPLAN. Freeze it - hash the final bytes and record the identity - **before** any measurement exists.
2. Run the experiment. Preserve the raw output at a stable path, then hash it.
3. Write the XREPORT, putting the plan's digest in its `upstream` and the raw evidence locators and digests in `evidence`.
4. Write the handoff, putting the plan's and report's digests in its output rows. The handoff's own digest never goes inside the handoff, and a handoff does not list itself among its own outputs.
5. Hash last, and hash again after any further edit. A digest computed before one more edit describes bytes that no longer exist.
6. Read your own references back after the last write. Every `upstream`, `supersedes`, output row, evidence locator and invalidation condition that names a revision, a path or a digest has to resolve, right now, to bytes that match. Digests get repeated - the same file typically appears in an evidence list, an output row and an invalidation condition - and a stale copy in any one of them is the same defect as a wrong primary reference, just harder to notice.

A digest is only true while the bytes behind it are reachable. Before you overwrite a file whose digest you cite, copy the current bytes to a stable authorised location, verify the copy's digest against what you are citing, and point the reference at the copy. If you cannot preserve them, record that in `missing_inputs` and cite only what exists. A digest with no reachable bytes behind it is a claim the next reader cannot check.

`producer.skill_revision` is the SHA-256 of the installed `SKILL.md` file's bytes - one file. It is not a digest of the package, and it is not the plugin version, which can be identical across two different drafts and therefore identifies nothing. Say which one you have, in the artifact and not only in your message to the user. Where nothing observable gives you the value, `unknown` is the honest entry; a plausible-looking digest is not.

## Filling the plan

`assets/experiment-plan.md` is the governing template, copied into this package unchanged. Fill a copy at the destination; never fill the package template in place.

- **Source requirement/decision references** and **Hypothesis** carry the whole point of the document. The hypothesis has to be falsifiable - a claim with a threshold and an observation that could contradict it.
- **Why inspection alone is insufficient** is the check against running an experiment nobody needed. If you cannot answer it, the honest result is that no experiment is warranted.
- **Permitted prototype path**, **Allowed tools and services** and **Time/resource bound** are the fence. They come from the user or the assignment. A bound you invented is a proposal, and it must be labelled as one.
- The **case table** needs a distinct success threshold and failure condition per case. "It works" is neither.
- **Plan identity frozen before execution** records the plan's own digest and where that identity is held. Where an external freeze exists - a commit in an authorised experiment worktree, an operator-held receipt - name it. Where none exists, say so plainly: self-recorded is self-recorded, and no CLI capability currently binds a plan's bytes outside the evaluated agent's reach.

## Filling the report

`assets/prototype-report.md` is the governing template, copied unchanged.

- **Experiment identity** must name the exact plan revision, the prototype location or snapshot, its file manifest, and the runtime and configuration the measurements depend on. A number without an environment is not reproducible.
- The **observations table** carries the actual output per case with a locator for the raw evidence. `NOT_RUN` is the template's starting value and has to be replaced by what happened - an observation, a failure, or `COULD_NOT_RUN` with its actual cause.
- **Interpretation** compares the evidence to the threshold **that the plan recorded**. State the comparison, then keep observation and recommendation in visibly separate sentences.
- **Disposition** is a proposal. `User decision reference` stays `null` until the user actually adopts one. `Required production hardening` is where the gap between the prototype and shippable code is written down honestly - security, tests, persistence, migration, error handling.
- **Changed product/design/architecture assumptions** names exact upstream references so their owners can find them. Naming them is routing, not amending.

## Placeholders

A template placeholder left in a required field means the result is a draft and cannot be presented as ready. A missing fact goes in `missing_inputs`, never into template filler, and never into a plausible-sounding substitute. This applies to every `{{...}}` in every one of these documents, including the ones nobody is likely to read.
