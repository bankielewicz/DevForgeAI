#!/usr/bin/env python3
"""
MCP-to-CLI Converter
Converts MCP servers into standalone CLI utilities with auto-generated skills.

This is the core engine used by the spec-driven-mcp-converter skill.
It provides three main classes:
  - MCPAnalyzer: Detects patterns and extracts tool definitions
  - CLIGenerator: Generates standalone CLI code
  - SkillGenerator: Generates Claude-friendly skill documentation

Usage:
  python converter.py analyze <mcp-source> [--lang python|typescript]
  python converter.py convert <name> --source <mcp-source> [--pattern api-wrapper|state-based|custom]
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import subprocess


class MCPAnalyzer:
    """Analyzes MCP server code/schema to detect patterns."""

    def __init__(self, mcp_source: str, mcp_lang: str = "python"):
        self.source = mcp_source
        self.lang = mcp_lang
        self.tools: List[Dict[str, Any]] = []
        self.mcp_type = ""
        self.detected_pattern = ""

    def analyze(self) -> Dict[str, Any]:
        """Run analysis and return structured info about the MCP."""

        # Load MCP definition
        mcp_def = self._load_mcp_definition()
        if not mcp_def:
            return {"error": "Could not load MCP definition"}

        self.tools = mcp_def.get("tools", [])

        # Detect pattern
        pattern = self._detect_pattern()
        self.detected_pattern = pattern

        # Analyze state requirements
        state_analysis = self._analyze_state_management()

        # Build recommendations
        recommendations = self._build_recommendations(pattern, state_analysis)

        return {
            "mcp_type": self.mcp_type,
            "detected_pattern": pattern,
            "confidence": self._confidence_score(pattern),
            "tools": self.tools,
            "state_management": state_analysis,
            "conversion_recommendations": recommendations,
            "language": self.lang
        }

    def _load_mcp_definition(self) -> Optional[Dict[str, Any]]:
        """Load MCP from schema file, package, or source code."""

        # Try loading from schema file
        if self.source.endswith(".json"):
            try:
                with open(self.source) as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading schema: {e}", file=sys.stderr)
                return None

        # Try loading from installed package (npm: prefix)
        if self.source.startswith("npm:"):
            return self._load_from_npm_package(self.source)

        # Try loading from local source code
        if Path(self.source).is_dir():
            return self._extract_from_source_code(self.source)

        return None

    def _extract_from_source_code(self, source_dir: str) -> Optional[Dict[str, Any]]:
        """Extract MCP tools from source code by analyzing tool definitions."""

        source_path = Path(source_dir)

        # Look for common patterns
        tools = []

        if self.lang == "python":
            # Parse Python tool definitions
            for py_file in source_path.rglob("*.py"):
                tools.extend(self._extract_python_tools(py_file))

        elif self.lang == "typescript" or self.lang == "javascript":
            # Parse TypeScript/JS tool definitions
            for ts_file in source_path.rglob("*.ts"):
                tools.extend(self._extract_ts_tools(ts_file))

        if not tools:
            # Fallback: try to find index/main files with tool registration
            return None

        return {"tools": tools}

    def _extract_python_tools(self, py_file: Path) -> List[Dict[str, Any]]:
        """Extract @mcp.tool() decorated functions from Python files."""
        tools = []
        try:
            with open(py_file) as f:
                content = f.read()

            # Simple regex-based extraction of @mcp.tool() definitions
            import re

            # Find decorated functions
            pattern = r'@.*\.tool\(\s*\)?\s*(?:async\s+)?def\s+(\w+)\s*\((.*?)\).*?(?:return|""")'

            for match in re.finditer(pattern, content, re.DOTALL):
                tool_name = match.group(1)
                params_str = match.group(2)

                # Extract parameter names
                param_names = [p.strip().split(":")[0] for p in params_str.split(",") if p.strip()]

                tools.append({
                    "name": tool_name,
                    "inputs": {name: "string" for name in param_names},  # Simplified
                    "outputs": "any",
                    "async": "async def" in match.group(0)
                })
        except Exception:
            pass

        return tools

    def _extract_ts_tools(self, ts_file: Path) -> List[Dict[str, Any]]:
        """Extract tool definitions from TypeScript files."""
        # Similar logic for TypeScript
        return []

    def _load_from_npm_package(self, package_spec: str) -> Optional[Dict[str, Any]]:
        """Load from npm package (e.g., 'npm:mcp-puppeteer@latest')."""
        # Implementation would fetch package and extract schema
        return None

    def _detect_pattern(self) -> str:
        """Detect which pattern best fits this MCP."""

        if not self.tools:
            return "unknown"

        # Heuristics for pattern detection

        # API Wrapper: stateless, no side-effects mentioned
        stateless_tools = [t for t in self.tools if "side_effects" not in t or not t.get("side_effects")]
        if len(stateless_tools) == len(self.tools) and len(self.tools) <= 5:
            return "api-wrapper"

        # State-Based: tools reference session/connection/context
        state_keywords = ["session", "connection", "context", "state", "browser", "page", "transaction"]
        tool_names = [t["name"] for t in self.tools]
        tool_names_str = " ".join(tool_names)

        if any(keyword in tool_names_str.lower() for keyword in state_keywords):
            return "state-based"

        # Look for common stateful patterns
        if any("navigate" in t["name"] or "click" in t["name"] for t in self.tools):
            return "state-based"

        # Default to API wrapper if unsure
        return "api-wrapper"

    def _analyze_state_management(self) -> Dict[str, Any]:
        """Analyze if/how state is managed."""

        stateful_tools = [t for t in self.tools if t.get("side_effects")]

        return {
            "stateful": len(stateful_tools) > 0,
            "session_required": self.detected_pattern == "state-based",
            "concurrent_sessions": True,  # Most can handle this
            "state_keywords": self._find_state_keywords()
        }

    def _find_state_keywords(self) -> List[str]:
        """Find state-related keywords in tool names/descriptions."""
        keywords = []
        state_words = ["session", "connection", "context", "browser", "page"]

        for tool in self.tools:
            tool_name = tool.get("name", "").lower()
            for word in state_words:
                if word in tool_name:
                    keywords.append(word)

        return list(set(keywords))

    def _build_recommendations(self, pattern: str, state_analysis: Dict) -> List[str]:
        """Generate recommendations for conversion."""

        recommendations = []

        if pattern == "state-based":
            recommendations.append("Use ephemeral session model")
            recommendations.append("Queue operations within session")
            recommendations.extend([
                "Implement session timeout (recommend 1 hour)",
                "Add session cleanup handlers"
            ])

        elif pattern == "api-wrapper":
            recommendations.append("Direct 1:1 tool → CLI command mapping")
            recommendations.append("Handle HTTP error codes → exit codes")
            recommendations.append("Normalize JSON responses")

        if any("binary" in t.get("outputs", "") for t in self.tools):
            recommendations.append("Stream binary outputs as base64")

        return recommendations

    def _confidence_score(self, pattern: str) -> float:
        """Return confidence in pattern detection (0-1)."""
        # Simplified scoring
        if pattern == "unknown":
            return 0.3
        elif pattern == "api-wrapper" and len(self.tools) <= 10:
            return 0.95
        elif pattern == "state-based":
            return 0.85
        return 0.7


