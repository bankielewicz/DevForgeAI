# Fixtures — all synthetic

Every file under `evals/fixtures/` is **synthetic**. The "Shiftline" project, its requirements,
architecture rules, capability IDs, session assignment and backlog do not exist and describe no real
system, organisation or person. The digests inside these fixtures are real SHA-256 values of the sibling
fixture files they cite, so that reference resolution and staleness can be exercised without a network
or a live project; nothing else in them is a fact about the world.

They are authoring inputs. They are not evidence about behaviour, and reading them establishes nothing
about this skill.

| Directory | What it stages | Used by |
| --- | --- | --- |
| `shared/` | The adopted scope: `PROD-001` (product brief) and `ARCH-001` revision 2 (architecture contract), plus `UX-001` as a *proposed* design spec | Direct activation, missing behavior, traceability |
| `good/` | A conforming `EPIC-001`, `STORY-001` and `HANDOFF-001` written against `shared/` | Deterministic field and side-effect assertions; a reference for what a finished result looks like |
| `draft-placeholder/` | `STORY-009`, identical in shape to a finished story but with a template placeholder surviving in a required field | Placeholder case |
| `stale-upstream/` | A live `ARCH-001` at revision 3, the preserved revision-2 bytes under `preserved/`, and `STORY-004` citing revision 2 by digest | Stale upstream case |
| `collision/` | `SESSION-042`, an operator-authored assignment giving the story destination to a different writer | Ownership collision case |
| `backlog/` | An existing `EPIC-002` with two stories and an accepted `CHG-004` | Indirect activation, revise-not-regenerate |
| `unsupported-criterion/` | Four acceptance criteria supplied by the user, one of which no requirement supports | Traceability case |
| `could-not-run/` | `STORY-007`, whose architecture reference points at an artifact that is deliberately absent | COULD_NOT_RUN case |

`shared/UX-001.md` is deliberately `status: proposed`. A proposed design informs a story; it does not
become a production constraint by being copied downstream, and a case that treats it as adopted is
observing a defect.

The evaluated worker is never given the expected answer inside a fixture. `collision/SESSION-042.md`
states the assignment and nothing about what the worker should do with it.
