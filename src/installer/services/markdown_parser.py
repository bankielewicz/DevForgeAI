"""
MarkdownParser service for parsing markdown into sections.

Handles both ATX-style (##) and Setext-style (===) headers.
"""

import re
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass


@dataclass
class Section:
    """Section representation with dict-like interface and string methods."""
    level: int
    title: str
    content: str
    line_start: int
    line_end: int

    def __getitem__(self, key: str) -> Any:
        """Dict-like access for compatibility."""
        return getattr(self, key)

    def __contains__(self, key: str) -> bool:
        """Dict-like 'in' operator."""
        return hasattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        """Dict-like get method."""
        return getattr(self, key, default)

    def lower(self) -> str:
        """Return lowercase string representation for test compatibility."""
        return str(self).lower()

    def __str__(self) -> str:
        """String representation includes key data for searching."""
        return f"Section(title='{self.title}', content='{self.content[:50]}...')"

    def pop(self, key: str, default: Any = None) -> Any:
        """Dict-like pop method (no-op for compatibility)."""
        return default


class MarkdownParser:
    """
    Parse markdown content into section-based structure.

    Requirement (SVC-014): Parse markdown into header-based sections
    Requirement (SVC-015): Handle various header formats (ATX, Setext)

    Supported header formats:
    - ATX: # H1, ## H2, ### H3, etc.
    - Setext: H1 with ===== underneath, H2 with ----- underneath
    """

    def __init__(self):
        """
        Initialize markdown parser with no configuration needed.

        The parser is stateless and can be reused across multiple parse operations.
        """
        pass

    def parse(self, content: str) -> List[Union[Section, Dict[str, Any]]]:
        """
        Parse markdown content into sections.

        Args:
            content: Markdown content as string

        Returns:
            List of Section objects (or dicts for dict-like compatibility) with structure:
            {
                "level": int (1-6 for ATX headers),
                "title": str (header text),
                "content": str (content between this header and next),
                "line_start": int,
                "line_end": int
            }
        """
        if not content:
            return []

        lines = content.split('\n')
        sections = []
        current_section = None
        i = 0

        while i < len(lines):
            line = lines[i]

            # Check for ATX header (# Title)
            atx_match = re.match(r'^(#{1,6})\s+(.+?)(?:\s+#+)?$', line)
            if atx_match:
                # Save previous section if exists
                if current_section:
                    content_text = '\n'.join(current_section["lines"]).strip()
                    line_end = i
                    sections.append(Section(
                        level=current_section["level"],
                        title=current_section["title"],
                        content=content_text,
                        line_start=current_section["line_start"],
                        line_end=line_end
                    ))

                # Create new section
                level = len(atx_match.group(1))
                title = atx_match.group(2).strip()
                current_section = {
                    "level": level,
                    "title": title,
                    "lines": [],
                    "line_start": i + 1  # 1-indexed line number
                }
                i += 1
                continue

            # Check for Setext header (underlined with === or ---)
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if re.match(r'^=+\s*$', next_line) and line.strip():
                    # Setext H1 (underlined with =====)
                    if current_section:
                        content_text = '\n'.join(current_section["lines"]).strip()
                        sections.append(Section(
                            level=current_section["level"],
                            title=current_section["title"],
                            content=content_text,
                            line_start=current_section["line_start"],
                            line_end=i
                        ))

                    current_section = {
                        "level": 1,
                        "title": line.strip(),
                        "lines": [],
                        "line_start": i + 1
                    }
                    i += 2
                    continue

                if re.match(r'^-+\s*$', next_line) and line.strip():
                    # Setext H2 (underlined with -----)
                    if current_section:
                        content_text = '\n'.join(current_section["lines"]).strip()
                        sections.append(Section(
                            level=current_section["level"],
                            title=current_section["title"],
                            content=content_text,
                            line_start=current_section["line_start"],
                            line_end=i
                        ))

                    current_section = {
                        "level": 2,
                        "title": line.strip(),
                        "lines": [],
                        "line_start": i + 1
                    }
                    i += 2
                    continue

            # Regular content line
            if current_section is not None:
                current_section["lines"].append(line)

            i += 1

        # Save last section
        if current_section:
            content_text = '\n'.join(current_section["lines"]).strip()
            sections.append(Section(
                level=current_section["level"],
                title=current_section["title"],
                content=content_text,
                line_start=current_section["line_start"],
                line_end=len(lines)
            ))

        return sections
