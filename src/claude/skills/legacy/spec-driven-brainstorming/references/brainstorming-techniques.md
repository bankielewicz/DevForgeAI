---
description: Brainstorming methodology bank referenced by Stream C additions to spec-driven-brainstorming phase files. Each section documents one established technique with source, when-to-use, and a canonical prompt template.
version: "1.0"
created: 2026-05-13
type: reference
---

# Brainstorming Techniques Reference

This file is the methodology source for Stream C work items (Z13-Z18) that add divergent thinking, idea combination, reframing, pre-mortem, out-of-scope generation, time-boxing, and stakeholder role-play to the brainstorming workflow. Each section names a technique, attributes its source, states when the skill should invoke it, and provides a canonical prompt template phases can adapt.

For background on why these are needed, see the parent plan §4 (Stream C: Missing Brainstorming Methodology) at `/home/bryan/.claude/plans/synchronous-meandering-willow.md`.

---

## 1. Divergent / Convergent Separation

**Source:** Alex Osborn, *Applied Imagination* (1953). The original brainstorming framework explicitly separates idea generation (divergent — many ideas, no judgment) from selection (convergent — narrow to best).

**When to use:** Whenever the workflow is about to compile a fixed-size list of opportunities from a small set of structured prompts. Divergent thinking should precede compilation.

**Skill integration point:** Phase 04 (Future-State & Opportunity Mapping) Step 4.3 (added by Z13). Runs after Blue-Sky Visioning (Step 4.2) and before Success Vision (Step 4.4).

**Canonical prompt template:**
```
Display:
"Rapid Ideation mode. Quantity over quality. Quality and feasibility don't matter yet — we narrow later.
List as many ideas as come to mind. Add wild ones, impractical ones, partial ones."

LOOP:
  AskUserQuestion: template=QT-5 (intent: list)
    question_text: "Idea {N}: what's another way to address this?"
    header: "Idea {N}"
  IF user picks "Done — no more to add": BREAK
  IF user provides a description: append to session.divergent_ideas[]
  N += 1

Display: "{count} ideas captured. We'll narrow these in Phase 09."

VERIFY: session.divergent_ideas.length >= 5
  IF less than 5: Display warning that real divergent thinking typically yields 10+; offer one more prompt round.
```

**Quality cue (no real timer):** Phase 04 Step 4.3 may include a one-line note: `This is time-boxed discipline — favor quantity. Five minutes of free generation typically beats an hour of careful selection at this stage.`

---

## 2. Idea Combination (Combinatorial Creativity)

**Source:** Frans Johansson, *The Medici Effect* (2004). Cross-pollination of ideas from different sources produces breakthrough insights more reliably than refining ideas in isolation.

**When to use:** After Step 4.8 (Compile Opportunities) when the session has multiple opportunities from heterogeneous sources (user_vision, technology, competitor, adjacent). Highest yield when at least one opportunity comes from each source category.

**Skill integration point:** Phase 04 (Future-State & Opportunity Mapping) Step 4.9 (added by Z14).

**Canonical prompt template:**
```
Display:
"Some of the strongest opportunities come from combining ideas across sources.
Below are pairings of high-impact opportunities from different categories.
Tell me if any combinations would be stronger than the individuals."

# Compute pairings
top_pairs = pick_top_3_to_5_pairings_by_source_diversity(session.opportunities)

FOR each pair (A, B) in top_pairs:
  AskUserQuestion: template=QT-1 (variant: 2-option)
    question_text: "Can '{A.description}' and '{B.description}' combine into something stronger? (e.g., A's mechanism applied to B's target)"
    header: "Combine?"
  IF response == "Yes":
    AskUserQuestion: template=QT-5 (intent: describe)
      question_text: "Describe the combined opportunity."
      header: "Combined"
    Append to session.combined_opportunities[]

VERIFY: session.combined_opportunities recorded (may be empty if no productive combinations identified)
```

---

## 3. "How Might We..." Reframing (HMW)

**Source:** Min Basadur, IDEO design-thinking practice. Reframing a problem statement as a "How might we...?" question opens solution space that "the problem is X" framing constrains.

**When to use:** After a problem statement is finalized but before opportunity generation. Tests whether alternate framings yield distinct solution paths.

