# Sprint Planning Reference

Complete guide for planning, executing, and tracking 2-week iterations in the DevForgeAI orchestration system.

## Purpose

This reference provides detailed procedures for sprint management: calculating capacity, selecting stories from backlog, planning sprints, tracking progress, and conducting retrospectives.

## When to Use

Reference this document when:
- Planning new sprint from epic backlog
- Calculating team capacity
- Selecting and prioritizing stories
- Tracking sprint progress
- Conducting sprint reviews and retrospectives

---

## Sprint Planning Process

### Step 1: Determine Sprint Metadata

**Sprint Identification:**
```
Sprint Number: Sequential within epic (1, 2, 3...)
Sprint ID: SPRINT-XXX (auto-increment globally)
Sprint Name: Brief theme/focus (e.g., "Core Checkout Flow")
Duration: 2 weeks (standard)
Dates: Start Monday, end Friday 2 weeks later
```

### Step 2: Calculate Team Capacity

**Capacity Formula:**
```
Base Capacity = Team Size × Days × Points per Day

Example:
Team Size: 4 developers
Working Days: 10 days (2 weeks)
Points per Day: 0.5 (conservative) to 1.0 (aggressive)

Capacity Range: 20-40 points per sprint

Adjustments:
- Holidays: Subtract days × team size × 0.5
- Partial availability: Reduce capacity for known absences
- New team: Start at 70% of calculated capacity
- Mature team: Use historical velocity
```

**Velocity-Based Capacity (Preferred):**
```
IF team has 3+ sprint history:
    capacity = average(last_3_sprints.completed_points)
ELSE:
    capacity = estimated_capacity × 0.8  # Conservative buffer

Example:
Last 3 sprints: 22, 24, 18 points completed
Average velocity: 21 points
Sprint capacity: 21 points (use rolling average)
```

### Step 3: Review Epic Backlog

**Load epic stories:**
```
epic_id = get_current_epic()
Read(file_path=".ai_docs/Epics/{epic_id}.md")

Find all backlog stories:
Grep(pattern="epic: {epic_id}", glob="**/*.story.md")

Filter by status:
backlog_stories = filter(status == "Backlog")
```

**Story Readiness Criteria:**
```
Story ready for sprint when:
✓ Has clear acceptance criteria (3+ criteria)
✓ Has technical specification
✓ Estimated (story points assigned)
✓ No blocking dependencies (or dependencies resolved)
✓ Small enough for sprint (≤13 points recommended)
```

### Step 4: Prioritize Stories

**Priority Framework:**

**High Priority (Must Have) 🔴**
- Critical for sprint goal
- Blocks other stories
- High business value
- User-facing core functionality

**Medium Priority (Should Have) 🟡**
- Important but not critical
- Enhances core functionality
- Can defer to next sprint if needed

**Low Priority (Nice to Have) 🟢**
- Optional enhancements
- Polish and improvements
- Fill extra capacity only

**Prioritization Process:**
```
FOR each backlog story:
    business_value = assess_business_value(story)
    technical_risk = assess_technical_complexity(story)
    dependencies = check_dependencies(story)

    IF blocks_other_stories OR critical_path:
        priority = "High"
    ELSE IF high_business_value AND low_risk:
        priority = "High"
    ELSE IF moderate_business_value:
        priority = "Medium"
    ELSE:
        priority = "Low"
```

### Step 5: Select Stories for Sprint

