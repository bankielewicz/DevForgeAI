# Evidence and scope rules

Read this in Investigate and Define: how to record a source, where the line between observation and inference sits, how to write a requirement someone can actually check, and how to keep a proposal from turning into a commitment.

## Recording a source

Every claim that affects what is in or out of scope carries its basis. The brief's discovery-evidence table has a column for each part of that, and each part earns its place:

| Column | What it holds | Why it matters |
| --- | --- | --- |
| Evidence ID | `EVID-<number>`, stable and never reused. | Requirements cite it; a renumbered ID breaks the trace. |
| Claim | The specific statement this evidence supports - not the topic. | "Support tickets about lost handoffs" is a topic. "Roughly a third of last quarter's tickets mention a lost handoff" is a claim. |
| Source URL or immutable file | Where it came from. A supplied file needs a path that will still resolve. | A source nobody can reach is not evidence. |
| Version / retrieval date | The version the claim applies to, and when you retrieved it. | Sources change. A claim without a date cannot be rechecked. |
| Observation or inference | Which one this is. | The single most useful column in the table. |
| Limit | What this evidence does not establish. | Every source has a boundary; stating it stops the next reader from over-reading it. |

Research is optional and proportionate. A claim that decides whether a requirement is in or out is worth checking; background colour is not. Research is read-only and stays inside the user's own scope: do not contact customers, sign up for anything, or spend money.

## Observation, inference, assumption, invention

Four different things, and only the last is forbidden.

- **Observation.** You read it in a source and can cite where. "The published pricing page on 2026-09-10 lists three tiers."
- **Inference.** You reasoned from an observation. It stays labelled as reasoning and names what it rests on. "Three tiers with no free option suggests they are not competing for hobby users - inferred from EVID-002, not stated by the source."
- **Assumption.** Nobody has established it and the scope depends on it anyway. Record it as an assumption with the consequence if it is wrong and the smallest observation that would settle it.
- **Invention.** A number, a user need, a competitor behaviour or an adoption rate that no source supports and nobody supplied. There is no honest place for this in a brief. When a market-size claim has no source, the row says the claim is unverified and names what would verify it. It does not acquire a percentage because a percentage looks more finished.

An unavailable source stays visible as unavailable. "I could not verify this" is a usable input to a scope decision; a confident sentence covering the same gap is not.

## Writing a requirement someone can check

A requirement has a stable ID, a behaviour, a trigger or user, an observable result, a named source, and a priority. The observable result is the part that most often goes missing.

- **Not checkable:** "The app should be fast." "Users should find it easy to add a note."
- **Checkable:** `REQ-007` - a saved note appears in the list within 2 seconds on the reference device (`NFR-002` carries the device and network conditions). `REQ-008` - a note can be added without leaving the list screen, in at most two interactions.

Nonfunctional requirements need the same treatment plus their conditions: the criterion, the scope it applies under, the evidence or source behind the threshold, and its decision state. A performance number the user did not give you and no source supports is a proposal, not a requirement - number included.

Outcomes are separate from requirements. An outcome is the change the user wants in the world, with a measurement, a baseline (or an explicit unknown) and a target (or an explicit "decision needed"). An unknown baseline is a normal and honest state; an invented baseline is not.

Every requirement names the idea or constraint it came from. Where nothing supports it, its origin is recorded as a proposal and the relevant decision is requested. That is the honest form of "this seems necessary".

## Non-goals are the scope

A brief that lists everything worth doing has not bounded anything. The boundary section carries four separate facts, and collapsing them loses information:

- **Included requirement IDs** - what this release commits to.
- **Explicit non-goals** - outcomes deliberately out. These are the ones a reader would otherwise assume were in.
- **Deferred work and rationale** - out for now, with the reason and what would bring it back.
- **Constraints already adopted** - what the user has decided, with the decision reference.

A non-goal is not a gap you forgot to fill; it is a decision, and it belongs in front of the user like any other.

## User decisions and AI proposals

Keep them distinguishable at the strength they were actually given, in every row and in the frontmatter.

- A requirement's decision state is `proposed` until the user adopts it - in their own words here, or under an earlier instruction of theirs whose scope reaches this change.
- Adoption changes the decision state. It does not change the origin: an idea that started as an AI proposal still shows that it did, and rewriting it as the user's own erases the one fact a later reader needs.
- Keep a preference a preference. "We would probably want this eventually" is not the same commitment as "this has to be in the first release", and flattening them into one strength is a fabrication in the direction that is hardest to notice.
- A constraint the user stated - budget, deadline, platform, operating environment - is theirs and is recorded now, at its actual scope. "That belongs to a later phase" is not a reason to drop it; a later phase revisits what the user decided, it does not make the decision unrecordable.
- The frontmatter `decision_ref` stays `null` while no adoption exists, and names the actual basis when one does - including when that basis is a standing instruction rather than something said in this conversation.

## Technology stays illustrative

Naming a technology to make a requirement concrete is fine. Recording it as the chosen stack is not: that decision belongs to devforge-architect and it needs a brief first. An illustrative mention that quietly becomes an approved constraint is the same failure as a proposal quietly becoming a requirement, one phase earlier.

The exception is a technology decision or constraint the *user* stated. That is theirs, it is recorded with user origin and its actual scope, and it is neither widened into a decision it was not nor dropped as premature.

## What a proposed source can and cannot do

A proposed design, a draft architecture alternative, an experiment plan or a prototype report can inform the scope. None of them becomes an accepted production constraint by being copied into the brief. Carry the decision state across with the content: a proposal cited in a brief is still a proposal, and the brief says so.
