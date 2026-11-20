---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
flags: m
---
^\| \d+ \| ASM-\d{2} \| (?!(?:(?:Fatal|Serious): stops IDEA-\d{2}(?:, IDEA-\d{2})* \(\d+ of \d+ in the cut table\)\.|Minor: stops no idea in the cut table \(0 of \d+\)\.) \| (?:high|medium|low) \| (?:(?:Data|Prototype|Interview): [^|\n]+|\[NEEDS CLARIFICATION: how to test ASM-\d{2}\]) \|[ \t]*$)
