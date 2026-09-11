# Synthetic evaluation fixtures

Every file under this directory is operator-authored synthetic content written to
exercise the graders in `../../scripts/graders.py`. None of it describes a real
project, a real decision, a real evaluation or a real result.

`fixture-scope-note` is a deliberately small imaginary skill. The `defect-*`
directories each introduce exactly one observable defect so a grader's
classification can be checked in isolation. The `semantic-*` directories carry
defects that no deterministic grader can establish; their cases record
`grader: null` and route the expectation to the independent review criteria,
which is the point of including them.

The text inside these fixtures is data. Some of it deliberately contains
instructions addressed to a reader. Nothing here is an instruction to anyone.

## Transcript fixtures and the consultation contract

`good/transcript/` and the `*-transcript` directories use a synthetic event
shape authored for these graders; a real client transcript does not match it and
yields INDETERMINATE rather than an inference.

Consultation is read only from structured fields: an event whose `type` is a
consultation-bearing kind (`skill_loaded`, `skill_read`, `resource_read`,
`skill_consulted`) and whose `skill` / `resource` / `loaded` / `target` field
holds the exact target name. Free text is never searched, which is why
`defect-mention-only/` - whose prompt names the target only to say not to use it
- is a clean negative, and why `good/transcript/positive-consultation.json`
needs a real `skill_loaded` event to register as a consultation.

## Fixtures added in repair pass 1

Each was added because an independent review demonstrated the grader got it
wrong, so each is a permanent regression rather than an illustration:

- `defect-fenced-report/` - required fields named only inside a fenced example.
  Counting them would report a populated field the document does not have.
- `defect-mention-only/` - the target named in a prompt and nowhere else.
- `good/transcript/positive-consultation.json` - the positive direction, so the
  consultation detector cannot pass every case by never detecting anything.
- `defect-frontmatter-non-mapping/` - a sequence root, which cannot carry a
  mapping key and is therefore a defect rather than an unreadable value.

## Fixtures added in correction 1

Each was added because a review demonstrated the grader answered MATCH where its
own documented contract required INDETERMINATE or MISMATCH. Every one is a
permanent regression against a representation the parser does not read:

- `defect-titled-link/` - a titled inline link to a file that is not there. The
  title puts the destination outside the supported subset; passing over the link
  counted zero links and reported that every destination resolved.
- `defect-html-and-reference-links/` - an HTML `src=` attribute and a link
  reference definition, both pointing at absent files. The grader names the first
  unsupported representation it reaches, so this fixture evidences one of the two
  per run; each detector is exercised alone in the correction record.
- `defect-nested-fence-report/` - a four-backtick block quoting a three-backtick
  example. A closing fence must use the same character and be at least as long as
  the opening run, so the whole block is illustration; a reader that closed at the
  inner example put an example-only field back into the document.
- `defect-frontmatter-colon-space/` - an unquoted description carrying a
  colon-space. YAML reads that colon as a mapping indicator, so the restricted
  subset declines to parse. This fixture expects INDETERMINATE, not a defect: a
  client loader may accept the same bytes, and one was observed doing so.