**Skill integration point:** Phase 03 (Problem & Current-State Analysis) Step 3.8 (added by Z15). Runs after Step 3.7 (Generate Problem Statement).

**Canonical prompt template:**
```
Display:
"The problem statement we agreed on is:
  '{problem_statement}'

Let's try reframing it as 'How might we...' questions. Different framings reveal different solution paths."

LOOP (target: 3-5 reframings):
  AskUserQuestion: template=QT-5 (intent: describe)
    question_text: "Reframe #{N} — 'How might we ___?' Fill in the blank."
    header: "HMW {N}"
  Append to session.hmw_reframings[]
  IF user picks "Skip this question" or session.hmw_reframings.length >= 5: BREAK

VERIFY: session.hmw_reframings.length >= 1
RECORD: Persist to checkpoint; mark as input to Phase 04 opportunity generation.
```

---

## 4. Cross-Industry Analogy

**Source:** Clayton Christensen, "jobs-to-be-done" theory. Studying how a completely different industry solves a structurally similar problem reveals novel approaches.

**When to use:** As the second reframing sub-exercise (after HMW). Particularly valuable when the user's industry has long-established orthodoxies that constrain thinking.

**Skill integration point:** Phase 03 (Problem & Current-State Analysis) Step 3.9 (added by Z15).

**Canonical prompt template:**
```
AskUserQuestion: template=QT-1 (variant: 2-option)
  question_text: "Would a cross-industry analogy help? (We'll consider how other industries solve structurally similar problems.)"
  header: "Try analogy?"
IF response == "No": SKIP this exercise

AskUserQuestion: (custom; not a template — list is too domain-specific)
  question_text: "Which industry should we look at?"
  header: "Industry"
  multiSelect: false
  options:
    - label: "Healthcare / hospitals"
    - label: "Aviation / airlines"
    - label: "Retail / e-commerce"
    - label: "Manufacturing / supply chain"
    - label: "Entertainment / streaming"
    - label: "Education"

selected_industry = response

AskUserQuestion: template=QT-5 (intent: describe)
  question_text: "If a {selected_industry} organization faced this problem, what's a step they would take that you wouldn't normally consider?"
  header: "Analogy"

RECORD: Append to session.cross_industry_analogies[]
```

---

## 5. Pre-Mortem (Devil's Advocate / Black Hat)

**Source:** Gary Klein (2007) — formalization of the pre-mortem technique. Imagining failure BEFORE execution surfaces risks that post-mortems would only discover too late. Related to Edward de Bono's Six Thinking Hats — Black Hat thinking.

**When to use:** During risk analysis, after the risk register is drafted. Targets the top opportunities by impact.

**Skill integration point:** Phase 06 (Risk Analysis) Step 6.4 (added by Z16).

**Canonical prompt template:**
```
Display:
"Pre-Mortem exercise.
Imagine it's 6 months from now and our top opportunity failed catastrophically. What was the cause?
This isn't pessimism — it's surfacing risks while we can still address them."

top_3 = select_top_3_opportunities_by_impact_effort(session.opportunities)

FOR each opp in top_3:
  AskUserQuestion: template=QT-5 (intent: explain)
    question_text: "If '{opp.description}' failed catastrophically in 6 months, what was the most likely cause?"
    header: "Pre-Mortem"
  Append to session.premortem[] as {opportunity_id: opp.id, failure_cause: response}

  AskUserQuestion: template=QT-1 (variant: 2-option, with Skip)
    question_text: "Should we add a hypothesis to test this risk?"
    header: "Add hypothesis?"
  IF response == "Yes":
    Append to session.hypotheses[] with source: "premortem"

VERIFY: session.premortem.length >= 1 (or explicit user skip after at least one prompt)
```

---

## 6. Out-of-Scope Generation (Explicit Non-Goals)

**Source:** Lean Startup, Eric Ries (2011). Explicit non-goals are as important as goals for focused MVPs. Forward-looking complement to historical "failed solutions" capture.

**When to use:** During constraint discovery, after technical and organizational constraints are captured. Different from MoSCoW "Won't Have" because it generates anti-features rather than classifying existing items.

**Skill integration point:** Phase 07 (Constraints & Solution Scope) Step 7.6 (added by Z17).

