"""
CLAUDE.md Markdown Section Parser Module

Parses CLAUDE.md into structured sections with preservation of exact content.
No whitespace normalization or reformatting.
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional


# Constants for section parsing
SECTION_HEADER_PATTERN = r'^(#{2,4})\s+(.+)$'
MIN_HEADER_LEVEL = 2
MAX_HEADER_LEVEL = 4
DEVFORGEAI_MARKER = 'DEVFORGEAI'


@dataclass
class Section:
    """Represents a markdown section (## Level 2 and below)."""
    name: str
    level: int  # 2 for ##, 3 for ###, 4 for ####
    content: str
    line_start: int
    line_end: int

    def is_user_section(self) -> bool:
        """Check if section is marked as user section (not DEVFORGEAI)."""
        return not self.content.startswith(f'<!-- {DEVFORGEAI_MARKER}')

    def is_devforgeai_section(self) -> bool:
        """Check if section is a DEVFORGEAI framework section."""
        return DEVFORGEAI_MARKER.lower() in self.name.lower() or self.content.startswith(f'<!-- {DEVFORGEAI_MARKER}')


def _is_section_header(line: str) -> Optional[tuple[int, str]]:
    """
    Check if line is a section header and extract level and name.

    Args:
        line: Line to check

    Returns:
        Tuple of (level, name) or None if not a header
    """
    match = re.match(SECTION_HEADER_PATTERN, line)
    if match:
        level = len(match.group(1))
        name = match.group(2).strip()
        return level, name
    return None


def _create_section(section_info: Dict, section_lines: List[str], start: int, end: int) -> Section:
    """
    Create a Section object from parsed data.

    Args:
        section_info: Dict with 'name' and 'level' keys
        section_lines: List of content lines
        start: Starting line number
        end: Ending line number

    Returns:
        Section object
    """
    content = '\n'.join(section_lines)
    return Section(
        name=section_info['name'],
        level=section_info['level'],
        content=content,
        line_start=start,
        line_end=end
    )


class CLAUDEmdParser:
    """Parses CLAUDE.md into sections with exact content preservation."""

    def __init__(self, content: str):
        """Initialize parser with CLAUDE.md content."""
        self.content = content
        self.lines = content.split('\n')
        self.sections: List[Section] = []
        self._parse_sections()

    def _parse_sections(self) -> None:
        """Parse content into sections based on ## headers."""
        current_section = None
        section_lines = []
        section_start = 0

        for i, line in enumerate(self.lines):
            # Check for section header
            header_info = _is_section_header(line)

            if header_info:
                # Save previous section if exists
                if current_section is not None:
                    section = _create_section(current_section, section_lines, section_start, i - 1)
                    self.sections.append(section)

                # Start new section
                level, name = header_info
                current_section = {'name': name, 'level': level}
                section_lines = [line]
                section_start = i
            elif current_section is not None:
                # Add line to current section
                section_lines.append(line)

        # Save last section
        if current_section is not None:
            section = _create_section(current_section, section_lines, section_start, len(self.lines) - 1)
            self.sections.append(section)

    def parse_sections(self, content: Optional[str] = None) -> List[Section]:
        """
        Parse content into sections.

        Args:
            content: Content to parse. If None, uses constructor content.

        Returns:
            List of Section objects.
        """
        if content is not None:
            self.content = content
            self.lines = content.split('\n')
            self.sections = []
            self._parse_sections()

        return self.sections

    def extract_user_sections(self) -> List[Section]:
        """
        Extract sections not marked with <!-- DEVFORGEAI -->.

        Returns:
            List of user-authored sections.
        """
        return [s for s in self.sections if s.is_user_section()]

    def extract_framework_sections(self) -> List[Section]:
        """
        Extract sections marked as DEVFORGEAI framework sections.

        Returns:
            List of framework sections.
        """
        return [s for s in self.sections if s.is_devforgeai_section()]

    def detect_section_nesting(self, content: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Detect hierarchy of sections (##, ###, ####).

        Returns:
            Dictionary mapping parent sections to subsections.
        """
        if content is not None:
            self.content = content
            self.lines = content.split('\n')

        hierarchy: Dict[str, List[str]] = {}
        current_level2: Optional[str] = None

        for line in self.lines:
            header_info = _is_section_header(line)
            if header_info:
                level, name = header_info

                if level == MIN_HEADER_LEVEL:
                    current_level2 = name
                    if name not in hierarchy:
                        hierarchy[name] = []
                elif level > MIN_HEADER_LEVEL and current_level2:
                    hierarchy[current_level2].append(name)

        return hierarchy

    def preserve_exact_content(self) -> str:
        """
        Reassemble content preserving exact formatting and whitespace.

        Returns:
            Content with sections reassembled exactly as parsed.
        """
        return '\n'.join(self.lines)

    def _mark_user_section(self, section_name: str) -> str:
        """
        Generate user section marker comment.

        Args:
            section_name: Name of the section

        Returns:
            HTML comment marker string
        """
        return f'<!-- USER_SECTION: {section_name} -->'

    def _is_user_section_header(self, section_name: str) -> bool:
        """
        Check if section header is a user section.

        Args:
            section_name: Section name to check

        Returns:
            True if user section, False if framework section
        """
        return not (DEVFORGEAI_MARKER in section_name or DEVFORGEAI_MARKER.lower() in section_name.lower())

    def add_user_section_markers(self, content: Optional[str] = None) -> str:
        """
        Add <!-- USER_SECTION: Name --> markers to user sections.

        Args:
            content: Content to mark. If None, uses constructor content.

        Returns:
            Content with user section markers added.
        """
        if content is not None:
            self.content = content
            self.lines = content.split('\n')

        marked_lines = []

        for line in self.lines:
            # Check if this is a section header
            header_info = _is_section_header(line)

            if header_info:
                _, section_name = header_info

                # Add marker for user sections
                if self._is_user_section_header(section_name):
                    marked_lines.append(self._mark_user_section(section_name))

            marked_lines.append(line)

        return '\n'.join(marked_lines)

    def get_section_by_name(self, name: str) -> Optional[Section]:
        """Get section by name."""
        for section in self.sections:
            if section.name == name:
                return section

        return None

    def get_parser_report(self) -> str:
        """
        Get report of parsed sections.

        Returns:
            Report string like "Detected N user sections (total M lines)".
        """
        user_sections = self.extract_user_sections()
        total_lines = len(self.lines)

        return f"Detected {len(user_sections)} user sections (total {total_lines} lines)"
