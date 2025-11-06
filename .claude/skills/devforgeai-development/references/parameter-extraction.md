# Parameter Extraction from Conversation Context

**Purpose:** How the development skill extracts the story ID and other parameters from conversation context.

**Applies to:** devforgeai-development skill (and pattern reusable for other skills)

---

## Background

Skills CANNOT accept command-line parameters. Instead, they extract parameters from:
1. Loaded file content (YAML frontmatter)
2. Explicit context markers in conversation
3. Natural language in user messages

---

## CRITICAL: Extracting Parameters from Conversation Context

**IMPORTANT:** Skills CANNOT accept runtime parameters. All information must be extracted from conversation context.

### How Slash Commands Pass "Parameters" to Skills

When a slash command invokes this skill, it:
1. Loads story file via @file reference: `@.ai_docs/Stories/STORY-XXX.story.md`
2. States context explicitly: "Story ID: STORY-XXX"
3. Invokes skill WITHOUT arguments: `Skill(command="devforgeai-development")`

**You must extract story ID from the conversation.**

### Story ID Extraction

The slash command loads the story file via @file reference, making story content available in conversation.

**Extract story ID from conversation:**

**Method 1: Read YAML frontmatter**
```
Look for YAML frontmatter in conversation:
  ---
  id: STORY-XXX
  title: ...
  status: ...
  ---

Extract: id field = Story ID
```

**Method 2: Search for file reference**
```
Search conversation for pattern:
  ".ai_docs/Stories/STORY-XXX"

Extract STORY-XXX from file path
```

**Method 3: Search for explicit statement**
```
Search conversation for:
  "Story ID: STORY-XXX"
  "Story: STORY-XXX"

Extract STORY-XXX
```

**Method 4: Grep loaded content**
```
If methods 1-3 fail:
  Grep conversation for "STORY-[0-9]+" pattern
  Use first match found
```

### Validation Before Proceeding

Before starting TDD workflow, verify:
- [ ] Story ID extracted successfully
- [ ] Story content available in conversation (via @file load)
- [ ] Acceptance criteria accessible from story content
- [ ] Technical specification present

**If extraction fails:**
```
HALT with error:
"Cannot extract story ID from conversation context.

Expected to find:
  - YAML frontmatter with 'id: STORY-XXX' field
  - OR file reference like '.ai_docs/Stories/STORY-XXX.story.md'
  - OR explicit statement like 'Story ID: STORY-XXX'

Please ensure story is loaded via slash command or provide story ID explicitly."
```
