"""Retain bounded Codex 0.154.0 parser/feature observations without starting app-server."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = Path("C:/Projects/DevForgeAI")
CODEX = Path(
    "C:/Users/bryan/.codex/packages/standalone/releases/"
    "0.154.0-x86_64-pc-windows-msvc/bin/codex.exe"
)

spec = spec_from_file_location("native_evidence_record", ROOT / "record.py")
if spec is None or spec.loader is None:
    raise RuntimeError("could not load evidence recorder")
record = module_from_spec(spec)
spec.loader.exec_module(record)


def keep(label: str, *args: str) -> None:
    record.capture(
        f"profile-research/{label}",
        [CODEX, *args],
        cwd=WORK,
        timeout=30,
    )


keep("01-version", "--version")
keep("02-help", "--help")
keep("03-app-server-help", "app-server", "--help")

invalid_cases = [
    ("04-model-provider-type", "model_provider=7"),
    ("05-login-method-enum", 'forced_login_method="bogus"'),
    ("06-web-search-enum", 'web_search="bogus"'),
    ("07-memories-type", 'features.memories="bogus"'),
    ("08-hooks-type", 'features.hooks="bogus"'),
    ("09-app-default-type", 'apps._default.enabled="bogus"'),
    ("10-app-id-type", 'apps."connector_openai_codex_document_control".enabled="bogus"'),
    ("11-mcp-id-type", 'mcp_servers."node_repl".enabled="bogus"'),
    (
        "12-plugin-id-type",
        'plugins."documents@openai-primary-runtime".enabled="bogus"',
    ),
    ("13-unknown-control", 'definitely_unknown_qa_key="bogus"'),
]
for label, override in invalid_cases:
    keep(label, "-c", override, "features", "list")

keep("14-features-baseline", "features", "list")

effect_features = [
    "apps",
    "browser_use",
    "browser_use_external",
    "browser_use_full_cdp_access",
    "computer_use",
    "hooks",
    "image_generation",
    "in_app_browser",
    "memories",
    "multi_agent",
    "plugins",
    "shell_tool",
    "tool_suggest",
    "view_image",
]
disable_args: list[str] = []
for feature in effect_features:
    disable_args.extend(["-c", f"features.{feature}=false"])
keep("15-features-disabled", *disable_args, "features", "list")

keep(
    "16-strict-features-unsupported",
    "--strict-config",
    "-c",
    'model_provider="openai"',
    "features",
    "list",
)
