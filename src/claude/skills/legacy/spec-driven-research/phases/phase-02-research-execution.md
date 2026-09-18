# Phase 02: Research Execution

## Entry Gate

```bash
devforgeai-validate phase-check ${RESEARCH_ID} --workflow=research --from=01 --to=02 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 02 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - Phase 01 not complete |

## Contract

- **PURPOSE:** Execute comprehensive research using internet-sleuth subagent with category-specific methodology
- **REQUIRED SUBAGENTS:** internet-sleuth (BLOCKING)
- **REQUIRED REFERENCES:** `references/internet-sleuth-delegation.md`, `references/search-strategies.md`
- **REQUIRED ARTIFACTS:** Topic, category, and questions from Phase 01 checkpoint
- **STEP COUNT:** 3 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-research/references/internet-sleuth-delegation.md")
Read(file_path=".claude/skills/spec-driven-research/references/search-strategies.md")
```

IF either Read fails: HALT -- "Phase 02 reference file missing"

---

## Mandatory Steps (3)

### Step 2.1: Map Category to internet-sleuth Mode

**EXECUTE:**
```
# Category-to-mode mapping (from internet-sleuth-delegation.md)
category_to_mode = {
    "competitive": "competitive-analysis",
    "technology": "repository-archaeology",
    "market": "market-intelligence",
    "integration": "investigation",
    "architecture": "discovery"
}

research_mode = category_to_mode[category_code]

Display: f"Research mode: {research_mode} (from category: {category_code})"
```

**VERIFY:**
`research_mode` is one of: competitive-analysis, repository-archaeology, market-intelligence, investigation, discovery.
IF not: HALT -- "Invalid research mode mapping"

**RECORD:**
```bash
devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=02 --step=2.1 --project-root=. 2>&1
```

---

### Step 2.2: Invoke internet-sleuth Subagent [BLOCKING]

**EXECUTE:**
```
# Format questions for prompt
questions_formatted = ""
FOR i, q in enumerate(questions):
  questions_formatted += f"{i+1}. {q}\n"

IF questions_formatted == "":
  questions_formatted = "No specific questions defined. Research the topic broadly."
```

Build the registry-protected Phase 02 handoff for `internet-sleuth`. This
dispatch writes a research result from topic/category inputs rather than editing
repo source files, so the handoff is floor-only.

```bash
mkdir -p tmp/${RESEARCH_ID}
: > tmp/${RESEARCH_ID}/research-phase02-internet-sleuth-handoff-changed-files.txt

HANDOFF_OUTPUT_INTERNET_SLEUTH=$(devforgeai-validate build-subagent-handoff ${RESEARCH_ID} \
  --workflow=spec-driven-research \
  --phase=02 \
  --subagent=internet-sleuth \
  --changed-files-file=tmp/${RESEARCH_ID}/research-phase02-internet-sleuth-handoff-changed-files.txt \
  --project-root=. 2>&1)
HANDOFF_PATH_INTERNET_SLEUTH=$(echo "$HANDOFF_OUTPUT_INTERNET_SLEUTH" | jq -r '.handoff_md_path')
```

VERIFY before dispatch:
- `HANDOFF_PATH_INTERNET_SLEUTH` exists and is non-empty.
- `tmp/${RESEARCH_ID}/handoffs/phase-02-internet-sleuth-handoff.manifest.json` exists.
- The manifest has `context_pack.coverage_matrix == {}` and `unresolved == []`.

