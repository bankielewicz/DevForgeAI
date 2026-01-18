"""Credential Masker for STORY-244 - sanitizes output to prevent credential exposure."""
import re
from typing import List, Pattern


class CredentialMasker:
    """Sanitizes output to prevent credential exposure (AC#7)."""

    def __init__(self):
        self._patterns = self._compile_patterns()

    def _compile_patterns(self) -> List[Pattern]:
        """Compile regex patterns for credential detection."""
        pattern_strings = [
            # NPM tokens (npm_xxx format) - but exclude common command names (exact match only)
            # We use a negative lookahead with word boundary to only exclude exact matches
            r'npm_(?!(?:install|update|audit|ci|test|run|start|build|init|publish|pack|link|uninstall|outdated|ls|dedupe|prune|shrinkwrap|cache|config|version|help|search|info|view|docs|bugs|repo|prefix|root|whoami|login|logout|ping|owner|access|team|adduser|deprecate|unpublish|star|unstar|stars|explore|edit|fund|explain|exec|pkg|query|set-script|diff|hook|org|profile|rebuild|restart|stop|completion)(?:\s|$))[a-zA-Z0-9_-]+',
            # GitHub tokens - classic PAT (ghp_), OAuth (gho_), user-to-server (ghu_),
            # server-to-server (ghs_), refresh (ghr_) - any length for testing
            r'gh[pousr]_[a-zA-Z0-9]+',
            # GitHub fine-grained PAT (github_pat_xxx)
            r'github_pat_[a-zA-Z0-9_]+',
            # NuGet API keys (start with oy2) - allow shorter lengths too
            r'oy2[a-zA-Z0-9nx]+',
            # AWS Access Keys (AKIA prefix)
            r'AKIA[0-9A-Z]{16}',
            # AWS Secret Access Keys (40 char mixed case alphanumeric with some special chars)
            r'(?:AWS_SECRET_ACCESS_KEY|aws_secret_access_key)\s*[=:]\s*["\']?[A-Za-z0-9/+=]{40}["\']?',
            # Generic secrets in env var format (PASSWORD, TOKEN, SECRET, API_KEY vars)
            r'(?:TWINE_PASSWORD|DOCKER_PASSWORD|NUGET_API_KEY|NPM_TOKEN|GITHUB_TOKEN|CARGO_REGISTRY_TOKEN)\s*=\s*\S+',
            # Bearer tokens
            r'Bearer\s+[a-zA-Z0-9_-]+\.?[a-zA-Z0-9_-]*\.?[a-zA-Z0-9_-]*',
            # Basic auth header
            r'Basic\s+[a-zA-Z0-9+/=]+',
            # URL credentials with explicit password format (user:pass@host) - require both user and pass
            r'://[^/:@\s]+:[^/@\s]+@',
            # Generic password/secret/api_key/token key-value patterns with = or :
            r'(?:password|secret|api_key|apikey|api-key|secret_key|token)\s*[=:]\s*["\']?[^\s"\']+["\']?',
            # npmToken and similar camelCase token patterns (JSON format)
            r'"?(?:npmToken|npm[Tt]oken|github[Tt]oken|apiToken)"?\s*[=:]\s*["\']?[^\s"\']+["\']?',
            # Docker password in -p flag (docker login -p xxx)
            r'-p\s+[^\s]+',
            # Cargo tokens (cio_ format or cargo_token format)
            r'(?:cio_|cargo[_-]?(?:registry[_-]?)?token[_-]?)[a-zA-Z0-9_-]+',
            # Long alphanumeric strings that look like tokens (40+ chars)
            r'(?<![a-zA-Z0-9])[a-zA-Z0-9]{40,}(?![a-zA-Z0-9])',
        ]
        return [re.compile(p, re.IGNORECASE) for p in pattern_strings]

    def get_patterns(self) -> List[Pattern]:
        """Return credential regex patterns (AC#7)."""
        return self._patterns.copy()

    def mask_output(self, text: str) -> str:
        """Replace credential patterns with *** (AC#7)."""
        if text is None:
            return None
        if not text:
            return ""

        result = text
        for pattern in self._patterns:
            result = pattern.sub('***', result)
        return result

    def scan_for_leaks(self, text: str) -> List[str]:
        """Detect potential credential leaks (AC#7)."""
        if not text:
            return []

        leaks = []
        for pattern in self._patterns:
            matches = pattern.findall(text)
            leaks.extend(matches)
        return leaks
