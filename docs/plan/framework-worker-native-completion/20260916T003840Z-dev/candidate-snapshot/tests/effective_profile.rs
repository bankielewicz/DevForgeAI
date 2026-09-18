use devforgeai_codex_worker_probe::{effective_profile, launch_policy};
use serde_json::{Map, Value, json};
use std::path::{Path, PathBuf};

fn disabled_features() -> Value {
    Value::Object(
        launch_policy::REQUIRED_DISABLED_FEATURES
            .iter()
            .map(|name| ((*name).to_owned(), Value::Bool(false)))
            .collect(),
    )
}

fn disabled_named(names: &[&str]) -> Value {
    Value::Object(
        names
            .iter()
            .map(|name| ((*name).to_owned(), json!({"enabled":false})))
            .collect(),
    )
}

fn fixed_config() -> Value {
    json!({
        "model_provider":"openai",
        "forced_login_method":"chatgpt",
        "web_search":"disabled",
        "sandbox_mode":"read-only",
        "approval_policy":"never",
        "features":disabled_features(),
        "apps":{
            "_default":{"enabled":false},
            "connector_openai_codex_document_control":{"enabled":false}
        },
        "mcp_servers":disabled_named(&["node_repl","openaiDeveloperDocs"]),
        "plugins":disabled_named(&[
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
            "chrome@openai-bundled"
        ])
    })
}

fn config_response(user_config: &Path) -> Value {
    let fixed = fixed_config();
    let mut origins = Map::new();
    for key in [
        "model_provider",
        "forced_login_method",
        "web_search",
        "sandbox_mode",
        "approval_policy",
    ] {
        origins.insert(
            key.to_owned(),
            json!({"name":{"type":"sessionFlags"},"version":"1"}),
        );
    }
    json!({
        "config":fixed,
        "origins":origins,
        "layers":[
            {
                "config":{"unretained_secret":"must-never-be-journaled"},
                "disabledReason":null,
                "name":{"type":"user","file":user_config,"profile":null},
                "version":"1"
            },
            {
                "config":fixed_config(),
                "disabledReason":null,
                "name":{"type":"sessionFlags"},
                "version":"1"
            }
        ]
    })
}

fn feature(name: &str, enabled: bool) -> Value {
    json!({
        "name":name,
        "enabled":enabled,
        "defaultEnabled":true,
        "stage":"stable",
        "description":"not retained",
        "displayName":"not retained",
        "announcement":null
    })
}

