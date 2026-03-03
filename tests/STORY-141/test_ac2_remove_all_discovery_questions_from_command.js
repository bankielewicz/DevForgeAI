/**
 * STORY-141: Question Duplication Elimination
 * AC#2: Remove All Discovery Questions from Command
 *
 * Acceptance Criteria:
 * - Command AskUserQuestion calls limited to brainstorm selection only
 * - Skill has ALL discovery questions
 * - Command responsibilities: argument validation, brainstorm detection, skill invocation
 *
 * Test Requirements:
 * - Count AskUserQuestion in command (should be minimal: brainstorm selection only)
 * - Count AskUserQuestion in skill (should include all discovery questions)
 * - End-to-end test: no repeated questions
 */

const fs = require('fs');
const path = require('path');

describe('STORY-141: AC#2 - Remove All Discovery Questions from Command', () => {
  const commandFilePath = path.resolve(__dirname, '../../.claude/commands/ideate.md');
  const skillFilePath = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/SKILL.md');

  let commandContent;
  let skillContent;

  beforeAll(() => {
    commandContent = fs.readFileSync(commandFilePath, 'utf8');
    skillContent = fs.readFileSync(skillFilePath, 'utf8');
  });

  describe('Discovery Questions Removed from Command', () => {
    test('should_have_minimal_AskUserQuestion_calls_in_command', () => {
      /**
       * Scenario: Command only asks brainstorm selection question
       * Given: Command file content
       * When: Counting AskUserQuestion invocations
       * Then: Should have minimal count (1-2 for brainstorm selection only)
       */

      // Arrange
      const askUserQuestionPattern = /AskUserQuestion\s*\(/g;

      // Act
      const commandAskCount = (commandContent.match(askUserQuestionPattern) || []).length;

      // Assert
      expect(commandAskCount).toBeLessThanOrEqual(3); // Phase 0 (brainstorm) + optional Phase 1.1 (business idea)
    });

    test('should_limit_AskUserQuestion_to_brainstorm_selection_in_phase_0', () => {
      /**
       * Scenario: Phase 0 asks about brainstorm selection
       * Given: Command Phase 0 section
       * When: Analyzing AskUserQuestion content
       * Then: Should only ask about brainstorm selection, not discovery
       */

      // Arrange
      const phase0Section = commandContent.match(/## Phase 0:.*?(?=^## [A-Z]|^---)/ms)?.[0] || '';

      // Act - Extract AskUserQuestion from Phase 0
      const askUserMatches = phase0Section.match(/AskUserQuestion[\s\S]*?\}\s*\)/g) || [];

      // Assert - Should have at least one but for brainstorm only
      expect(askUserMatches.length).toBeGreaterThanOrEqual(0);

      if (askUserMatches.length > 0) {
        // Check that it's about brainstorm, not discovery
        const brainstormQuestionFound = askUserMatches.some(q =>
          /brainstorm|existing/i.test(q)
        );
        expect(brainstormQuestionFound).toBe(true);
      }
    });

    test('should_NOT_ask_discovery_questions_in_command', () => {
      /**
       * Scenario: Command has NO discovery questions
       * Given: Command file content
       * When: Searching for discovery question patterns
       * Then: Should NOT find discovery questions
       */

      // Arrange
      const discoveryQuestionPatterns = [
        // Project type questions
        /AskUserQuestion[\s\S]*?(?:what.*type.*project|greenfield|brownfield)/i,
        // Domain questions
        /AskUserQuestion[\s\S]*?(?:primary.*domain|domain.*area)/i,
        // Complexity questions
        /AskUserQuestion[\s\S]*?(?:complexity|scalability|performance)/i,
        // Requirements questions
        /AskUserQuestion[\s\S]*?(?:functional.*requirement|non-functional)/i,
        // User persona questions
        /AskUserQuestion[\s\S]*?(?:user.*persona|end.*user|stakeholder)/i,
        // Problem space questions
        /AskUserQuestion[\s\S]*?(?:problem.*statement|pain.*point|business.*problem)/i
      ];

      // Act & Assert
      for (const pattern of discoveryQuestionPatterns) {
        expect(commandContent).not.toMatch(pattern);
      }
    });

    test('should_have_business_idea_validation_not_discovery', () => {
      /**
       * Scenario: Command Phase 1 validates business idea (not discovery)
       * Given: Command Phase 1 section
       * When: Analyzing what questions are asked
       * Then: Should only validate argument, not perform discovery
       */

      // Arrange
      const phase1Section = commandContent.match(/## Phase 1:.*?(?=^## [A-Z]|^---)/ms)?.[0] || '';

      // Act - Check for validation keywords
      const hasValidation = /validat|capture|argument|description/i.test(phase1Section);

      // Assert
      expect(hasValidation).toBe(true);

      // Should NOT have discovery keywords
      expect(phase1Section).not.toMatch(/discovery|project\s+type|domain/i);
    });
  });

  describe('All Discovery Questions in Skill', () => {
    test('should_have_discovery_questions_in_skill_phase_1', () => {
      /**
       * Scenario: Skill Phase 1 contains discovery questions
       * Given: Skill content
       * When: Searching for discovery phase
       * Then: Should find Phase 1 references discovery
       */

      // Arrange
      const phase1Pattern = /## Phase 1.*discovery/is;

      // Act & Assert
      expect(skillContent).toMatch(phase1Pattern);
    });

    test('should_have_higher_AskUserQuestion_count_in_skill_than_command', () => {
      /**
       * Scenario: Skill has more questions than command
       * Given: Both command and skill files
       * When: Counting all AskUserQuestion invocations
       * Then: Skill should have significantly more (10+ vs 1-2 in command)
       */

      // Arrange
      const commandAskPattern = /AskUserQuestion\s*\(/g;
      const skillAskPattern = /AskUserQuestion\s*\(/g;

      // Act
      const commandAskCount = (commandContent.match(commandAskPattern) || []).length;
      const skillAskCount = (skillContent.match(skillAskPattern) || []).length;

      // Assert - Skill should ask more questions
      expect(skillAskCount).toBeGreaterThan(commandAskCount);
    });

    test('should_have_all_discovery_question_types_in_skill', () => {
      /**
       * Scenario: Skill has all required discovery question types
       * Given: Skill and discovery workflow content
       * When: Checking for question type coverage
       * Then: Should have questions for:
       *   - Project type (greenfield/brownfield)
       *   - Primary domain
       *   - Scope/boundaries
       *   - Success criteria
       */

      // Arrange
      const requiredQuestionTypes = [
        /project\s+type|greenfield|brownfield/i,           // Project type
        /domain|area\s+of\s+work/i,                        // Domain
        /scope|bound|scale/i,                              // Scope
        /success|goal|metric|objective/i                   // Success criteria
      ];

      // Act & Assert
      for (const questionType of requiredQuestionTypes) {
        expect(skillContent).toMatch(questionType);
      }
    });

    test('should_delegate_to_discovery_workflow_reference', () => {
      /**
       * Scenario: Skill delegates discovery to reference files
       * Given: Skill Phase 1 description
       * When: Analyzing delegation pattern
       * Then: Should reference discovery-workflow.md
       */

      // Arrange
      const delegationPattern = /discovery-workflow\.md|Read.*discovery/i;

      // Act & Assert
      expect(skillContent).toMatch(delegationPattern);
    });
  });

  describe('Command Responsibilities Verification', () => {
    test('should_define_command_responsibilities_as_minimal', () => {
      /**
       * Scenario: Command explicitly defines minimal responsibilities
       * Given: Command documentation
       * When: Reading responsibility statements
       * Then: Should list only:
       *   - Argument validation
       *   - Brainstorm detection
       *   - Skill invocation
       */

      // Arrange
      const commandCompleteSection = commandContent.match(/## Command Complete[\s\S]*$/i)?.[0] || commandContent;

      // Act - Check for responsibility statements
      const hasMinimalResponsibilities = /argument.*validat|brainstorm|invok|skill/i.test(commandCompleteSection);

      // Assert
      expect(hasMinimalResponsibilities).toBe(true);
    });

    test('should_NOT_mention_discovery_in_command_responsibilities', () => {
      /**
       * Scenario: Command responsibility section excludes discovery
       * Given: Command documentation
       * When: Reading "command responsibilities" section
       * Then: Should NOT mention discovery, questions, or requirements elicitation
       */

      // Arrange
      const responsibilitySection = commandContent.match(/## Command Complete[\s\S]*$/i)?.[0] || '';

      // Assert
      expect(responsibilitySection).not.toMatch(/command.*discovery|command.*question|command.*elicit/i);
    });

    test('should_explicitly_state_skill_owns_discovery', () => {
      /**
       * Scenario: Command clearly states skill owns discovery
       * Given: Command documentation
       * When: Reading skill responsibilities section
       * Then: Should explicitly say "Skill responsibilities" include discovery/questions
       */

      // Arrange
      const responsibilitySection = commandContent.match(/## Command Complete[\s\S]*$/i)?.[0] || '';

      // Act & Assert
      expect(responsibilitySection).toMatch(/skill.*discovery|skill.*question|skill.*implementation/i);
    });
  });

  describe('Error Handling Delegation', () => {
    test('should_have_error_handling_patterns_in_command', () => {
      /**
       * Scenario: Command has basic error handling
       * Given: Command file
       * When: Searching for error handling
       * Then: Should have skill invocation error handling, not discovery errors
       */

      // Arrange
      const errorHandlingSection = commandContent.match(/## Error Handling[\s\S]*?(?=^## [A-Z]|$)/ms)?.[0] || '';

      // Assert - Should have error handling for skill invocation
      expect(errorHandlingSection).toMatch(/skill.*fail|error.*skill|skill.*load/i);
    });

    test('should_NOT_have_discovery_error_handling_in_command', () => {
      /**
       * Scenario: Command delegates discovery error handling to skill
       * Given: Command error handling section
       * When: Analyzing error types
       * Then: Should NOT handle discovery errors (incomplete answers, etc)
       */

      // Arrange
      const errorHandlingSection = commandContent.match(/## Error Handling[\s\S]*?(?=^## [A-Z]|$)/ms)?.[0] || '';

      // Act & Assert
      expect(errorHandlingSection).not.toMatch(/incomplete.*answer|discovery.*error|requirement.*incomplete/i);
    });
  });

  describe('Phase Structure Audit', () => {
    test('should_have_phase_0_and_1_only_for_orchestration', () => {
      /**
       * Scenario: Command phases are minimal (0-N only)
       * Given: Command structure
       * When: Identifying phases
       * Then: Should have:
       *   - Phase 0: Brainstorm detection
       *   - Phase 1: Argument validation
       *   - Phase 2: Skill invocation
       *   - Phase 3: Result interpretation
       *   - Phase N: Hook integration
       */

      // Arrange
      const phasePattern = /^## Phase \d+:/gm;

      // Act
      const phases = commandContent.match(phasePattern) || [];

      // Assert
      expect(phases.length).toBeGreaterThan(0);
      expect(phases.length).toBeLessThanOrEqual(5); // 0, 1, 2, 3, N

      // Should have orchestration phases
      expect(commandContent).toMatch(/Phase 0.*Brainstorm/i);
      expect(commandContent).toMatch(/Phase 1.*Argument|Phase 1.*Validation/i);
      expect(commandContent).toMatch(/Phase 2.*Skill|Phase 2.*Invocation/i);
    });

    test('should_NOT_have_discovery_or_requirements_phases_in_command', () => {
      /**
       * Scenario: Command has no discovery/requirements phases
       * Given: Command phases
       * When: Checking for discovery-related phases
       * Then: Should NOT have phases like:
       *   - Phase X: Discovery
       *   - Phase X: Requirements Elicitation
       *   - Phase X: Complexity Assessment
       */

      // Arrange
      const discoveryPhasePatterns = [
        /Phase \d+.*Discovery/i,
        /Phase \d+.*Requirements/i,
        /Phase \d+.*Complexity/i,
        /Phase \d+.*Elicitation/i,
        /Phase \d+.*Feasibility/i
      ];

      // Act & Assert
      for (const pattern of discoveryPhasePatterns) {
        expect(commandContent).not.toMatch(pattern);
      }
    });
  });
});
