---
# F4 Schema: Structured Requirements for Cross-Session AI Consumption
version: "1.0"
project_name: "business-skills-framework"
created: "2026-02-21"
status: "draft"
author: "DevForgeAI Ideation"
source_brainstorm: "BRAINSTORM-011-business-skills-framework"
plan_file: "/home/bryan/.claude/plans/jiggly-launching-backus.md"
---

# Business Skills Framework — Requirements Specification

## User Personas

personas:
  - id: "P-001"
    name: "Solo Developer"
    role: "Individual building a software project who wants to turn it into a business"
    goals:
      - "Turn existing project into revenue-generating business"
      - "Gain business confidence and knowledge"
      - "Overcome ADHD/executive dysfunction barriers to action"
    frustrations:
      - "Overwhelm from number of business steps"
      - "Imposter syndrome about being a 'real' entrepreneur"
      - "Difficulty breaking large goals into actionable tasks"
    tech_comfort: "High (developer)"
    business_comfort: "Low to Medium"

  - id: "P-002"
    name: "Aspiring Entrepreneur"
    role: "Person with a business idea but no technical product yet"
    goals:
      - "Structure and validate business idea"
      - "Create actionable business plan"
      - "Build confidence to take first steps"
    frustrations:
      - "Don't know where to start"
      - "Self-doubt about idea viability"
      - "Analysis paralysis"
    tech_comfort: "Low to Medium"
    business_comfort: "Low"

---

## Functional Requirements