**Selection Algorithm:**
```
capacity_remaining = sprint_capacity
selected_stories = []

# 1. Select High Priority stories first
FOR story IN high_priority_stories (sorted by business value):
    IF story.points <= capacity_remaining:
        selected_stories.append(story)
        capacity_remaining -= story.points

# 2. Fill remaining capacity with Medium Priority
FOR story IN medium_priority_stories:
    IF story.points <= capacity_remaining:
        selected_stories.append(story)
        capacity_remaining -= story.points

# 3. Add Low Priority only if capacity remains
IF capacity_remaining >= 3:
    FOR story IN low_priority_stories:
        IF story.points <= capacity_remaining:
            selected_stories.append(story)
            capacity_remaining -= story.points

# Target: 80-90% capacity utilization
utilization = (sprint_capacity - capacity_remaining) / sprint_capacity
IF utilization < 0.8:
    WARN: "Under-committed sprint ({utilization}%)"
IF utilization > 0.95:
    WARN: "Over-committed sprint ({utilization}%)"
```

**Buffer Strategy:**
```
Reserve 10-20% capacity for:
- Unexpected bugs
- Production issues
- Technical debt
- Story expansion (scope creep)

Example:
Sprint Capacity: 20 points
Buffer (15%): 3 points
Committed Stories: 17 points
```

### Step 6: Validate Dependencies

**Dependency Check:**
```
FOR each selected_story:
    Read(file_path="ai_docs/Stories/{story.id}.md")
    dependencies = extract_section("Dependencies")

    FOR each dependency:
        dep_status = get_story_status(dependency.story_id)

        IF dep_status NOT IN ["Released", "QA Approved"]:
            WARN: "{story.id} depends on {dependency.story_id} (status: {dep_status})"
            AskUserQuestion: "Proceed with dependent story or defer?"
```

### Step 7: Create Sprint Document

**Use sprint template:**
```
Read(file_path=".claude/skills/devforgeai-orchestration/assets/templates/sprint-template.md")

Write(file_path=".ai_docs/Sprints/SPRINT-{number}.md")

Fill frontmatter:
- id: SPRINT-XXX
- number: Sprint number in epic
- name: Sprint theme
- epic: EPIC-XXX
- start_date: YYYY-MM-DD
- end_date: YYYY-MM-DD (2 weeks later)
- capacity: Calculated capacity
- committed_points: Sum of selected story points
- status: Planning
- team: Team name
```

**Populate Sprint Backlog:**
```
For each priority category:
    Add story entry:
    #### STORY-XXX: [Title]
    - Points: X
    - Assignee: [Developer or TBD]
    - Status: Backlog
    - Description: One-line summary
    - Dependencies: List or None
```

### Step 8: Define Sprint Goal

**Sprint Goal Criteria:**
- Single, clear objective
- User-focused outcome
- Measurable success
- Achievable within sprint

**Example Sprint Goals:**
```
✓ "Enable users to complete checkout as guest or with saved payment"
✓ "Deliver admin dashboard with user management and analytics"
✓ "Migrate user service to microservices with zero downtime"

✗ "Complete 8 stories" (not outcome-focused)
✗ "Work on checkout and admin panel" (not focused, multiple goals)
```

---

## Sprint Execution and Tracking

### Daily Standups

**Daily Update Template:**
```
### [Date] - Day [X]

**Yesterday:**
- [Developer 1]: Completed STORY-XXX Phase 3, started Phase 4
- [Developer 2]: QA approved STORY-YYY, started STORY-ZZZ

**Today:**
- [Developer 1]: Complete STORY-XXX refactoring, push for QA
- [Developer 2]: Complete STORY-ZZZ architecture phase

**Blockers:**
- [ ] STORY-XXX waiting for API documentation (Owner: External team, ETA: tomorrow)
- [x] Database access issue resolved

**Burn Rate:** 12 points completed / 20 points committed (60%)
```

**Blocker Management:**
```
IF blocker identified:
    Document blocker
    Assign owner
    Set ETA for resolution
    Update story status to Blocked if needed
    Escalate if ETA > 2 days
```

### Mid-Sprint Review (Day 5)

