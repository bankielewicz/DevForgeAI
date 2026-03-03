# Lean Canvas Workflow Reference

Detailed workflow for the Lean Canvas guided phase of the planning-business skill.

## 1. Overview

The Lean Canvas workflow guides users through 9 blocks to create a one-page business model. Question depth adapts to user experience level. The workflow supports fresh creation, iteration and refinement of existing canvases, and resume from partial completion.

All user interaction uses AskUserQuestion. No Bash prompts.

**Output file:** `devforgeai/specs/business/business-plan/lean-canvas.md`

---

## 2. Adaptive Question Depth

Three experience levels control how questions are presented for each block.

### Beginner

Users new to business modeling. Questions include extended explanations, contextual examples, and additional guided sub-questions to help them think through each block. More questions per block than other levels.

**Characteristics:**
- Detailed context and definitions before each question
- Extended examples from well-known companies
- Additional sub-questions that break down complex blocks
- Prompts for common pitfalls and misconceptions

**Example (Problem block):**
```
Question: "Let's identify the top problems your product solves.

A 'problem' in Lean Canvas means a pain point your target customers
experience today. Good problems are specific and measurable.

Example: Airbnb's problem was 'Hotels are too expensive for budget
travelers, and homeowners have unused space.'

Sub-questions:
1. What frustration do your customers face today?
2. How are they currently solving this problem (existing alternatives)?
3. What makes the current solutions inadequate?"
Header: "Block 1: Problem"
```

### Intermediate

Users with some business experience. Standard question depth with brief context. This is the default level when no profile is available.

**Characteristics:**
- Brief context for each block
- One primary question per block with optional follow-up
- Assumes basic familiarity with business concepts

**Example (Problem block):**
```
Question: "What are the top 1-3 problems your product solves?
Consider: What existing alternatives do customers use today?"
Header: "Block 1: Problem"
```

### Advanced

Experienced entrepreneurs or business professionals. Questions are concise and streamlined, skipping introductory explanations. Brief prompts that get straight to the point with minimal overhead.

**Characteristics:**
- Concise, direct questions
- No introductory explanations
- Assumes full understanding of Lean Canvas methodology
- Streamlined flow for rapid canvas completion

**Example (Problem block):**
```
Question: "Top 1-3 problems and existing alternatives?"
Header: "Block 1: Problem"
```

---

## 3. The 9 Lean Canvas Blocks

Each block is presented via AskUserQuestion in the following order. Question depth adapts based on user experience level (see Section 2: Adaptive Question Depth).

### Block Presentation Order and Purposes

| Block | Order | Purpose |
|-------|-------|---------|
| Problem | 1 | Identify the top 1-3 problems the business solves |
| Customer Segments | 2 | Define target customer groups and early adopters |
| Unique Value Proposition | 3 | Single, clear, compelling message that states why you are different |
| Solution | 4 | Top 3 features or capabilities that address identified problems |
| Channels | 5 | Path to customers - how you reach customer segments |
| Revenue Streams | 6 | Revenue model - how the business makes money |
| Cost Structure | 7 | Customer acquisition, distribution, hosting, staffing, and operational costs |
| Key Metrics | 8 | Key activities and numbers to measure business performance |
| Unfair Advantage | 9 | Something that cannot be easily copied or bought by competitors |

### Question Depth by Block

Each block receives one of three adaptive question depths based on user experience level:

**Beginner Questions** include extended explanations, contextual examples, additional guided sub-questions, and prompts for common pitfalls. Examples:

- **Problem:** Extended explanation with examples from well-known companies, sub-questions about frustrations and existing alternatives
- **Customer Segments:** Detailed guidance on segmentation with demographic and behavioral questions
- **UVP:** Explanation with formula and examples, sub-questions about differentiation
- **Solution:** Guidance on mapping solutions to problems with MVP scope questions
- **Channels:** Explanation of channel types (inbound/outbound/direct/indirect) with customer journey questions
- **Revenue Streams:** Detailed explanation of models (subscription, one-time, freemium) with pricing strategy questions
- **Cost Structure:** Breakdown of cost categories with fixed vs variable cost sub-questions
- **Key Metrics:** Explanation of pirate metrics (AARRR) with leading vs lagging indicator questions
- **Unfair Advantage:** Explanation of defensibility types (network effects, IP, community) with self-assessment guidance

**Intermediate Questions** (default) provide brief context with one primary question per block plus optional follow-up. Assumes basic familiarity with business concepts. Examples:

- **Problem:** "What are the top 1-3 problems your product solves? Consider: What existing alternatives do customers use today?"
- **Customer Segments:** Direct question about target segments and early adopters
- **UVP:** Direct question about what makes the product unique
- **Solution:** Direct question about top features per problem
- **Channels:** Direct question about primary acquisition channels
- **Revenue Streams:** Direct question about revenue model and pricing
- **Cost Structure:** Direct question about primary cost drivers
- **Key Metrics:** Direct question about key metrics to track
- **Unfair Advantage:** Direct question about competitive advantages

**Advanced Questions** are concise and streamlined, skipping introductory explanations. Examples:

- **Problem:** Concise prompt for problems and alternatives
- **Customer Segments:** Concise prompt for segments and early adopters
- **UVP:** Concise prompt for UVP statement
- **Solution:** Concise prompt for solution features
- **Channels:** Concise prompt for channels
- **Revenue Streams:** Concise prompt for revenue model
- **Cost Structure:** Concise prompt for cost structure
- **Key Metrics:** Concise prompt for key metrics
- **Unfair Advantage:** Concise prompt for unfair advantage

---

## 4. Iteration and Refinement Workflow

When an existing lean-canvas.md file is detected, the skill enters iteration mode.

### Step 1: Read Existing Canvas

```
Read(file_path="devforgeai/specs/business/business-plan/lean-canvas.md")
```

Load the existing canvas and parse each block's content.

### Step 2: Present Current State

Display the current canvas values to the user. Show each block with its existing content so the user can review what they have.

```
Question: "Here is your current Lean Canvas. Which blocks would you like to modify?

1. Problem: [current content summary]
2. Customer Segments: [current content summary]
3. Unique Value Proposition: [current content summary]
4. Solution: [current content summary]
5. Channels: [current content summary]
6. Revenue Streams: [current content summary]
7. Cost Structure: [current content summary]
8. Key Metrics: [current content summary]
9. Unfair Advantage: [current content summary]"
Header: "Lean Canvas Iteration"
Options:
  - "Edit specific blocks"
  - "Walk through all blocks (keep/modify each)"
  - "Start fresh (clear all)"
multiSelect: false
```

### Step 3: Modify Selected Blocks

For each block the user wants to update or change:
- Present the current value
- Ask for the new value via AskUserQuestion
- Allow the user to keep the existing value unchanged

Unchanged blocks are preserved exactly as they were.

### Step 4: Write Updated Canvas

Save the updated canvas back to lean-canvas.md. Unchanged blocks retain their original content exactly. Only modified blocks reflect new user input.

```
Write(file_path="devforgeai/specs/business/business-plan/lean-canvas.md", content=updated_canvas)
```

---

## 5. Partial Completion and Resume

The workflow supports resume from incomplete canvases. When a user exits mid-workflow (e.g., context window clears), any blocks already written to lean-canvas.md are preserved.

### Detection

On re-invocation, check for an existing lean-canvas.md:

1. Read the existing file
2. Parse each block to identify which are complete vs incomplete
3. An incomplete block is one marked as TODO, empty, or missing from the file
4. A complete block has user-provided content

### Resume Workflow

1. Preserve partial blocks - retain all existing content, keeping partial work intact
2. Present a summary showing which blocks are filled and which are empty or missing
3. Offer to resume from the first incomplete block
4. Walk through only the incomplete blocks, maintaining the same adaptive depth

```
Question: "Your Lean Canvas is partially complete.

Filled blocks: Problem, Customer Segments, UVP
Empty/missing blocks: Solution, Channels, Revenue Streams, Cost Structure,
Key Metrics, Unfair Advantage

Would you like to continue from where you left off?"
Header: "Resume Lean Canvas"
Options:
  - "Continue from first incomplete block"
  - "Review all blocks (including completed ones)"
  - "Start fresh"
multiSelect: false
```

### Preservation Rules

- Completed blocks are never overwritten during resume unless the user explicitly chooses to edit them
- Partial content within a block is maintained exactly as written
- The output file is written after each block completion to minimize data loss on interruption

---

## 6. Output Format

The generated lean-canvas.md follows this structure:

```markdown
# Lean Canvas

**Product:** [Product Name]
**Date:** [Generation Date]
**Version:** [1.0 | iteration count]

## Problem

[User-provided content]

## Customer Segments

[User-provided content]

## Unique Value Proposition

[User-provided content]

## Solution

[User-provided content]

## Channels

[User-provided content]

## Revenue Streams

[User-provided content]

## Cost Structure

[User-provided content]

## Key Metrics

[User-provided content]

## Unfair Advantage

[User-provided content]
```

Empty blocks confirmed by the user are marked as:

```markdown
## [Block Name]

*TODO: To be completed in next iteration*
```