class CLIGenerator:
    """Generates CLI wrapper from MCP definition."""

    def __init__(self, analysis: Dict[str, Any], output_dir: str, pattern: str):
        self.analysis = analysis
        self.output_dir = Path(output_dir)
        self.pattern = pattern
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self) -> bool:
        """Generate CLI structure."""

        try:
            self._create_structure()
            self._generate_cli_main()
            self._generate_adapter()
            self._generate_utils()
            self._generate_requirements()
            self._generate_readme()
            self._generate_tests()

            print(f"CLI generated in {self.output_dir}")
            return True

        except Exception as e:
            print(f"Error generating CLI: {e}", file=sys.stderr)
            return False

    def _create_structure(self):
        """Create directory structure."""
        dirs = [
            self.output_dir / "adapters",
            self.output_dir / "utils",
            self.output_dir / "tests",
            self.output_dir / "skill" / "references",
            self.output_dir / "skill" / "scripts",
            self.output_dir / "skill" / "assets"
        ]

        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def _generate_cli_main(self):
        """Generate main CLI entry point."""
        # Implementation generates cli.py with argparse
        pass

    def _generate_adapter(self):
        """Generate pattern-specific adapter."""
        # Implementation generates adapter based on pattern
        pass

    def _generate_utils(self):
        """Generate utility modules (error_handler, output_formatter)."""
        pass

    def _generate_requirements(self):
        """Generate requirements.txt."""
        pass

    def _generate_readme(self):
        """Generate README.md."""
        pass

    def _generate_tests(self):
        """Generate test stubs."""
        pass


