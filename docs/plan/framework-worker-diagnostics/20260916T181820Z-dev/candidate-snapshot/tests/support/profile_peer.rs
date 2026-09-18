// External profile-preflight peer. It records and validates the worker's
// outbound protocol without importing production validation predicates.
use serde_json::{Value, json};
use std::{
    fs::OpenOptions,
    io::{self, BufRead, Write},
    os::windows::process::CommandExt,
    path::PathBuf,
    time::Duration,
};

const FEATURES: &[&str] = &[
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
const PLUGINS: &[&str] = &[
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

fn send(value: Value) {
    println!("{value}");
    io::stdout().flush().unwrap();
}

fn result(id: &Value, value: Value) {
    send(json!({"id":id,"result":value}));
}

fn main() {
    let args: Vec<_> = std::env::args().collect();
    if args.get(1).is_some_and(|arg| arg == "--transient") {
        return;
    }
    assert_eq!(args.len(), 7);
    assert_eq!(args[1], "--case");
    let case = &args[2];
    assert_eq!(args[3], "--trace");
    let trace_path = PathBuf::from(&args[4]);
    assert_eq!(args[5], "--fixture-root");
    let root = PathBuf::from(&args[6]);
    let covered = root.join("peer-case.txt");
    let mut trace = OpenOptions::new()
        .create_new(true)
        .write(true)
        .open(&trace_path)
        .unwrap();
    let mut expected_id = 1_u64;
    let mut feature_pages = 0_u8;
    let mut mcp_pages = 0_u8;

    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        writeln!(trace, "{line}").unwrap();
        trace.sync_all().unwrap();
        let value: Value = serde_json::from_str(&line).unwrap();
        let method = value["method"].as_str().unwrap();
        let params = &value["params"];
        if method == "initialized" {
            assert_eq!(params, &json!({}));
            continue;
        }
        let id = &value["id"];
        assert_eq!(id, &json!(expected_id));
        expected_id += 1;

        if case == "initialize-rpc-error" && method == "initialize" {
            send(
                json!({"id":id,"error":{"code":-32603,"message":"PRIVATE_RPC_MESSAGE","unknown":{"token":"PRIVATE_TOKEN"}}}),
            );
            continue;
        }
        if case == "initialize-exit" && method == "initialize" {
            return;
        }
        if case == "config-descendant" && method == "config/read" {
            let status = std::process::Command::new(std::env::current_exe().unwrap())
                .arg("--transient")
                .creation_flags(windows_sys::Win32::System::Threading::DETACHED_PROCESS)
                .status()
                .unwrap();
            assert!(status.success());
        }

        if case == "rpc-error" && method == "config/read" {
            send(json!({"id":id,"error":{"code":-32603,"message":"PRIVATE_RPC_MESSAGE"}}));
            continue;
        }
        if case == "timeout" && method == "initialize" {
            std::thread::sleep(Duration::from_secs(30));
            continue;
        }
        if case == "notification" && method == "initialize" {
            send(json!({"method":"turn/started","params":{"private":"PRIVATE_NOTIFICATION"}}));
        }

        match method {
            "initialize" => {
                assert_eq!(
                    params,
                    &json!({"clientInfo":{"name":"devforgeai_worker_probe","version":"0.1.0"},"capabilities":{"experimentalApi":false}})
                );
                if case == "transient-descendant" || case == "diagnostic-transient" {
                    let mut child = std::process::Command::new(std::env::current_exe().unwrap());
                    child.arg("--transient");
                    if case == "diagnostic-transient" {
                        child.creation_flags(
                            windows_sys::Win32::System::Threading::DETACHED_PROCESS,
                        );
                    }
                    let status = child.status().unwrap();
                    assert!(status.success());
                }
                result(id, json!({"userAgent":"synthetic-profile-peer"}));
            }
            "config/read" => {
                assert_eq!(params, &json!({"cwd":root,"includeLayers":true}));
                let fixed = json!({
                    "model_provider":"openai",
                    "forced_login_method":"chatgpt",
                    "web_search":"disabled",
                    "sandbox_mode":"read-only",
                    "approval_policy":"never",
                    "features":FEATURES.iter().map(|name| ((*name).to_owned(), Value::Bool(false))).collect::<serde_json::Map<String,Value>>(),
                    "apps":{"_default":{"enabled":false},"connector_openai_codex_document_control":{"enabled":false}},
                    "mcp_servers":{"node_repl":{"enabled":false},"openaiDeveloperDocs":{"enabled":false}},
                    "plugins":PLUGINS.iter().map(|name| ((*name).to_owned(), json!({"enabled":false}))).collect::<serde_json::Map<String,Value>>()
                });
                let mut config = fixed.clone();
                if case == "active-config" {
                    config["sandbox_mode"] = json!("workspace-write");
                    config["PRIVATE_KEY"] = json!({"token":"PRIVATE_TOKEN"});
                }
                if case == "secret-config" {
                    config["private"] = json!("PRIVATE_CONFIG_SENTINEL");
                }
                let mut response = json!({
                    "config":config,
                    "layers":[
                        {"name":{"type":"user","file":covered,"profile":null},"version":"1","disabledReason":null,"config":{"unretained_secret":"PRIVATE_LAYER_SECRET"}},
                        {"name":{"type":"sessionFlags"},"version":"1","disabledReason":null,"config":fixed}
                    ],
                    "origins":{
                        "model_provider":{"name":{"type":"sessionFlags"},"version":"1"},
                        "forced_login_method":{"name":{"type":"sessionFlags"},"version":"1"},
                        "web_search":{"name":{"type":"sessionFlags"},"version":"1"},
                        "sandbox_mode":{"name":{"type":"sessionFlags"},"version":"1"},
                        "approval_policy":{"name":{"type":"sessionFlags"},"version":"1"}
                    }
                });
                match case.as_str() {
                    "config-layer-source" => {
                        response["layers"][0]["name"]["type"] = json!("PRIVATE_UNKNOWN_SOURCE")
                    }
                    "config-layer-key" => {
                        response["layers"][1]["config"]["PRIVATE_KEY"] = json!("PRIVATE_VALUE")
                    }
                    "config-origin" => {
                        response["origins"]["model_provider"]["name"]["type"] =
                            json!("PRIVATE_ORIGIN")
                    }
                    "config-shape" => response["config"] = json!(["PRIVATE_SECRET"]),
                    _ => {}
                }
                result(id, response);
            }
            "configRequirements/read" => {
                assert_eq!(params, &json!({}));
                let requirements = if case == "requirement-conflict" {
                    json!({"allowed_sandbox_modes":["workspace-write"]})
                } else {
                    Value::Null
                };
                result(id, json!({"requirements":requirements}));
            }
            "experimentalFeature/list" => {
                feature_pages += 1;
                assert_eq!(params["limit"], 100);
                assert!(params["threadId"].is_null());
                if feature_pages == 1 {
                    assert!(params["cursor"].is_null());
                }
                let mut data: Vec<Value> = FEATURES
                    .iter()
                    .map(|name| json!({"name":name,"enabled":false,"defaultEnabled":false,"stage":"stable"}))
                    .collect();
                if case == "active-feature" {
                    data[0]["enabled"] = json!(true);
                } else if case == "missing-feature" {
                    data.pop();
                }
                let next = match case.as_str() {
                    "feature-bad-cursor" => json!(7),
                    "feature-loop" => json!(format!("feature-{feature_pages}")),
                    _ => Value::Null,
                };
                let mut response = json!({"data":data,"nextCursor":next});
                if case == "feature-omitted-cursor" {
                    response.as_object_mut().unwrap().remove("nextCursor");
                }
                result(id, response);
            }
            "hooks/list" => {
                assert_eq!(params, &json!({"cwds":[root]}));
                let hooks = if case == "active-hook" {
                    vec![
                        json!({"currentHash":"h","displayOrder":0,"enabled":true,"eventName":"sessionStart","isManaged":false,"key":"k","source":"user","sourcePath":covered,"timeoutSec":1,"trustStatus":"trusted","handlerType":"command","command":"PRIVATE_HOOK_COMMAND"}),
                    ]
                } else {
                    vec![]
                };
                let errors = if case == "hook-error" {
                    vec![json!({"path":"PRIVATE_HOOK_PATH","message":"PRIVATE_HOOK_MESSAGE"})]
                } else {
                    vec![]
                };
                result(
                    id,
                    json!({"data":[{"cwd":root,"errors":errors,"hooks":hooks,"warnings":[]}]}),
                );
            }
            "plugin/list" => {
                assert_eq!(
                    params,
                    &json!({"cwds":[root],"forceRefetch":false,"marketplaceKinds":["local"]})
                );
                let plugins = if case == "active-plugin" || case == "secret-plugin" {
                    vec![
                        json!({"id":"private-plugin","name":"PRIVATE_PLUGIN_SENTINEL","enabled":case=="active-plugin","installed":true,"authPolicy":"ON_USE","installPolicy":"AVAILABLE","source":{"type":"local","path":covered}}),
                    ]
                } else {
                    vec![]
                };
                let marketplaces = if plugins.is_empty() {
                    vec![]
                } else {
                    vec![json!({"id":"local","name":"local","kind":"local","plugins":plugins})]
                };
                let errors = if case == "plugin-error" {
                    vec![json!({"marketplace":"local","message":"PRIVATE_PLUGIN_ERROR"})]
                } else {
                    vec![]
                };
                result(
                    id,
                    json!({"marketplaces":marketplaces,"marketplaceLoadErrors":errors,"featuredPluginIds":[]}),
                );
            }
            "app/installed" => {
                assert_eq!(params, &json!({"forceRefresh":false,"threadId":null}));
                result(
                    id,
                    json!({"apps":[{"id":"connector_openai_codex_document_control","enabled":case=="active-app","callable":case=="active-app","runtimeName":null}]}),
                );
            }
            "mcpServerStatus/list" => {
                mcp_pages += 1;
                assert_eq!(params["limit"], 100);
                assert!(params["threadId"].is_null());
                assert_eq!(params["detail"], "toolsAndAuthOnly");
                let active = case == "active-mcp";
                let data = ["node_repl", "openaiDeveloperDocs"]
                    .into_iter()
                    .map(|name| json!({"name":name,"authStatus":"unknown","resourceTemplates":[],"resources":[],"tools":if active {json!({"private":{"name":"private","inputSchema":{}}})} else {json!({})},"toolsError":null,"runtimeStatus":if active {json!("connected")} else {json!("disabled")},"serverInfo":null,"pluginId":null}))
                    .collect::<Vec<_>>();
                let next = if case == "mcp-loop" {
                    json!(format!("mcp-{mcp_pages}"))
                } else {
                    Value::Null
                };
                let mut response = json!({"data":data,"nextCursor":next});
                if case == "mcp-omitted-cursor" {
                    response.as_object_mut().unwrap().remove("nextCursor");
                }
                result(id, response);
            }
            "account/read" => {
                assert_eq!(params, &json!({"refreshToken":false}));
                result(
                    id,
                    json!({"account":{"type":"chatgpt","email":"PRIVATE_EMAIL","planType":if case=="wrong-account" {"plus"} else {"pro"}},"requiresOpenaiAuth":true}),
                );
            }
            "model/list" => {
                assert_eq!(params["limit"], 100);
                result(
                    id,
                    json!({"data":[{"id":"test-model","model":"test-model","description":"test","displayName":"test","hidden":false,"isDefault":true,"defaultReasoningEffort":"test-effort","supportedReasoningEfforts":[{"reasoningEffort":"test-effort","description":"test"}]}],"nextCursor":null}),
                );
            }
            "account/rateLimits/read" => {
                assert_eq!(params, &json!({}));
                let limits = match case.as_str() {
                    "rate-limit-missing" => json!({"primary":{},"secondary":null}),
                    "rate-limit-malformed" => {
                        json!({"primary":{"usedPercent":"unknown"},"secondary":null})
                    }
                    "rate-limit-exhausted" => {
                        json!({"primary":{"usedPercent":100},"secondary":null})
                    }
                    _ => json!({"primary":{"usedPercent":0},"secondary":null}),
                };
                result(id, json!({"rateLimits":limits}));
            }
            _ => panic!("unexpected outbound method: {method}"),
        }
    }
}