functional_requirements:

  # === EPIC-A: Assessment & Coaching Core (MVP Phase 1) ===

  - id: "FR-001"
    category: "Assessment"
    epic: "EPIC-A"
    description: "Guided self-assessment questionnaire covering work style, challenges, motivations, energy management, and previous business attempts"
    priority: "High"
    user_story: "As a user, I want to complete a guided self-assessment so that the AI can adapt its coaching approach to my cognitive style and needs"
    acceptance_criteria:
      - "Assessment covers 6 dimensions: work style, task completion, motivation, energy, previous attempts, self-reported challenges"
      - "Assessment takes 10-15 minutes to complete"
      - "Results are persisted to devforgeai/specs/business/user-profile.yaml"
      - "User can recalibrate via /assess-me --recalibrate"

  - id: "FR-002"
    category: "Assessment"
    epic: "EPIC-A"
    description: "Adaptive profile generation that calibrates 7 dimensions: task chunk size, session length, check-in frequency, progress visualization, celebration intensity, reminder style, and overwhelm prevention"
    priority: "High"
    user_story: "As a user with ADHD, I want the AI to automatically adjust task sizes and pacing based on my assessment so that business tasks feel manageable"
    acceptance_criteria:
      - "Profile generates adaptation levels for all 7 dimensions"
      - "Low adaptation: 30-60 min tasks, weekly summaries, full roadmap"
      - "High adaptation: 5-15 min micro-tasks, per-task progress, next 3 tasks only"
      - "Profile stored in YAML, managed exclusively through AI-guided sessions"

  - id: "FR-003"
    category: "Coaching"
    epic: "EPIC-A"
    description: "Dynamic persona blend engine that shifts between empathetic coach and professional consultant based on user context and emotional state"
    priority: "High"
    user_story: "As a user, I want the AI to adapt its communication style to my emotional state so that I receive encouragement when struggling and structure when focused"
    acceptance_criteria:
      - "AI detects emotional indicators from user responses"
      - "Coach mode: empathetic, encouraging, celebrates wins, addresses self-doubt"
      - "Consultant mode: structured, deliverable-focused, professional frameworks"
      - "Transitions are seamless within and across sessions"

  - id: "FR-004"
    category: "Coaching"
    epic: "EPIC-A"
    description: "Emotional state tracking across sessions with tone adaptation for subsequent sessions"
    priority: "High"
    user_story: "As a returning user, I want the AI to remember my emotional state from the previous session so that it adapts its approach accordingly"
    acceptance_criteria:
      - "Emotional indicators logged to coaching/session-log.yaml"
      - "Next session opens with adapted tone based on previous session state"
      - "Example: 'Last session you seemed frustrated — let's start lighter today'"
      - "User can override: 'I'm feeling great today, let's push hard'"

  - id: "FR-005"
    category: "Coaching"
    epic: "EPIC-A"
    description: "Confidence-building patterns including imposter syndrome interventions, momentum tracking, and progressive affirmation"
    priority: "High"
    user_story: "As a user with self-doubt, I want the AI to build my confidence through specific interventions so that I believe I can succeed as an entrepreneur"
    acceptance_criteria:
      - "Includes imposter syndrome recognition and reframing"
      - "Tracks confidence trend over sessions"
      - "Provides evidence-based affirmation ('You've completed X milestones, that puts you ahead of 80% of aspiring entrepreneurs')"
      - "Never dismisses feelings; validates then redirects"

  - id: "FR-006"
    category: "Gamification"
    epic: "EPIC-A"
    description: "Terminal-compatible streak tracking, celebration engine, and progress visualization using ASCII art"
    priority: "High"
    user_story: "As an ADHD user, I want to see visible progress and celebrations after each task so that I get dopamine rewards that motivate continued action"
    acceptance_criteria:
      - "ASCII progress bars showing completion percentage"
      - "Streak counter (consecutive sessions)"
      - "Milestone celebrations with encouraging messages"
      - "All renders correctly in Claude Code Terminal"

  - id: "FR-007"
    category: "Dashboard"
    epic: "EPIC-A"
    description: "Single aggregated /my-business dashboard showing progress across all business domains"
    priority: "High"
    user_story: "As a user, I want one command (/my-business) that shows my progress across all business skill areas so that I can see my overall journey at a glance"
    acceptance_criteria:
      - "Aggregates progress from all business skill artifacts"
      - "Shows: completed milestones, current milestone, streak, next task"
      - "Renders in terminal-compatible ASCII"
      - "Shows estimated time for next task"

  # === EPIC-B: Business Planning & Viability (MVP Phase 2) ===

  - id: "FR-008"
    category: "Business Planning"
    epic: "EPIC-B"
    description: "Lean Canvas guided workflow that walks users through all 9 blocks with adaptive questioning"
    priority: "High"
    user_story: "As an aspiring entrepreneur, I want to complete a Lean Canvas so that I have a structured one-page business model"
    acceptance_criteria:
      - "Guides through all 9 Lean Canvas blocks"
      - "Adapts question depth to user's business knowledge level"
      - "Outputs to devforgeai/specs/business/business-plan/lean-canvas.md"
      - "Supports iteration (refine over multiple sessions)"

  - id: "FR-009"
    category: "Business Planning"
    epic: "EPIC-B"
    description: "Milestone-based business plan with 10 adaptive milestones, soft time targets, and micro-task decomposition"
    priority: "High"
    user_story: "As a user, I want a business plan organized by milestones instead of calendar dates so that I progress at my own pace without deadline anxiety"
    acceptance_criteria:
      - "10 milestones from Problem Validated to Launch Ready"
      - "Each milestone has: definition, soft timeframe, micro-tasks, validation gate, celebration"
      - "Guard rails: 7-day minimum, 180-day soft max"
      - "Recalibration triggered if 180 days exceeded"

  - id: "FR-010"
    category: "Business Planning"
    epic: "EPIC-B"
    description: "Business model pattern matching (SaaS, marketplace, service, product) with viability scoring"
    priority: "Medium"
    user_story: "As a user, I want the AI to identify what type of business model fits my idea so that I can apply the right frameworks"
    acceptance_criteria:
      - "Detects business model type from user description"
      - "Provides model-specific guidance and frameworks"
      - "Viability scoring rubric with clear pass/fail criteria"

  - id: "FR-011"
    category: "Business Planning"
    epic: "EPIC-B"
    description: "Dual-mode operation: project-anchored (analyzes DevForgeAI project) and standalone (pure business idea)"
    priority: "High"
    user_story: "As a user without a coding project, I want to use business planning skills standalone so that I can plan my business without a DevForgeAI development project"
    acceptance_criteria:
      - "Detects whether user has an active DevForgeAI project"
      - "Project-anchored: analyzes codebase for business potential"
      - "Standalone: works with business idea description only"
      - "Both modes produce same output format"

  # === EPIC-C: Market Research (MVP Phase 3) ===

  - id: "FR-012"
    category: "Market Research"
    epic: "EPIC-C"
    description: "Market sizing (TAM/SAM/SOM) guided workflow with research integration"
    priority: "High"
    user_story: "As an entrepreneur, I want help estimating my market size so that I understand the revenue opportunity"
    acceptance_criteria:
      - "Guides through TAM/SAM/SOM estimation"
      - "Uses internet-sleuth for market data when available"
      - "Outputs to devforgeai/specs/business/market-research/market-sizing.md"

  - id: "FR-013"
    category: "Market Research"
    epic: "EPIC-C"
    description: "Competitive landscape analysis leveraging internet-sleuth subagent"
    priority: "High"
    user_story: "As a user, I want to understand my competitive landscape so that I can differentiate my business"
    acceptance_criteria:
      - "Identifies 3-10 competitors with strengths/weaknesses"
      - "Generates competitive positioning matrix"
      - "Outputs to devforgeai/specs/business/market-research/competitive-analysis.md"

  - id: "FR-014"
    category: "Market Research"
    epic: "EPIC-C"
    description: "Customer interview question generator based on business model and hypotheses"
    priority: "Medium"
    user_story: "As a user preparing for customer discovery, I want AI-generated interview questions so that I can validate my assumptions with real customers"
    acceptance_criteria:
      - "Generates 10-20 questions tailored to business model"
      - "Questions organized by hypothesis being tested"
      - "Includes interviewing best practices guidance"

  # === EPIC-D: Marketing (Post-MVP Phase 1) ===

  - id: "FR-015"
    category: "Marketing"
    epic: "EPIC-D"
    description: "Go-to-market strategy builder with channel selection matrix"
    priority: "Medium"
    user_story: "As an entrepreneur, I want a go-to-market strategy so that I know how to reach my first customers"
    acceptance_criteria:
      - "Channel selection based on business model and budget"
      - "Prioritized action items for first 30 days post-launch"
      - "Outputs to devforgeai/specs/business/marketing/go-to-market.md"

  - id: "FR-016"
    category: "Marketing"
    epic: "EPIC-D"
    description: "Positioning and messaging framework"
    priority: "Medium"
    user_story: "As a user, I want help crafting my positioning statement and key messages so that my marketing is consistent and compelling"
    acceptance_criteria:
      - "Generates positioning statement using standard framework"
      - "Creates 3-5 key messages for different audiences"
      - "Outputs to devforgeai/specs/business/marketing/positioning.md"

  # === EPIC-E: Legal & Compliance (Post-MVP Phase 2) ===

  - id: "FR-017"
    category: "Legal"
    epic: "EPIC-E"
    description: "Business structure decision tree with professional referral triggers"
    priority: "Medium"
    user_story: "As a new entrepreneur, I want guidance on business structure (LLC, S-Corp, etc.) so that I make an informed legal decision"
    acceptance_criteria:
      - "Decision tree based on revenue, partners, liability, tax preferences"
      - "Clear 'consult a professional' triggers for complex situations"
      - "Disclaimer on all legal guidance"

  - id: "FR-018"
    category: "Legal"
    epic: "EPIC-E"
    description: "IP protection checklist for software projects"
    priority: "Medium"
    user_story: "As a developer-entrepreneur, I want to understand how to protect my software IP so that my business asset is secure"
    acceptance_criteria:
      - "Covers: copyright, trademark, patent basics, trade secrets"
      - "Specific to software/SaaS projects"
      - "Links to professional resources"

  # === EPIC-F: Financial Planning (Post-MVP Phase 3) ===

  - id: "FR-019"
    category: "Financial"
    epic: "EPIC-F"
    description: "Startup financial model generator with pricing strategy framework"
    priority: "Medium"
    user_story: "As an entrepreneur, I want help creating revenue projections and pricing so that I understand my financial viability"
    acceptance_criteria:
      - "Guided pricing strategy (cost-plus, value-based, competitive)"
      - "Simple revenue projection model"
      - "Break-even analysis"
      - "Terminal table output format"

  - id: "FR-020"
    category: "Financial"
    epic: "EPIC-F"
    description: "Funding options guide (bootstrap, grants, angels, VC)"
    priority: "Low"
    user_story: "As a user needing capital, I want to understand my funding options so that I can choose the right path for my business"
    acceptance_criteria:
      - "Decision tree based on business stage, needs, preferences"
      - "Pros/cons for each funding type"
      - "Clear guidance on when each option is appropriate"

  # === EPIC-G: Operations & Launch (Post-MVP Phase 4) ===

  - id: "FR-021"
    category: "Operations"
    epic: "EPIC-G"
    description: "MVP launch checklist with tool selection guide"
    priority: "Medium"
    user_story: "As a user ready to launch, I want a comprehensive checklist so that I don't miss critical launch steps"
    acceptance_criteria:
      - "Covers: legal, financial, marketing, technical, operations"
      - "Tool recommendations (CRM, payments, analytics) with rationale"
      - "Integration with DevForgeAI /release for code deployment"

  # === EPIC-H: Team Building (Post-MVP Phase 5) ===

  - id: "FR-022"
    category: "Team"
    epic: "EPIC-H"
    description: "First hire decision framework and co-founder compatibility assessment"
    priority: "Low"
    user_story: "As a growing entrepreneur, I want guidance on when and who to hire first so that I build the right team"
    acceptance_criteria:
      - "Decision framework: when to hire vs outsource"
      - "Co-founder compatibility questionnaire"
      - "Contractor vs employee decision tree"

  # === EPIC-R: Revisitation (Cross-cutting) ===

  - id: "FR-023"
    category: "Framework Evolution"
    epic: "EPIC-R"
    description: "Post-epic revisitation loop that re-evaluates brainstorm and integration quality after each epic completes"
    priority: "Medium"
    user_story: "As a framework maintainer, I want an automated revisitation process so that each new epic integrates well with previously implemented skills"
    acceptance_criteria:
      - "Triggered after each epic's QA approval"
      - "Re-reads BRAINSTORM-011 and compares to current state"
      - "Generates integration recommendations"
      - "Uses /brainstorm --resume BRAINSTORM-011 pattern"

