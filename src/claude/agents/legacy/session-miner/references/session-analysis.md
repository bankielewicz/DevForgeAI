---
parent: session-miner
topic: session-analysis
description: STORY-226 N-gram sequence analysis for command patterns
---

# N-gram Sequence Analysis (STORY-226)

**Purpose:** Extract and analyze command sequence patterns from parsed SessionEntry data.

---

## N-gram Extraction Workflow

### Phase 1: Build Sequence Windows

**Steps:**
1. GROUP all SessionEntry objects by `session_id`
2. SORT entries within each session by `timestamp` (ascending)
3. FOR each session with 2+ commands:
   - EXTRACT 2-grams (bigrams): sliding window of consecutive command pairs
   - EXTRACT 3-grams (trigrams): sliding window of consecutive command triples
4. DO NOT span sequences across session boundaries (each session is independent)

---

### 2-gram (Bigram) Extraction

```
FOR session in sessions:
  commands = [entry.command for entry in session.entries]
  FOR i in range(len(commands) - 1):
    bigram = (commands[i], commands[i+1])
    increment frequency_count[bigram]
```

**Example:**
```
Session abc123: ["/ideate", "/create-story", "/dev", "/qa"]

Bigrams extracted:
  ("/ideate", "/create-story")
  ("/create-story", "/dev")
  ("/dev", "/qa")
```

---

### 3-gram (Trigram) Extraction

```
FOR session in sessions:
  commands = [entry.command for entry in session.entries]
  FOR i in range(len(commands) - 2):
    trigram = (commands[i], commands[i+1], commands[i+2])
    increment frequency_count[trigram]
```

**Example:**
```
Session abc123: ["/ideate", "/create-story", "/dev", "/qa"]

Trigrams extracted:
  ("/ideate", "/create-story", "/dev")
  ("/create-story", "/dev", "/qa")
```

---

## Success Rate Calculation

### Phase 2: Calculate Per-Sequence Success Rates

**Steps:**
1. FOR each unique n-gram sequence:
   - COUNT total_attempts (occurrences across all sessions)
   - COUNT successful_completions (where final command status = "success")
2. CALCULATE success_rate using formula:
   ```
   success_rate = successful_completions / total_attempts
   ```
3. HANDLE partial status as non-success for rate calculation
4. ROUND success_rate to 2 decimal places (percentage precision: 0.XX)

**Status Mapping for Success Rate:**

| Status | Counts as Success |
|--------|-------------------|
| success | Yes |
| error | No |
| partial | No |

---

## Top Patterns Report Generation

### Phase 3: Generate Ranked Pattern Report

**Steps:**
1. RANK all sequences by frequency (descending)
2. APPLY tie-breaking rule for sequences with equal frequency:
   - When two sequences have same frequency, apply secondary sort
   - Use alphabetical order of first command as tie-breaker
3. SELECT top 10 sequences (or fewer if less than 10 unique patterns exist)
4. OUTPUT report with columns: rank, sequence, frequency, success_rate

**Output Format:**

```json
{
  "top_patterns": [
    {
      "rank": 1,
      "sequence": ["/dev", "/qa"],
      "frequency": 47,
      "success_rate": 0.85
    },
    {
      "rank": 2,
      "sequence": ["/ideate", "/create-story", "/dev"],
      "frequency": 23,
      "success_rate": 0.78
    }
  ],
  "metadata": {
    "total_unique_bigrams": 156,
    "total_unique_trigrams": 89,
    "sessions_analyzed": 42
  }
}
```

---

## Edge Cases

| Case | Handling |
|------|----------|
| Empty file | Return empty top_patterns array, metadata counts = 0 |
| Single command sessions | Skip for n-gram extraction (no pairs/triples possible) |
| Malformed entries | Exclude from sequence building (already filtered by parser) |
| Fewer than 10 patterns | Return all available patterns (may be less than 10) |
| Missing session_id | Group by null session_id as single session |
| Duplicate timestamps | Preserve original order from file |

---

## Integration with session-miner Workflow

N-gram analysis operates on SessionEntry output from Steps 1-6:

```
session-miner parsing (Steps 1-6)
       |
SessionEntry[] with session_id grouping
       |
N-gram Extraction (Phase 1)
       |
Success Rate Calculation (Phase 2)
       |
Top Patterns Report (Phase 3)
       |
STORY-226 output ready for insights
```

---

## Detailed Algorithm: Complete N-gram Workflow

```
FUNCTION extract_ngrams(session_entries):
  # Group by session
  sessions = group_by_session_id(session_entries)

  bigrams = {}
  trigrams = {}

  FOR session_id, entries in sessions:
    # Sort by timestamp
    sorted_entries = entries.sort(by="timestamp")
    commands = [e.command for e in sorted_entries]
    statuses = [e.status for e in sorted_entries]

    # Extract bigrams
    FOR i in range(len(commands) - 1):
      key = (commands[i], commands[i+1])
      IF key not in bigrams:
        bigrams[key] = {"total": 0, "success": 0}
      bigrams[key]["total"] += 1
      IF statuses[i+1] == "success":
        bigrams[key]["success"] += 1

    # Extract trigrams
    FOR i in range(len(commands) - 2):
      key = (commands[i], commands[i+1], commands[i+2])
      IF key not in trigrams:
        trigrams[key] = {"total": 0, "success": 0}
      trigrams[key]["total"] += 1
      IF statuses[i+2] == "success":
        trigrams[key]["success"] += 1

  RETURN bigrams, trigrams

FUNCTION calculate_success_rates(ngrams):
  result = []
  FOR sequence, counts in ngrams:
    success_rate = counts["success"] / counts["total"]
    result.append({
      "sequence": list(sequence),
      "frequency": counts["total"],
      "success_rate": round(success_rate, 2)
    })
  RETURN result

FUNCTION generate_top_patterns(bigrams, trigrams, top_n=10):
  # Combine and sort
  all_patterns = calculate_success_rates(bigrams) + calculate_success_rates(trigrams)

  # Sort by frequency (descending), then alphabetically by first command
  sorted_patterns = all_patterns.sort(
    by=["frequency DESC", "sequence[0] ASC"]
  )

  # Take top N
  top = sorted_patterns[:top_n]

  # Add ranks
  FOR i, pattern in enumerate(top):
    pattern["rank"] = i + 1

  RETURN {
    "top_patterns": top,
    "metadata": {
      "total_unique_bigrams": len(bigrams),
      "total_unique_trigrams": len(trigrams),
      "sessions_analyzed": len(sessions)
    }
  }
```

---

## Common Command Sequences

**Expected high-frequency patterns:**

| Sequence | Description | Expected Frequency |
|----------|-------------|-------------------|
| `/dev` -> `/qa` | Dev to QA handoff | High |
| `/ideate` -> `/create-story` | Ideation to story creation | Medium |
| `/create-story` -> `/dev` | Story to implementation | Medium |
| `/qa` -> `/release` | QA approval to release | Medium |
| `/brainstorm` -> `/ideate` | Brainstorm to ideation | Low |

---

## Invocation Template

```markdown
Task(
  subagent_type="session-miner",
  description="Extract command sequence patterns",
  prompt="""
  Perform N-gram analysis on history.jsonl:

  1. Parse history with session-miner
  2. Group entries by session_id
  3. Extract bigrams and trigrams
  4. Calculate success rates per sequence
  5. Generate top 10 patterns report

  Return top patterns with frequency and success rates.
  """
)
```

---

## Success Criteria

**Functional Requirements:**
- [ ] Group entries by session_id before extraction
- [ ] Extract bigrams (2-grams) from consecutive commands
- [ ] Extract trigrams (3-grams) from consecutive commands
- [ ] Calculate success rate based on final command status
- [ ] Generate ranked top 10 patterns report
- [ ] Apply tie-breaking (alphabetical) for equal frequencies

**Non-Functional Requirements:**
- [ ] Do not span sequences across session boundaries
- [ ] Handle single-command sessions (skip for n-gram)
- [ ] Round success rates to 2 decimal places
- [ ] Return fewer than 10 patterns if dataset is small
