# Confidence Assessment Workflow

Workflow for assessing confidence levels and imposter syndrome patterns based on self-reported experiences.

**Note: This workflow does not provide clinical assessment. It helps identify self-reported confidence patterns to calibrate coaching support levels.**

---

## Purpose

Many aspiring entrepreneurs experience self-doubt that affects their ability to take action. This workflow identifies self-reported confidence patterns and recommends progressive exposure techniques to build confidence through action.

---

## Confidence Dimensions

### 1. Technical Confidence

How confident the user feels in their technical skills:

- Can they build what they envision?
- Do they feel their skills are "enough"?
- Do they compare themselves unfavorably to others?

### 2. Business Confidence

How confident the user feels about business decisions:

- Pricing their products/services
- Marketing and sales activities
- Financial planning and management

### 3. Social Confidence

How comfortable the user is with public-facing activities:

- Sharing work publicly
- Networking and outreach
- Handling criticism and feedback

### 4. Decision Confidence

How the user approaches decision-making:

- Analysis paralysis patterns
- Decision avoidance
- Second-guessing after decisions

---

## Assessment Questions

Use AskUserQuestion for each confidence dimension:

```
AskUserQuestion(
  question="On a scale of 1-5, how confident do you feel about your technical skills for this venture?",
  header="Technical Confidence",
  options=["1 - Not confident at all", "2 - Slightly confident", "3 - Moderately confident", "4 - Quite confident", "5 - Very confident"]
)
```

Repeat for business, social, and decision confidence.

---

## Imposter Syndrome Patterns

Common self-reported patterns (not clinical labels):

| Pattern | Self-Reported Behavior | Adaptation |
|---------|----------------------|------------|
| Perfectionism | "I can't launch until it's perfect" | Set "good enough" criteria upfront |
| Expert trap | "I need to learn more before starting" | Define minimum knowledge threshold |
| Comparison | "Everyone else seems more qualified" | Focus on unique strengths |
| Discounting | "My success was just luck" | Evidence journaling of skills used |
| Fear of exposure | "People will find out I don't know enough" | Incremental visibility increases |

---

## Progressive Exposure Techniques

Build confidence through graduated action steps:

### Level 1: Private Practice
- Build something small with no audience
- Practice pitching to yourself or a trusted friend
- Write content without publishing

### Level 2: Safe Audience
- Share with a small trusted group (friends, family)
- Join a supportive community (forums, Discord)
- Get feedback from mentors

### Level 3: Limited Public
- Publish a blog post or social media update
- Launch a small free offering
- Attend a networking event

### Level 4: Full Public
- Launch a paid product/service
- Present at a meetup or conference
- Actively market and promote

### Level 5: Leadership
- Teach others what you know
- Mentor aspiring entrepreneurs
- Build a public brand

---

## Calibration Output

Based on self-reported confidence levels, adjust:

- **Task difficulty**: Start with easier wins for low confidence
- **Visibility level**: Match public exposure to comfort level
- **Support frequency**: More check-ins for lower confidence
- **Milestone size**: Smaller milestones for gradual confidence building
- **Feedback timing**: More immediate positive feedback for low confidence areas