#[test]
fn pinned_profile_observations_validate_and_project_only_approved_fields() {
    let cwd = PathBuf::from(r"C:\qa\fixture");
    let user_config = PathBuf::from(r"C:\Users\qa\.codex\config.toml");
    let config = effective_profile::validate_config(
        &config_response(&user_config),
        &cwd,
        std::slice::from_ref(&user_config),
    )
    .unwrap();
    assert_eq!(
        config,
        json!({
            "approval_policy":"never",
            "apps_default_enabled":false,
            "config_layer_count":2,
            "covered_disk_layer_count":1,
            "forced_login_method":"chatgpt",
            "model_provider":"openai",
            "sandbox_mode":"read-only",
            "session_flags_layers":1,
            "web_search":"disabled"
        })
    );

    assert_eq!(
        effective_profile::validate_requirements(&json!({"requirements":null})).unwrap(),
        json!({"requirements_present":false})
    );

    let required = launch_policy::REQUIRED_DISABLED_FEATURES;
    let split = required.len() / 2;
    let feature_pages = vec![
        json!({
            "data":required[..split].iter().map(|name| feature(name,false)).collect::<Vec<_>>(),
            "nextCursor":"opaque-secret-cursor"
        }),
        json!({
            "data":required[split..].iter().map(|name| feature(name,false)).chain([feature("safe_other",false)]).collect::<Vec<_>>(),
            "nextCursor":null
        }),
    ];
    assert_eq!(
        effective_profile::validate_feature_pages(&feature_pages, required).unwrap(),
        json!({"disabled_required":required.len(),"feature_count":required.len()+1,"pages":2})
    );

    let hooks = json!({"data":[{
        "cwd":cwd,
        "errors":[],
        "warnings":[],
        "hooks":[{
            "key":"sensitive-hook-id",
            "currentHash":"not-retained",
            "displayOrder":0,
            "enabled":false,
            "eventName":"sessionStart",
            "isManaged":false,
            "source":"user",
            "sourcePath":r"C:\Users\qa\.codex\hooks.json",
            "timeoutSec":5,
            "trustStatus":"trusted",
            "handlerType":"command",
            "command":"secret command is never retained"
        }]
    }]});
    assert_eq!(
        effective_profile::validate_hooks(&hooks, &cwd).unwrap(),
        json!({"configured_hook_count":1,"cwd_count":1,"errors":0,"warnings":0})
    );

    let plugins = json!({
        "marketplaces":[{"name":"secret-market","path":r"C:\secret", "plugins":[{
            "id":"secret-plugin-id","name":"secret name","enabled":false,"installed":true,
            "source":{"type":"local","path":r"C:\secret\plugin"},
            "authPolicy":"ON_USE","installPolicy":"AVAILABLE"
        }]}],
        "marketplaceLoadErrors":[],
        "featuredPluginIds":["secret-plugin-id"]
    });
    assert_eq!(
        effective_profile::validate_plugins(&plugins).unwrap(),
        json!({"enabled_plugin_count":0,"installed_plugin_count":1,"marketplace_count":1,"plugin_count":1})
    );

    let apps = json!({"apps":[{
        "id":"secret-app-id","enabled":false,"callable":false,"runtimeName":"secret runtime"
    }]});
    assert_eq!(
        effective_profile::validate_apps(&apps).unwrap(),
        json!({"app_count":1,"callable_app_count":0,"enabled_app_count":0})
    );

    let mcp_pages = vec![
        json!({"data":[{
            "name":"secret-mcp-a","authStatus":"unsupported","runtimeStatus":"disabled",
            "pluginId":null,"serverInfo":null,"tools":{},"toolsError":null,
            "resources":[],"resourceTemplates":[]
        }],"nextCursor":"another-secret-cursor"}),
        json!({"data":[{
            "name":"secret-mcp-b","authStatus":"unknown","runtimeStatus":"disabled",
            "pluginId":"secret-plugin-id","serverInfo":null,"tools":{},"toolsError":null,
            "resources":[],"resourceTemplates":[]
        }],"nextCursor":null}),
    ];
    assert_eq!(
        effective_profile::validate_mcp_pages(&mcp_pages).unwrap(),
        json!({"disabled_server_count":2,"pages":2,"server_count":2})
    );

    let combined = json!([
        config,
        effective_profile::validate_feature_pages(&feature_pages, required).unwrap(),
        effective_profile::validate_hooks(&hooks, &cwd).unwrap(),
        effective_profile::validate_plugins(&plugins).unwrap(),
        effective_profile::validate_apps(&apps).unwrap(),
        effective_profile::validate_mcp_pages(&mcp_pages).unwrap()
    ])
    .to_string();
    for secret in [
        "must-never",
        "opaque-secret",
        "secret-hook",
        "secret command",
        "secret-plugin",
        "secret-app",
        "secret-mcp",
        r"C:\secret",
    ] {
        assert!(!combined.contains(secret), "projection leaked {secret}");
    }
}

