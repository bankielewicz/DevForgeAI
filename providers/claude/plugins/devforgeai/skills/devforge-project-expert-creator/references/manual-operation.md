# Manual operation: who owns which command

The user initiates each skill and each command. These packages preserve ordinary discovery; they do not schedule one another. Authoring, evaluation, test operation and integration are distinct responsibilities, and a user authorising several of them in one assignment does not merge them - an author still cannot supply the independent judgement of its own candidate.

## Artifact mapping

The working design document derived from `assets/skill-design-spec.md` is the detailed design. The expert specification (XSPEC) states or references its capability scope, authority, source and API versions, decisions and requirements. The expert package record (XPKG) is the exact candidate and provenance map: canonical and intended installed paths, source pins and the file manifest. Do not maintain a second independent design alongside these.

On the evaluator's side, a validation plan is the detailed evaluation plan (EVPLAN) and the results and decision records are the report (EVREPORT). Envelope records link those exact artifacts where a downstream consumer needs the identity. Preserve the repair specification and both producers' handoffs. Never give a document its own complete-byte digest.

**Creator exit:** candidate, design and XSPEC, XPKG, change record, and a prepared evaluator handoff.
**Evaluator exit:** EVPLAN, EVREPORT and evidence, a bounded repair specification, and a prepared creator handoff.

A receiving task becomes concrete only when the producer's saved handoff exists and the receiver's package, input locations, output fence and any required allowance are resolved. Writing a prompt, sending a recommendation or calling a reviewer is not a user-mediated transfer. Each receiver loads the producer's real artifacts and records the exact inputs, outputs, outcome and remaining work.

Invocation form is the operator's choice, not yours to assert. A project-local Claude skill is invoked as `/<skill-name>`; a plugin skill is namespaced as `/<plugin-name>:<skill-name>`, or bare when no name collides. Treat both as illustrative and confirm what is actually installed before naming one in a handoff. Where the receiving skill is not installed, write the next task in plain language with resolvable absolute paths instead.

## Concise handoffs and retained evidence

The handoff is an entry point into existing evidence, not a second copy of it. Keep the outcome, a short rationale, the next owner and action, the material blockers and the permissions visible. Full requirements stay in the specification, changes and dispositions in the change record, and source and provenance inventories in XSPEC, XPKG and the preserved inputs. Save missing required information in the appropriate record before linking to it; a shortened handoff cannot discard it, and an unsubstantiated summary does not replace it.

Give a reading order with the relevant requirement, finding and section IDs. Record exact pins once in the handoff envelope and use names or links in the brief. This routes attention; it does not reduce the receiver's review coverage, skip a required check, or turn a missing observation into a pass.

A copyable receiving task needs an actually available skill or a plain task, resolvable evidence locations, an assigned writable destination, and any required execution or review allowance. Resolve these for the receiving environment - a path that exists only inside the producer's sandbox is not a usable host path. If a required binding is unknown, mark the transfer prepared with that prerequisite and its owner and supply a setup task, rather than implying the receiver is ready to run.

Use the assigned durable artifact location and retain the referenced exact bytes. Before an owner cleans up or relocates temporary evidence, preserve a snapshot and record the path mapping. A hash does not preserve content. Never add a later receipt or a receiving result into a frozen producer handoff.

## Command boundaries

Use absolute paths for the project and the policy; the assignment supplies them. Inspect the selected executable's own `--help` before relying on any of this. Each row states what the command actually proves - which is always narrower than the phase it supports.

| Owner and action | Command | What it proves, and what it does not |
| --- | --- | --- |
| Operator or creator recovers grounding context | `devforge expert prepare --project <abs-project> --policy <abs-policy>` | Loads the external policy and project and returns grounding inputs. Read-only. Invalid or missing input refuses. It is not proof that any phase completed. |
| Integration owner binds a project expert | `devforge expert bind --project <abs-project> --policy <abs-policy> --expert <declared-relative-expert-dir>` | Records the exact policy, upstream document and package digests plus binding history in the project's expert directory. It explicitly leaves behaviour `NOT_EVALUATED`. Missing input or a collision refuses. Not the creator's command. |
| Operator checks freshness | `devforge expert status --project <abs-project> --policy <abs-policy>` | Reports `MISSING`, `CURRENT` or `STALE` against the recorded binding, and a separate behavioural status that stays `NOT_EVALUATED` until a real terminal evaluation is recorded. |
| Operator gates a project candidate | `devforge check --project <abs-project> --policy <abs-policy>` | Checks approved dependencies, layout, tooling pins and expert provenance. It does not check this skill's workflow and does not certify semantic behaviour. |
| Integration owner exports a runtime plugin | The companion repository's `scripts/install_framework.py` with `--framework <DevForgeAI> --provider claude --export-plugin <parent>/devforgeai` | Writes a new export directory only, omitting `evals/`, history and caches. A collision or an unsupported component refuses. Export is staging for isolated resource testing; it is not adoption and not evidence of native admission. |
| Integration owner installs into a project | The same script with `--framework <DevForgeAI> --provider claude --project <project>` | Generates the project-local installed copies from the selected provider source. Installation is not activation, not evaluation and not acceptance. |
| Evaluator inspects a package or reduces evidence | Not available in this environment | These helpers belong to the Claude `devforge-evaluate-expert` package, which is a separate port. Record the dependency; do not name a path for a helper you have not confirmed exists. |

`devforge expert bind`, `devforge expert status` and `devforge check` accept their flags at the leaf subcommand, as their own `--help` output shows. The installer script is the companion DevForge repository's existing tool: it is legacy Python awaiting the required migration into the Rust CLI, and naming it here is a description of the current integration route, not an endorsement of adding more logic in that language.

The Codex-only `--manual-experts-only --manual-evidence` installation mode and its adoption-evidence predicate are `NOT_APPLICABLE` to this package. They refresh two recognised Codex identities and say nothing about a Claude package.

## What these commands do not cover

The five phases in `SKILL.md` are the workflow this skill performs. They are not CLI subcommands and no command above intercepts them. The commands implement exactly the predicates stated in their rows: they do not guard manual authoring, receiving, or native execution against phase evidence.

Missing, stale or invalid package evidence blocks the claim that depends on it - it does not block reporting. Semantic quality requires a separate independent review, which no command here performs. Do not present any of these as universal enforcement, and do not simulate a transition that no command performed.

## Historical identities

The DevForge managed-runtime workflow IDs `skill-builder` and `skill-validator` belong to an older protocol on the Codex side. They are historical identities preserved in provenance records, not discoverable aliases for this package and not a managed adapter this package admits. The managed `advance` / `resume` / `complete` helper sequence belongs to that protocol as well: do not call it here, and do not assemble a hand-run substitute for it. Automated scheduling, automatic receiver invocation, retry and repair loops and funded-launch qualification are deferred, and the failures recorded against them are preserved rather than resolved by this port.
