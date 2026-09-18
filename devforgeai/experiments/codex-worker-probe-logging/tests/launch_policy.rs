use devforgeai_codex_worker_probe::{launch_policy, request};

const EXPECTED_FEATURES: &[&str] = &[
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
const EXPECTED_POLICY_SHA256: &str =
    "c8ef7b6184e20fd55833c9b8f7cd17b6dc1f0af494ca367c857953680dab1b49";

fn expected_args() -> Vec<String> {
    [
        "app-server",
        "--listen",
        "stdio://",
        "--strict-config",
        "-c",
        "model_provider=\"openai\"",
        "-c",
        "forced_login_method=\"chatgpt\"",
        "-c",
        "web_search=\"disabled\"",
        "-c",
        "features.memories=false",
        "-c",
        "apps._default.enabled=false",
        "-c",
        "mcp_servers.node_repl.enabled=false",
        "-c",
        "mcp_servers.openaiDeveloperDocs.enabled=false",
        "-c",
        "plugins.documents@openai-primary-runtime.enabled=false",
        "-c",
        "plugins.pdf@openai-primary-runtime.enabled=false",
        "-c",
        "plugins.spreadsheets@openai-primary-runtime.enabled=false",
        "-c",
        "plugins.presentations@openai-primary-runtime.enabled=false",
        "-c",
        "plugins.template-creator@openai-primary-runtime.enabled=false",
        "-c",
        "plugins.sites@openai-bundled.enabled=false",
        "-c",
        "plugins.visualize@openai-bundled.enabled=false",
        "-c",
        "plugins.codex-app-tools@openai-bundled.enabled=false",
        "-c",
        "plugins.computer-use@openai-bundled.enabled=false",
        "-c",
        "plugins.unified-computer-use@openai-bundled.enabled=false",
        "-c",
        "plugins.browser@openai-bundled.enabled=false",
        "-c",
        "plugins.chrome@openai-bundled.enabled=false",
        "-c",
        "apps.connector_openai_codex_document_control.enabled=false",
        "-c",
        "features.hooks=false",
        "-c",
        "features.plugins=false",
        "-c",
        "features.apps=false",
        "-c",
        "features.browser_use=false",
        "-c",
        "features.browser_use_external=false",
        "-c",
        "features.browser_use_full_cdp_access=false",
        "-c",
        "features.computer_use=false",
        "-c",
        "features.image_generation=false",
        "-c",
        "features.in_app_browser=false",
        "-c",
        "features.multi_agent=false",
        "-c",
        "features.shell_tool=false",
        "-c",
        "features.tool_suggest=false",
        "-c",
        "features.view_image=false",
        "-c",
        "features.auth_elicitation=false",
        "-c",
        "features.code_mode_host=false",
        "-c",
        "features.goals=false",
        "-c",
        "features.guardian_approval=false",
        "-c",
        "features.in_app_chat=false",
        "-c",
        "features.in_app_dictation=false",
        "-c",
        "features.in_app_local_automation=false",
        "-c",
        "features.in_app_updates=false",
        "-c",
        "features.plugin_sharing=false",
        "-c",
        "features.prevent_idle_sleep=false",
        "-c",
        "features.remote_plugin=false",
        "-c",
        "features.shell_snapshot=false",
        "-c",
        "features.skill_mcp_dependency_install=false",
        "-c",
        "features.skill_search=false",
        "-c",
        "features.sleep_tool=false",
        "-c",
        "features.sqlite=false",
        "-c",
        "features.tool_call_mcp_elicitation=false",
        "-c",
        "features.unified_exec=false",
        "-c",
        "features.unified_exec_tty=false",
        "-c",
        "features.workspace_dependencies=false",
        "-c",
        "features.worktrees=false",
        "-c",
        "sandbox_mode=\"read-only\"",
        "-c",
        "approval_policy=\"never\"",
    ]
    .into_iter()
    .map(str::to_owned)
    .collect()
}

#[test]
fn fixed_policy_has_exact_closed_identity_and_argument_vector() {
    let expected = expected_args();
    assert_eq!(
        launch_policy::ID,
        "codex-0.154.0-readonly-no-external-tools-v3"
    );
    assert_eq!(launch_policy::REQUIRED_DISABLED_FEATURES, EXPECTED_FEATURES);
    assert_eq!(launch_policy::digest(), EXPECTED_POLICY_SHA256);
    assert_eq!(
        launch_policy::args(
            "codex-0.154.0-stdio",
            2,
            launch_policy::ID,
            &launch_policy::digest()
        ),
        Ok(expected.clone())
    );

    let parsed: serde_json::Value = serde_json::from_str(launch_policy::RECORD).unwrap();
    assert_eq!(
        parsed,
        serde_json::json!({
            "schema_version": 1,
            "policy_id": "codex-0.154.0-readonly-no-external-tools-v3",
            "adapter": "codex-0.154.0-stdio",
            "argv": expected,
        })
    );
    assert_eq!(
        launch_policy::digest(),
        request::digest(launch_policy::RECORD.as_bytes())
    );

    let argv = parsed["argv"].as_array().unwrap();
    assert_eq!(
        &argv[..4],
        ["app-server", "--listen", "stdio://", "--strict-config"]
    );
    assert_eq!(argv[4..].len() % 2, 0);
    assert!(argv[4..].chunks_exact(2).all(|pair| pair[0] == "-c"));
}

#[test]
fn policy_binding_rejects_every_caller_controlled_identity_mismatch() {
    let id = launch_policy::ID;
    let sha = launch_policy::digest();
    for (adapter, schema, policy_id, policy_sha) in [
        ("peer", 2, id, sha.as_str()),
        ("codex-0.154.0-stdio", 1, id, sha.as_str()),
        ("codex-0.154.0-stdio", 4, id, sha.as_str()),
        ("codex-0.154.0-stdio", 2, "caller-selected", sha.as_str()),
        ("codex-0.154.0-stdio", 2, id, "0"),
        ("codex-0.154.0-stdio", 2, id, &"0".repeat(64)),
    ] {
        assert_eq!(
            launch_policy::args(adapter, schema, policy_id, policy_sha),
            Err("profile_unqualified".to_owned()),
            "unexpected admission for {adapter}/{schema}/{policy_id}/{policy_sha}"
        );
    }
}
