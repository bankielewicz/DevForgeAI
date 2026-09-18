# User interface specification

Read this resource when the selected story actually includes web, desktop, mobile or terminal interactions. Infer from the selected behavior and existing product design; keyword matches are only hints. Ask about an unresolved interface decision, not one already answered by the request. For backend-only or documentation-only scope, state the actual non-applicability reason in the story and omit the conditional UI section.

Keep the UI specification inside the same story. A textual wireframe/table is sufficient for this authoring workflow; no browser, image generator or design service is required. Cite an existing design artifact when selected, with its current identity and relevant screen/state. Do not claim rendered UI correctness from prose.

## Components and layout

For each screen/region/component identify purpose, data source/owner, inputs, displayed values, actions, state and validation. Match names to the product's actual component conventions. Include a terminal-readable layout showing hierarchy, navigation and action placement. Define relevant responsive/reflow behavior from project constraints rather than inventing device breakpoints.

For example, a form specification can name the input labels/types, required/optional status, submit/cancel actions and locations of field/global feedback. It must also describe loading, empty, error, success and disabled/read-only states when those states can occur. Do not introduce login, analytics or payment widgets just because a template illustrates them.

## Interfaces and interaction

Document component input/output/events and validation contracts at the level needed by the implementation. Connect each meaningful user action to its data/API dependency, state change, success observation, failure message and recovery path. Include duplicate submission, stale data, cancellation, navigation away and retry when applicable. Define whether entered data is preserved after failure and which actions remain available.

For desktop/mobile, identify native lifecycle, input and navigation constraints. For terminal interactions, specify prompts/defaults, noninteractive behavior, output streams, exit results, keyboard navigation where applicable and cancellation. No user interaction should depend solely on a GUI if the selected product contract requires terminal parity.

## Accessibility and verification

Use the project's selected accessibility standard and target level; do not assert certification. Specify keyboard reachability/order, focus entry/return, accessible names/roles, label/error associations, status announcements, non-color cues, contrast targets, zoom/reflow and motion behavior as applicable. Resolve unknown essential targets through the governing design rather than importing arbitrary example numbers.

Map UI interactions and states to ACs and verification observations. Separate unit/component behavior, integration with real data, assistive-technology checks and actual native visual QA. Mark unperformed UI/platform observations explicitly. The completed text specification enables later tests; it does not prove that a rendered screen works.
