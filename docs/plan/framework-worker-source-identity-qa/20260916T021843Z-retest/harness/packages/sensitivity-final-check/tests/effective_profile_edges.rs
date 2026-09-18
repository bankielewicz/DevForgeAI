use devforgeai_codex_worker_probe::{effective_profile, launch_policy};
use serde_json::{Map, Value, json};
use std::path::{Path, PathBuf};

const MCP_NAMES: &[&str] = &["node_repl", "openaiDeveloperDocs"];
const APP_NAME: &str = "connector_openai_codex_document_control";
const PLUGIN_NAMES: &[&str] = &[
    "documents@openai-primary-runtime",
    "pdf@openai-primary-runtime",
    "spreadsheets@openai-primary-runtime",
    "presentations@openai-primary-runtime",
    "template-creator@openai-primary-runtime",
    "sites@openai-bundled",
    "visualize@openai-bundled",
    "codex-app-tools@openai-bundled",
    "computer-use@openai-bundled",
    "unified-computer-use@openai-bundled",
    "browser@openai-bundled",
    "chrome@openai-bundled",
];
const ALLOWED_ENABLED_FEATURES: &[&str] = &[
    "collaboration_modes",
    "compaction_image_budget",
    "content_item_kinds",
    "enable_request_compression",
    "fast_mode",
    "item_ids",
    "mentions_v2",
    "personality",
    "remote_compaction_v2",
    "resize_all_images",
    "secret_auth_storage",
    "steer",
    "terminal_resize_reflow",
    "tool_search_always_defer_mcp_tools",
    "tui_app_server",
    "unbounded_connection_retries",
    "unified_exec_zsh_fork",
];

fn disabled_feature_config() -> Value {
    Value::Object(
        launch_policy::REQUIRED_DISABLED_FEATURES
            .iter()
            .map(|name| ((*name).to_owned(), Value::Bool(false)))
            .collect(),
    )
}

fn disabled_entries(names: &[&str]) -> Value {
    Value::Object(
        names
            .iter()
            .map(|name| ((*name).to_owned(), json!({"enabled":false})))
            .collect(),
    )
}

fn restrictive_config() -> Value {
    json!({
        "model_provider":"openai",
        "forced_login_method":"chatgpt",
        "web_search":"disabled",
        "sandbox_mode":"read-only",
        "approval_policy":"never",
        "features":disabled_feature_config(),
        "apps":{
            "_default":{"enabled":false},
            APP_NAME:{"enabled":false}
        },
        "mcp_servers":disabled_entries(MCP_NAMES),
        "plugins":disabled_entries(PLUGIN_NAMES)
    })
}

fn session_origin() -> Value {
    json!({"name":{"type":"sessionFlags"},"version":"1"})
}

fn disk_layer(source: Value) -> Value {
    json!({
        "config":{"sensitive_input":"not retained"},
        "disabledReason":null,
        "name":source,
        "version":"1"
    })
}

fn session_layer() -> Value {
    json!({
        "config":restrictive_config(),
        "disabledReason":null,
        "name":{"type":"sessionFlags"},
        "version":"1"
    })
}

fn config_response(user_config: &Path) -> Value {
    let mut origins = Map::new();
    for key in [
        "model_provider",
        "forced_login_method",
        "web_search",
        "sandbox_mode",
        "approval_policy",
    ] {
        origins.insert(key.to_owned(), session_origin());
    }
    json!({
        "config":restrictive_config(),
        "origins":origins,
        "layers":[
            disk_layer(json!({"type":"user","file":user_config,"profile":null})),
            session_layer()
        ]
    })
}

fn assert_error(actual: Result<Value, String>, expected: &str) {
    assert_eq!(actual.unwrap_err(), expected);
}

fn feature(name: &str, enabled: bool) -> Value {
    json!({
        "name":name,
        "enabled":enabled,
        "defaultEnabled":false,
        "stage":"stable"
    })
}

fn complete_feature_data() -> Vec<Value> {
    launch_policy::REQUIRED_DISABLED_FEATURES
        .iter()
        .map(|name| feature(name, false))
        .collect()
}