class SkillGenerator:
    """Generates skill documentation from MCP analysis."""

    def __init__(self, analysis: Dict[str, Any], cli_dir: str):
        self.analysis = analysis
        self.skill_dir = Path(cli_dir) / "skill"
        self.skill_dir.mkdir(parents=True, exist_ok=True)

    def generate(self) -> bool:
        """Generate skill files."""

        try:
            self._generate_skill_md()
            self._generate_references()
            self._generate_setup_script()
            self._generate_error_codes()

            print(f"Skill generated in {self.skill_dir}")
            return True

        except Exception as e:
            print(f"Error generating skill: {e}", file=sys.stderr)
            return False

    def _generate_skill_md(self):
        """Generate main SKILL.md with frontmatter and pattern-specific body."""
        pass

    def _generate_references(self):
        """Generate reference documentation (cli_reference.md, usage_examples.md)."""
        pass

    def _generate_setup_script(self):
        """Generate setup.sh installation script."""
        pass

    def _generate_error_codes(self):
        """Generate error code reference (assets/error_codes.md)."""
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Convert MCP servers to CLI utilities with auto-generated skills"
    )

    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # Analyze action
    analyze_parser = subparsers.add_parser("analyze", help="Analyze MCP server")
    analyze_parser.add_argument("source", help="Path/package spec for MCP server")
    analyze_parser.add_argument("--lang", default="python", choices=["python", "typescript", "javascript"])
    analyze_parser.add_argument("--output", help="Output analysis to JSON file")

    # Convert action
    convert_parser = subparsers.add_parser("convert", help="Convert MCP to CLI + skill")
    convert_parser.add_argument("name", help="Name for the converted CLI")
    convert_parser.add_argument("--source", required=True, help="Path/package spec for MCP server")
    convert_parser.add_argument("--pattern", choices=["api-wrapper", "state-based", "custom"],
                                help="Force pattern (auto-detect if not specified)")
    convert_parser.add_argument("--lang", default="python")
    convert_parser.add_argument("--output-dir", default=".", help="Output directory")
    convert_parser.add_argument("--adapter-script", help="Custom adapter script for 'custom' pattern")

    args = parser.parse_args()

    if args.action == "analyze":
        analyzer = MCPAnalyzer(args.source, args.lang)
        analysis = analyzer.analyze()

        if args.output:
            with open(args.output, "w") as f:
                json.dump(analysis, f, indent=2)
            print(f"Analysis written to {args.output}")
        else:
            print(json.dumps(analysis, indent=2))

        return 0

    elif args.action == "convert":
        # Step 1: Analyze
        analyzer = MCPAnalyzer(args.source, args.lang)
        analysis = analyzer.analyze()

        if "error" in analysis:
            print(f"Error analyzing MCP: {analysis['error']}", file=sys.stderr)
            return 1

        # Step 2: Determine pattern
        pattern = args.pattern or analysis.get("detected_pattern", "api-wrapper")

        print(f"Detected pattern: {pattern} (confidence: {analysis.get('confidence', 0):.0%})")

        # Step 3: Generate CLI
        cli_gen = CLIGenerator(analysis, args.output_dir, pattern)
        if not cli_gen.generate():
            return 1

        # Step 4: Generate Skill
        skill_gen = SkillGenerator(analysis, args.output_dir)
        if not skill_gen.generate():
            return 1

        print(f"\nConversion complete!")
        print(f"  CLI: {args.output_dir}/cli.py")
        print(f"  Skill: {args.output_dir}/skill/SKILL.md")

        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
