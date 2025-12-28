/**
 * STORY-141: Question Duplication Elimination
 * AC#1: Remove Project Type Question from Command
 *
 * Acceptance Criteria:
 * - Command Phase 1 only validates business idea argument
 * - Skill Phase 1 Step 1 asks all discovery questions including project type
 * - Single source of truth for discovery questions: skill only
 *
 * Test Requirements:
 * - Grep command file for "project type" - should NOT appear
 * - Verify skill asks project type
 * - Verify no duplicate question in workflow
 */

const fs = require('fs');
const path = require('path');

describe('STORY-141: AC#1 - Remove Project Type Question from Command', () => {
  const commandFilePath = path.resolve(__dirname, '../../.claude/commands/ideate.md');
  const skillFilePath = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/SKILL.md');
  const discoveryWorkflowPath = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/references/discovery-workflow.md');

  let commandContent;
  let skillContent;
  let discoveryContent;

  beforeAll(() => {
    commandContent = fs.readFileSync(commandFilePath, 'utf8');
    skillContent = fs.readFileSync(skillFilePath, 'utf8');
    discoveryContent = fs.readFileSync(discoveryWorkflowPath, 'utf8');
  });

  describe('Project Type Question Removal', () => {
    test('should_NOT_contain_project_type_question_in_command_phase_1', () => {
      /**
       * Scenario: Command has been refactored to remove project type question
       * Given: The /ideate command file (Phase 1: Argument Validation section)
       * When: Searching for "project type" patterns
       * Then: Should NOT find project type question in command
       */

      // Arrange
      const projectTypePatterns = [
        /what\s+type\s+of\s+project/i,  // "What type of project"
        /project\s+type\s+question/i,   // "project type question"
        /greenfield\s*\|\s*brownfield/i, // "greenfield | brownfield" (discovery classification)
        /AskUserQuestion.*project\s+type/is // AskUserQuestion with project type
      ];

      // Act & Assert
      for (const pattern of projectTypePatterns) {
        expect(commandContent).not.toMatch(pattern);
      }
    });

    test('should_contain_project_type_question_in_skill_discovery_phase', () => {
      /**
       * Scenario: Skill Phase 1 owns all discovery questions
       * Given: The devforgeai-ideation skill discovery workflow
       * When: Searching for "project type" in skill
       * Then: Should find project type question in skill's Phase 1 or discovery-workflow.md
       */

      // Arrange
      const projectTypeInSkill = /project\s+type|greenfield|brownfield/i;
      const projectTypeInDiscovery = /project\s+type|greenfield|brownfield/i;

      // Act & Assert
      expect(skillContent).toMatch(projectTypeInSkill);
      expect(discoveryContent).toMatch(projectTypeInDiscovery);
    });

    test('should_NOT_duplicate_project_type_question_in_command_and_skill', () => {
      /**
       * Scenario: End-to-end workflow has no duplicate questions
       * Given: Both command and skill files
       * When: Analyzing the complete workflow
       * Then: Project type should be asked ONLY in skill, never in command
       */

      // Arrange
      // Extract Phase 1 section from command
      const phase1CommandMatch = commandContent.match(/## Phase 1:.*?(?=^## [A-Z]|$)/ms);
      const phase1Command = phase1CommandMatch ? phase1CommandMatch[0] : '';

      // Act - Check if project type question appears in command Phase 1
      const projectTypeInCommandPhase1 = /project\s+type|greenfield|brownfield/i.test(phase1Command);

      // Assert
      expect(projectTypeInCommandPhase1).toBe(false);
      // But should appear in skill
      expect(skillContent).toMatch(/project\s+type|greenfield|brownfield/i);
    });

    test('should_only_validate_business_idea_in_command_phase_1', () => {
      /**
       * Scenario: Command Phase 1 limited to argument validation
       * Given: Command file Phase 1 section
       * When: Analyzing responsibilities
       * Then: Should only mention:
       *   - Business idea argument validation
       *   - Non-empty check
       *   - Minimum word count
       *   - NOT discovery questions
       */

      // Arrange
      const phase1Section = commandContent.match(/## Phase 1:.*?(?=^## [A-Z]|^---)/ms)?.[0] || '';

      // Act - Check what Phase 1 does
      const allowedPatterns = [
        /argument.{0,50}validat/i,
        /business\s+idea/i,
        /capture.*business/i,
        /validate\s+descri/i,
        /minimum\s+word/i
      ];

      const discoveryPatterns = [
        /domain\s+question/i,
        /complexity\s+assessment/i,
        /project\s+type/i
      ];

      // Assert - Should have validation language
      const hasValidation = allowedPatterns.some(p => p.test(phase1Section));
      expect(hasValidation).toBe(true);

      // Assert - Should NOT have discovery language
      const hasDiscovery = discoveryPatterns.some(p => p.test(phase1Section));
      expect(hasDiscovery).toBe(false);
    });
  });

  describe('Command vs Skill Responsibility Boundary', () => {
    test('should_have_clear_responsibility_delegation', () => {
      /**
       * Scenario: Responsibilities clearly separated
       * Given: Command and skill documentation
       * When: Reading responsibility statements
       * Then: Command should say "skill handles discovery"
       */

      // Arrange
      const skillResponsibilityMarkers = [
        /skill\s+handles.*discovery/i,
        /skill.*all.*discovery\s+questions/i,
        /discovery.*skill.*responsibility/i,
        /delegate.*discovery.*skill/i
      ];

      // Act & Assert
      // Check command delegates discovery to skill
      expect(commandContent).toMatch(
        /delegate|skill.*discovery|all.*questions.*skill/i
      );
    });

    test('should_have_skill_discovery_ownership_documented', () => {
      /**
       * Scenario: Skill clearly owns discovery phase
       * Given: Skill documentation
       * When: Reading phase descriptions
       * Then: Should explicitly state skill owns all discovery questions
       */

      // Arrange
      const discoveryOwnershipPatterns = [
        /Phase\s+1.*discovery/i,
        /discovery.*all.*questions/i,
        /skill.*owns.*discover/i
      ];

      // Act & Assert
      const hasOwnership = discoveryOwnershipPatterns.some(p => p.test(skillContent));
      expect(hasOwnership).toBe(true);
    });
  });

  describe('Question Template Location Audit', () => {
    test('should_have_discovery_question_templates_in_skill_references', () => {
      /**
       * Scenario: Question templates are in skill references, not command
       * Given: Skill reference files exist
       * When: Checking for question templates
       * Then: Should find templates in references (discovery-workflow.md, etc)
       */

      // Arrange
      const referencesDir = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/references');
      const referenceFiles = fs.readdirSync(referencesDir).filter(f => f.endsWith('.md'));

      // Act
      const discoveryFiles = referenceFiles.filter(f =>
        f.includes('discovery') || f.includes('workflow') || f.includes('elicitation')
      );

      // Assert
      expect(discoveryFiles.length).toBeGreaterThan(0);

      // Verify discovery-workflow.md exists
      expect(discoveryFiles).toContain('discovery-workflow.md');
      expect(discoveryFiles).toContain('requirements-elicitation-workflow.md');
    });

    test('should_NOT_have_discovery_templates_in_command', () => {
      /**
       * Scenario: Command file is clean - no question templates
       * Given: Command file content
       * When: Searching for discovery question patterns
       * Then: Should NOT find discovery question templates
       */

      // Arrange
      const discoveryTemplatePatterns = [
        /## Discovery Questions/i,
        /What type of project/i,
        /What is your primary domain/i,
        /AskUserQuestion.*discovery/is,
        /question templates/i
      ];

      // Act & Assert
      for (const pattern of discoveryTemplatePatterns) {
        expect(commandContent).not.toMatch(pattern);
      }
    });
  });

  describe('Skill Question Count Verification', () => {
    test('should_have_multiple_discovery_questions_in_skill', () => {
      /**
       * Scenario: Skill has ALL discovery questions (Phase 1)
       * Given: Discovery workflow reference file
       * When: Counting AskUserQuestion patterns
       * Then: Should find multiple discovery questions (5-10 as per spec)
       */

      // Arrange
      const askUserQuestionPattern = /AskUserQuestion/g;

      // Act
      const discoveryAskCount = (discoveryContent.match(askUserQuestionPattern) || []).length;

      // Assert
      expect(discoveryAskCount).toBeGreaterThan(0);
      // Expect at least some questions in discovery workflow
      expect(discoveryAskCount).toBeGreaterThanOrEqual(3);
    });
  });
});
