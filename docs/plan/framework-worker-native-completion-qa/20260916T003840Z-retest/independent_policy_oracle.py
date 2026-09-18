"""Contract-derived oracle for the compiled restrictive policy bytes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


POLICY = Path(
    r"C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe\src\restrictive-launch-policy.json"
)
EXPECTED_DIGEST = "1dbc48c4a3627f7c5fc7a996935ec507426e4cd90adac058eb81100ac9b526b5"


def pair(value: str) -> list[str]:
    return ["-c", value]


def main() -> int:
    original = [
        'model_provider="openai"',
        'forced_login_method="chatgpt"',
        'web_search="disabled"',
        "features.memories=false",
        "apps._default.enabled=false",
        'mcp_servers."node_repl".enabled=false',
        'mcp_servers."openaiDeveloperDocs".enabled=false',
        'plugins."documents@openai-primary-runtime".enabled=false',
        'plugins."pdf@openai-primary-runtime".enabled=false',
        'plugins."spreadsheets@openai-primary-runtime".enabled=false',
        'plugins."presentations@openai-primary-runtime".enabled=false',
        'plugins."template-creator@openai-primary-runtime".enabled=false',
        'plugins."sites@openai-bundled".enabled=false',
        'plugins."visualize@openai-bundled".enabled=false',
        'plugins."codex-app-tools@openai-bundled".enabled=false',
        'plugins."computer-use@openai-bundled".enabled=false',
        'plugins."unified-computer-use@openai-bundled".enabled=false',
        'plugins."browser@openai-bundled".enabled=false',
        'plugins."chrome@openai-bundled".enabled=false',
        'apps."connector_openai_codex_document_control".enabled=false',
        "features.hooks=false",
        "features.plugins=false",
        "features.apps=false",
        "features.browser_use=false",
        "features.browser_use_external=false",
        "features.browser_use_full_cdp_access=false",
        "features.computer_use=false",
        "features.image_generation=false",
        "features.in_app_browser=false",
        "features.multi_agent=false",
        "features.shell_tool=false",
        "features.tool_suggest=false",
        "features.view_image=false",
    ]
    additional_features = [
        "auth_elicitation",
        "code_mode_host",
        "goals",
        "guardian_approval",
        "in_app_chat",
        "in_app_dictation",
        "in_app_local_automation",
        "in_app_updates",
        "plugin_sharing",
        "prevent_idle_sleep",
        "remote_plugin",
        "shell_snapshot",
        "skill_mcp_dependency_install",
        "skill_search",
        "sleep_tool",
        "sqlite",
        "tool_call_mcp_elicitation",
        "unified_exec",
        "unified_exec_tty",
        "workspace_dependencies",
        "worktrees",
    ]
    expected = ["app-server", "--listen", "stdio://", "--strict-config"]
    for value in original:
        expected.extend(pair(value))
    for name in additional_features:
        expected.extend(pair(f"features.{name}=false"))
    expected.extend(pair('sandbox_mode="read-only"'))
    expected.extend(pair('approval_policy="never"'))

    raw = POLICY.read_bytes()
    actual_digest = hashlib.sha256(raw).hexdigest()
    record = json.loads(raw)
    errors: list[str] = []
    if set(record) != {"schema_version", "policy_id", "adapter", "argv"}:
        errors.append("policy schema is not closed")
    if record.get("schema_version") != 1:
        errors.append("schema_version")
    if record.get("policy_id") != "codex-0.154.0-readonly-no-external-tools-v2":
        errors.append("policy_id")
    if record.get("adapter") != "codex-0.154.0-stdio":
        errors.append("adapter")
    if record.get("argv") != expected:
        errors.append("ordered argv differs from contract")
    if actual_digest != EXPECTED_DIGEST:
        errors.append("policy digest")
    feature_disables = [
        item.removeprefix("features.").removesuffix("=false")
        for item in expected
        if item.startswith("features.") and item.endswith("=false")
    ]
    if len(feature_disables) != 35 or len(set(feature_disables)) != 35:
        errors.append("feature disable cardinality")
    if any(item in {"cmd", "cmd.exe", "powershell", "pwsh", "/c", "-command"} for item in expected):
        errors.append("shell token")
    output = {
        "schema_version": 1,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "policy_sha256": actual_digest,
        "argv_count": len(expected),
        "config_override_count": (len(expected) - 4) // 2,
        "required_false_feature_count": len(feature_disables),
        "unique_required_false_feature_count": len(set(feature_disables)),
    }
    print(json.dumps(output, sort_keys=True, ensure_ascii=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

