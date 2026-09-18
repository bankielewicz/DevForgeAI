//! Closed native launch policy for the pinned Codex adapter.
use crate::request::{Result, digest as sha256};
use serde::Deserialize;

pub const ID: &str = "codex-0.154.0-readonly-no-external-tools-v3";
pub const ADAPTER: &str = "codex-0.154.0-stdio";
pub const RECORD: &str = include_str!("restrictive-launch-policy.json");

/// Feature families that the effective-profile preflight must observe as disabled.
pub const REQUIRED_DISABLED_FEATURES: &[&str] = &[
    "memories",
    "hooks",
    "plugins",
    "apps",
    "browser_use",
    "browser_use_external",
    "browser_use_full_cdp_access",
    "computer_use",
    "image_generation",
    "in_app_browser",
    "multi_agent",
    "shell_tool",
    "tool_suggest",
    "view_image",
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
];

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Policy {
    schema_version: u32,
    policy_id: String,
    adapter: String,
    argv: Vec<String>,
}

/// SHA-256 of the exact compiled record bytes, including their final newline.
pub fn digest() -> String {
    sha256(RECORD.as_bytes())
}

/// Return the compiled argument vector only when every caller binding matches.
/// The caller cannot add configuration or replace the compiled record.
pub fn args(
    adapter: &str,
    schema_version: u32,
    policy_id: &str,
    policy_sha256: &str,
) -> Result<Vec<String>> {
    if adapter != ADAPTER
        || !(2..=3).contains(&schema_version)
        || policy_id != ID
        || policy_sha256 != digest()
    {
        return Err("profile_unqualified".into());
    }
    let policy: Policy =
        serde_json::from_str(RECORD).map_err(|_| "profile_unqualified".to_owned())?;
    if policy.schema_version != 1
        || policy.policy_id != ID
        || policy.adapter != ADAPTER
        || policy.argv.is_empty()
    {
        return Err("profile_unqualified".into());
    }
    Ok(policy.argv)
}
