use crate::fixture_config::{expected_projection, response};
use probe::effective_profile::{validate_config, validate_config_observed};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};

fn base() -> Value { response(Path::new(r"C:\qa-independent\reviewed.toml"), "QA_U_CANARY_7F4139") }
fn reject(value: &Value, section: &str, predicate: &str, reason: &str) {
    let cwd = Path::new(r"C:\qa-independent\fixture");
    let covered = [PathBuf::from(r"C:\qa-independent\reviewed.toml")];
    let failure = validate_config_observed(value, cwd, &covered).unwrap_err();
    assert_eq!(serde_json::to_value(failure.section).unwrap(), section);
    assert_eq!(serde_json::to_value(failure.predicate).unwrap(), predicate);
    assert_eq!(failure.reason, reason);
    assert_eq!(validate_config(value, cwd, &covered), Err(reason.to_owned()));
    assert!(!format!("{failure:?}").contains("QA_U_CANARY_7F4139"));
}

#[test]
fn qa_u01_config_shape_and_absence() {
    for value in [Value::Null, json!([]), json!({})] {
        reject(&value, "effective", "shape", "protocol_error");
    }
    for key in ["config", "origins", "layers"] {
        for bad in [None, Some(Value::Null), Some(json!(false))] {
            let mut value = base();
            if let Some(bad) = bad { value[key] = bad; } else { value.as_object_mut().unwrap().remove(key); }
            let section = if key == "config" { "effective" } else { key };
            reject(&value, section, "shape", "protocol_error");
        }
    }
    for key in ["features", "apps", "mcp_servers", "plugins"] {
        let mut value = base();
        value["config"].as_object_mut().unwrap().remove(key);
        reject(&value, "effective", key, "protocol_error");
    }
}

#[test]
fn qa_u02_policy_precedence() {
    let cases = [
        ("/config/model_providers", json!({"QA_PROVIDER_6E99":{"secret":"QA_U_CANARY_7F4139"}}), "provider_map", "profile_unqualified"),
        ("/config/model_providers", json!(2), "provider_map", "protocol_error"),
        ("/config/base_url", json!("QA_U_CANARY_7F4139"), "endpoint_override", "profile_unqualified"),
        ("/config/base_url", json!([]), "endpoint_override", "protocol_error"),
        ("/config/model_provider", json!("QA_U_CANARY_7F4139"), "model_provider", "profile_unqualified"),
        ("/config/forced_login_method", json!(null), "login_method", "profile_unqualified"),
        ("/config/web_search", json!("live"), "web_search", "profile_unqualified"),
        ("/config/sandbox_mode", json!("workspace-write"), "sandbox_mode", "profile_unqualified"),
        ("/config/approval_policy", json!("on-request"), "approval_policy", "profile_unqualified"),
        ("/config/features/hooks", json!(true), "features", "profile_unqualified"),
        ("/config/apps/_default/enabled", json!(true), "apps", "profile_unqualified"),
        ("/config/mcp_servers/node_repl/enabled", json!(true), "mcp_servers", "profile_unqualified"),
        ("/config/plugins/chrome@openai-bundled/enabled", json!(true), "plugins", "profile_unqualified"),
    ];
    for (pointer, bad, predicate, reason) in cases {
        let mut value = base();
        // First two optional properties are introduced as input, all others preexist.
        if pointer == "/config/model_providers" { value["config"]["model_providers"] = bad; }
        else if pointer == "/config/base_url" { value["config"]["base_url"] = bad; }
        else { *value.pointer_mut(pointer).unwrap() = bad; }
        value["origins"] = Value::Null; // Later simultaneous failure must not replace first.
        reject(&value, "effective", predicate, reason);
    }
    let mut value = base();
    value["config"]["model_providers"] = json!({"x":{}});
    value["config"]["base_url"] = json!(5);
    reject(&value, "effective", "provider_map", "profile_unqualified");
    for group in ["apps", "mcp_servers", "plugins"] {
        let mut value = base();
        value["config"][group]["QA_UNKNOWN_71B3"] = json!({"enabled":true,"nested":"QA_U_CANARY_7F4139"});
        reject(&value, "effective", group, "profile_unqualified");
    }
}