---

## Non-Functional Requirements

non_functional_requirements:

  performance:
    - id: "NFR-P001"
      description: "Skill load time must not exceed token budget"
      metric: "SKILL.md line count"
      target: "<1,000 lines per skill (500-800 target)"

    - id: "NFR-P002"
      description: "Progressive disclosure reduces initial context load"
      metric: "Percentage of total content in SKILL.md vs references"
      target: "<40% in SKILL.md, >60% in references"

  safety:
    - id: "NFR-S001"
      description: "Never diagnose ADHD, anxiety, depression, or any mental health condition"
      compliance: "All health-related content includes disclaimer"

    - id: "NFR-S002"
      description: "All legal guidance includes 'consult a professional' disclaimer"
      compliance: "Every legal output file contains disclaimer header"

    - id: "NFR-S003"
      description: "All financial guidance includes 'not financial advice' disclaimer"
      compliance: "Every financial output file contains disclaimer header"

  compatibility:
    - id: "NFR-C001"
      description: "All UX must work within Claude Code Terminal"
      metric: "ASCII-only rendering"
      target: "Zero GUI dependencies"

    - id: "NFR-C002"
      description: "All skills must follow DevForgeAI framework constraints"
      metric: "Context file compliance"
      target: "Read 6 context files before processing; gerund naming; progressive disclosure"

  architecture:
    - id: "NFR-A001"
      description: "Dual-path development architecture"
      metric: "Code location compliance"
      target: "All development in src/ tree; tests in tests/; operational .claude/ after QA only"

    - id: "NFR-A002"
      description: "Session continuity via YAML persistence"
      metric: "Data survival across sessions"
      target: "User profile, milestones, coaching log, streak data persist in devforgeai/specs/business/"

