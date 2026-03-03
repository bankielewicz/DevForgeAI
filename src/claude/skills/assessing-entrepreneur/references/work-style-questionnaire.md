# Work Style Questionnaire

Detailed question sets for the 6-dimension self-reported assessment. Each dimension contains primary and follow-up questions delivered via AskUserQuestion.

---

## Dimension 1: Work Style

Primary question about preferred work structure.

### Questions

**Q1.1: Daily Structure**
```
AskUserQuestion(
  question="How do you prefer to structure your work day?",
  header="Work Style - Daily Structure",
  options=[
    "Strict schedule with time blocks",
    "Flexible flow - work when inspiration hits",
    "Short focused bursts with frequent breaks",
    "Long deep-work sessions with minimal interruption",
    "Varies significantly day to day"
  ]
)
```

**Q1.2: Environment**
```
AskUserQuestion(
  question="What work environment helps you focus best?",
  header="Work Style - Environment",
  options=[
    "Quiet, distraction-free space",
    "Background noise (cafe, music)",
    "Changing locations throughout the day",
    "Home office with personal setup",
    "Co-working space with others around"
  ]
)
```

**Q1.3: Collaboration**
```
AskUserQuestion(
  question="How do you prefer to collaborate?",
  header="Work Style - Collaboration",
  options=[
    "Work alone, share results",
    "Pair work on difficult problems",
    "Regular check-ins with teammates",
    "Asynchronous communication only",
    "Mix of solo and collaborative work"
  ]
)
```

---

## Dimension 2: Task Completion

Patterns in how the user finishes tasks and projects.

### Questions

**Q2.1: Multi-Step Projects**
```
AskUserQuestion(
  question="When working on a multi-step project, which pattern best describes you?",
  header="Task Completion - Project Patterns",
  options=[
    "I complete tasks sequentially, one at a time",
    "I juggle multiple tasks and finish them in bursts",
    "I start strong but sometimes struggle to finish the last 10%",
    "I need external deadlines to finish things",
    "I finish quickly when excited but delay routine tasks"
  ]
)
```

**Q2.2: Interruptions**
```
AskUserQuestion(
  question="How do you handle interruptions during focused work?",
  header="Task Completion - Interruption Recovery",
  options=[
    "I can resume quickly after interruptions",
    "It takes me significant time to get back on track",
    "I often switch to a different task after being interrupted",
    "I try to prevent all interruptions during focus time",
    "Interruptions don't bother me much"
  ]
)
```

---

## Dimension 3: Motivation

What drives and sustains the user's effort.

### Questions

**Q3.1: Primary Drivers**
```
AskUserQuestion(
  question="What motivates you most to keep working on a project?",
  header="Motivation - Primary Drivers",
  options=[
    "Seeing measurable progress (metrics, milestones)",
    "Learning new things and solving novel problems",
    "Financial goals and revenue targets",
    "Helping others or making an impact",
    "Competition or proving myself",
    "Autonomy and freedom"
  ],
  multiSelect=true
)
```

**Q3.2: Losing Motivation**
```
AskUserQuestion(
  question="When do you tend to lose motivation on a project?",
  header="Motivation - Drop-off Points",
  options=[
    "When the novelty wears off",
    "When progress feels slow",
    "When I hit a difficult technical problem",
    "When I have to do repetitive or boring tasks",
    "When I don't see financial results",
    "When I feel overwhelmed by scope"
  ],
  multiSelect=true
)
```

---

## Dimension 4: Energy Management

How the user manages energy and focus throughout the day.

### Questions

**Q4.1: Peak Focus Time**
```
AskUserQuestion(
  question="When during the day do you feel most focused and productive?",
  header="Energy Management - Peak Hours",
  options=[
    "Early morning (before 9am)",
    "Late morning (9am-12pm)",
    "Early afternoon (12pm-3pm)",
    "Late afternoon (3pm-6pm)",
    "Evening (6pm-10pm)",
    "Late night (after 10pm)",
    "It varies unpredictably"
  ]
)
```

**Q4.2: Energy Recovery**
```
AskUserQuestion(
  question="How do you recharge when your energy is low?",
  header="Energy Management - Recovery",
  options=[
    "Short nap or rest",
    "Physical exercise or walking",
    "Switching to a different type of task",
    "Social interaction",
    "Solitude and quiet time",
    "Snacking or caffeine"
  ],
  multiSelect=true
)
```

---

## Dimension 5: Previous Attempts

Past entrepreneurial or project experiences and lessons learned.

### Questions

**Q5.1: Experience Level**
```
AskUserQuestion(
  question="Have you attempted to start a business or side project before?",
  header="Previous Attempts - Experience",
  options=[
    "No, this is my first attempt",
    "Yes, one attempt that I abandoned early",
    "Yes, one attempt that ran for a while",
    "Yes, multiple attempts with mixed results",
    "Yes, I have a currently running project/business"
  ]
)
```

**Q5.2: Lessons Learned** (if previous experience exists)
```
AskUserQuestion(
  question="What was the biggest lesson from your previous attempt(s)?",
  header="Previous Attempts - Lessons",
  options=[
    "I tried to do too much at once",
    "I didn't validate the idea with customers first",
    "I lost motivation over time",
    "I struggled with the business side (marketing, sales)",
    "I underestimated the time commitment",
    "Technical challenges were harder than expected",
    "I didn't have enough support or accountability"
  ],
  multiSelect=true
)
```

---

## Dimension 6: Self-Reported Challenges

Areas where the user feels they struggle most.

### Questions

**Q6.1: Primary Challenges**
```
AskUserQuestion(
  question="Which of these self-reported challenges resonate most with you?",
  header="Self-Reported Challenges - Primary",
  options=[
    "Staying focused on one thing long enough",
    "Getting started on tasks (procrastination)",
    "Finishing what I start",
    "Managing time and estimating effort",
    "Dealing with administrative/boring tasks",
    "Maintaining consistency over weeks/months",
    "Overthinking and analysis paralysis",
    "Balancing business work with personal life"
  ],
  multiSelect=true
)
```

**Q6.2: Support Preferences**
```
AskUserQuestion(
  question="What kind of support would help you most with these challenges?",
  header="Self-Reported Challenges - Support",
  options=[
    "Step-by-step instructions for every task",
    "Regular accountability check-ins",
    "Templates and frameworks to follow",
    "Encouragement and confidence building",
    "Help prioritizing what matters most",
    "Breaking big goals into tiny steps"
  ],
  multiSelect=true
)
```

---

## Scoring and Normalization

Responses are passed to the entrepreneur-assessor subagent for normalization into a structured profile. The subagent maps categorical responses to profile tags and generates adaptation recommendations for each dimension.