#[test]
fn qa_u03_session_keys_and_count() {
    for key in ["model_provider","forced_login_method","web_search","sandbox_mode","approval_policy","features","apps","mcp_servers","plugins"] {
        let mut value = base();
        value["layers"][1]["config"].as_object_mut().unwrap().remove(key);
        reject(&value, "layers", "fixed_keys", "profile_unqualified");
    }
    let mut value = base();
    value["layers"][1]["config"]["QA_EXTRA_KEY_7719"] = json!("QA_U_CANARY_7F4139");
    reject(&value, "layers", "fixed_keys", "profile_unqualified");
    for group in ["features", "apps", "mcp_servers", "plugins"] {
        let mut value = base();
        value["layers"][1]["config"][group]["QA_EXTRA_291D"] = if group == "features" { json!(false) } else { json!({"enabled":false}) };
        reject(&value, "layers", group, "profile_unqualified");
    }
    let mut absent = base();
    absent["layers"].as_array_mut().unwrap().remove(1);
    reject(&absent, "layers", "session_flags_count", "profile_unqualified");
    let mut duplicate = base();
    let session = duplicate["layers"][1].clone();
    duplicate["layers"].as_array_mut().unwrap().push(session);
    reject(&duplicate, "layers", "session_flags_count", "profile_unqualified");
    duplicate["layers"][2]["config"]["features"]["hooks"] = json!(true);
    reject(&duplicate, "layers", "features", "profile_unqualified");
}

#[test]
fn qa_u04_origin_layer_paths() {
    let mut value = base();
    value["origins"].as_object_mut().unwrap().remove("model_provider");
    reject(&value, "origins", "selected_origin", "profile_unqualified");
    let mut value = base();
    value["origins"]["QA_UNSELECTED_872A"] = json!({"name":{"type":"QA_UNKNOWN_ORIGIN_3B52"},"version":"qa"});
    reject(&value, "origins", "origin_source", "profile_unqualified");
    for source in [json!({"type":"user","file":r"C:\qa-independent\uncovered.toml"}), json!({"type":"enterpriseManaged"}), json!({"type":"QA_UNKNOWN_LAYER_D3F1"})] {
        let mut value = base(); value["layers"][0]["name"] = source;
        reject(&value, "layers", "layer_source", "profile_unqualified");
    }
    let mut value = base();
    value["origins"]["QA_UNSELECTED_872A"] = json!({"name":{"type":"user","file":r"C:\qa-independent\uncovered.toml"},"version":"qa"});
    reject(&value, "origins", "origin_source", "profile_unqualified");
    for (cwd, covered) in [(Path::new("relative"), vec![]), (Path::new(r"C:\qa-independent\fixture"), vec![PathBuf::from("relative.toml")])] {
        let failure = validate_config_observed(&base(), cwd, &covered).unwrap_err();
        assert_eq!(serde_json::to_value(failure.section).unwrap(), "origins");
        assert_eq!(serde_json::to_value(failure.predicate).unwrap(), "source_paths");
        assert_eq!(failure.reason, "profile_unqualified");
    }
}

fn canary_free(value: &Value, canaries: &[&str]) -> bool {
    let serialized = value.to_string();
    canaries.iter().all(|canary| !serialized.contains(canary))
}

#[test]
fn qa_u05_projection_privacy() {
    let canaries = ["QA_CONFIG_59C3", "QA_LAYER_F133", "QA_ORIGIN_119B", "QA_SOURCE_741C", "QA_ROOT_717E"];
    let mut value = base();
    value["config"]["QA_unknown"] = json!({"deep":{"token":canaries[0]}});
    value["layers"][0]["config"]["QA_unknown"] = json!({"deep":[canaries[1]]});
    value["origins"]["model_provider"]["QA_unknown"] = json!({"token":canaries[2]});
    value["origins"]["model_provider"]["name"]["QA_unknown"] = json!(canaries[3]);
    value["QA_unknown"] = json!(canaries[4]);
    let observed = validate_config_observed(&value, Path::new(r"C:\qa-independent\fixture"), &[PathBuf::from(r"C:\qa-independent\reviewed.toml")]).unwrap();
    assert_eq!(observed, expected_projection());
    assert!(canary_free(&observed, &canaries));
    let mut contaminated = observed.clone(); contaminated["extra"] = json!({"secret":canaries[1]});
    assert!(!canary_free(&contaminated, &canaries), "negative control must reject contaminated evidence");
    assert_ne!(contaminated, expected_projection(), "closed-field oracle must detect extra evidence fields");
    value["config"]["sandbox_mode"] = json!(canaries[0]);
    reject(&value, "effective", "sandbox_mode", "profile_unqualified");
}

#[test]
fn qa_u06_rpc_closed_labels() {
    use crate::diagnostic::RpcPredicate;
    for (reason, expected) in [("rpc_error","rpc_error"),("protocol_error","protocol_error"),("deadline","deadline"),("user_cancel","user_cancel"),("invalid_control","control_error"),("profile_unqualified","process_guard_rejected"),("worker_exited","other_rpc_failure"),("unsupported_request","other_rpc_failure"),("evidence_write_failed","other_rpc_failure"),("QA_UNKNOWN_ERROR_730EDB","other_rpc_failure")] {
        assert_eq!(serde_json::to_value(RpcPredicate::from_reason(reason)).unwrap(), expected);
    }
}
