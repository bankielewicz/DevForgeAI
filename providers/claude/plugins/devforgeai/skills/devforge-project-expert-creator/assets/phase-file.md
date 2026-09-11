# Phase file template

One `phases/phase-NN-name.md` in a multi-step workflow skill. Copy this into the package you are authoring and fill it there; a reference-only expert has no phases and needs none of this.

Number the files in the order they are normally reached (`phase-01-…`), and name them for the work, not for a ceremony. The entry `SKILL.md` links every phase file directly, so each is one level deep from the file the client always loads.

```markdown
# Phase NN: {{Name}}

**Classification:** {{Enforced / Optional, and the governing record that says so - or `PROPOSED - not adopted` with the owner who would decide.}}
**Applies:** {{Always, or the condition that selects this phase.}}

## Purpose

{{What this phase is for, in one or two sentences. Why the work stops here rather than running on.}}

## Needed inputs

{{Which of the entry point's declared inputs this phase consumes, and which earlier phase's output it continues from. Name the rows; do not restate the table.}}

## Substantive work

{{The actual instructions: the decisions, the rules that must hold, the judgement calls and how to make them, and the conditional branches. This is the part that justifies a separate file.}}

## Produced outputs

{{What exists afterwards that did not before - artifacts, records, decisions - and where it is saved.}}

## Next phase

{{The one immediate continuation, as a relative link. Then the alternative exits: the condition that ends the workflow early, and the condition that stops and hands back. Every route names the phase it goes to.}}
```

## Rules that keep the set coherent

- **No duplication with the entry point.** `SKILL.md` carries activation, scope, the authority and safety boundaries that must stay visible for the whole task, the phase map and the stopping condition. Detail lives in exactly one place.
- **One immediate continuation.** Each phase names the next phase, plus any early exit and any stop-and-hand-back condition. Every route ends at the final reporting phase.
- **Reachable both ways.** Every phase file appears in the map, and every map entry is a file that exists.
- **A phase file does not enforce anything.** It states obligations. Phase state, transitions, gates and acceptance belong to the compiled runtime; do not write phase acknowledgements, self-issued PASS labels, a copy-and-tick progress checklist or a simulated advance sequence in place of a check that does not exist.
- **Keep each file readable on its own.** Anyone arriving at this phase should be able to act from this file plus the entry point. Add a short contents list if the file passes about a hundred lines.
- **Preserve identity when refactoring.** Moving an inline workflow into phase files keeps its behaviour, its accepted decisions, its stable IDs and the meaning of every reference. Anything omitted or changed is called out explicitly, not left for a reader to discover.