**Progress Assessment:**
```
# Calculate metrics
completed_points = sum(status == "Released")
in_progress_points = sum(status IN ["In Development", "QA In Progress"])
expected_at_midpoint = sprint_capacity × 0.5

progress_percentage = completed_points / committed_points
on_track = (completed_points + in_progress_points) >= expected_at_midpoint

IF on_track:
    STATUS: "On Track"
ELSE IF progress_percentage >= 0.3:
    STATUS: "At Risk"
    ACTION: Identify acceleration strategies
ELSE:
    STATUS: "Behind Schedule"
    ACTION: Consider descoping
```

**Sprint Adjustments:**
```
IF ahead of schedule:
    Pull additional stories from Medium priority

IF behind schedule:
    Option 1: Defer Low priority stories
    Option 2: Split large stories
    Option 3: Request help from other team members

IF blocked:
    Option 1: Work on unblocked stories
    Option 2: Create workaround/mock
    Option 3: Escalate blocker
```

### Burndown Tracking

**Daily Burndown Calculation:**
```
points_remaining = committed_points - completed_points

Ideal burndown:
Day 1: 100% remaining
Day 5: 50% remaining
Day 10: 0% remaining

Actual vs Ideal:
IF actual > ideal:
    Behind schedule
ELSE IF actual < ideal:
    Ahead of schedule
ELSE:
    On track
```

**Update Sprint Document:**
```
Edit sprint burndown section daily:
```
Sprint Burndown (Points Remaining):
Day 1:  20 points (100%)
Day 2:  18 points (90%)
Day 3:  15 points (75%)
Day 4:  13 points (65%)
Day 5:  10 points (50%)  ← Mid-sprint checkpoint
```
```

---

## Sprint Review and Demo

### Sprint Review Meeting

**Agenda:**
```
1. Review sprint goal (5 min)
2. Demo completed stories (30 min)
3. Stakeholder feedback (15 min)
4. Review incomplete work (10 min)
5. Next sprint preview (10 min)
```

**Demo Preparation:**
```
FOR each completed_story (status == "Released"):
    Prepare demo:
    - Show working feature
    - Highlight acceptance criteria met
    - Demonstrate user flow
    - Address NFRs (performance, security)

Demo Format:
- Live application demo (preferred)
- Recorded video (if live not feasible)
- Screenshots with narration (last resort)
```

**Collect Feedback:**
```
FOR each demo:
    Record stakeholder feedback
    Classify:
    - Approval: Feature meets expectations
    - Enhancement: Suggestions for improvement
    - Issue: Problem identified (create bug/story)

Update sprint document:
**Stories Demoed:**
1. STORY-XXX: [Title]
   - Demo: [What was shown]
   - Feedback: [Stakeholder response]
   - Action: [Follow-up if needed]
```

### Sprint Metrics

**Completion Metrics:**
```
stories_completed = count(status == "Released")
stories_total = count(all sprint stories)
completion_rate = stories_completed / stories_total

points_completed = sum(status == "Released", points)
points_committed = sum(all sprint stories, points)
velocity = points_completed
```

**Quality Metrics:**
```
qa_approved_first_time = count(QA passed without QA Failed state)
qa_rework_required = count(transitioned QA Failed → In Development)
rework_rate = qa_rework_required / stories_completed

critical_bugs_found = count(severity == "Critical")
```

**Velocity Tracking:**
```
Update rolling velocity:
sprints = last_3_sprints + current_sprint
rolling_velocity = average(sprints.completed_points)

Use for next sprint capacity planning
```

---

## Sprint Retrospective

### Retrospective Format

**What Went Well ✅**
```
Identify successes:
- Practices that worked
- Team collaboration wins
- Tool/process improvements
- Individual contributions

Example:
- "TDD workflow caught bugs early, reducing QA cycles by 50%"
- "Pair programming on complex algorithm solved in half the time"
```

**What Didn't Go Well ❌**
```
Identify challenges:
- Process bottlenecks
- Technical issues
- Communication gaps
- External blockers

Example:
- "External API dependency caused 2-day delay on STORY-XXX"
- "Unclear acceptance criteria led to QA rework on STORY-YYY"
```

