# Implementation Prompt: DevForgeAI Release Skill

Copy and paste this prompt to Claude Code to begin implementing the devforgeai-release skill:

---

## Prompt for Claude

I need you to implement the **devforgeai-release** skill for the DevForgeAI spec-driven development framework. This is the final stage skill that orchestrates safe, repeatable production deployments.

**Context:**
- The complete design specification is in: `devforgeai/specs/requirements/devforgeai-release-skill-design.md`
- Use the skill-creator template as your guide: `.claude/skills/skill-creator/skill.md`
- Follow the implementation roadmap in: `devforgeai/specs/requirements/devforgeai-skills-implementation-roadmap.md`
- Reference existing skills for patterns: `.claude/skills/devforgeai-qa/SKILL.md`, `.claude/skills/devforgeai-orchestration/SKILL.md`

**Implementation Requirements:**

1. **Read the design specification first:**
   - Read `devforgeai/specs/requirements/devforgeai-release-skill-design.md` (complete specification)

2. **Create the skill structure:**
   ```
   .claude/skills/devforgeai-release/
   ├── SKILL.md (main skill file)
   ├── references/
   │   ├── deployment-strategies.md
   │   ├── smoke-testing-guide.md
   │   ├── rollback-procedures.md
   │   ├── monitoring-metrics.md
   │   └── release-checklist.md
   ├── assets/
   │   └── templates/
   │       ├── release-notes-template.md
   │       ├── rollback-plan-template.md
   │       └── deployment-config-template.yaml
   └── scripts/
       ├── health_check.py
       ├── smoke_test_runner.py
       ├── metrics_collector.py
       ├── rollback_automation.sh
       ├── release_notes_generator.py
       └── README.md
   ```

3. **Implementation Order:**
   - Phase 1: Create SKILL.md with YAML frontmatter and all 6 workflow phases
   - Phase 2: Create 5 reference files
   - Phase 3: Create 3 asset templates
   - Phase 4: Create 5 automation scripts
   - Phase 5: Test and validate

4. **Key Requirements:**
   - Use IMPERATIVE/INFINITIVE form (not second person) throughout
   - Include 8+ AskUserQuestion patterns from the design spec
   - Follow the 6-phase workflow exactly as specified (Pre-Release → Staging → Production → Validation → Documentation → Monitoring)
   - Use native tools (Read, Write, Edit) for file operations
   - Include deployment commands for multiple platforms (Kubernetes, Azure, AWS, Docker)
   - Token budget: ~75,000 tokens total
   - Comprehensive rollback procedures for all platforms

5. **Critical Design Principles:**
   - **"Deploy with Confidence, Fail Gracefully"** - Automated checks at every stage
   - **"Safety Over Speed"** - Never skip release gates
   - **"Environment Parity"** - Staging must mirror production
   - Support 4 deployment strategies: Blue-Green, Rolling Update, Canary, Recreate
   - Automatic rollback on failures
   - Complete audit trail and release documentation

6. **Integration Points:**
   - Input: Story with status "QA Approved" from devforgeai-qa
   - Output: Story with status "Released", release notes, changelog
   - Handoff to: devforgeai-orchestration (update story status, sprint progress)
   - Must validate QA approval before allowing deployment

7. **Deployment Platform Support:**
   - Kubernetes (kubectl, Helm)
   - Azure App Service (az CLI)
   - AWS ECS/Lambda (aws CLI)
   - Docker (docker, docker-compose)
   - Traditional VPS (Ansible, Terraform)
   - Provide fallback commands for manual deployment

8. **Quality Checklist:**
   - [ ] YAML frontmatter includes all deployment tool permissions (kubectl, docker, az, aws, gcloud, helm, terraform, ansible)
   - [ ] All 6 workflow phases implemented in SKILL.md
   - [ ] 8+ AskUserQuestion patterns documented
   - [ ] 5 reference files created with comprehensive content
   - [ ] 3 asset templates created
   - [ ] 5 automation scripts implemented with usage examples
   - [ ] Rollback procedures for all supported platforms
   - [ ] Smoke testing automation included
   - [ ] Metrics monitoring and baseline comparison
   - [ ] Release notes generation
   - [ ] Integration points clearly documented
   - [ ] Success criteria section included

9. **Special Considerations:**
   - Include comprehensive smoke test examples (health checks, API contracts, database connectivity)
   - Document metrics to monitor (error rate, response time, CPU, memory)
   - Provide baseline establishment techniques
   - Include alert configuration examples (CloudWatch, Datadog, Prometheus)
   - Document rollback decision tree (automatic vs. manual triggers)
   - Include post-deployment monitoring (24-hour window)

10. **Testing Requirements:**
    - Test with example story that has QA Approved status
    - Verify release gate validation (blocks if QA not approved)
    - Test release notes generation
    - Test story status update to "Released"
    - Verify changelog update
    - Test rollback procedures (dry run)

**Start by reading the design specification, then create the skill structure, and implement each component in order. Pay special attention to the deployment strategy implementations (Blue-Green, Canary, Rolling, Recreate) as these are the most complex parts.**

Let's begin with Phase 1: Creating SKILL.md with the 6-phase workflow.