```
Task(
  subagent_type="internet-sleuth",
  description=f"{category_code} research: {topic}",
  prompt=f"""
Handoff: {HANDOFF_PATH_INTERNET_SLEUTH}
Read the handoff first. Use its context_pack.coverage_matrix and role-domain rules as the context source. If a required domain or artifact is absent, return H-CONTEXT-MISS and stop.

Research Mode: {research_mode}
Topic: {topic}
Research ID: {RESEARCH_ID}

Research Questions:
{questions_formatted}

Execute comprehensive research following your methodology for {research_mode} mode.

Return structured findings with:
1. Executive summary (2-3 sentences max)
2. Key findings with evidence and citations
3. Recommendations ranked by priority (High/Medium/Low)
4. Sources with credibility assessment (title, URL, brief description)
5. Framework compliance check results (validate against DevForgeAI context files if applicable)

Format your output clearly with section headers so findings can be parsed:
- Use "## Key Findings" for findings
- Use "## Recommendations" for recommendations
- Use "## Sources" for sources

Note: Results will be formatted into {RESEARCH_ID} research document.
Include a subagent-result-v1 coverage_attestation with context_pack_path='{HANDOFF_PATH_INTERNET_SLEUTH}', context_pack_consumed=true, and context_miss=[].
"""
)
```

**VERIFY:**
Task completed and returned output. Check that output contains findings, recommendations, and sources sections.

```
IF task output is empty or error:
  Display: "internet-sleuth returned error or empty output"
  GOTO Step 2.3 Fallback
ELSE:
  # Parse sleuth output
  findings = extract_section("Key Findings", sleuth_output)
  recommendations = extract_section("Recommendations", sleuth_output)
  sources = extract_section("Sources", sleuth_output)

  Display: f"Research execution complete"
  Display: f"  Findings extracted: {count_findings(findings)}"
  Display: f"  Recommendations extracted: {count_recommendations(recommendations)}"
  Display: f"  Sources extracted: {count_sources(sources)}"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=02 --step=2.2 --project-root=. 2>&1
```

---

### Step 2.3: Handle Results or Fallback

**EXECUTE:**
```
IF sleuth_output was successful (findings, recommendations, sources all non-empty):
  Display: "internet-sleuth results validated - proceeding to synthesis"
  # Data is ready for Phase 03

ELSE:
  # FALLBACK: Direct web search using search-strategies.md
  Display: "Falling back to direct web search (search-strategies.md methodology)"

  # The search-strategies.md reference was loaded at the start of this phase.
  # Execute the category-specific search strategy from that reference.

  # Execute category-specific searches
  IF category_code == "competitive":
    # Competitive Analysis: 5-step search sequence
    search_1 = WebSearch(query=f"{topic} features pricing 2026")
    search_2 = WebSearch(query=f"{topic} reviews developer experience 2026")
    search_3 = WebSearch(query=f"{topic} comparison alternatives 2026")
    # Fetch key pages from search results
    FOR relevant_url in top_results:
      WebFetch(url=relevant_url, prompt="Extract key features, pricing, positioning")

  ELIF category_code == "technology":
    search_1 = WebSearch(query=f"{topic} performance benchmarks 2026")
    search_2 = WebSearch(query=f"{topic} github stars adoption 2026")
    search_3 = WebSearch(query=f"{topic} vs alternatives comparison 2026")

  ELIF category_code == "market":
    search_1 = WebSearch(query=f"{topic} statistics market size 2026")
    search_2 = WebSearch(query=f"developer survey {topic} 2025 2026")
    search_3 = WebSearch(query=f"{topic} trends predictions 2026")

  ELIF category_code == "integration":
    search_1 = WebSearch(query=f"{topic} API documentation integration guide")
    search_2 = WebSearch(query=f"{topic} SDK examples 2026")
    search_3 = WebSearch(query=f"{topic} integration issues problems 2026")

  ELIF category_code == "architecture":
    search_1 = WebSearch(query=f"{topic} design pattern explained 2026")
    search_2 = WebSearch(query=f"{topic} best practices implementation")
    search_3 = WebSearch(query=f"{topic} advantages disadvantages trade-offs")

  # Compile findings from search results
  findings = compile_search_findings(search_results)
  recommendations = generate_recommendations(findings)
  sources = extract_sources(search_results)
```

**VERIFY:**
Either sleuth output or fallback search produced non-empty findings, recommendations, and sources.
IF all empty: HALT -- "Research execution produced no results"

**RECORD:**
```bash
devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=02 --step=2.3 --project-root=. 2>&1
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${RESEARCH_ID} --workflow=research --phase=02 --checkpoint-passed --project-root=. 2>&1
```