fn hook(key: &str, event: &str, source: &str, trust: &str, handler: &str) -> Value {
    let mut value = json!({
        "key":key,
        "currentHash":format!("hash-{key}"),
        "displayOrder":0,
        "enabled":false,
        "eventName":event,
        "isManaged":false,
        "source":source,
        "sourcePath":format!(r"C:\reviewed\{key}.json"),
        "timeoutSec":5,
        "trustStatus":trust,
        "handlerType":handler
    });
    match handler {
        "command" => value["command"] = json!(format!("sensitive-command-{key}")),
        "mcpTool" => {
            value["server"] = json!(format!("sensitive-server-{key}"));
            value["tool"] = json!(format!("sensitive-tool-{key}"));
        }
        _ => {}
    }
    value
}

fn plugin(id: &str, source: Value, auth: &str, install: &str, installed: bool) -> Value {
    json!({
        "id":id,
        "name":format!("sensitive-name-{id}"),
        "enabled":false,
        "installed":installed,
        "source":source,
        "authPolicy":auth,
        "installPolicy":install
    })
}

fn mcp(name: &str, auth: &str) -> Value {
    json!({
        "name":name,
        "authStatus":auth,
        "runtimeStatus":"disabled",
        "tools":{},
        "toolsError":null,
        "resources":[],
        "resourceTemplates":[]
    })
}

#[test]
fn reviewed_config_sources_and_single_session_layer_are_enforced() {
    let cwd = PathBuf::from(r"C:\qa\fixture\child");
    let packaged = PathBuf::from(r"C:\Program Files\Codex\defaults.toml");
    let system = PathBuf::from(r"C:\ProgramData\OpenAI\Codex\config.toml");
    let legacy = PathBuf::from(r"C:\ProgramData\OpenAI\Codex\legacy.toml");
    let user = PathBuf::from(r"C:\Users\qa\.codex\config.toml");
    let project = PathBuf::from(r"C:\qa\fixture\.codex\config.toml");
    let covered = vec![
        packaged.clone(),
        system.clone(),
        legacy.clone(),
        user.clone(),
        project.clone(),
    ];

    let disk_sources = [
        json!({"type":"packagedDefaults","file":packaged}),
        json!({"type":"system","file":system}),
        json!({"type":"legacyManagedConfigTomlFromFile","file":legacy}),
        json!({"type":"user","file":user,"profile":null}),
        json!({"type":"project","dotCodexFolder":r"C:\qa\fixture\.codex"}),
    ];
    let mut origins = Map::new();
    for key in [
        "model_provider",
        "forced_login_method",
        "web_search",
        "sandbox_mode",
        "approval_policy",
    ] {
        origins.insert(key.to_owned(), session_origin());
    }
    for (index, source) in disk_sources.iter().enumerate() {
        origins.insert(
            format!("reviewed_source_{index}"),
            json!({"name":source,"version":"1"}),
        );
    }
    let mut layers: Vec<Value> = disk_sources.into_iter().map(disk_layer).collect();
    layers.push(session_layer());
    let valid = json!({
        "config":restrictive_config(),
        "origins":origins,
        "layers":layers
    });
    assert_eq!(
        effective_profile::validate_config(&valid, &cwd, &covered).unwrap(),
        json!({
            "approval_policy":"never",
            "apps_default_enabled":false,
            "config_layer_count":6,
            "covered_disk_layer_count":5,
            "forced_login_method":"chatgpt",
            "model_provider":"openai",
            "sandbox_mode":"read-only",
            "session_flags_layers":1,
            "web_search":"disabled"
        })
    );

    let mut case = valid.clone();
    case["layers"][3]["name"]["profile"] = json!("unexpected-profile");
    assert_error(
        effective_profile::validate_config(&case, &cwd, &covered),
        "profile_unqualified",
    );

    let mut case = valid.clone();
    case["layers"][4]["name"]["dotCodexFolder"] = json!(r"C:\outside\.codex");
    assert_error(
        effective_profile::validate_config(&case, &cwd, &covered),
        "profile_unqualified",
    );

    for source_type in [
        "mdm",
        "enterpriseManaged",
        "legacyManagedConfigTomlFromMdm",
        "futureUnknownSource",
    ] {
        let mut case = valid.clone();
        case["layers"][0]["name"] = json!({"type":source_type});
        assert_error(
            effective_profile::validate_config(&case, &cwd, &covered),
            "profile_unqualified",
        );
    }

    let mut case = valid.clone();
    case["layers"] = json!([]);
    assert_error(
        effective_profile::validate_config(&case, &cwd, &covered),
        "protocol_error",
    );

    let mut case = valid.clone();
    case["layers"] = Value::Array((0..65).map(|_| session_layer()).collect());
    assert_error(
        effective_profile::validate_config(&case, &cwd, &covered),
        "protocol_error",
    );

    let mut case = valid.clone();
    case["layers"].as_array_mut().unwrap().pop();
    assert_error(
        effective_profile::validate_config(&case, &cwd, &covered),
        "profile_unqualified",
    );

    let mut case = valid.clone();
    case["layers"].as_array_mut().unwrap().push(session_layer());
    assert_error(
        effective_profile::validate_config(&case, &cwd, &covered),
        "profile_unqualified",
    );

    let mut case = valid.clone();
    case["layers"][0]["disabledReason"] = json!(17);
    assert_error(
        effective_profile::validate_config(&case, &cwd, &covered),
        "protocol_error",
    );

    let mut case = valid.clone();
    let excessive_origins: Map<String, Value> = (0..1_001)
        .map(|index| (format!("origin_{index}"), session_origin()))
        .chain([
            ("model_provider".to_owned(), session_origin()),
            ("forced_login_method".to_owned(), session_origin()),
            ("web_search".to_owned(), session_origin()),
            ("sandbox_mode".to_owned(), session_origin()),
            ("approval_policy".to_owned(), session_origin()),
        ])
        .collect();
    case["origins"] = Value::Object(excessive_origins);
    assert_error(
        effective_profile::validate_config(&case, &cwd, &covered),
        "protocol_error",
    );

    assert_error(
        effective_profile::validate_config(&valid, Path::new("relative-fixture"), &covered),
        "profile_unqualified",
    );
}

