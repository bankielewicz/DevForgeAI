/**
 * STORY-141: Question Duplication Elimination
 * AC#3: Skill Owns Question Templates
 *
 * Acceptance Criteria:
 * - Question templates in skill reference files (discovery-workflow.md, requirements-elicitation-workflow.md)
 * - Command does NOT contain question templates (except brainstorm selection)
 * - All question templates are well-formatted and complete
 *
 * Test Requirements:
 * - Verify question templates in skill references
 * - Verify command has no question templates (grep for AskUserQuestion patterns)
 * - Verify templates are complete and well-formatted
 */

const fs = require('fs');
const path = require('path');

describe('STORY-141: AC#3 - Skill Owns Question Templates', () => {
  const commandFilePath = path.resolve(__dirname, '../../.claude/commands/ideate.md');
  const discoveryWorkflowPath = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/references/discovery-workflow.md');
  const requirementsElicitationPath = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/references/requirements-elicitation-workflow.md');
  const skillFilePath = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/SKILL.md');
  const referencesDir = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/references');

  let commandContent;
  let discoveryContent;
  let requirementsContent;
  let skillContent;
  let referenceFiles;

  beforeAll(() => {
    commandContent = fs.readFileSync(commandFilePath, 'utf8');
    discoveryContent = fs.readFileSync(discoveryWorkflowPath, 'utf8');
    requirementsContent = fs.readFileSync(requirementsElicitationPath, 'utf8');
    skillContent = fs.readFileSync(skillFilePath, 'utf8');
    referenceFiles = fs.readdirSync(referencesDir).filter(f => f.endsWith('.md'));
  });

  describe('Question Templates in Skill References', () => {
    test('should_have_discovery_workflow_reference_file', () => {
      /**
       * Scenario: Discovery workflow reference exists
       * Given: Skill references directory
       * When: Checking for discovery-workflow.md
       * Then: File should exist and contain discovery questions
       */

      // Arrange
      const discoveryWorkflowFile = path.resolve(referencesDir, 'discovery-workflow.md');

      // Act
      const fileExists = fs.existsSync(discoveryWorkflowFile);

      // Assert
      expect(fileExists).toBe(true);
      expect(discoveryContent.length).toBeGreaterThan(100);
    });

    test('should_have_requirements_elicitation_reference_file', () => {
      /**
       * Scenario: Requirements elicitation reference exists
       * Given: Skill references directory
       * When: Checking for requirements-elicitation-workflow.md
       * Then: File should exist and contain elicitation questions
       */

      // Arrange
      const requirementsElicitationFile = path.resolve(referencesDir, 'requirements-elicitation-workflow.md');

      // Act
      const fileExists = fs.existsSync(requirementsElicitationFile);

      // Assert
      expect(fileExists).toBe(true);
      expect(requirementsContent.length).toBeGreaterThan(100);
    });

    test('should_have_discovery_questions_in_discovery_workflow', () => {
      /**
       * Scenario: Discovery workflow contains discovery questions
       * Given: discovery-workflow.md content
       * When: Searching for question patterns
       * Then: Should contain AskUserQuestion patterns for discovery
       */

      // Arrange
      const discoveryQuestionPatterns = [
        /project\s+type|greenfield|brownfield/i,
        /domain|problem\s+space|scope/i,
        /success.*criteria|goal|objective/i
      ];

      // Act & Assert
      for (const pattern of discoveryQuestionPatterns) {
        expect(discoveryContent).toMatch(pattern);
      }

      // Should have AskUserQuestion invocations
      expect(discoveryContent).toMatch(/AskUserQuestion/);
    });

    test('should_have_requirements_questions_in_requirements_elicitation', () => {
      /**
       * Scenario: Requirements elicitation contains requirement questions
       * Given: requirements-elicitation-workflow.md content
       * When: Searching for question patterns
       * Then: Should contain AskUserQuestion patterns for requirements
       */

      // Arrange
      const requirementQuestionPatterns = [
        /functional.*requirement|user.*story/i,
        /data.*model|entity|relationship/i,
        /integration|external|api/i,
        /non.?functional|performance|security/i
      ];

      // Act & Assert
      for (const pattern of requirementQuestionPatterns) {
        expect(requirementsContent).toMatch(pattern);
      }

      // Should have AskUserQuestion invocations
      expect(requirementsContent).toMatch(/AskUserQuestion/);
    });

    test('should_have_well_formatted_question_templates_in_skill', () => {
      /**
       * Scenario: Question templates follow consistent format
       * Given: Skill reference files
       * When: Analyzing question format
       * Then: Should follow AskUserQuestion pattern with:
       *   - questions array
       *   - question property
       *   - options property (for choice questions)
       *   - header property
       */

      // Arrange
      const askUserQuestionPattern = /AskUserQuestion\s*\(\s*\{[\s\S]*?questions\s*:\s*\[[\s\S]*?\]\s*\}/g;

      // Act
      const discoveryMatches = (discoveryContent.match(askUserQuestionPattern) || []).length;
      const requirementsMatches = (requirementsContent.match(askUserQuestionPattern) || []).length;

      // Assert - Should have properly formatted questions
      expect(discoveryMatches + requirementsMatches).toBeGreaterThan(0);
    });
  });

  describe('Command Has No Question Templates', () => {
    test('should_NOT_contain_question_templates_in_command', () => {
      /**
       * Scenario: Command is free of question templates
       * Given: Command file content
       * When: Searching for discovery question templates
       * Then: Should NOT find question templates (except Phase 0 brainstorm)
       */

      // Arrange
      // Extract Phase 1 section (argument validation should NOT have questions)
      const phase1Section = commandContent.match(/## Phase 1:.*?(?=^## [A-Z]|^---)/ms)?.[0] || '';

      // Act - Check for discovery question patterns
      const discoveryQuestionPatterns = [
        /project\s+type.*question/i,
        /domain.*question/i,
        /complexity.*question/i,
        /functional.*requirement.*question/i,
        /What type of project/i,
        /What is your primary domain/i
      ];

      // Assert
      for (const pattern of discoveryQuestionPatterns) {
        expect(phase1Section).not.toMatch(pattern);
      }
    });

    test('should_only_have_brainstorm_template_in_command_phase_0', () => {
      /**
       * Scenario: Command Phase 0 only has brainstorm selection template
       * Given: Command Phase 0 section
       * When: Analyzing AskUserQuestion content
       * Then: Should only find brainstorm-related question
       */

      // Arrange
      const phase0Section = commandContent.match(/## Phase 0:.*?(?=^## [A-Z]|^---)/ms)?.[0] || '';

      // Act - Find AskUserQuestion in Phase 0
      const askUserMatches = phase0Section.match(/AskUserQuestion[\s\S]*?\}\s*\)/g) || [];

      // Assert
      if (askUserMatches.length > 0) {
        // Check that it's about brainstorm
        expect(phase0Section).toMatch(/brainstorm|existing/i);

        // Should NOT be about discovery
        expect(phase0Section).not.toMatch(/project\s+type|domain|complexity/i);
      }
    });

    test('should_NOT_duplicate_brainstorm_template_in_skill', () => {
      /**
       * Scenario: Brainstorm question is NOT duplicated in skill
       * Given: Skill and command files
       * When: Searching for brainstorm selection question
       * Then: Should be in command Phase 0 only, not in skill Phase 1
       */

      // Arrange
      const phase0Brainstorm = commandContent.match(/## Phase 0:[\s\S]*?(?=^## Phase|^---)/im)?.[0] || '';
      const phase1Skill = skillContent.match(/### Phase 1[\s\S]*?(?=### Phase|$)/im)?.[0] || '';

      // Act - Extract brainstorm question from command Phase 0
      const brainstormQuestion = phase0Brainstorm.match(/AskUserQuestion[\s\S]*?\}\s*\)/)?.[0] || '';

      // Assert - Skill's Phase 1 should not have the same brainstorm selection question
      // (Skill has other discovery questions, but not brainstorm selection)
      expect(phase1Skill).not.toMatch(/Would you like to use an existing brainstorm/i);
    });

    test('should_NOT_have_unused_question_templates', () => {
      /**
       * Scenario: No orphaned or unused question templates in command
       * Given: Command AskUserQuestion invocations
       * When: Analyzing each invocation
       * Then: Each should be used, not commented out or orphaned
       */

      // Arrange
      const askUserMatches = commandContent.match(/AskUserQuestion\s*\(/g) || [];

      // Act
      // Check if any are commented out
      const commentedOut = commandContent.match(/\/\/.*AskUserQuestion|#.*AskUserQuestion/g) || [];

      // Assert
      expect(commentedOut.length).toBe(0); // No commented out questions
      expect(askUserMatches.length).toBeGreaterThan(0); // But have some questions
    });
  });

  describe('Template Quality and Completeness', () => {
    test('should_have_complete_discovery_question_template_structure', () => {
      /**
       * Scenario: Discovery questions have complete structure
       * Given: Discovery workflow reference
       * When: Analyzing question structure
       * Then: Should have:
       *   - question property (the question text)
       *   - header property (category)
       *   - options array (for choice questions)
       */

      // Arrange
      const questionStructure = /question\s*:|header\s*:|options\s*:/g;

      // Act
      const matches = discoveryContent.match(questionStructure) || [];

      // Assert
      expect(matches.length).toBeGreaterThan(0);
    });

    test('should_have_complete_requirements_question_template_structure', () => {
      /**
       * Scenario: Requirements questions have complete structure
       * Given: Requirements elicitation workflow reference
       * When: Analyzing question structure
       * Then: Should have proper formatting
       */

      // Arrange
      const questionStructure = /question\s*:|header\s*:/g;

      // Act
      const matches = requirementsContent.match(questionStructure) || [];

      // Assert
      expect(matches.length).toBeGreaterThan(0);
    });

    test('should_have_question_descriptions_not_just_names', () => {
      /**
       * Scenario: Questions have helpful descriptions
       * Given: Question templates
       * When: Analyzing question details
       * Then: Should have descriptions explaining context
       */

      // Arrange
      // Look for question blocks with description-like content
      const descriptionPatterns = [
        /description\s*:|why\s+this/i,
        /context\s*:/i,
        /helps\s+us|helps\s+determine/i
      ];

      // Act & Assert
      const hasDescriptions = descriptionPatterns.some(p => discoveryContent.match(p));
      expect(hasDescriptions).toBe(true);
    });

    test('should_have_multi_option_questions_where_appropriate', () => {
      /**
       * Scenario: Choice questions provide options
       * Given: Question templates
       * When: Checking for choice questions
       * Then: Should have options array with multiple choices
       */

      // Arrange
      const multiOptionPattern = /options\s*:\s*\[[\s\S]*?\{[\s\S]*?\}/;

      // Act
      const discoveryHasOptions = multiOptionPattern.test(discoveryContent);

      // Assert
      expect(discoveryHasOptions).toBe(true);
    });

    test('should_reference_templates_from_skill', () => {
      /**
       * Scenario: Skill explicitly loads template references
       * Given: Skill SKILL.md
       * When: Searching for template loading
       * Then: Should have Read() calls for reference files
       */

      // Arrange
      const templateReferencePatterns = [
        /Read.*discovery-workflow/i,
        /Read.*requirements-elicitation/i,
        /references.*workflow/i
      ];

      // Act & Assert
      const hasReferences = templateReferencePatterns.some(p => skillContent.match(p));
      expect(hasReferences).toBe(true);
    });
  });

  describe('Reference File Organization', () => {
    test('should_have_required_reference_files', () => {
      /**
       * Scenario: All required reference files exist
       * Given: Skill references directory
       * When: Listing reference files
       * Then: Should have at minimum:
       *   - discovery-workflow.md
       *   - requirements-elicitation-workflow.md
       */

      // Arrange
      const requiredFiles = [
        'discovery-workflow.md',
        'requirements-elicitation-workflow.md'
      ];

      // Act & Assert
      for (const requiredFile of requiredFiles) {
        expect(referenceFiles).toContain(requiredFile);
      }
    });

    test('should_have_clear_file_naming_for_question_ownership', () => {
      /**
       * Scenario: File names clearly indicate ownership and purpose
       * Given: Reference file names
       * When: Analyzing names
       * Then: Should clearly indicate they're for ideation/discovery
       */

      // Arrange
      const skillReferenceFiles = [
        'discovery-workflow.md',
        'requirements-elicitation-workflow.md',
        'complexity-assessment-workflow.md',
        'feasibility-analysis-workflow.md'
      ];

      // Act & Assert - Check at least discovery files exist
      expect(referenceFiles).toContain('discovery-workflow.md');
      expect(referenceFiles).toContain('requirements-elicitation-workflow.md');
    });

    test('should_NOT_have_question_templates_in_command_file', () => {
      /**
       * Scenario: Command file contains no question files/templates
       * Given: Command directory structure
       * When: Checking for embedded question files
       * Then: Should NOT have question definition files in command directory
       */

      // Arrange
      const commandDir = path.resolve(__dirname, '../../.claude/commands');
      const commandDirFiles = fs.existsSync(commandDir)
        ? fs.readdirSync(commandDir).filter(f => f.includes('question') || f.includes('discovery'))
        : [];

      // Act & Assert
      expect(commandDirFiles.length).toBe(0);
    });

    test('should_have_all_workflow_references_in_skill_references_only', () => {
      /**
       * Scenario: All workflow reference files are in skill/references only
       * Given: Skill directory structure
       * When: Checking reference file locations
       * Then: All workflow files should be in .claude/skills/devforgeai-ideation/references/
       */

      // Arrange
      const skillReferencesDir = path.resolve(__dirname, '../../.claude/skills/devforgeai-ideation/references');

      // Act - Check that files exist in skill references
      const discoveryExists = fs.existsSync(path.join(skillReferencesDir, 'discovery-workflow.md'));
      const requirementsExists = fs.existsSync(path.join(skillReferencesDir, 'requirements-elicitation-workflow.md'));

      // Assert
      expect(discoveryExists).toBe(true);
      expect(requirementsExists).toBe(true);
    });
  });

  describe('Cross-Reference Integrity', () => {
    test('should_have_discovery_workflow_referenced_in_skill', () => {
      /**
       * Scenario: Skill Phase 1 references discovery-workflow.md
       * Given: Skill SKILL.md content
       * When: Searching for reference
       * Then: Should have explicit reference to load discovery-workflow.md
       */

      // Arrange
      const phase1Section = skillContent.match(/Phase 1.*?(?=###|$)/is)?.[0] || '';

      // Act & Assert
      expect(phase1Section).toMatch(/discovery-workflow/i);
    });

    test('should_have_requirements_elicitation_referenced_in_skill', () => {
      /**
       * Scenario: Skill Phase 2 references requirements-elicitation-workflow.md
       * Given: Skill SKILL.md content
       * When: Searching for reference
       * Then: Should have explicit reference to load requirements-elicitation-workflow.md
       */

      // Arrange
      const phase2Section = skillContent.match(/Phase 2.*?(?=###|$)/is)?.[0] || '';

      // Act & Assert
      expect(phase2Section).toMatch(/requirements-elicitation/i);
    });

    test('should_NOT_have_template_references_in_command', () => {
      /**
       * Scenario: Command doesn't load template reference files
       * Given: Command file
       * When: Searching for template file references
       * Then: Should NOT have Read() calls for question templates
       */

      // Arrange
      const templateReferences = [
        /Read.*discovery-workflow/i,
        /Read.*requirements-elicitation/i,
        /Read.*complexity-assessment/i
      ];

      // Act & Assert
      for (const ref of templateReferences) {
        expect(commandContent).not.toMatch(ref);
      }
    });
  });
});
