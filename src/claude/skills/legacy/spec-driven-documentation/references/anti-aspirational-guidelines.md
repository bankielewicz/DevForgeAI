# Anti-Aspirational Documentation Guidelines

Rules enforced during Phase 2 content generation. The documentation-writer subagent MUST follow these constraints.

---

## Prohibited Language

| Pattern | Why It Fails | Replace With |
|---------|-------------|--------------|
| "will be", "will support", "planned" | Describes unimplemented features | Remove entirely, or move to Roadmap file only |
| "you can extend this to..." | Aspirational filler | Document what exists, not what could exist |
| "in the future", "upcoming" | Vague timeline promises | Remove entirely |
| "powerful", "robust", "seamless" | Marketing language, not documentation | Describe the specific behavior instead |
| "easy to use", "simple", "intuitive" | Subjective claims | Show a usage example and let the reader decide |
| "best practices" (without specifics) | Empty authority appeal | State the specific practice and why it applies |

---

## Structural Rules

### 1. No Filler Sections

If a module has nothing to say for a doc type, skip that section entirely. An empty or boilerplate section is worse than no section.

```
WRONG:
## Troubleshooting
No known issues at this time.

RIGHT:
(Section omitted — nothing to troubleshoot)
```

### 2. Problem-First Troubleshooting

Troubleshooting headings are symptoms, not module names. Readers search by what went wrong.

```
WRONG:
## Assessing Entrepreneur
### Profile not found

RIGHT:
## Profile not found after running /assess-me
```

### 3. Match Existing Voice

When inserting a section into an existing framework document, the documentation-writer receives the full document content. The new section must match the tone, heading style, and depth of surrounding sections. Do not introduce a different writing style mid-document.

### 4. Concrete Examples Required

Every API section must include at least one invocation example. Every configuration section must include at least one real value. No placeholder-only documentation.

```
WRONG:
Invoke with: Skill(command="your-skill-name")

RIGHT:
Invoke with: Skill(command="assessing-entrepreneur")
```

### 5. No Duplicate Introductions

When content merges into a framework document that already has an introduction, do not write another introduction for the module section. Start with what the module does in one sentence, then move directly to specifics.

---

## Enforcement

Phase 5 (Validation) checks generated content against these rules:
- Grep for prohibited language patterns
- Verify no empty sections (heading followed immediately by another heading)
- Verify examples contain real values, not placeholders

If violations found, return content to documentation-writer with specific fix instructions before writing files.
