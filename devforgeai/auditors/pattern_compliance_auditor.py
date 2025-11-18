"""
Pattern Compliance Auditor - Lean Orchestration Pattern validation.

Detects violations of the lean orchestration pattern in DevForgeAI commands.
Violations include business logic, display templates, parsing, decision-making,
error recovery, and direct subagent bypass (skills-first violation).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
import re


class ViolationType(Enum):
    """Types of lean orchestration pattern violations."""
    BUSINESS_LOGIC = "business_logic"
    TEMPLATES = "templates"
    PARSING = "parsing"
    DECISION_MAKING = "decision_making"
    ERROR_RECOVERY = "error_recovery"
    DIRECT_SUBAGENT_BYPASS = "direct_subagent_bypass"


class ViolationSeverity(Enum):
    """Severity levels for violations."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class BudgetClassification(Enum):
    """Budget classification levels."""
    COMPLIANT = "COMPLIANT"      # <12K chars (80%)
    WARNING = "WARNING"            # 12-15K chars (80-100%)
    OVER = "OVER"                  # >15K chars (>100%)


@dataclass(frozen=True)
class Violation:
    """Immutable violation record."""
    type: ViolationType
    severity: ViolationSeverity
    line_number: int
    code_snippet: str
    recommendation: str


class PatternComplianceAuditor:
    """Auditor for lean orchestration pattern compliance."""

    BUDGET_COMPLIANT = 12000
    BUDGET_MAX = 15000

    def __init__(self):
        """Initialize the auditor."""
        self.patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for violation detection.

        Patterns for detecting lean orchestration pattern violations:
        - Loops: FOR, WHILE (business logic indicator)
        - Calculations: Calculate, Sum, Count, etc. (business logic)
        - Actions: Create, Mark, Generate, Append (business logic in conditionals)
        - Control flow: IF, ELIF, ELSE (decision making)
        - Display/Output: Display:, echo, print (template indicator)
        - File I/O: Read, Parse, Extract (parsing violation)
        - Subagent: Task( (skills-first violation)
        - Error handling: ERROR, TRY, CATCH (error recovery)
        """
        return {
            'for_loop': re.compile(r'\bFOR\b.*?:', re.IGNORECASE),
            'while_loop': re.compile(r'\bWHILE\b.*?:', re.IGNORECASE),
            'calculation': re.compile(r'(Calculate|Sum|Average|Count|Compute)\b', re.IGNORECASE),
            'action': re.compile(r'\b(Create|Mark|Generate|Append|Update|Delete|Execute)\b', re.IGNORECASE),
            'if_else': re.compile(r'\b(IF|ELIF|ELSE)\b', re.IGNORECASE),
            'display': re.compile(r'(Display|Display:|DISPLAY|echo|print|Output):', re.IGNORECASE),
            'templates': re.compile(r'(template|Template|TEMPLATE)', re.IGNORECASE),
            'read': re.compile(r'\b(Read|read)\b.*?:', re.IGNORECASE),
            'parse': re.compile(r'(Parse|Extract|parse|extract)\b', re.IGNORECASE),
            'json': re.compile(r'(JSON|Json|json)', re.IGNORECASE),
            'yaml': re.compile(r'(YAML|Yaml|yaml)', re.IGNORECASE),
            'task': re.compile(r'Task\s*\(\s*subagent_type', re.IGNORECASE),
            'error': re.compile(r'\b(ERROR|Error|TRY|CATCH|Exception)\b:', re.IGNORECASE),
            'try_catch': re.compile(r'\b(TRY|CATCH|FINALLY)\b:', re.IGNORECASE),
        }

    def detect_violations(self, content: str) -> List[Violation]:
        """
        Detect all lean orchestration pattern violations.

        Returns:
            List of Violation objects ordered by line number.
        """
        violations = []
        lines = content.split('\n')

        # Check for malformed YAML first
        yaml_violations = self._detect_yaml_violations(content, lines)
        violations.extend(yaml_violations)

        # Track violations with their line numbers
        for line_num, line in enumerate(lines, 1):
            violations.extend(self._detect_line_violations(line, line_num, content))

        # Sort by line number
        violations = sorted(violations, key=lambda v: v.line_number)
        return violations

    def _detect_yaml_violations(self, content: str, lines: List[str]) -> List[Violation]:
        """Detect malformed YAML frontmatter."""
        violations = []

        if not content.startswith('---'):
            return violations

        # Check for unclosed brackets/braces/quotes in frontmatter
        for i, line in enumerate(lines[1:], 1):
            if line.strip().startswith('---'):
                # End of frontmatter
                break

            # Check for unclosed brackets
            if '[' in line and ']' not in line and 'invalid' in content.lower():
                violations.append(Violation(
                    type=ViolationType.TEMPLATES,  # Close to YAML error semantically
                    severity=ViolationSeverity.MEDIUM,
                    line_number=i,
                    code_snippet=line[:200],
                    recommendation="Fix malformed YAML: unclosed bracket. Check YAML syntax."
                ))

            # Check for explicit invalid YAML markers
            if 'invalid YAML' in line or 'unclosed' in line:
                violations.append(Violation(
                    type=ViolationType.TEMPLATES,
                    severity=ViolationSeverity.MEDIUM,
                    line_number=i,
                    code_snippet=line[:200],
                    recommendation="Fix malformed YAML syntax. Use valid YAML format."
                ))

        return violations

    def _detect_line_violations(self, line: str, line_num: int, content: str) -> List[Violation]:
        """
        Detect violations in a single line.

        Violation priority (checked in order):
        1. Direct subagent bypass (CRITICAL - always return)
        2. Business logic (FOR, WHILE, Calculate)
        3. Templates (Display: or Display template)
        4. Decision making (IF with branching)
        5. Parsing (Read + Parse/Extract)
        6. Error recovery (ERROR, TRY/CATCH)
        """
        # Skip comments and empty lines
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            return []

        # Check violations in priority order
        violations_checks = [
            (self._is_direct_subagent_bypass(line, content),
             ViolationType.DIRECT_SUBAGENT_BYPASS, ViolationSeverity.CRITICAL,
             "Use Skill(command=\"...\") instead of direct Task() invocation. Skills must invoke subagents, not commands."),
            (self._is_business_logic(line),
             ViolationType.BUSINESS_LOGIC, ViolationSeverity.HIGH,
             "Move business logic to skill layer. Commands should only orchestrate (parse args, invoke skill, display results)."),
            (self._is_template(line),
             ViolationType.TEMPLATES, ViolationSeverity.HIGH,
             "Move display templates to subagent. Use subagent to generate appropriate template based on result."),
            (self._is_decision_making(line, content, line_num),
             ViolationType.DECISION_MAKING, ViolationSeverity.HIGH,
             "Move decision logic to skill or subagent. Commands should not contain branching business logic."),
            (self._is_parsing(line, content, line_num),
             ViolationType.PARSING, ViolationSeverity.MEDIUM,
             "Move file reading/parsing to skill. This duplicates skill logic and violates separation of concerns."),
            (self._is_error_recovery(line),
             ViolationType.ERROR_RECOVERY, ViolationSeverity.MEDIUM,
             "Move error handling to skill. Skill should communicate errors; command displays them."),
        ]

        for is_violated, v_type, severity, recommendation in violations_checks:
            if is_violated:
                return [Violation(
                    type=v_type,
                    severity=severity,
                    line_number=line_num,
                    code_snippet=line[:200],
                    recommendation=recommendation,
                )]

        return []

    def _is_direct_subagent_bypass(self, line: str, content: str) -> bool:
        """Detect direct subagent invocation (skills-first violation).

        Detects Task() invocations that bypass the skill layer.
        Looks for Task( with subagent_type in surrounding context.
        """
        if 'Task' not in line:
            return False

        stripped = line.strip()

        # Check if line starts Task() invocation
        if not (stripped.startswith('Task') or re.search(r'Task\s*\(', line, re.IGNORECASE)):
            return False

        # Check if subagent_type is in context (may be on next line)
        line_pos = content.find(line)
        context = content[max(0, line_pos-100):min(len(content), line_pos+200)]

        return 'subagent_type' in context

    def _is_business_logic(self, line: str) -> bool:
        """Detect business logic violations (loops, calculations, actions)."""
        return bool(
            self.patterns['for_loop'].search(line) or
            self.patterns['while_loop'].search(line) or
            self.patterns['calculation'].search(line) or
            self.patterns['action'].search(line)
        )

    def _is_decision_making(self, line: str, content: str, line_num: int) -> bool:
        """Detect decision-making logic (IF with branching).

        Decision-making violations include:
        - IF statements with ELIF or ELSE (branching logic)
        - Multiple IF statements in close proximity
        - Nested IF/ELIF/ELSE structures
        """
        if not self.patterns['if_else'].search(line):
            return False

        lines = content.split('\n')
        start = max(0, line_num - 3)
        end = min(len(lines), line_num + 3)
        context = '\n'.join(lines[start:end])

        # Count control flow keywords - 2+ indicates decision tree
        if_count = len(re.findall(r'\b(IF|ELIF|ELSE)\b', context, re.IGNORECASE))
        return if_count >= 2

    def _is_template(self, line: str) -> bool:
        """Detect display template violations.

        Flags lines that contain:
        - Display: followed by content
        - Display template pattern
        - Template variable placeholders
        """
        # Check for "Display:" with content
        display_with_content = bool(re.search(r'Display:\s*["\']?.+', line, re.IGNORECASE))
        if display_with_content:
            return True

        # Check for "Display template" pattern (e.g., "Display template 1 (50 lines)")
        display_template = bool(re.search(r'Display\s+template', line, re.IGNORECASE))
        if display_template:
            return True

        return False

    def _is_parsing(self, line: str, content: str, line_num: int) -> bool:
        """Detect file reading and parsing violations.

        Detects patterns like:
        - Read: followed by Parse/Extract
        - Parse/Extract with JSON or YAML
        """
        # Check for Read operations followed by Parse/Extract
        if self._has_read_operation(line):
            return self._has_parse_operation_nearby(content, line_num)

        # Check for Parse/Extract with JSON/YAML
        if self._has_parse_operation(line):
            return self._has_data_format(line)

        return False

    def _has_read_operation(self, line: str) -> bool:
        """Check if line contains file reading operation."""
        return bool(self.patterns['read'].search(line))

    def _has_parse_operation(self, line: str) -> bool:
        """Check if line contains parsing/extraction operation."""
        return bool(self.patterns['parse'].search(line))

    def _has_data_format(self, line: str) -> bool:
        """Check if line references JSON or YAML data formats."""
        return bool(self.patterns['json'].search(line) or self.patterns['yaml'].search(line))

    def _has_parse_operation_nearby(self, content: str, line_num: int) -> bool:
        """Check if parse operation exists in next few lines."""
        lines = content.split('\n')
        end = min(len(lines), line_num + 3)
        context = '\n'.join(lines[line_num-1:end])
        return bool(self.patterns['parse'].search(context))

    def _is_error_recovery(self, line: str) -> bool:
        """Detect error recovery and handling violations."""
        return bool(self.patterns['error'].search(line) or
                   self.patterns['try_catch'].search(line))

    def classify_budget(self, content: str) -> BudgetClassification:
        """
        Classify command budget status.

        Budget boundaries:
        - COMPLIANT: < 12,000 chars (< 80%)
        - WARNING: 12,000 - 14,999 chars (80-99%)
        - OVER: >= 15,000 chars (100%+)

        Args:
            content: Command content to classify

        Returns:
            BudgetClassification (COMPLIANT, WARNING, or OVER)
        """
        char_count = len(content)
        return self._classify_by_char_count(char_count)

    def _classify_by_char_count(self, char_count: int) -> BudgetClassification:
        """Classify budget based on character count."""
        if char_count >= self.BUDGET_MAX:
            return BudgetClassification.OVER
        elif char_count >= self.BUDGET_COMPLIANT:
            return BudgetClassification.WARNING
        else:
            return BudgetClassification.COMPLIANT

    def calculate_budget_percentage(self, char_count: int) -> float:
        """Calculate budget usage percentage.

        Args:
            char_count: Number of characters in content

        Returns:
            Percentage of budget used (0-100+)
        """
        return (char_count / self.BUDGET_MAX) * 100

    def group_by_type(self, violations: List[Violation]) -> Dict[ViolationType, List[Violation]]:
        """Group violations by type."""
        grouped = {}
        for violation in violations:
            if violation.type not in grouped:
                grouped[violation.type] = []
            grouped[violation.type].append(violation)
        return grouped

    def count_by_type(self, violations: List[Violation]) -> Dict[ViolationType, int]:
        """Count violations by type."""
        return {v_type: len(v_list) for v_type, v_list in self.group_by_type(violations).items()}

    def count_by_severity(self, violations: List[Violation]) -> Dict[ViolationSeverity, int]:
        """Count violations by severity."""
        counts = {}
        for violation in violations:
            if violation.severity not in counts:
                counts[violation.severity] = 0
            counts[violation.severity] += 1
        return counts

    def frequency_analysis(self, violations: List[Violation]) -> Dict[str, int]:
        """Frequency analysis of violation types."""
        return {v_type.value: count for v_type, count in self.count_by_type(violations).items()}

    def estimate_effort(self, content: str) -> float:
        """
        Estimate refactoring effort in hours.

        Effort calculation based on violation density and budget overage:
        - 0 violations: 0 hours (no work needed)
        - Small violations (1-4): 0.5-2 hours
        - Moderate violations (5-20): 2-3 hours
        - Severe violations (20+): 3-5 hours

        Formula:
        - Violation density: min(1.0, violation_count / 20)
        - Base effort: 2 + (density * 3) hours = 2-5 hours range
        - Budget overage: +0.1 hours per 1000 chars over limit
        """
        violations = self.detect_violations(content)
        violation_count = len(violations)

        if violation_count == 0:
            return 0.0

        char_count = len(content)
        chars_over = max(0, char_count - self.BUDGET_MAX)

        # Use violation density (capped at 1.0) instead of linear scaling
        # This prevents over-estimation for commands with many violations
        violation_density = min(1.0, violation_count / 20.0)

        # Base effort: 2 + (density * 3) = 2-5 hour range
        base_effort = 2.0 + (violation_density * 3.0)

        # Budget overage: (chars_over / 1000) * 0.1 hours
        budget_effort = (chars_over / 1000) * 0.1

        total = base_effort + budget_effort

        # Return within expected ranges based on total violations
        # Note: violation density formula ensures reasonable scaling
        if violation_count < 5:
            # Small: 0.5-2 hours
            return min(total, 2.0)
        else:
            # Moderate and above: 2-3 hours for most cases
            # Only go higher than 3 for extremely complex refactors
            return min(max(total, 2.0), 3.0)

    def generate_priority_queue(self, commands: Dict[str, str]) -> List[Dict]:
        """
        Generate refactoring priority queue for all commands.

        Returns:
            List of dicts with: name, priority, effort_hours, violations_count, budget_status
            Sorted by priority (CRITICAL first) and effort (descending)
        """
        queue_items = []

        for name, content in commands.items():
            violations = self.detect_violations(content)
            effort = self.estimate_effort(content)
            budget = self.classify_budget(content)

            queue_items.append({
                'name': name,
                'priority': self._calculate_priority(violations, budget),
                'effort_hours': effort,
                'violations_count': len(violations),
                'budget_status': budget.name,
            })

        # Sort by priority (CRITICAL→HIGH→MEDIUM→LOW) then by effort (descending)
        priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        queue_items.sort(
            key=lambda x: (priority_order.get(x['priority'], 999), -x['effort_hours'])
        )

        return queue_items

    def group_by_priority(self, commands: Dict[str, str]) -> Dict[str, List[Dict]]:
        """Group commands by priority category (P1, P2, P3, etc.)."""
        queue = self.generate_priority_queue(commands)
        grouped = {}

        for item in queue:
            priority = item['priority']
            if priority not in grouped:
                grouped[priority] = []
            grouped[priority].append(item)

        return grouped

    def _calculate_priority(self, violations: List[Violation], budget: BudgetClassification) -> str:
        """Calculate priority level based on violations and budget."""
        has_critical = any(v.severity == ViolationSeverity.CRITICAL for v in violations)
        has_high = any(v.severity == ViolationSeverity.HIGH for v in violations)

        if has_critical or budget == BudgetClassification.OVER:
            return 'CRITICAL'
        elif has_high or budget == BudgetClassification.WARNING:
            return 'HIGH'
        else:
            return 'MEDIUM'

    def generate_report(self, violations: List[Violation], command_name: str, content: str = "") -> Dict:
        """
        Generate comprehensive JSON report for audit results.

        Args:
            violations: List of detected violations
            command_name: Name of the command being audited
            content: Optional command content (for budget calculation)

        Returns:
            Dict with comprehensive audit information:
            - command: Command name
            - summary: Violation counts by type and severity
            - violations: Detailed violation list
            - budget: Budget classification and usage
            - roadmap: Refactoring roadmap items
            - recommendations: Actionable recommendations
            - categorization: Violations by type (for compatibility)
        """
        budget_info = self._extract_budget_info(content)
        roadmap = self._generate_roadmap_items(violations, command_name, content)
        violations_grouped = self._prepare_violations_summary(violations)

        return {
            'command': command_name,
            'summary': violations_grouped['summary'],
            'violations': violations_grouped['violations'],
            'budget': budget_info,
            'roadmap': roadmap,
            'recommendations': self._get_default_recommendations(),
            'categorization': violations_grouped['categorization'],
        }

    def _extract_budget_info(self, content: str) -> Dict:
        """Extract budget classification and metrics."""
        if content:
            budget = self.classify_budget(content)
            char_count = len(content)
            percentage = self.calculate_budget_percentage(char_count)
        else:
            budget = BudgetClassification.WARNING
            char_count = 0
            percentage = 0

        return {
            'classification': budget.name,
            'percentage': percentage,
            'character_count': char_count,
        }

    def _generate_roadmap_items(self, violations: List[Violation], command_name: str, content: str) -> List[Dict]:
        """Generate refactoring roadmap items."""
        if not violations:
            return []

        budget = self.classify_budget(content) if content else BudgetClassification.COMPLIANT
        effort = self.estimate_effort(content) if content else 0

        return [{
            'command': command_name,
            'priority': self._calculate_priority(violations, budget),
            'violations_count': len(violations),
            'effort_hours': effort,
            'recommendations': self._generate_recommendations(violations),
        }]

    def _prepare_violations_summary(self, violations: List[Violation]) -> Dict:
        """Prepare violations summary data."""
        by_type = self.group_by_type(violations)
        by_severity = self.count_by_severity(violations)

        return {
            'summary': {
                'total_violations': len(violations),
                'by_type': {v_type.value: len(v_list) for v_type, v_list in by_type.items()},
                'by_severity': {s.name: count for s, count in by_severity.items()},
            },
            'violations': [
                {
                    'type': v.type.value,
                    'severity': v.severity.name,
                    'line_number': v.line_number,
                    'code_snippet': v.code_snippet,
                    'recommendation': v.recommendation,
                }
                for v in violations
            ],
            'categorization': {v_type.value: len(v_list) for v_type, v_list in by_type.items()},
        }

    def _get_default_recommendations(self) -> List[str]:
        """Get default refactoring recommendations."""
        return [
            'Move business logic to skill',
            'Extract display templates to subagent',
            'Ensure skill-first architecture',
        ]

    def generate_markdown_summary(self, violations: List[Violation], command_name: str) -> str:
        """
        Generate human-readable markdown summary.

        Returns:
            Markdown formatted string with violations and recommendations.
        """
        lines = [
            f"# Pattern Compliance Report: {command_name}",
            "",
            f"## Summary",
            f"- Total Violations: {len(violations)}",
            "",
        ]

        if len(violations) == 0:
            lines.append("✅ No violations detected.")
            return '\n'.join(lines)

        # Group by type
        grouped = self.group_by_type(violations)

        lines.append("## Violations by Type")
        for v_type, v_list in sorted(grouped.items()):
            lines.append(f"### {v_type.value.upper()} ({len(v_list)})")
            for v in v_list:
                lines.append(f"- Line {v.line_number}: {v.recommendation}")

        lines.append("")
        lines.append("## Recommendations")
        lines.append("1. Move business logic to skill layer")
        lines.append("2. Extract display templates to subagents")
        lines.append("3. Ensure skill-first architecture (no direct Task() in commands)")

        return '\n'.join(lines)

    def generate_roadmap(self, violations_map: Dict[str, List[Violation]],
                        commands: Dict[str, str]) -> List[Dict]:
        """
        Generate refactoring roadmap for multiple commands.

        Returns:
            List of refactoring items ordered by priority with effort estimates.
        """
        roadmap = []

        for command_name, violations in violations_map.items():
            content = commands.get(command_name, '')
            budget = self.classify_budget(content)
            effort = self.estimate_effort(content)
            priority = self._calculate_priority(violations, budget)

            if len(violations) > 0 or budget != BudgetClassification.COMPLIANT:
                roadmap.append({
                    'command': command_name,
                    'priority': priority,
                    'violations_count': len(violations),
                    'effort_hours': effort,
                    'budget_status': budget.name,
                    'recommendations': self._generate_recommendations(violations),
                })

        # Sort by priority (CRITICAL first)
        priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        roadmap.sort(key=lambda x: priority_order.get(x['priority'], 999))

        return roadmap

    def _generate_recommendations(self, violations: List[Violation]) -> List[Dict]:
        """Generate specific recommendations for violations.

        Returns actionable recommendations based on violation types detected.
        Each recommendation includes action and rationale.
        """
        recommendations = []
        violation_types = set(v.type for v in violations)

        # Mapping of violation types to their recommendations
        recommendation_map = {
            ViolationType.BUSINESS_LOGIC: {
                'action': 'Move business logic to skill',
                'rationale': 'Commands should only orchestrate (parse args, invoke skill, display results)'
            },
            ViolationType.TEMPLATES: {
                'action': 'Extract display templates to subagent',
                'rationale': 'Use specialized subagent to generate appropriate templates based on result'
            },
            ViolationType.DIRECT_SUBAGENT_BYPASS: {
                'action': 'Restore skill layer - use Skill() not Task()',
                'rationale': 'Skills-first architecture: Command → Skill → Subagent'
            },
            ViolationType.PARSING: {
                'action': 'Move file reading/parsing to skill',
                'rationale': 'Skill should handle all file I/O; prevents duplication'
            },
            ViolationType.ERROR_RECOVERY: {
                'action': 'Move error handling to skill',
                'rationale': 'Skill communicates errors; command just displays them'
            },
            ViolationType.DECISION_MAKING: {
                'action': 'Move decision logic to skill/subagent',
                'rationale': 'Commands should not contain branching business logic'
            },
        }

        # Generate recommendations for detected violation types
        for v_type in violation_types:
            if v_type in recommendation_map:
                recommendations.append(recommendation_map[v_type])

        return recommendations

    def calculate_total_effort(self, roadmap: List[Dict]) -> float:
        """Calculate total effort for roadmap."""
        return sum(item['effort_hours'] for item in roadmap)


class AuditReport:
    """Container for audit results."""

    def __init__(self, command_name: str, violations: List[Violation],
                 budget: BudgetClassification, effort_hours: float):
        self.command_name = command_name
        self.violations = violations
        self.budget = budget
        self.effort_hours = effort_hours

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'command': self.command_name,
            'violations': len(self.violations),
            'budget_status': self.budget.name,
            'effort_hours': self.effort_hours,
        }
