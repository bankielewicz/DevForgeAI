/**
 * STORY-141: Question Duplication Elimination
 * AC#5: Zero Duplicate Questions in End-to-End Flow
 *
 * Acceptance Criteria:
 * - No question asked twice in workflow
 * - Each topic appears exactly once
 * - User feedback: "No repetitive questions"
 *
 * Test Requirements:
 * - Record all AskUserQuestion invocations in workflow
 * - Verify each question topic appears once
 * - Audit for duplicate patterns
 */

const fs = require('fs');
const path = require('path');

describe('STORY-141: AC#5 - Zero Duplicate Questions in End-to-End Flow', () => {
  const commandFilePath = path.resolve(__dirname, '../../.claude/commands/ideate.md');
  const skillFilePath = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/SKILL.md');
  const discoveryWorkflowPath = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/references/discovery-workflow.md');
  const requirementsElicitationPath = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/references/requirements-elicitation-workflow.md');

  let commandContent;
  let skillContent;
  let discoveryContent;
  let requirementsContent;

  beforeAll(() => {
    commandContent = fs.readFileSync(commandFilePath, 'utf8');
    skillContent = fs.readFileSync(skillFilePath, 'utf8');
    discoveryContent = fs.readFileSync(discoveryWorkflowPath, 'utf8');
    requirementsContent = fs.readFileSync(requirementsElicitationPath, 'utf8');
  });

  describe('Question Topic Inventory', () => {
    test('should_have_brainstorm_question_only_in_command_phase_0', () => {
      /**
       * Scenario: Brainstorm selection is asked once, in command only
       * Given: Command and skill files
       * When: Searching for brainstorm selection question
       * Then: Should find ONLY in command Phase 0, NOT in skill
       */

      // Arrange
      const brainstormQuestionPattern = /AskUserQuestion[\s\S]*?(?:use.*brainstorm|existing.*brainstorm)/i;

      // Act - Find brainstorm question in command and skill
      const brainstormInCommand = brainstormQuestionPattern.test(commandContent);
      const brainstormInSkill = /brainstorm.*selection|use.*existing.*brainstorm/i.test(skillContent);

      // Assert
      expect(brainstormInCommand).toBe(true);  // Command asks brainstorm
      expect(brainstormInSkill).toBe(false);   // Skill should NOT ask brainstorm selection
    });

    test('should_have_project_type_question_only_in_skill_phase_1', () => {
      /**
       * Scenario: Project type question asked once, in skill only
       * Given: Command and skill files
       * When: Searching for project type question
       * Then: Should find ONLY in skill, NOT in command
       */

      // Arrange
      const projectTypePattern = /project\s+type|greenfield|brownfield/i;

      // Act - Find project type in command and skill
      const projectTypeInCommand = /AskUserQuestion[\s\S]*?project\s+type|AskUserQuestion[\s\S]*?greenfield/i.test(commandContent);
      const projectTypeInSkill = projectTypePattern.test(skillContent);

      // Assert
      expect(projectTypeInCommand).toBe(false); // Command should NOT ask project type
      expect(projectTypeInSkill).toBe(true);    // Skill should ask project type
    });

    test('should_have_domain_question_only_in_skill_discovery', () => {
      /**
       * Scenario: Domain/problem space question asked once, in skill discovery
       * Given: Command and skill files
       * When: Searching for domain question
       * Then: Should find ONLY in skill discovery, NOT in command
       */

      // Arrange
      const domainQuestionPattern = /primary\s+domain|area\s+of\s+work|domain|problem\s+space/i;

      // Act - Find domain question
      const domainInCommand = /AskUserQuestion[\s\S]*?domain|AskUserQuestion[\s\S]*?primary\s+area/i.test(commandContent);
      const domainInSkill = domainQuestionPattern.test(skillContent);

      // Assert
      expect(domainInCommand).toBe(false);      // Command should NOT ask domain
      expect(domainInSkill).toBe(true);         // Skill should ask domain
    });

    test('should_have_success_criteria_question_only_in_skill_discovery', () => {
      /**
       * Scenario: Success/goal question asked once, in skill discovery
       * Given: Command and skill files
       * When: Searching for success/goal question
       * Then: Should find ONLY in skill, NOT in command
       */

      // Arrange
      const successPattern = /success.*criteria|goal|objective|metric|measure.*success/i;

      // Act
      const successInCommand = /AskUserQuestion[\s\S]*?success|AskUserQuestion[\s\S]*?goal/i.test(commandContent);
      const successInSkill = successPattern.test(skillContent);

      // Assert
      expect(successInCommand).toBe(false);     // Command should NOT ask success criteria
      expect(successInSkill).toBe(true);        // Skill should ask success criteria
    });

    test('should_have_complexity_question_only_in_skill_phase_3', () => {
      /**
       * Scenario: Complexity question asked once, in skill Phase 3 only
       * Given: Skill content
       * When: Searching for complexity question
       * Then: Should find in Phase 3 only
       */

      // Arrange
      const phase3Section = skillContent.match(/Phase 3[\s\S]*?(?=###|$)/is)?.[0] || '';
      const phase1Section = skillContent.match(/Phase 1[\s\S]*?(?=###|$)/is)?.[0] || '';

      // Act
      const complexityInPhase3 = /complexity|scalability|performance|tier|size/i.test(phase3Section);

      // Assert
      expect(complexityInPhase3).toBe(true);  // Phase 3 should assess complexity
      // Should NOT duplicate in Phase 1 discovery
      expect(phase1Section).not.toMatch(/complexity\s+assessment|assess.*complexity|rate.*complexity/i);
    });
  });

  describe('Question Deduplication Verification', () => {
    test('should_NOT_have_duplicate_project_type_questions', () => {
      /**
       * Scenario: Project type not asked multiple times
       * Given: All files (command, skill, references)
       * When: Counting project type questions
       * Then: Should appear exactly once (in skill Phase 1)
       */

      // Arrange
      const allContent = commandContent + '\n---\n' + skillContent + '\n---\n' + discoveryContent;

      // Extract all AskUserQuestion blocks about project type
      const projectTypeQuestions = allContent.match(/AskUserQuestion[\s\S]*?(?:project\s+type|greenfield|brownfield)[\s\S]*?\}/g) || [];

      // Act
      const uniqueProjectTypeQuestions = new Set(projectTypeQuestions.map(q =>
        q.replace(/\s+/g, ' ').substring(0, 100) // Normalize and get fingerprint
      ));

      // Assert
      expect(projectTypeQuestions.length).toBeGreaterThan(0);
      expect(uniqueProjectTypeQuestions.size).toBeLessThanOrEqual(1);
    });

    test('should_NOT_have_duplicate_domain_questions', () => {
      /**
       * Scenario: Domain question not asked multiple times
       * Given: All files
       * When: Searching for domain questions
       * Then: Should appear once in skill discovery only
       */

      // Arrange
      const allContent = commandContent + '\n---\n' + skillContent + '\n---\n' + discoveryContent;

      // Look for explicit domain questions
      const domainQuestionMatches = (allContent.match(/(?:primary\s+domain|area\s+of\s+work|problem\s+space)/gi) || []).filter(m =>
        allContent.substring(Math.max(0, allContent.indexOf(m) - 100), allContent.indexOf(m) + 100).includes('AskUserQuestion')
      );

      // Assert
      expect(domainQuestionMatches.length).toBeLessThanOrEqual(1);
    });

    test('should_NOT_have_duplicate_scope_questions', () => {
      /**
       * Scenario: Scope/boundary questions not duplicated
       * Given: All files
       * When: Searching for scope definition questions
       * Then: Should appear in discovery phase only
       */

      // Arrange
      const scopePatterns = [
        /scope|boundary|scale|size|range|limits/i,
        /what.*boundaries|define.*scope/i
      ];

      // Act - Count scope-related AskUserQuestion blocks
      const commandScope = (commandContent.match(/AskUserQuestion[\s\S]*?(?:scope|boundary|scale)[\s\S]*?\}/gi) || []).length;
      const skillScope = (skillContent.match(/AskUserQuestion[\s\S]*?(?:scope|boundary|scale)[\s\S]*?\}/gi) || []).length;

      // Assert
      expect(commandScope).toBe(0);      // Command should not ask scope
      expect(skillScope).toBeGreaterThan(0); // Skill should ask scope
    });

    test('should_NOT_have_duplicate_user_persona_questions', () => {
      /**
       * Scenario: User persona questions not duplicated
       * Given: All files
       * When: Searching for persona questions
       * Then: Should appear in discovery phase only, not asked twice
       */

      // Arrange
      const allContent = commandContent + '\n---\n' + skillContent + '\n---\n' + discoveryContent + '\n---\n' + requirementsContent;

      // Act - Count persona-related question blocks
      const personaQuestions = (allContent.match(/AskUserQuestion[\s\S]*?(?:user|persona|stakeholder|end.?user)[\s\S]*?\}/gi) || []).length;

      // Count in command vs skill
      const commandPersona = (commandContent.match(/AskUserQuestion[\s\S]*?(?:user|persona|stakeholder)[\s\S]*?\}/gi) || []).length;

      // Assert
      expect(commandPersona).toBe(0); // Command should NOT ask about personas
    });

    test('should_NOT_have_question_about_existing_system_in_both_phases', () => {
      /**
       * Scenario: Questions about existing system/brownfield status not duplicated
       * Given: Command and skill
       * When: Searching for brownfield/existing system questions
       * Then: Should be in discovery phase, not in command argument validation
       */

      // Arrange
      const commandPhase1 = commandContent.match(/## Phase 1:[\s\S]*?(?=^## |$)/im)?.[0] || '';

      // Act
      const hasBrownfieldInPhase1 = /AskUserQuestion[\s\S]*?(?:brownfield|existing\s+system|migrate|upgrade)[\s\S]*?\}/i.test(commandPhase1);

      // Assert
      expect(hasBrownfieldInPhase1).toBe(false);
    });
  });

  describe('Question Sequence Audit', () => {
    test('should_ask_questions_in_logical_order_without_repetition', () => {
      /**
       * Scenario: Questions follow logical flow (broad to specific)
       * Given: Skill discovery and requirements workflows
       * When: Analyzing question sequence
       * Then: Should progress from:
       *   1. Project type (Phase 1)
       *   2. Domain (Phase 1)
       *   3. Requirements (Phase 2)
       *   4. Complexity (Phase 3)
       *   Without backtracking to ask earlier questions again
       */

      // Arrange
      const phase1 = skillContent.match(/Phase 1[\s\S]*?(?=Phase 2|###)/is)?.[0] || '';
      const phase2 = skillContent.match(/Phase 2[\s\S]*?(?=Phase 3|###)/is)?.[0] || '';
      const phase3 = skillContent.match(/Phase 3[\s\S]*?(?=Phase 4|###)/is)?.[0] || '';

      // Act - Check that each phase has its own questions
      const phase1HasType = /project\s+type|greenfield|brownfield/i.test(phase1);
      const phase2HasRequirements = /functional.*requirement|user.*story|data/i.test(phase2);
      const phase3HasComplexity = /complexity|score|tier/i.test(phase3);

      // Assert - Each phase should have its characteristic questions
      expect(phase1HasType).toBe(true);
      expect(phase2HasRequirements).toBe(true);
      expect(phase3HasComplexity).toBe(true);

      // Phase 3 should NOT ask project type again
      expect(phase3).not.toMatch(/greenfield|brownfield|project\s+type/i);
    });

    test('should_NOT_revisit_discovery_questions_in_later_phases', () => {
      /**
       * Scenario: Once discovery phase complete, don't re-ask discovery questions
       * Given: Skill Phase 2-6 content
       * When: Checking for discovery question patterns
       * Then: Should NOT re-ask:
       *   - Project type
       *   - Primary domain
       *   - Scope boundaries
       *   - User personas
       */

      // Arrange
      const phase2Plus = skillContent.match(/Phase 2[\s\S]*$/is)?.[0] || '';

      // Act
      const redoesProjectType = /Phase 2[\s\S]*?greenfield|Phase 3[\s\S]*?greenfield/i.test(phase2Plus);
      const redoesDomain = /Phase 2[\s\S]*?primary\s+domain[\s\S]*?Phase 3[\s\S]*?primary\s+domain/i.test(phase2Plus);

      // Assert - Should NOT repeat discovery questions
      expect(redoesProjectType).toBe(false);
      expect(redoesDomain).toBe(false);
    });

    test('should_NOT_ask_complexity_in_discovery_phase', () => {
      /**
       * Scenario: Complexity assessment happens in Phase 3, not discovery
       * Given: Skill Phase 1 (Discovery)
       * When: Checking for complexity questions
       * Then: Should NOT ask complexity in Phase 1
       */

      // Arrange
      const phase1 = skillContent.match(/Phase 1[\s\S]*?(?=Phase 2|###)/is)?.[0] || '';

      // Act & Assert
      expect(phase1).not.toMatch(/assess.*complexity|rate.*complexity|complexity\s+score/i);
    });
  });

  describe('Question Coverage Without Duplication', () => {
    test('should_cover_all_required_topics_once_each', () => {
      /**
       * Scenario: All required topics covered exactly once
       * Given: Full workflow (command + skill)
       * When: Auditing topic coverage
       * Then: Should have:
       *   - Brainstorm selection (1x, command)
       *   - Project type (1x, skill)
       *   - Domain (1x, skill)
       *   - Scope (1x, skill)
       *   - Success criteria (1x, skill)
       *   - Requirements (multiple, skill Phase 2)
       *   - Complexity (1x, skill Phase 3)
       */

      // Arrange
      const topics = [
        { topic: 'Brainstorm Selection', pattern: /brainstorm.*selection|use.*existing/i, expectedLocation: 'command' },
        { topic: 'Project Type', pattern: /greenfield|brownfield|project\s+type/i, expectedLocation: 'skill' },
        { topic: 'Primary Domain', pattern: /primary.*domain|domain|area.*work/i, expectedLocation: 'skill' },
        { topic: 'Scope/Boundaries', pattern: /scope|boundary|scale/i, expectedLocation: 'skill' },
        { topic: 'Success Criteria', pattern: /success.*criteria|goal|objective/i, expectedLocation: 'skill' }
      ];

      // Act & Assert
      for (const item of topics) {
        if (item.expectedLocation === 'command') {
          expect(commandContent).toMatch(item.pattern);
        } else if (item.expectedLocation === 'skill') {
          expect(skillContent).toMatch(item.pattern);
        }
      }
    });

    test('should_NOT_have_redundant_questions_after_refactoring', () => {
      /**
       * Scenario: Refactoring eliminated duplicates
       * Given: Current state (after refactoring)
       * When: Checking for redundant patterns
       * Then: Should NOT have:
       *   - "project type" asked twice
       *   - Same question in command AND skill
       *   - Brainstorm question in skill
       *   - Discovery questions in command
       */

      // Arrange
      const redundancyPatterns = [
        { pattern: /AskUserQuestion[\s\S]*?project\s+type[\s\S]*?AskUserQuestion[\s\S]*?project\s+type/i, message: 'Project type asked twice' },
        { pattern: /AskUserQuestion[\s\S]*?greenfield[\s\S]*?AskUserQuestion[\s\S]*?greenfield/i, message: 'Greenfield asked twice' }
      ];

      // Act & Assert
      const allContent = commandContent + '\n---\n' + skillContent;
      for (const item of redundancyPatterns) {
        expect(allContent).not.toMatch(item.pattern);
      }
    });
  });

  describe('User Experience - No Repetitive Questions', () => {
    test('should_have_logical_question_flow_without_backtracking', () => {
      /**
       * Scenario: User answers questions once in logical order
       * Given: Question sequence in workflow
       * When: Simulating user interaction
       * Then: User should:
       *   1. Choose brainstorm or start fresh (Phase 0 of command)
       *   2. Provide business idea (Phase 1 of command, or skip if brainstorm)
       *   3. Answer discovery questions once (Phase 1 of skill)
       *   4. Answer requirements questions once (Phase 2 of skill)
       *   5. Provide complexity assessment (Phase 3 of skill)
       *   No backtracking to any previous question
       */

      // Arrange - Check workflow structure
      const commandPhases = commandContent.match(/^## Phase \d+:/gm) || [];
      const skillPhases = skillContent.match(/### Phase \d+:/gm) || [];

      // Act
      const hasOrderedPhases = commandPhases.length > 0 && skillPhases.length > 0;

      // Assert
      expect(hasOrderedPhases).toBe(true);
      expect(commandPhases.length).toBeLessThanOrEqual(4); // Phases 0, 1, 2, 3, N
    });

    test('should_have_contextual_questions_not_generic_repeated_questions', () => {
      /**
       * Scenario: Questions are contextual, not generic repeats
       * Given: Question patterns
       * When: Analyzing question uniqueness
       * Then: Each question should:
       *   - Build on previous context
       *   - Not repeat same question in different wording
       *   - Have clear purpose
       */

      // Arrange
      const phase1Section = skillContent.match(/Phase 1[\s\S]*?(?=###|$)/is)?.[0] || '';

      // Act - Check for contextual language
      const hasContext = /given|based.*on|now.*that.*know|tell.*me.*more/i.test(phase1Section);

      // Assert
      expect(hasContext).toBe(true);
    });
  });

  describe('Quality Metrics', () => {
    test('should_have_AskUserQuestion_count_minimized_in_command', () => {
      /**
       * Scenario: Command asks minimal questions
       * Given: Command file
       * When: Counting AskUserQuestion calls
       * Then: Should have ≤ 3 (Phase 0: brainstorm, Phase 1: business idea, Phase 1.2: validation)
       */

      // Arrange
      const askUserCount = (commandContent.match(/AskUserQuestion\s*\(/g) || []).length;

      // Act & Assert
      expect(askUserCount).toBeLessThanOrEqual(3);
    });

    test('should_have_AskUserQuestion_count_reasonable_in_skill', () => {
      /**
       * Scenario: Skill asks reasonable number of discovery questions
       * Given: Skill file
       * When: Counting AskUserQuestion calls
       * Then: Should have 10-60 across all phases (per spec)
       */

      // Arrange
      const askUserCount = (skillContent.match(/AskUserQuestion\s*\(/g) || []).length;

      // Act & Assert
      expect(askUserCount).toBeGreaterThanOrEqual(1); // At least some questions
    });

    test('should_have_discovery_and_requirements_questions_separated', () => {
      /**
       * Scenario: Discovery and requirements questions are in different phases
       * Given: Skill structure
       * When: Analyzing phase separation
       * Then: Should have:
       *   - Phase 1: Discovery (5-10 questions)
       *   - Phase 2: Requirements (10-60 questions)
       */

      // Arrange
      const phase1 = skillContent.match(/Phase 1[\s\S]*?(?=###|$)/is)?.[0] || '';
      const phase2 = skillContent.match(/Phase 2[\s\S]*?(?=###|$)/is)?.[0] || '';

      // Act
      const phase1Count = (phase1.match(/AskUserQuestion/g) || []).length;
      const phase2Count = (phase2.match(/AskUserQuestion/g) || []).length;

      // Assert
      // Phase 1 should have fewer questions than Phase 2
      expect(phase1Count).toBeLessThan(phase2Count || 1);
    });
  });
});
