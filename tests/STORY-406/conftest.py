"""
Shared fixtures for STORY-406: Message Chain Detection tests.
Story: STORY-406-add-message-chain-detection
Generated: 2026-02-16
"""
import re
import pytest


# === Grep Pattern Under Test ===
# This is the Stage 1 pattern specified in the story AC#1
# Extended to also match constructor-initiated chains: \w+\([^)]*\)(\.\w+\([^)]*\)){2,}
# The combined pattern matches both styles:
# - Standard chains: obj.a().b().c() - minimum 3 chained calls
# - Constructor chains: Ctor().a().b().c() - constructor + 2+ chained calls
MESSAGE_CHAIN_PATTERN = r'(\w+(\.\w+\([^)]*\)){3,}|\w+\([^)]*\)(\.\w+\([^)]*\)){2,})'


# === Sample Code Fixtures ===

@pytest.fixture
def navigation_chain_code():
    """Navigation chain - should be DETECTED (Law of Demeter violation)."""
    return "order.getCustomer().getAddress().getCity()"


@pytest.fixture
def builder_chain_code():
    """Builder pattern - should be SUPPRESSED (fluent API)."""
    return "QueryBuilder().where(x).orderBy(y).limit(10)"


@pytest.fixture
def promise_chain_code():
    """Promise chain - should be SUPPRESSED (fluent API).
    Note: Simple form for Stage 1 pattern matching. Complex arrow functions
    with nested parens may not match the simple Stage 1 grep pattern."""
    return "fetch(url).then(handler).then(handler2).catch(errorHandler)"


@pytest.fixture
def short_chain_code():
    """2-level chain - should NOT match (below threshold)."""
    return "obj.getA().getB()"


@pytest.fixture
def long_navigation_chain():
    """4-level navigation chain - should be DETECTED."""
    return "user.getProfile().getSettings().getTheme().getName()"


@pytest.fixture
def jquery_chain_code():
    """jQuery chain - should be SUPPRESSED (fluent API)."""
    return "$('#element').addClass('active').show().animate({opacity: 1})"


@pytest.fixture
def string_builder_chain():
    """StringBuilder chain - should be SUPPRESSED (fluent API)."""
    return "StringBuilder().append('hello').append(' ').append('world').toString()"


@pytest.fixture
def grep_pattern():
    """The Stage 1 Grep pattern from AC#1."""
    return MESSAGE_CHAIN_PATTERN


@pytest.fixture
def confidence_threshold():
    """The Stage 2 confidence threshold from the spec."""
    return 0.7


@pytest.fixture
def required_output_fields():
    """Required JSON output fields from AC#6."""
    return [
        "smell_type",
        "severity",
        "file",
        "line",
        "chain_excerpt",
        "chain_length",
        "confidence",
        "evidence",
        "remediation",
    ]


@pytest.fixture
def sample_finding():
    """A complete MessageChainFinding conforming to AC#6 schema."""
    return {
        "smell_type": "message_chain",
        "severity": "LOW",
        "file": "src/services/order_service.py",
        "line": 42,
        "chain_excerpt": "order.getCustomer().getAddress().getCity()",
        "chain_length": 3,
        "confidence": 0.85,
        "evidence": "Navigation chain accessing nested objects via get*() methods",
        "remediation": "Extract a method on Order that encapsulates the nested access",
    }


@pytest.fixture
def scanner_spec_path():
    """Path to the anti-pattern-scanner spec file."""
    return ".claude/agents/anti-pattern-scanner.md"


@pytest.fixture
def src_scanner_spec_path():
    """Path to the src copy of anti-pattern-scanner spec."""
    return "src/claude/agents/anti-pattern-scanner.md"
