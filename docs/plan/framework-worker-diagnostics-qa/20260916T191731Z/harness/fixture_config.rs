// Values transcribed from the selected contract, never production policy helpers.
use serde_json::{json, Value};
use std::path::Path;

pub fn fixed() -> Value {
    let features = "memories hooks plugins apps browser_use browser_use_external browser_use_full_cdp_access computer_use image_generation in_app_browser multi_agent shell_tool tool_suggest view_image auth_elicitation code_mode_host goals guardian_approval in_app_chat in_app_dictation in_app_local_automation in_app_updates plugin_sharing prevent_idle_sleep remote_plugin shell_snapshot skill_mcp_dependency_install skill_search sleep_tool sqlite tool_call_mcp_elicitation unified_exec unified_exec_tty workspace_dependencies worktrees";
    let plugins = "documents@openai-primary-runtime pdf@openai-primary-runtime spreadsheets@openai-primary-runtime presentations@openai-primary-runtime template-creator@openai-primary-runtime sites@openai-bundled visualize@openai-bundled codex-app-tools@openai-bundled computer-use@openai-bundled unified-computer-use@openai-bundled browser@openai-bundled chrome@openai-bundled";
    let mut value = json!({"model_provider":"openai","forced_login_method":"chatgpt",
        "web_search":"disabled","sandbox_mode":"read-only","approval_policy":"never",
        "features":{},"apps":{"_default":{"enabled":false},"connector_openai_codex_document_control":{"enabled":false}},
        "mcp_servers":{"node_repl":{"enabled":false},"openaiDeveloperDocs":{"enabled":false}},"plugins":{}});
    for key in features.split_whitespace() { value["features"][key] = json!(false); }
    for key in plugins.split_whitespace() { value["plugins"][key] = json!({"enabled":false}); }
    value
}

pub fn response(source: &Path, canary: &str) -> Value {
    let mut value = json!({"config":fixed(), "origins":{}, "layers":[
        {"name":{"type":"user","file":source,"profile":null,"unknown":{"token":canary}},
         "version":"qa","config":{"unknown":{"token":canary}},"extra":canary},
        {"name":{"type":"sessionFlags","unknown":{"token":canary}},"version":"qa","config":fixed(),"extra":canary}
    ],"unknown":{"nested":canary}});
    for key in ["model_provider","forced_login_method","web_search","sandbox_mode","approval_policy"] {
        value["origins"][key] = json!({"name":{"type":"sessionFlags","extra":{"token":canary}},"version":"qa","extra":canary});
    }
    value["config"]["unknown"] = json!({"nested":[{"token":canary}]});
    value["config"]["apps"]["_default"]["unknown"] = json!({"token":canary});
    value
}

pub fn expected_projection() -> Value {
    json!({"approval_policy":"never","apps_default_enabled":false,"config_layer_count":2,
        "covered_disk_layer_count":1,"forced_login_method":"chatgpt","model_provider":"openai",
        "sandbox_mode":"read-only","session_flags_layers":1,"web_search":"disabled"})
}