#[test]
fn provider_endpoints_and_closed_session_policy_fail_closed() {
    let cwd = PathBuf::from(r"C:\qa\fixture");
    let user = PathBuf::from(r"C:\Users\qa\.codex\config.toml");
    let mut inert = config_response(&user);
    inert["config"]["model_providers"] = Value::Null;
    inert["config"]["chatgpt_base_url"] = Value::Null;
    inert["config"]["openai_base_url"] = json!("");
    inert["config"]["api_base"] = Value::Null;
    inert["config"]["base_url"] = json!("");
    assert!(effective_profile::validate_config(&inert, &cwd, std::slice::from_ref(&user)).is_ok());
    inert["config"]["model_providers"] = json!({});
    assert!(effective_profile::validate_config(&inert, &cwd, std::slice::from_ref(&user)).is_ok());

    let valid = config_response(&user);
    for (field, value, expected) in [
        ("model_providers", json!([]), "protocol_error"),
        (
            "model_providers",
            json!({"alternate":{"base_url":"https://provider.invalid"}}),
            "profile_unqualified",
        ),
        (
            "chatgpt_base_url",
            json!("https://provider.invalid"),
            "profile_unqualified",
        ),
        ("openai_base_url", json!(42), "protocol_error"),
        ("api_base", json!(true), "protocol_error"),
    ] {
        let mut case = valid.clone();
        case["config"][field] = value;
        assert_error(
            effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&user)),
            expected,
        );
    }

    let mut case = valid.clone();
    case["layers"][1]["config"]["unexpected"] = json!(false);
    assert_error(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&user)),
        "profile_unqualified",
    );

    let mut case = valid.clone();
    case["layers"][1]["config"]
        .as_object_mut()
        .unwrap()
        .remove("apps");
    assert_error(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&user)),
        "profile_unqualified",
    );

    for pointer in [
        "/layers/1/config/apps/_default/enabled",
        "/layers/1/config/apps/connector_openai_codex_document_control/enabled",
        "/layers/1/config/mcp_servers/node_repl/enabled",
        "/layers/1/config/plugins/chrome@openai-bundled/enabled",
        "/layers/1/config/features/hooks",
    ] {
        let mut case = valid.clone();
        *case.pointer_mut(pointer).unwrap() = json!(true);
        assert_error(
            effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&user)),
            "profile_unqualified",
        );
    }

    let mut case = valid.clone();
    case["layers"][1]["config"]["apps"]
        .as_object_mut()
        .unwrap()
        .remove(APP_NAME);
    assert_error(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&user)),
        "profile_unqualified",
    );

    let mut case = valid.clone();
    case["layers"][1]["config"]["mcp_servers"]["extra"] = json!({"enabled":false});
    assert_error(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&user)),
        "profile_unqualified",
    );

    let mut case = valid.clone();
    case["layers"][1]["config"]["plugins"]["chrome@openai-bundled"] = json!(false);
    assert_error(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&user)),
        "profile_unqualified",
    );
}