---

## Constraints

constraints:

  technical:
    - id: "CON-T001"
      description: "Claude Code Terminal only — no GUI, web, or desktop components"
      rationale: "Framework operates entirely within terminal environment"

    - id: "CON-T002"
      description: "Markdown documentation only — no executable code in skills"
      rationale: "Skills are prompt expansions, not programs (Source: tech-stack.md)"

    - id: "CON-T003"
      description: "Skills must use gerund naming convention"
      rationale: "Framework standard (Source: tech-stack.md, lines 405-432)"

    - id: "CON-T004"
      description: "SKILL.md under 1,000 lines; target 500-800"
      rationale: "Token budget management (Source: coding-standards.md, lines 111-119)"

    - id: "CON-T005"
      description: "All development in src/ tree; tests in tests/; operational .claude/ after QA"
      rationale: "Dual-path architecture (Source: source-tree.md, lines 789-818)"

  business:
    - id: "CON-B001"
      description: "Never diagnose mental health conditions; only adapt based on self-reported and observed patterns"
      rationale: "AI is not a medical professional; liability and ethical concerns"

    - id: "CON-B002"
      description: "All legal/financial guidance must include professional referral disclaimer"
      rationale: "AI cannot replace licensed professionals; liability concern"

    - id: "CON-B003"
      description: "Iterative epic delivery — each epic builds on the previous"
      rationale: "Agile rollout with revisitation loops per user requirement"

---

## Dependencies

dependencies:

  internal_systems:
    - name: "internet-sleuth subagent"
      integration_type: "Task() invocation"
      criticality: "High"
      purpose: "Market research, competitive analysis, trend data"

    - name: "stakeholder-analyst subagent"
      integration_type: "Task() invocation"
      criticality: "Medium"
      purpose: "Persona analysis for business coaching"

    - name: "DevForgeAI /release command"
      integration_type: "Skill integration"
      criticality: "Low"
      purpose: "Connect business launch to code deployment (EPIC-G)"

    - name: "DevForgeAI feedback system"
      integration_type: "Hook integration"
      criticality: "Medium"
      purpose: "Capture coaching session feedback and AI analysis"

  external_systems: []
  # No external dependencies — framework operates entirely within Claude Code Terminal

  third_party_services: []
  # No third-party services required

