# Celebration Engine

Terminal-compatible gamification reference for ADHD-friendly entrepreneur coaching. All visual elements use ASCII-safe characters only for terminal rendering.

---

## ASCII Progress Patterns

Progress bars use block drawing characters for terminal-compatible visualization. No GUI markup or emoji characters are used.

### Progress Bar Format

```
[████████████░░░░░░░░] 60% Complete
[████████████████████] 100% Complete
[██░░░░░░░░░░░░░░░░░░] 10% Complete
```

### Usage Guidelines

- Use `█` (filled block) for completed portion
- Use `░` (light shade) for remaining portion
- Always append percentage after the bar
- Keep bar width consistent (20 characters recommended)

### Examples by Context

| Progress | Bar | Label |
|----------|-----|-------|
| Business plan | `████████░░░░ 66%` | Business Plan Progress |
| Customer discovery | `██████████░░ 83%` | Customer Interviews |
| Revenue target | `████░░░░░░░░ 33%` | Monthly Revenue Goal |

---

## Streak Tracking

Track session consistency to build momentum. Display streak information in session summaries to reinforce habit formation.

### streak-tracker.yaml Schema

```yaml
streak_tracker:
  current_streak:
    type: Integer
    description: Number of consecutive sessions completed
    constraints: ">= 0"
    default: 0

  longest_streak:
    type: Integer
    description: Highest consecutive session count achieved
    constraints: ">= 0"
    default: 0

  last_session_date:
    type: DateTime
    description: ISO 8601 timestamp of most recent session
    format: "YYYY-MM-DDTHH:MM:SSZ"
    example: "2026-03-04T14:30:00Z"
```

### Session Summary Display

```
Session Streak: 5 days in a row
Personal Best:  12 days
Last Session:   2026-03-03
```

---

## Celebration Tiers

Three intensity tiers control how celebrations are delivered. Messages must be achievement-specific and reference the actual accomplishment, not generic praise.

### High Intensity Tier

Celebrates every task completion with immediate, context-specific feedback.

- Triggers on: Every completed task, each action item finished
- Display: Full progress bar update + achievement-specific message
- Example messages:
  - "You just validated your first customer segment! That takes real courage."
  - "Revenue milestone hit -- your prototype is generating real income."
  - "You completed all 5 customer interviews this week. That is serious momentum."

### Medium Intensity Tier

Celebrates significant tasks and notable accomplishments only.

- Triggers on: Significant milestones, important deliverables, notable progress
- Display: Brief progress update + achievement-specific message
- Example messages:
  - "Customer discovery phase completed. You have real market data now."
  - "First paying customer acquired. Your business model is validated."
  - "You launched your MVP. That built confidence for the next phase."

### Low Intensity Tier

Minimal celebration, reserved for milestone completions only.

- Triggers on: Major milestone completions only (phase transitions, big wins)
- Display: Milestone acknowledgment only
- Example messages:
  - "Milestone reached: Business plan finalized."
  - "Milestone reached: First revenue generated."

### Message Design Principles

All celebration messages must be **achievement-specific** and reference the **context** of what was accomplished. Avoid generic messages like "Good job!" or "Well done!" -- instead, name the specific achievement and why it matters.

---

## Profile-Driven Adaptation

Gamification behavior adapts based on user profile dimensions. When a profile is missing or unavailable, the system uses a **default of medium** intensity as the fallback behavior.

### Fallback Behavior

If the user profile is unavailable or missing, default to **medium** celebration intensity and standard progress visualization. This ensures a reasonable experience without requiring profile configuration.

### Adaptation Mapping

| Profile Setting | High | Medium | Low |
|----------------|------|--------|-----|
| celebration_intensity | Every task celebrated | Significant tasks only | Milestones only |
| progress_visualization | After every task | After significant tasks | Weekly summary |