#[test]
fn feature_pages_accept_only_complete_bounded_closed_state() {
    assert_eq!(launch_policy::REQUIRED_DISABLED_FEATURES.len(), 35);
    assert_eq!(ALLOWED_ENABLED_FEATURES.len(), 17);
    let mut data = complete_feature_data();
    data.extend(
        ALLOWED_ENABLED_FEATURES
            .iter()
            .map(|name| feature(name, true)),
    );
    let split = data.len() / 2;
    let pages = vec![
        json!({"data":data[..split],"nextCursor":"page-two"}),
        json!({"data":data[split..],"nextCursor":null}),
    ];
    assert_eq!(
        effective_profile::validate_feature_pages(
            &pages,
            launch_policy::REQUIRED_DISABLED_FEATURES,
        )
        .unwrap(),
        json!({"disabled_required":35,"feature_count":52,"pages":2})
    );

    assert_error(
        effective_profile::validate_feature_pages(&[], launch_policy::REQUIRED_DISABLED_FEATURES),
        "protocol_error",
    );
    assert_error(
        effective_profile::validate_feature_pages(&pages, &[]),
        "protocol_error",
    );
    assert_error(
        effective_profile::validate_feature_pages(&pages, &["hooks"]),
        "protocol_error",
    );

    let eleven_pages = vec![json!({"data":[],"nextCursor":null}); 11];
    assert_error(
        effective_profile::validate_feature_pages(
            &eleven_pages,
            launch_policy::REQUIRED_DISABLED_FEATURES,
        ),
        "protocol_error",
    );

    let oversized = vec![json!({
        "data":(0..101).map(|index| feature(&format!("inactive-{index}"),false)).collect::<Vec<_>>(),
        "nextCursor":null
    })];
    assert_error(
        effective_profile::validate_feature_pages(
            &oversized,
            launch_policy::REQUIRED_DISABLED_FEATURES,
        ),
        "protocol_error",
    );

    let mut case = vec![json!({"data":complete_feature_data(),"nextCursor":null})];
    case[0]["data"][0]["stage"] = json!("future-stage");
    assert_error(
        effective_profile::validate_feature_pages(&case, launch_policy::REQUIRED_DISABLED_FEATURES),
        "protocol_error",
    );

    let mut duplicate = complete_feature_data();
    duplicate.push(duplicate[0].clone());
    assert_error(
        effective_profile::validate_feature_pages(
            &[json!({"data":duplicate,"nextCursor":null})],
            launch_policy::REQUIRED_DISABLED_FEATURES,
        ),
        "protocol_error",
    );

    let repeated_cursor = vec![
        json!({"data":[],"nextCursor":"repeat"}),
        json!({"data":[],"nextCursor":"repeat"}),
        json!({"data":complete_feature_data(),"nextCursor":null}),
    ];
    assert_error(
        effective_profile::validate_feature_pages(
            &repeated_cursor,
            launch_policy::REQUIRED_DISABLED_FEATURES,
        ),
        "protocol_error",
    );

    let unfinished = vec![json!({"data":complete_feature_data(),"nextCursor":"more"})];
    assert_error(
        effective_profile::validate_feature_pages(
            &unfinished,
            launch_policy::REQUIRED_DISABLED_FEATURES,
        ),
        "protocol_error",
    );

    let mut unknown_enabled = complete_feature_data();
    unknown_enabled.push(feature("future_effectful_feature", true));
    assert_error(
        effective_profile::validate_feature_pages(
            &[json!({"data":unknown_enabled,"nextCursor":null})],
            launch_policy::REQUIRED_DISABLED_FEATURES,
        ),
        "profile_unqualified",
    );
}

