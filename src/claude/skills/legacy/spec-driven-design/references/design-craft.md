# Web design craft contract

Load this contract only for Web generation in Phases 03, 04, and 05. It
defines Web quality only. GUI work continues to use `gui-best-practices.md`;
Terminal/TUI work continues to use `tui-best-practices.md`. Neither surface
receives a generated Web artifact or rendered jury review.

## Brief authority and customization

A pinned user or brand direction is authoritative. This includes intentional
use of a palette, typeface, density, structure, or aesthetic that would
otherwise look generic. Anti-default rules constrain only axes the brief leaves
free; never overwrite a pinned choice to satisfy a heuristic.

Resolve and preserve these inputs before planning:

- subject and its concrete world;
- audience and their primary need;
- page job: the single outcome the page must enable;
- brand/design tokens;
- aesthetic direction;
- one signature element;
- density;
- motion preference;
- real content; and
- supplied local references.

Present inputs override defaults. Use real, brief-specific content. Where facts
are unavailable, use clearly labelled placeholders. Never invent business
metrics, customer claims, performance numbers, or social proof.

## Two-pass subject-grounded plan

First plan, then build:

1. Ground every choice in the subject, audience, and page job. Hero is the
   thesis: it expresses the most characteristic useful truth about the subject,
   rather than a generic metric-plus-gradient layout.
2. Define 4–6 named color tokens, 2+ type roles, layout alternatives as short
   prose plus ASCII wireframes, and one signature element. Compare the layouts
   against the brief before choosing.
3. Audit the plan for defaults that could fit any neighboring product. Revise
   only the free axes. Then implement the revised tokens and structure exactly.
4. Spend boldness in one place: the signature. Keep surrounding choices quiet,
   precise, and subordinate.

Match complexity to the direction. Minimal work needs exact spacing, type, and
detail; maximal work needs coherent execution rather than extra decoration.
Structural devices must encode real meaning. Motion must support comprehension
or state change, not merely prove that animation exists.

## Seven cardinal sins

These are P0 failures unless a stated exception applies:

1. **Default indigo** hardcoded as the active accent. An explicitly declared
   global `--accent` token may intentionally contain indigo; the same literal
   hardcoded elsewhere remains a failure.
2. **Purple or trust gradient** tropes: decorative purple→blue or blue→cyan
   gradients without a functional hierarchy purpose.
3. **Emoji UI icons** in headings, buttons, list controls, or icon slots. Use a
   coherent local SVG/icon treatment.
4. **Sans-serif display** text when the declared design binds a serif display
   role.
5. **Rounded left-accent cards** that combine generic rounded tiles with a
   colored left border.
6. **Invented metrics** such as unsupported multipliers, uptime, productivity,
   or conversion claims.
7. **Filler copy** such as lorem ipsum, “feature one,” placeholder prose, or
   sample content presented as final content.

Also avoid external placeholder-image services, excessive raw color literals,
meaningless decorative blobs, perfect symmetry without tension, and the stock
Hero→Features→Pricing→FAQ→CTA sequence when the brief leaves structure free.

## Soul and accent discipline

Use roughly 80% proven interaction patterns and 20% subject-specific character.
Soul comes from one bold visual move, product-specific voice, one memorable
micro-interaction, and one detail that could only come from understanding the
product. A screenshot should be identifiable as this subject, not merely this
page category.

Plan neutrals as the dominant surface, one accent as a scarce signal, semantic
colors for state, and effects only when justified. Aim for no more than two
visible accent uses per viewport; links and focus rings count. This is a source
approximation, not a claim about actual rendered visibility. Preserve WCAG
contrast and never signal state by color alone.

## Web-applicable laws of UX

- **Proximity, Similarity, Common Region, Prägnanz, and Uniform
  Connectedness:** establish grouping first with spacing and alignment; use
  containers and connectors only when they communicate structure.
- **Selective Attention and Von Restorff:** reserve strongest contrast for the
  primary goal and make one exceptional item distinct with a non-color cue.
- **Hick's Law and Choice Overload:** give equivalent choices hierarchy and
  progressive disclosure; do not flatten every option to equal weight.
- **Anchoring and Pareto:** order quantitative comparisons honestly and
  emphasize the few actions that carry the primary journey.
- **Tesler and Cognitive Load:** place irreducible complexity where it can be
  explained contextually; remove extraneous jargon, chrome, and inconsistency.
- **Miller/Chunking and Working Memory:** group familiar units and preserve
  context rather than forcing recall.
- **Serial Position, Peak-End, Zeigarnik, and Goal-Gradient:** order important
  items deliberately, end flows clearly, and show only truthful progress.
- **Fitts's Law:** size and space targets for accurate input, including the
  platform touch-target floor.
- **Doherty Threshold and Flow:** provide prompt, proportionate feedback and a
  clear sense of control through latency.
- **Jakob's Law and Mental Models:** retain familiar category interaction
  grammar; spend novelty on the signature rather than basic operability.
- **Aesthetic-Usability:** polish earns confidence but never substitutes for
  actual usability or accessibility.

## Implementation floor

- Self-contained `artifact.html`: no network, CDN, remote font/image, build
  step, or framework runtime.
- Same tokens, components, content, states, and interactions as `design.md` and
  the framework-specific output.
- Responsive down to the required mobile viewport without horizontal loss.
- Visible focus, logical headings, meaningful alt text, named controls, and
  adequate target sizes.
- If animation or transition exists, provide a reduced motion rule and honor
  the user's motion preference.
- Verify selector precedence, overflow, empty/loading/error states, and every
  interactive path before review.

The linter and rendered jury are evidence gates, not substitutes for this
contract. A generated artifact must satisfy both.
