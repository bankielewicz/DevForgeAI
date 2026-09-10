# Mockups, preview, and what a mockup does not prove

Read this at the Render phase, and whenever you are about to write something about how a mockup looks.

## What to build

Self-contained local HTML and CSS in the declared design directory. One file per screen or state, or one file with clearly separated state sections - either is fine as long as the flow and state IDs in the design-spec map onto something a reviewer can actually open.

Self-contained means: no build step, no package install, no network fetch required to see the page. A mockup that needs `npm install` before anyone can look at it is not reviewable, and a mockup that silently depends on a CDN will render differently, or not at all, for the person reviewing it offline. Inline the CSS or ship it beside the HTML; embed small images as data URIs or keep them in the same directory.

Where the project has an approved existing UI tooling path - a component library with a running storybook, a design tool the project has adopted - use it instead, and record which one and how to open the result.

## Using the project's conventions

An established project has approved conventions: its component vocabulary, its spacing and type scale, its existing screens. Match them. A mockup that looks nothing like the product it belongs to makes the review about the styling rather than about the flow.

Where you want to depart from an approved convention, that is a proposal with a stated reason, recorded in the decisions section - not a substitution made in passing. Where no stack or conventions are approved yet, what you write is a proposal too: say so explicitly, and do not let a mockup's incidental choices become the project's de facto design system by being copied downstream.

## Preview instructions

Every asset row needs an instruction a person can follow without asking you anything. That means an absolute path or a `file://` URL, not "open the mockup".

```text
file:///abs/path/to/project/docs/devforge/design/mockups/UX-001/signup-error.html
```

For approved tooling, the exact command to run, in a `text` fence, with the absolute project path filled in.

## Inspection is a separate fact from existence

Writing the file proves the file exists. It does not prove anything about how it renders.

| `Inspection result` | When it applies |
| --- | --- |
| `NOT_RUN` | The file was written and nothing rendered it. This is the default and the common case. |
| `COULD_NOT_RUN` | A visual check was required for the claim being made and the tooling was unavailable or failed. Record the actual cause - "no browser tool available in this session", not "could not check". |
| A recorded observation | A browser or rendering tool actually displayed the page. Record which tool, at what viewport, and what you actually saw - including anything that looked wrong. |

Do not describe rendered appearance you did not observe. "The error banner sits above the form and the focus ring is visible on the retry button" is a claim about pixels; if nothing rendered the page, it is a guess dressed as an observation, and the reviewer has no way to tell.

When the tooling is unavailable, the useful result is still substantial: the files exist, the preview instruction is exact, and a person can look in ten seconds. Say that, and leave the inspection result honest.

## Viewports and device constraints

Where the project states target devices or breakpoints, design against them and say which ones each mockup covers. Where it does not, propose the set you are designing for - a phone width and a desktop width is a reasonable minimum - and label it a proposal.

If you did not render the page, you did not check the responsive behaviour either. Describe the intended behaviour as intent, and keep it out of the inspection column.

## What a mockup does not establish

State these limits in the design-spec's decisions section rather than leaving them implied:

- **Not backend functionality.** A mockup showing a successful save shows the intended experience of a successful save. Whether the system can do it is a question for architecture or a bounded prototype.
- **Not accessibility conformance.** Keyboard and focus behaviour written into the state table is intended behaviour. Conformance is a measured result from an actual audit against a named standard, and nothing here produces one. Say "intended keyboard behaviour", never "accessible".
- **Not production readiness.** Real data is longer, emptier and stranger than mockup data. Name the places where you know that gap is largest.
- **Not a resolved technical uncertainty.** If a flow depends on something nobody has demonstrated - a latency budget, a third-party API's real behaviour, whether an interaction is achievable in the approved stack - that is an open question for a bounded prototype, listed as one. Drawing it does not make it possible.

## Fixtures and synthetic content

Mockup content is illustrative. Use obviously synthetic names, amounts and dates, and say in the design-spec that the content is synthetic. Never paste real user data, credentials, or production identifiers into a mockup file - they are as durable as the file, and the file gets committed.