#[test]
fn hooks_cover_supported_shapes_without_retaining_payloads() {
    let cwd = PathBuf::from(r"C:\qa\fixture");
    let events = [
        "preToolUse",
        "permissionRequest",
        "postToolUse",
        "preCompact",
        "postCompact",
        "sessionStart",
        "sessionEnd",
        "userPromptSubmit",
        "subagentStart",
        "subagentStop",
        "stop",
        "interrupt",
    ];
    let sources = [
        "system",
        "user",
        "project",
        "mdm",
        "sessionFlags",
        "plugin",
        "cloudRequirements",
        "cloudManagedConfig",
        "legacyManagedConfigFile",
        "legacyManagedConfigMdm",
        "unknown",
    ];
    let trusts = ["managed", "untrusted", "trusted", "modified"];
    let handlers = ["command", "mcpTool", "prompt", "agent"];
    let hooks: Vec<Value> = events
        .iter()
        .enumerate()
        .map(|(index, event)| {
            hook(
                &format!("hook-{index}"),
                event,
                sources[index % sources.len()],
                trusts[index % trusts.len()],
                handlers[index % handlers.len()],
            )
        })
        .collect();
    let value = json!({"data":[{"cwd":cwd,"errors":[],"warnings":[],"hooks":hooks}]});
    let projection = effective_profile::validate_hooks(&value, &cwd).unwrap();
    assert_eq!(
        projection,
        json!({"configured_hook_count":12,"cwd_count":1,"errors":0,"warnings":0})
    );
    let text = projection.to_string();
    for forbidden in ["sensitive", "hook-", "reviewed"] {
        assert!(!text.contains(forbidden));
    }

    let mut case = value.clone();
    case["data"][0]["hooks"][1]["key"] = case["data"][0]["hooks"][0]["key"].clone();
    assert_error(
        effective_profile::validate_hooks(&case, &cwd),
        "profile_unqualified",
    );

    let mut case = value.clone();
    case["data"][0]["hooks"][0]["enabled"] = json!(true);
    assert_error(
        effective_profile::validate_hooks(&case, &cwd),
        "profile_unqualified",
    );

    for (field, bad) in [
        ("eventName", "futureEvent"),
        ("source", "futureSource"),
        ("trustStatus", "futureTrust"),
        ("handlerType", "futureHandler"),
    ] {
        let mut case = value.clone();
        case["data"][0]["hooks"][0][field] = json!(bad);
        assert_error(
            effective_profile::validate_hooks(&case, &cwd),
            "protocol_error",
        );
    }

    let mut case = value.clone();
    case["data"][0]["hooks"][1]
        .as_object_mut()
        .unwrap()
        .remove("tool");
    assert_error(
        effective_profile::validate_hooks(&case, &cwd),
        "protocol_error",
    );

    let oversized = json!({"data":[{
        "cwd":cwd,"errors":[],"warnings":[],"hooks":vec![Value::Null;1_001]
    }]});
    assert_error(
        effective_profile::validate_hooks(&oversized, &cwd),
        "protocol_error",
    );
}