**Canonical prompt template:**
```
Display:
"Now let's name what we are explicitly NOT building.
This isn't the same as MoSCoW 'Won't Have' (which classifies things we considered).
This is generative: name 3-5 things that someone might naturally expect or request, but you will deliberately exclude — to keep scope focused."

LOOP (target: 3-5 items):
  AskUserQuestion: template=QT-5 (intent: describe)
    question_text: "Out of scope #{N}: name something this initiative will deliberately NOT do."
    header: "Anti-feature {N}"
  IF user picks "Skip this question": BREAK
  Append to session.out_of_scope[]

  AskUserQuestion: template=QT-5 (intent: explain)
    question_text: "Why is '{anti_feature}' out of scope?"
    header: "Rationale"
  Append rationale to session.out_of_scope[N]

VERIFY: session.out_of_scope.length >= 1 (warn at < 3 — typical brainstorming yields 3-5)
```

---

## 7. Stakeholder Voice Role-Play

**Source:** Edward de Bono, *Six Thinking Hats* (1985), particularly the Red Hat (feelings) and Yellow Hat (benefits). Forces empathetic perspective-shift that the third-person stakeholder mapping in Phase 01 does not produce.

**When to use:** Late in Phase 02 (after stakeholders are identified and classified). Particularly valuable when primary and secondary stakeholders have known goal-conflict (e.g., end-users vs. operators, customer vs. compliance).

**Skill integration point:** Phase 02 (Stakeholder Analysis) Step 2.9 (added by Z18).

**Canonical prompt template:**
```
Display:
"Stakeholder Voice exercise.
You've described the stakeholders objectively. Now speak AS each one.
Each role gets ONE insistence or ONE veto — what's the single non-negotiable from that person's seat?"

FOR each stakeholder in session.stakeholders.primary + session.stakeholders.secondary:
  AskUserQuestion: template=QT-5 (intent: explain)
    question_text: "Speaking AS {stakeholder.role}: what's the ONE thing you'd insist on or absolutely veto in any solution to this problem?"
    header: "{stakeholder.role}"
  Append to session.stakeholder_voices[] as {stakeholder_id: stakeholder.id, voice: response}

VERIFY: session.stakeholder_voices.length >= len(session.stakeholders.primary)
  IF user skipped any primary stakeholder: prompt once more before accepting
```

---

## Cross-Reference Table — Technique to Integration Point

| Technique | Phase | Step | Adds Field | Work Item |
|-----------|-------|------|------------|-----------|
| 1. Divergent/Convergent | 04 | Step 4.3 | session.opportunity.divergent_ideas[] | Z13 |
| 2. Idea Combination | 04 | Step 4.9 | session.opportunity.combined_opportunities[] | Z14 |
| 3. HMW Reframing | 03 | Step 3.8 | session.hmw_reframings[] | Z15 |
| 4. Cross-Industry Analogy | 03 | Step 3.9 | session.cross_industry_analogies[] | Z15 |
| 5. Pre-Mortem | 06 | Step 6.4 | session.risk_analysis.premortem[] | Z16 |
| 6. Out-of-Scope | 07 | Step 7.6 | session.constraints_scope.out_of_scope[] | Z17 |
| 7. Stakeholder Voice | 02 | Step 2.9 | session.stakeholder_voices[] | Z18 |

---

## Methodology Sources (full citations)

- Alex Osborn, *Applied Imagination: Principles and Procedures of Creative Problem Solving* (Charles Scribner's Sons, 1953). Origin of the term "brainstorming"; established divergent/convergent separation.
- Edward de Bono, *Six Thinking Hats* (Little, Brown and Company, 1985). White/Red/Black/Yellow/Green/Blue framework for parallel thinking; Black Hat = pre-mortem ancestor.
- Min Basadur et al., "How Might We" question framing from IDEO design-thinking practice (publicized via *Stanford d.school* curriculum, mid-2000s).
- Clayton Christensen, *The Innovator's Solution* (Harvard Business School Press, 2003). Jobs-to-be-done theory underlying cross-industry analogy.
- Frans Johansson, *The Medici Effect* (Harvard Business Review Press, 2004). Cross-pollination as the driver of breakthrough innovation.
- Gary Klein, "Performing a Project Premortem," *Harvard Business Review* (September 2007). Formalized pre-mortem technique.
- Eric Ries, *The Lean Startup* (Crown Business, 2011). Explicit non-goals as MVP scope discipline.
