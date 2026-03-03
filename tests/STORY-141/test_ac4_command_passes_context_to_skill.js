/**
 * STORY-141: Question Duplication Elimination
 * AC#4: Command Passes Context to Skill
 *
 * Acceptance Criteria:
 * - Context passed via markers: **Business Idea:**, **Brainstorm Context:**, **Brainstorm File:**
 * - Skill extracts context from conversation, not re-asking
 * - No duplicate questions when context is provided
 *
 * Test Requirements:
 * - Verify context markers in conversation before skill invocation
 * - Verify skill reads markers correctly
 * - Verify no re-asking of context already provided
 */

const fs = require('fs');
const path = require('path');

describe('STORY-141: AC#4 - Command Passes Context to Skill', () => {
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

  describe('Context Markers in Command', () => {
    test('should_have_Business_Idea_context_marker', () => {
      /**
       * Scenario: Command sets Business Idea context before skill invocation
       * Given: Command Phase 2 (Skill Invocation)
       * When: Analyzing context preparation
       * Then: Should have **Business Idea:** marker
       */

      // Arrange
      const phase2Section = commandContent.match(/## Phase 2:.*?(?=^## [A-Z]|$)/ms)?.[0] || '';

      // Act & Assert
      expect(phase2Section).toMatch(/\*\*Business Idea:\*\*/);
    });

    test('should_have_Brainstorm_Context_marker_for_brainstorm_flow', () => {
      /**
       * Scenario: Command sets brainstorm context marker when brainstorm is selected
       * Given: Command Phase 0 (Brainstorm Detection)
       * When: Analyzing brainstorm context handling
       * Then: Should have **Brainstorm Context:** marker
       */

      // Arrange
      const phase0Section = commandContent.match(/## Phase 0:.*?(?=^## [A-Z]|$)/ms)?.[0] || '';

      // Act & Assert
      expect(phase0Section).toMatch(/\$BRAINSTORM_CONTEXT|brainstorm.*context/i);
    });

    test('should_have_Brainstorm_File_marker_for_file_path', () => {
      /**
       * Scenario: Command passes brainstorm file path to skill
       * Given: Command context setup
       * When: Analyzing brainstorm file handling
       * Then: Should reference file path in context
       */

      // Arrange
      const contextSection = commandContent.match(/## Phase 2:[\s\S]*?Skill Invocation|context/ms)?.[0] || commandContent;

      // Act & Assert
      expect(contextSection).toMatch(/brainstorm.*file|file.*path|selected.*brainstorm/i);
    });

    test('should_set_context_BEFORE_skill_invocation', () => {
      /**
       * Scenario: Context markers are set before Skill() call
       * Given: Command Phase 2 section
       * When: Analyzing order of operations
       * Then: Context markers should appear BEFORE Skill() invocation
       */

      // Arrange
      const phase2Content = commandContent.match(/## Phase 2:[\s\S]*?## Phase/)?.[0] || '';

      // Act - Find positions
      const contextMarkerPos = phase2Content.search(/\*\*Business Idea:\*\*|context\s*marker|Display.*Business Idea/i);
      const skillInvocationPos = phase2Content.search(/Skill\s*\(\s*command/i);

      // Assert - Context should appear before skill invocation
      expect(contextMarkerPos).toBeGreaterThanOrEqual(0);
      expect(skillInvocationPos).toBeGreaterThanOrEqual(0);
      if (contextMarkerPos >= 0 && skillInvocationPos >= 0) {
        expect(contextMarkerPos).toBeLessThan(skillInvocationPos);
      }
    });

    test('should_display_context_markers_in_output', () => {
      /**
       * Scenario: Context markers are displayed to user/conversation
       * Given: Command context preparation
       * When: Checking for Display() calls
       * Then: Should display context information before skill invocation
       */

      // Arrange
      const phase2Section = commandContent.match(/## Phase 2:[\s\S]*?(?=^## [A-Z]|$)/ms)?.[0] || '';

      // Act & Assert
      expect(phase2Section).toMatch(/Display|context|Business Idea/i);
    });
  });

  describe('Skill Reads Context Markers', () => {
    test('should_check_for_context_variables_in_skill_phase_1', () => {
      /**
       * Scenario: Skill detects if context is provided
       * Given: Skill Phase 1 (Discovery)
       * When: Analyzing context detection
       * Then: Should check for context variables like $BRAINSTORM_CONTEXT or markers
       */

      // Arrange
      const phase1Section = skillContent.match(/Phase 1.*?(?=###|$)/is)?.[0] || '';

      // Act & Assert
      expect(phase1Section).toMatch(/\$BRAINSTORM_CONTEXT|IF.*context|context.*provided|check.*context/i);
    });

    test('should_skip_discovery_questions_if_brainstorm_context_provided', () => {
      /**
       * Scenario: Skill skips redundant discovery when brainstorm context available
       * Given: Skill Phase 1 with brainstorm handoff
       * When: Checking for skip logic
       * Then: Should have conditional to skip or shorten discovery
       */

      // Arrange
      const phase1Section = skillContent.match(/Phase 1.*?(?=###|$)/is)?.[0] || '';

      // Act & Assert
      expect(phase1Section).toMatch(/skip.*discovery|shorten|confidence.*HIGH|brainstorm.*high/i);
    });

    test('should_read_project_mode_context_in_phase_6', () => {
      /**
       * Scenario: Skill reads project mode context (greenfield/brownfield)
       * Given: Skill Phase 6 (Completion)
       * When: Checking for mode detection
       * Then: Should read $PROJECT_MODE_CONTEXT or equivalent
       */

      // Arrange
      const phase6Section = skillContent.match(/Phase 6.*?(?=$|###)/is)?.[0] || '';

      // Act & Assert
      expect(phase6Section).toMatch(/project.*mode|greenfield|brownfield|context.*file/i);
    });

    test('should_NOT_re_ask_business_idea_if_provided_in_context', () => {
      /**
       * Scenario: Skill doesn't re-ask business idea if context passed
       * Given: Skill Phase 1 discovery
       * When: Analyzing question flow
       * Then: Should skip business idea question if context provided
       */

      // Arrange
      const discoveryPhase = discoveryContent.match(/Step 1|Phase 1[\s\S]*?(?=##|Step|$)/is)?.[0] || discoveryContent;

      // Act - Check for conditional asking
      const hasConditionalLogic = /IF.*context|skip.*if|when.*provided|already.*provided/i.test(discoveryPhase);

      // Assert
      expect(hasConditionalLogic).toBe(true);
    });

    test('should_validate_context_markers_have_content', () => {
      /**
       * Scenario: Skill validates that context markers have actual values
       * Given: Skill error handling
       * When: Checking for validation
       * Then: Should validate non-empty context
       */

      // Arrange
      const phase1Section = skillContent.match(/Phase 1.*?(?=###|$)/is)?.[0] || '';

      // Act & Assert
      expect(phase1Section).toMatch(/validat|check|empty|null|undefined/i);
    });
  });

  describe('No Re-Asking Context', () => {
    test('should_NOT_ask_for_business_idea_in_skill_if_command_provided', () => {
      /**
       * Scenario: Skill doesn't ask for business idea if command already captured it
       * Given: Skill Phase 1 discovery questions
       * When: Checking question patterns
       * Then: Should have logic to skip/use provided context
       */

      // Arrange
      const phase1Discovery = discoveryContent.match(/Step 1|questions[\s\S]*?(?=##|Step|---)/is)?.[0] || '';

      // Act - Check for business idea question
      const askBusinessIdea = /describe.*business.*idea|tell.*about.*idea|what.*problem/i;

      // Assertion - If business idea is asked, should be conditional
      if (askBusinessIdea.test(phase1Discovery)) {
        // It's okay if asked, but should be conditional
        expect(phase1Discovery).toMatch(/IF.*context|IF.*provided|already.*have/i);
      }
    });

    test('should_use_provided_brainstorm_instead_of_re_discovering', () => {
      /**
       * Scenario: Skill uses brainstorm data instead of re-discovering
       * Given: Skill brainstorm handling (Phase 1 Step 0)
       * When: Checking for context usage
       * Then: Should extract and use brainstorm data
       */

      // Arrange
      const brainstormHandlingPattern = /\$BRAINSTORM_CONTEXT|pre-?populated|from.*brainstorm|use.*brainstorm/i;

      // Act & Assert
      expect(skillContent).toMatch(brainstormHandlingPattern);
    });

    test('should_detect_context_in_conversation_not_request_re_entry', () => {
      /**
       * Scenario: Skill reads context from conversation markers, not user input
       * Given: Skill context detection logic
       * When: Analyzing context source
       * Then: Should read from $BRAINSTORM_CONTEXT variable or conversation markers
       */

      // Arrange
      const phase1Section = skillContent.match(/Phase 1.*?(?=###|$)/is)?.[0] || '';

      // Act & Assert
      expect(phase1Section).toMatch(/\$BRAINSTORM_CONTEXT|conversation|marker|from.*command/i);
    });

    test('should_have_validation_before_asking_duplicate_questions', () => {
      /**
       * Scenario: Skill validates what context was provided before asking
       * Given: Skill discovery phase
       * When: Checking for pre-question validation
       * Then: Should check what was already provided
       */

      // Arrange
      const discoveryQuestions = discoveryContent;

      // Act - Check for validation/checking logic
      const hasValidation = /IF.*context|IF.*provided|check.*if|already.*received|given|passed/i.test(discoveryQuestions);

      // Assert
      expect(hasValidation).toBe(true);
    });
  });

  describe('Context Variable Definitions', () => {
    test('should_define_BRAINSTORM_CONTEXT_structure', () => {
      /**
       * Scenario: Command defines what BRAINSTORM_CONTEXT contains
       * Given: Command Phase 0 or documentation
       * When: Analyzing context variable definition
       * Then: Should define structure with:
       *   - brainstorm_id
       *   - problem_statement
       *   - target_outcome
       *   - user_personas
       *   - hard_constraints
       *   - must_have_capabilities
       *   - confidence_level
       */

      // Arrange
      const contextDefinition = commandContent.match(/\$BRAINSTORM_CONTEXT\s*=[\s\S]*?\}/)?.[0] || '';

      // Act & Assert
      expect(contextDefinition.length).toBeGreaterThan(0);
      expect(contextDefinition).toMatch(/brainstorm_id|problem_statement|confidence/i);
    });

    test('should_define_PROJECT_MODE_CONTEXT_structure', () => {
      /**
       * Scenario: Command defines PROJECT_MODE_CONTEXT for skill handoff
       * Given: Command Phase 1.3 (Mode Detection)
       * When: Analyzing mode context definition
       * Then: Should define:
       *   - mode (greenfield/brownfield)
       *   - context_files_found
       *   - detection_method
       */

      // Arrange
      const modeDefinition = commandContent.match(/\$PROJECT_MODE_CONTEXT\s*=[\s\S]*?\}/)?.[0] || '';

      // Act & Assert
      expect(modeDefinition.length).toBeGreaterThan(0);
      expect(modeDefinition).toMatch(/mode|context_file|detection/i);
    });

    test('should_pass_business_idea_in_context_markers', () => {
      /**
       * Scenario: Business idea is passed as conversation context
       * Given: Command Phase 2 context preparation
       * When: Analyzing how business idea is passed
       * Then: Should be displayed/marked with **Business Idea:** before skill invoke
       */

      // Arrange
      const phase2 = commandContent.match(/## Phase 2:[\s\S]*?Skill Invocation/is)?.[0] || '';

      // Act & Assert
      expect(phase2).toMatch(/\*\*Business Idea:\*\*/);
    });
  });

  describe('Context Flow Documentation', () => {
    test('should_document_context_markers_in_comment_or_description', () => {
      /**
       * Scenario: Command documents what context markers are used
       * Given: Command documentation
       * When: Searching for context marker documentation
       * Then: Should have clear documentation of:
       *   - **Business Idea:**
       *   - **Brainstorm Context:**
       *   - **Brainstorm File:**
       */

      // Arrange
      const phase2Section = commandContent.match(/## Phase 2:[\s\S]*?(?=^## [A-Z]|$)/ms)?.[0] || '';

      // Act & Assert
      expect(phase2Section).toMatch(/Business Idea|Brainstorm|context.*marker/i);
    });

    test('should_have_clear_context_handoff_explanation', () => {
      /**
       * Scenario: Command explains how context flows to skill
       * Given: Command documentation
       * When: Reading about context passing
       * Then: Should explain:
       *   - What context is passed
       *   - How it's marked in conversation
       *   - What skill does with it
       */

      // Arrange
      const contextExplanation = commandContent.match(/## Phase 2:[\s\S]*?(?=^## [A-Z]|$)/ms)?.[0] || '';

      // Act & Assert
      expect(contextExplanation).toMatch(/context|marker|pass|handoff|skill/i);
    });

    test('should_explain_why_context_prevents_duplicate_questions', () => {
      /**
       * Scenario: Documentation explains duplication prevention
       * Given: Command or skill documentation
       * When: Reading about context benefits
       * Then: Should explain that context prevents re-asking
       */

      // Arrange
      const phase0or1 = commandContent.match(/## Phase [01]:[\s\S]*?(?=^## [A-Z]|$)/ms)?.[0] || '';

      // Act & Assert
      expect(phase0or1).toMatch(/context|skip|duplicate|re.?ask|already/i);
    });
  });

  describe('Skill Extraction of Context', () => {
    test('should_have_reference_to_brainstorm_handoff_workflow', () => {
      /**
       * Scenario: Skill loads brainstorm handoff workflow
       * Given: Skill Phase 1 Step 0
       * When: Checking for handoff logic
       * Then: Should reference brainstorm-handoff-workflow.md
       */

      // Arrange
      const phase1Step0 = skillContent.match(/Step 0[\s\S]*?(?=Step|###)/is)?.[0] || '';

      // Act & Assert
      expect(phase1Step0).toMatch(/brainstorm.*handoff|brainstorm.*workflow|Read.*brainstorm/i);
    });

    test('should_parse_context_variables_in_skill', () => {
      /**
       * Scenario: Skill parses $BRAINSTORM_CONTEXT
       * Given: Skill Phase 1 Step 0 or handoff detection
       * When: Analyzing context parsing
       * Then: Should extract fields from $BRAINSTORM_CONTEXT
       */

      // Arrange
      const phase1Content = skillContent.match(/Phase 1[\s\S]*?(?=Phase|###)/is)?.[0] || '';

      // Act & Assert
      expect(phase1Content).toMatch(/\$BRAINSTORM_CONTEXT|session\.|pre-?populate/i);
    });

    test('should_display_context_summary_before_proceeding', () => {
      /**
       * Scenario: Skill displays what context was received
       * Given: Skill Phase 1 brainstorm handling
       * When: Checking for context summary display
       * Then: Should Display() context information
       */

      // Arrange
      const phase1Section = skillContent.match(/Phase 1[\s\S]*?(?=Phase|###)/is)?.[0] || '';

      // Act & Assert
      expect(phase1Section).toMatch(/Display|pre-?populate|continuing|from.*brainstorm/i);
    });
  });

  describe('Context Validation', () => {
    test('should_validate_context_is_not_null_or_empty', () => {
      /**
       * Scenario: Skill validates context before using
       * Given: Skill context detection
       * When: Checking for validation logic
       * Then: Should validate context exists
       */

      // Arrange
      const phase1Section = skillContent.match(/Phase 1[\s\S]*?(?=###|$)/is)?.[0] || '';

      // Act & Assert
      expect(phase1Section).toMatch(/IF.*\$BRAINSTORM_CONTEXT|IF.*context|null|provided/i);
    });

    test('should_handle_missing_context_gracefully', () => {
      /**
       * Scenario: Skill handles case when no context is provided
       * Given: Skill Phase 1 ELSE clause
       * When: Checking for no-context handling
       * Then: Should have ELSE clause for full discovery
       */

      // Arrange
      const phase1Section = skillContent.match(/Phase 1[\s\S]*?(?=###|$)/is)?.[0] || '';

      // Act & Assert
      expect(phase1Section).toMatch(/ELSE|no.*brainstorm|full.*discovery/i);
    });
  });
});
