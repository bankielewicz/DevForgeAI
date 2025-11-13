No, Skills do **NOT** run in isolated contexts with no visibility. This is actually a key architectural distinction that's important for DevForgeAI.

Here's what actually happens:

## Skills Are Transparent, Step-by-Step Workflows

**Skills inject instructions, then Claude executes them with full visibility:**

1. **Skill invocation loads SKILL.md** → Instructions enter Claude's context
2. **Claude reads and interprets the instructions** → Plans the workflow
3. **Claude executes commands step-by-step** → Uses bash, Python, file tools
4. **Claude sees output from every command** → Receives stdout/stderr for each step
5. **Claude adapts based on results** → Can adjust approach if something fails

**Example of what Claude sees:**

When a PDF skill extracts text, Claude doesn't just invoke "extract_pdf(file)" and wait for results. Instead:

```
Claude: [reads SKILL.md instructions]
Claude: "I need to extract text from report.pdf"
Claude: [executes] python /skills/pdf/scripts/extract_text.py report.pdf
Output: "Extracted 1,234 words from 5 pages..."
Claude: [sees output] "Great, extraction succeeded. Now I'll format it..."
Claude: [executes next step based on results]
```

## Why This Matters for DevForgeAI

**Advantages of transparent execution:**

- **Error handling**: Claude sees failures immediately and can retry or adjust approach
- **Progress tracking**: Claude can report progress to users naturally ("Extracted page 1 of 10...")
- **Adaptive workflows**: If a step fails, Claude can try alternative approaches from the skill's instructions
- **Debugging**: Users see Claude's reasoning and can understand what's happening

**Architectural implications:**

```yaml
---
name: devforge-build-pipeline
description: Execute DevForgeAI build pipeline with validation
---

# Build Pipeline

When user requests a build:

1. Run validation checks first
   - Execute: `python scripts/validate_config.py`
   - If validation fails, explain errors to user and stop
   
2. If validation passes, execute build
   - Execute: `bash scripts/build.sh`
   - Monitor output for errors
   - If build fails, check logs and explain issue

3. Run tests on successful build
   - Execute: `python scripts/run_tests.py`
   - Report test results to user
```

Claude will execute each step and see the results, allowing it to provide detailed feedback and handle errors gracefully.

## The Nuance with Bundled Scripts

While **Claude sees all outputs**, bundled Python/bash scripts in `scripts/` directories do have one efficiency benefit:

- **Script source code** doesn't load into context (saves tokens)
- **Script execution output** does load into context (Claude sees results)

So a 5000-line Python script consumes ~0 tokens until executed, then only its output (maybe 200 tokens) enters context. But Claude absolutely sees that output and can react to it.

## Contrast with Traditional Black-Box Tools

Some traditional tool architectures are truly isolated:

- **Black-box function call**: `result = complex_operation()` → Claude only sees final result
- **Skills in Claude**: Claude executes each step and sees intermediate outputs

This transparency is actually one of Skills' strengths for complex workflows where error handling and adaptation matter.