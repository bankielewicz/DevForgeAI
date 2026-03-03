# Plan Calibration Engine

Engine for calibrating business plan complexity based on assessment profile results. Adjusts task granularity, timeline expectations, and support level to match individual self-reported preferences.

---

## Purpose

After the entrepreneur-assessor subagent produces a structured profile, this engine determines how to calibrate the business plan. Users who self-report challenges with focus get smaller tasks. Users who self-report high energy consistency get longer planning horizons.

---

## Calibration Dimensions

### 1. Task Granularity

How small should individual tasks be broken down?

| Profile Signal | Granularity Level | Task Duration | Example |
|---------------|-------------------|---------------|---------|
| High sustained focus, sequential completion | Large | 2-4 hours | "Build landing page" |
| Moderate focus, mixed completion | Medium | 45-90 minutes | "Write landing page headline and hero section" |
| Variable focus, burst completion | Small | 15-30 minutes | "Choose 3 headline options" |
| Short bursts, challenge with finishing | Micro | 5-15 minutes | "Write one headline" |

### 2. Timeline Buffer

How much extra time to add to estimates based on self-reported patterns:

| Profile Signal | Buffer Multiplier | Rationale |
|---------------|-------------------|-----------|
| Consistent completion, good time estimation | 1.1x | Minor buffer for unknowns |
| Moderate completion, some estimation challenges | 1.3x | Standard buffer |
| Variable completion, poor time estimation | 1.5x | Significant buffer |
| Struggles with finishing, significant estimation gaps | 2.0x | Double the estimate |

### 3. Check-in Frequency

How often should progress reviews happen:

| Profile Signal | Frequency | Format |
|---------------|-----------|--------|
| Self-directed, high completion rate | Weekly | Brief status update |
| Moderate self-direction | Every 3 days | Progress review with adjustments |
| Needs accountability, variable completion | Daily | Short check-in with next actions |
| Significant accountability needs | Twice daily | Morning plan + evening review |

### 4. Coaching Style

What communication and support style to use:

| Profile Signal | Style | Characteristics |
|---------------|-------|-----------------|
| High confidence, experienced | Peer advisory | Strategic discussions, challenge assumptions |
| Moderate confidence, some experience | Structured guidance | Frameworks, templates, options with recommendations |
| Low confidence, first attempt | Supportive coaching | Step-by-step, encouragement, celebrate small wins |
| Variable confidence across areas | Adaptive | Switch styles based on topic area |

---

## Calibration Algorithm

### Step 1: Extract Profile Signals

From the structured profile, extract key signals:

```
signals = {
  focus_level: profile.dimensions.energy_management.energy_pattern,
  completion_pattern: profile.dimensions.task_completion.primary_pattern,
  motivation_drivers: profile.dimensions.motivation.primary_drivers,
  challenge_areas: profile.dimensions.self_reported_challenges.primary_challenges,
  experience_level: profile.dimensions.previous_attempts.experience_level,
  work_style: profile.dimensions.work_style.primary_pattern
}
```

### Step 2: Calculate Calibration Settings

Map signals to calibration values:

```
calibration = {
  task_granularity: map_granularity(signals.focus_level, signals.completion_pattern),
  timeline_buffer: map_buffer(signals.completion_pattern, signals.challenge_areas),
  check_in_frequency: map_frequency(signals.completion_pattern, signals.experience_level),
  coaching_style: map_style(signals.experience_level, signals.motivation_drivers)
}
```

### Step 3: Apply Cross-Dimension Adjustments

- If motivation drops with routine tasks AND challenges include consistency -> increase check-in frequency
- If previous attempts failed due to scope -> reduce task granularity by one level
- If energy pattern is variable -> add flexibility buffers to schedule
- If high confidence but poor completion -> focus on accountability, not encouragement

### Step 4: Generate Calibrated Plan Parameters

Output a calibration profile:

```yaml
calibration:
  task_granularity: "small"  # micro | small | medium | large
  timeline_buffer: 1.5       # multiplier for time estimates
  check_in_frequency: "daily" # twice-daily | daily | every-3-days | weekly
  coaching_style: "supportive" # peer | structured | supportive | adaptive

  schedule:
    peak_work_hours: "9am-12pm"
    admin_hours: "2pm-3pm"
    flexible_hours: "3pm-5pm"

  milestones:
    size: "small"  # tiny | small | medium | large
    celebration: true
    visual_tracking: true

  risk_mitigation:
    scope_guard: true  # Prevent scope creep
    pivot_plan: true   # Pre-planned alternatives
    energy_matching: true  # Match task difficulty to energy
```

---

## Seven-Dimension Adaptive Calibration

Maps profile signals to the 7 adaptive dimensions used in user-profile.yaml:

| Dimension | Enum Values | Description |
|-----------|-------------|-------------|
| task_chunk_size | micro \| standard \| extended | Work chunk duration (5-60 min) |
| session_length | short \| medium \| long | Focus session duration (15-60 min) |
| check_in_frequency | frequent \| moderate \| minimal | Progress check cadence (every 1-5 tasks) |
| progress_visualization | per_task \| daily \| weekly | How often progress is visualized |
| celebration_intensity | high \| medium \| low | Acknowledgment frequency |
| reminder_style | specific \| balanced \| gentle | Action prompt directiveness |
| overwhelm_prevention | strict \| moderate \| open | Information visibility scope |

**Calibration mapping:**

- `task_chunk_size`: micro (5-15 min) → standard (15-45 min) → extended (45-60 min) based on focus signals
- `overwhelm_prevention`: strict (next-3-tasks-only) → moderate → open (full-roadmap) based on overwhelm signals

---

## Integration

- **Input**: Structured profile from entrepreneur-assessor subagent
- **Output**: Calibration parameters for business plan generation
- **Consumed by**: Business plan generation workflows, coaching sessions