#[test]
fn unsafe_incomplete_or_malformed_observations_fail_closed() {
    let cwd = PathBuf::from(r"C:\qa\fixture");
    let source = PathBuf::from(r"C:\Users\qa\.codex\config.toml");
    let valid = config_response(&source);

    let mut case = valid.clone();
    case["config"]["sandbox_mode"] = json!("danger-full-access");
    assert!(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&source)).is_err()
    );
    let mut case = valid.clone();
    case["config"]["model_providers"] =
        json!({"openai":{"base_url":"https://private-provider.invalid"}});
    assert!(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&source)).is_err()
    );
    let mut case = valid.clone();
    case["config"]["chatgpt_base_url"] = json!("https://private-provider.invalid");
    assert!(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&source)).is_err()
    );
    let mut case = valid.clone();
    case["layers"][1]["config"]["features"]["hooks"] = json!(true);
    assert!(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&source)).is_err()
    );
    let mut case = valid.clone();
    case["layers"][0]["name"]["file"] = json!(r"C:\unreviewed\config.toml");
    assert!(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&source)).is_err()
    );
    let mut case = valid.clone();
    case["layers"][1]["name"]["type"] = json!("enterpriseManaged");
    assert!(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&source)).is_err()
    );
    let mut case = valid.clone();
    case["origins"]["model_provider"]["name"]["type"] = json!("user");
    assert!(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&source)).is_err()
    );
    let mut case = valid.clone();
    case["origins"]["unrelated_setting"] =
        json!({"name":{"type":"enterpriseManaged","id":"managed","name":"policy"},"version":"1"});
    assert!(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&source)).is_err()
    );
    let mut case = valid.clone();
    case["origins"]["unrelated_setting"] = json!({
        "name":{"type":"user","file":r"C:\unreviewed\config.toml","profile":null},
        "version":"1"
    });
    assert!(
        effective_profile::validate_config(&case, &cwd, std::slice::from_ref(&source)).is_err()
    );
    assert!(
        effective_profile::validate_requirements(
            &json!({"requirements":{"featureRequirements":{"hooks":true}}})
        )
        .is_err()
    );

    let required = launch_policy::REQUIRED_DISABLED_FEATURES;
    let pages = vec![
        json!({"data":required.iter().map(|name| feature(name,false)).collect::<Vec<_>>(),"nextCursor":null}),
    ];
    let mut case = pages.clone();
    case[0]["data"][0]["enabled"] = json!(true);
    assert!(effective_profile::validate_feature_pages(&case, required).is_err());
    let mut case = pages.clone();
    case[0]["data"].as_array_mut().unwrap().pop();
    assert!(effective_profile::validate_feature_pages(&case, required).is_err());
    let mut case = pages.clone();
    case[0]["nextCursor"] = json!("unfinished");
    assert!(effective_profile::validate_feature_pages(&case, required).is_err());
    for enabled_unknown in ["js_repl", "new_unknown"] {
        let mut case = pages.clone();
        case[0]["data"]
            .as_array_mut()
            .unwrap()
            .push(feature(enabled_unknown, true));
        assert!(effective_profile::validate_feature_pages(&case, required).is_err());
    }

    for hooks in [
        json!({"data":[{"cwd":r"C:\other","errors":[],"warnings":[],"hooks":[]}]}),
        json!({"data":[{"cwd":cwd,"errors":[{"path":"x","message":"bad"}],"warnings":[],"hooks":[]}]}),
        json!({"data":[{"cwd":cwd,"errors":[],"warnings":["bad"],"hooks":[]}]}),
    ] {
        assert!(effective_profile::validate_hooks(&hooks, &cwd).is_err());
    }
    assert!(effective_profile::validate_plugins(&json!({"marketplaces":[{"name":"m","plugins":[{"id":"p","name":"p","enabled":true,"installed":true,"source":{"type":"local","path":"x"},"authPolicy":"x","installPolicy":"x"}]}],"marketplaceLoadErrors":[]})).is_err());
    assert!(
        effective_profile::validate_apps(
            &json!({"apps":[{"id":"a","enabled":false,"callable":true}]})
        )
        .is_err()
    );
    assert!(effective_profile::validate_mcp_pages(&[json!({"data":[{"name":"m","authStatus":"unknown","runtimeStatus":"connected","tools":{},"toolsError":null,"resources":[],"resourceTemplates":[]}],"nextCursor":null})]).is_err());
    assert!(
        effective_profile::validate_mcp_pages(&[json!({"data":[],"nextCursor":"unfinished"})])
            .is_err()
    );
}