**What We Learned 💡**
```
Extract lessons:
- New knowledge gained
- Improved understanding
- Better estimation techniques

Example:
- "Stories > 8 points should be split (took 2x longer than estimated)"
- "Architecture review before dev saves refactoring later"
```

**Action Items 🎯**
```
Create specific, actionable improvements:
- Assign owner
- Set due date
- Make measurable

Example:
✓ "Verify external dependencies in sprint planning" - Owner: Tech Lead - Due: Next planning
✓ "Add edge cases to acceptance criteria template" - Owner: Product Owner - Due: This week
✗ "Communicate better" (too vague, not actionable)
```

### Team Health Check

**Assess team health:**
```
Morale: High / Medium / Low
Collaboration: Excellent / Good / Needs Improvement
Workload: Balanced / Overloaded / Underutilized

IF morale == "Low" OR workload == "Overloaded":
    Investigate causes
    Adjust next sprint capacity
    Address burnout risks
```

---

## Sprint Closure

### Mark Incomplete Work

**Carryover Stories:**
```
FOR story IN (status NOT IN ["Released", "Backlog"]):
    Assess completion:
    - Partially complete: Carry to next sprint
    - Not started: Return to backlog
    - Blocked: Resolve blocker or deprioritize

    Document reason:
    - [ ] STORY-XXX: [Title] - Carried over (80% complete, need QA)
    - [ ] STORY-YYY: [Title] - Returned to backlog (deprioritized)
```

### Update Epic Progress

```
Edit(file_path=".ai_docs/Epics/{epic_id}.md")

Update sprint summary table:
| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| SPRINT-001 | Complete | 20 | 8 | 7 | 0 | 1 |

Update epic completed_points:
completed_points += sprint.completed_points
```

### Close Sprint

```
Edit(file_path=".ai_docs/Sprints/{sprint_id}.md",
     old_string="status: In Progress",
     new_string="status: Complete")

Archive sprint (optional):
- Move to archive directory
- Or keep in Sprints/ for reference
```

---

## Sprint Planning Best Practices

### Capacity Planning

**Conservative Start:**
- New team: 70% of calculated capacity
- First sprint: Under-commit to build confidence
- Increase gradually based on velocity

**Avoid Over-Commitment:**
- Target 80-90% capacity utilization
- Reserve 10-20% buffer for unknowns
- Better to exceed than miss sprint goal

### Story Selection

**Story Size Guidelines:**
- Ideal: 2-5 points (fits in 2-3 days)
- Maximum: 8 points (can split larger)
- Avoid: 13+ points (split into multiple stories)

**Balanced Portfolio:**
- Mix of feature work and technical debt (80/20 split)
- Include bug fixes if high priority
- Balance risk (mix simple and complex stories)

### Sprint Goal Focus

**Single Goal:**
- One clear objective per sprint
- All high-priority stories support goal
- Medium/low stories are complementary

**Measurable Outcome:**
- Sprint goal achieved = Yes / Partial / No
- Objective criteria (not subjective)

---

## Sprint Templates and Tools

### Sprint Document Template Location

```
Template: .claude/skills/devforgeai-orchestration/assets/templates/sprint-template.md

Use when:
- Creating new sprint
- Need complete sprint structure
- Onboarding to sprint format
```

### Sprint Planning Checklist

```
Sprint Planning Checklist:
- [ ] Calculate team capacity
- [ ] Review epic backlog
- [ ] Prioritize stories
- [ ] Select stories for sprint
- [ ] Validate dependencies
- [ ] Create sprint document
- [ ] Define sprint goal
- [ ] Assign stories to developers
- [ ] Schedule daily standups
- [ ] Schedule sprint review
- [ ] Schedule retrospective
```

---

**Use this reference when:**
- Planning new sprint from epic backlog
- Calculating capacity and velocity
- Selecting and prioritizing stories
- Tracking daily sprint progress
- Conducting reviews and retrospectives