#[test]
fn plugins_cover_supported_sources_and_reject_active_or_unbounded_state() {
    let plugins = vec![
        plugin(
            "local-plugin",
            json!({"type":"local","path":r"C:\reviewed\local"}),
            "ON_INSTALL",
            "NOT_AVAILABLE",
            false,
        ),
        plugin(
            "git-plugin",
            json!({"type":"git","url":"https://example.invalid/repository"}),
            "ON_USE",
            "AVAILABLE",
            true,
        ),
        plugin(
            "npm-plugin",
            json!({"type":"npm","package":"@reviewed/package"}),
            "ON_INSTALL",
            "INSTALLED_BY_DEFAULT",
            true,
        ),
        plugin(
            "remote-plugin",
            json!({"type":"remote"}),
            "ON_USE",
            "AVAILABLE",
            false,
        ),
    ];
    let value = json!({
        "marketplaces":[{"name":"reviewed-market","path":null,"plugins":plugins}],
        "marketplaceLoadErrors":[],
        "featuredPluginIds":["local-plugin"]
    });
    let projection = effective_profile::validate_plugins(&value).unwrap();
    assert_eq!(
        projection,
        json!({"enabled_plugin_count":0,"installed_plugin_count":2,"marketplace_count":1,"plugin_count":4})
    );
    let text = projection.to_string();
    for forbidden in ["reviewed-market", "local-plugin", "example.invalid"] {
        assert!(!text.contains(forbidden));
    }

    let too_many_markets = json!({
        "marketplaces":vec![json!({"name":"m","plugins":[]});101],
        "marketplaceLoadErrors":[]
    });
    assert_error(
        effective_profile::validate_plugins(&too_many_markets),
        "protocol_error",
    );

    let mut case = value.clone();
    case["marketplaceLoadErrors"] = json!([{"message":"load failed"}]);
    assert_error(
        effective_profile::validate_plugins(&case),
        "profile_unqualified",
    );

    let mut case = value.clone();
    case["marketplaces"][0]["path"] = json!(7);
    assert_error(effective_profile::validate_plugins(&case), "protocol_error");

    let mut case = value.clone();
    case["marketplaces"][0]["plugins"][1]["id"] = json!("local-plugin");
    assert_error(
        effective_profile::validate_plugins(&case),
        "profile_unqualified",
    );

    let mut case = value.clone();
    case["marketplaces"][0]["plugins"][0]["enabled"] = json!(true);
    assert_error(
        effective_profile::validate_plugins(&case),
        "profile_unqualified",
    );

    for (field, bad) in [("authPolicy", "SOMEDAY"), ("installPolicy", "SECRET")] {
        let mut case = value.clone();
        case["marketplaces"][0]["plugins"][0][field] = json!(bad);
        assert_error(effective_profile::validate_plugins(&case), "protocol_error");
    }

    for source in [
        json!({"type":"local"}),
        json!({"type":"git"}),
        json!({"type":"npm"}),
        json!({"type":"future"}),
    ] {
        let mut case = value.clone();
        case["marketplaces"][0]["plugins"][0]["source"] = source;
        assert_error(effective_profile::validate_plugins(&case), "protocol_error");
    }

    let many_plugins: Vec<Value> = (0..1_001)
        .map(|index| {
            plugin(
                &format!("plugin-{index}"),
                json!({"type":"remote"}),
                "ON_USE",
                "AVAILABLE",
                false,
            )
        })
        .collect();
    let oversized = json!({
        "marketplaces":[{"name":"m","plugins":many_plugins}],
        "marketplaceLoadErrors":[]
    });
    assert_error(
        effective_profile::validate_plugins(&oversized),
        "protocol_error",
    );
}

#[test]
fn apps_require_unique_disabled_non_callable_bounded_state() {
    let valid = json!({"apps":[
        {"id":"missing-runtime","enabled":false,"callable":false},
        {"id":"null-runtime","enabled":false,"callable":false,"runtimeName":null},
        {"id":"named-runtime","enabled":false,"callable":false,"runtimeName":"sensitive-runtime"}
    ]});
    let projection = effective_profile::validate_apps(&valid).unwrap();
    assert_eq!(
        projection,
        json!({"app_count":3,"callable_app_count":0,"enabled_app_count":0})
    );
    assert!(!projection.to_string().contains("sensitive-runtime"));

    let mut case = valid.clone();
    case["apps"][1]["id"] = json!("missing-runtime");
    assert_error(
        effective_profile::validate_apps(&case),
        "profile_unqualified",
    );

    for field in ["enabled", "callable"] {
        let mut case = valid.clone();
        case["apps"][0][field] = json!(true);
        assert_error(
            effective_profile::validate_apps(&case),
            "profile_unqualified",
        );
    }

    let mut case = valid.clone();
    case["apps"][0]["runtimeName"] = json!(42);
    assert_error(effective_profile::validate_apps(&case), "protocol_error");

    let oversized = json!({"apps":vec![Value::Null;1_001]});
    assert_error(
        effective_profile::validate_apps(&oversized),
        "protocol_error",
    );
}