---

## Epic Decomposition

epics:

  - id: "EPIC-A"
    name: "Assessment & Coaching Core"
    priority: "P0 (Must Have — MVP Phase 1)"
    requirements: ["FR-001", "FR-002", "FR-003", "FR-004", "FR-005", "FR-006", "FR-007"]
    estimated_stories: 8-12
    dependencies: []
    skills_created: ["assessing-entrepreneur", "coaching-entrepreneur"]
    commands_created: ["/assess-me", "/coach-me", "/my-business"]
    agents_created: ["entrepreneur-assessor", "business-coach"]

  - id: "EPIC-B"
    name: "Business Planning & Viability"
    priority: "P0 (Must Have — MVP Phase 2)"
    requirements: ["FR-008", "FR-009", "FR-010", "FR-011"]
    estimated_stories: 6-8
    dependencies: ["EPIC-A"]
    skills_created: ["planning-business"]
    commands_created: ["/business-plan"]

  - id: "EPIC-C"
    name: "Market Research & Competition"
    priority: "P0 (Must Have — MVP Phase 3)"
    requirements: ["FR-012", "FR-013", "FR-014"]
    estimated_stories: 4-6
    dependencies: ["EPIC-B"]
    skills_created: ["researching-market"]
    commands_created: ["/market-research"]
    agents_created: ["market-analyst"]

  - id: "EPIC-D"
    name: "Marketing & Customer Acquisition"
    priority: "P1 (Should Have — Post-MVP Phase 1)"
    requirements: ["FR-015", "FR-016"]
    estimated_stories: 4-5
    dependencies: ["EPIC-C"]
    skills_created: ["marketing-business"]
    commands_created: ["/marketing-plan"]

  - id: "EPIC-E"
    name: "Legal & Compliance"
    priority: "P1 (Should Have — Post-MVP Phase 2)"
    requirements: ["FR-017", "FR-018"]
    estimated_stories: 3-4
    dependencies: ["EPIC-B"]
    skills_created: ["advising-legal"]
    commands_created: ["/legal-check"]

  - id: "EPIC-F"
    name: "Financial Planning & Modeling"
    priority: "P1 (Should Have — Post-MVP Phase 3)"
    requirements: ["FR-019", "FR-020"]
    estimated_stories: 3-5
    dependencies: ["EPIC-B", "EPIC-C"]
    skills_created: ["managing-finances"]
    commands_created: ["/financial-model"]
    agents_created: ["financial-modeler"]

  - id: "EPIC-G"
    name: "Operations & Launch"
    priority: "P2 (Could Have — Post-MVP Phase 4)"
    requirements: ["FR-021"]
    estimated_stories: 3-4
    dependencies: ["EPIC-B", "EPIC-E"]
    skills_created: ["operating-business"]
    commands_created: ["/ops-plan"]

  - id: "EPIC-H"
    name: "Team Building & HR"
    priority: "P2 (Could Have — Post-MVP Phase 5)"
    requirements: ["FR-022"]
    estimated_stories: 2-3
    dependencies: ["EPIC-F", "EPIC-G"]
    skills_created: ["building-team"]
    commands_created: ["/build-team"]

  - id: "EPIC-R"
    name: "Revisitation & Framework Evolution"
    priority: "P1 (Should Have — Cross-cutting)"
    requirements: ["FR-023"]
    estimated_stories: 2-3
    dependencies: []
    skills_created: []
    commands_created: []

---

## Complexity Assessment

complexity:
  tier: 3
  label: "Complex"
  rationale: "9 new skills, 10 new commands, 4 new subagents, new artifact storage directory, cross-skill coordination, adaptive AI behavior, emotional state tracking"
  total_requirements: 23
  total_epics: 9
  estimated_total_stories: "35-50"
  estimated_sprints: "8-12"

---

## Recommended Next Actions

1. `/create-epic EPIC-A` — Create the Foundation epic (Assessment & Coaching Core)
2. Continue with EPIC-B through EPIC-R sequentially
3. After each epic: `/brainstorm --resume BRAINSTORM-011` for revisitation
4. Sprint planning after epic creation: `/create-sprint`

---

## Source Documents

- **Brainstorm:** `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md`
- **Plan:** `/home/bryan/.claude/plans/jiggly-launching-backus.md`
- **Context Files:** `devforgeai/specs/context/` (6 files)
- **Prompt Engineering:** `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/`
- **Skill Design:** `.claude/skills/claude-code-terminal-expert/references/skills/`