#[test]
fn mcp_pages_require_inactive_empty_unique_complete_state() {
    let auth_states = [
        "unknown",
        "unsupported",
        "notLoggedIn",
        "bearerToken",
        "oAuth",
    ];
    let servers: Vec<Value> = auth_states
        .iter()
        .enumerate()
        .map(|(index, auth)| mcp(&format!("server-{index}"), auth))
        .collect();
    let pages = vec![json!({"data":servers,"nextCursor":null})];
    assert_eq!(
        effective_profile::validate_mcp_pages(&pages).unwrap(),
        json!({"disabled_server_count":5,"pages":1,"server_count":5})
    );

    assert_error(effective_profile::validate_mcp_pages(&[]), "protocol_error");
    assert_error(
        effective_profile::validate_mcp_pages(&vec![json!({"data":[],"nextCursor":null}); 11]),
        "protocol_error",
    );
    assert_error(
        effective_profile::validate_mcp_pages(&[json!({
            "data":(0..101).map(|index| mcp(&format!("server-{index}"),"unknown")).collect::<Vec<_>>(),
            "nextCursor":null
        })]),
        "protocol_error",
    );

    let mut case = pages.clone();
    case[0]["data"][1]["name"] = json!("server-0");
    assert_error(
        effective_profile::validate_mcp_pages(&case),
        "protocol_error",
    );

    let mut case = pages.clone();
    case[0]["data"][0]["runtimeStatus"] = json!("starting");
    assert_error(
        effective_profile::validate_mcp_pages(&case),
        "profile_unqualified",
    );

    let mut case = pages.clone();
    case[0]["data"][0]["authStatus"] = json!("futureAuth");
    assert_error(
        effective_profile::validate_mcp_pages(&case),
        "protocol_error",
    );

    for (field, value) in [
        ("tools", json!({"danger":{"description":"tool"}})),
        ("resources", json!([{"uri":"secret"}])),
        ("resourceTemplates", json!([{"uriTemplate":"secret"}])),
        ("toolsError", json!({"message":"secret"})),
    ] {
        let mut case = pages.clone();
        case[0]["data"][0][field] = value;
        assert_error(
            effective_profile::validate_mcp_pages(&case),
            "profile_unqualified",
        );
    }

    let repeated_cursor = vec![
        json!({"data":[],"nextCursor":"same"}),
        json!({"data":[],"nextCursor":"same"}),
        json!({"data":[],"nextCursor":null}),
    ];
    assert_error(
        effective_profile::validate_mcp_pages(&repeated_cursor),
        "protocol_error",
    );
}

#[test]
fn requirements_and_public_roots_preserve_typed_error_boundaries() {
    assert_eq!(
        effective_profile::validate_requirements(&json!({"requirements":null})).unwrap(),
        json!({"requirements_present":false})
    );
    assert_error(
        effective_profile::validate_requirements(&json!({"requirements":{}})),
        "profile_unqualified",
    );
    assert_error(
        effective_profile::validate_requirements(&json!({})),
        "protocol_error",
    );
    assert_error(
        effective_profile::validate_requirements(&json!([])),
        "protocol_error",
    );

    let cwd = Path::new(r"C:\qa\fixture");
    assert_error(
        effective_profile::validate_config(&json!([]), cwd, &[]),
        "protocol_error",
    );
    assert_error(
        effective_profile::validate_hooks(&json!([]), cwd),
        "protocol_error",
    );
    assert_error(
        effective_profile::validate_plugins(&json!([])),
        "protocol_error",
    );
    assert_error(
        effective_profile::validate_apps(&json!([])),
        "protocol_error",
    );
    assert_error(
        effective_profile::validate_mcp_pages(&[json!([])]),
        "protocol_error",
    );
}
