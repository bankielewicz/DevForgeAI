// Independent protocol-edge peer for pre-thread preflight tests.
use serde_json::{Value, json};
use std::{
    fs::OpenOptions,
    io::{self, BufRead, Write},
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

fn fixed_config() -> Value {
    json!({
        "model_provider":"openai",
        "forced_login_method":"chatgpt",
        "web_search":"disabled",
        "sandbox_mode":"read-only",
        "approval_policy":"never",
        "features":FEATURES.iter().map(|name| ((*name).to_owned(), Value::Bool(false))).collect::<serde_json::Map<String,Value>>(),
        "apps":{"_default":{"enabled":false},"connector_openai_codex_document_control":{"enabled":false}},
        "mcp_servers":{"node_repl":{"enabled":false},"openaiDeveloperDocs":{"enabled":false}},
        "plugins":PLUGINS.iter().map(|name| ((*name).to_owned(), json!({"enabled":false}))).collect::<serde_json::Map<String,Value>>()
    })
}

fn main() {
    let args: Vec<_> = std::env::args().collect();
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
        .open(trace_path)
        .unwrap();
    let mut expected_id = 1_u64;
    let mut feature_pages = 0_u8;
    let mut awaiting_server_response: Option<&str> = None;

    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        writeln!(trace, "{line}").unwrap();
        trace.sync_all().unwrap();
        let value: Value = serde_json::from_str(&line).unwrap();

        if let Some(expected) = awaiting_server_response.take() {
            match expected {
                "approval" => assert_eq!(
                    value,
                    json!({"id":"server-approval","result":{"decision":"cancel"}})
                ),
                "unsupported" => assert_eq!(
                    value,
                    json!({"id":77,"error":{"code":-32601,"message":"Method not supported"}})
                ),
                _ => unreachable!(),
            }
            return;
        }

        let method = value["method"].as_str().unwrap();
        let params = &value["params"];
        if method == "initialized" {
            assert_eq!(params, &json!({}));
            continue;
        }
        let id = &value["id"];
        assert_eq!(id, &json!(expected_id));
        expected_id += 1;

        if method == "initialize" {
            assert_eq!(
                params,
                &json!({"clientInfo":{"name":"devforgeai_worker_probe","version":"0.1.0"},"capabilities":{"experimentalApi":false}})
            );
            match case.as_str() {
                "approval-request" => {
                    awaiting_server_response = Some("approval");
                    send(
                        json!({"id":"server-approval","method":"item/commandExecution/requestApproval","params":{"private":"PRIVATE_APPROVAL_REQUEST"}}),
                    );
                    continue;
                }
                "unsupported-request" => {
                    awaiting_server_response = Some("unsupported");
                    send(
                        json!({"id":77,"method":"account/login/start","params":{"private":"PRIVATE_UNSUPPORTED_REQUEST"}}),
                    );
                    continue;
                }
                "malformed-request-id" => {
                    send(
                        json!({"id":{"invalid":true},"method":"item/fileChange/requestApproval","params":{}}),
                    );
                    std::thread::sleep(Duration::from_secs(30));
                    continue;
                }
                "stderr" => {
                    eprintln!("PRIVATE_STDERR_SENTINEL");
                    io::stderr().flush().unwrap();
                    std::thread::sleep(Duration::from_millis(50));
                }
                _ => {}
            }
            result(id, json!({"userAgent":"synthetic-protocol-edges-peer"}));
            continue;
        }

        match method {
            "config/read" => {
                assert_eq!(params, &json!({"cwd":root,"includeLayers":true}));
                let fixed = fixed_config();
                result(
                    id,
                    json!({
                        "config":fixed,
                        "layers":[
                            {"name":{"type":"user","file":covered,"profile":null},"version":"1","disabledReason":null,"config":{}},
                            {"name":{"type":"sessionFlags"},"version":"1","disabledReason":null,"config":fixed}
                        ],
                        "origins":{
                            "model_provider":{"name":{"type":"sessionFlags"},"version":"1"},
                            "forced_login_method":{"name":{"type":"sessionFlags"},"version":"1"},
                            "web_search":{"name":{"type":"sessionFlags"},"version":"1"},
                            "sandbox_mode":{"name":{"type":"sessionFlags"},"version":"1"},
                            "approval_policy":{"name":{"type":"sessionFlags"},"version":"1"}
                        }
                    }),
                );
            }
            "configRequirements/read" => {
                assert_eq!(params, &json!({}));
                result(id, json!({"requirements":null}));
            }
            "experimentalFeature/list" => {
                feature_pages += 1;
                assert_eq!(params["limit"], 100);
                assert!(params["threadId"].is_null());
                let mut data: Vec<Value> = FEATURES
                    .iter()
                    .map(|name| json!({"name":name,"enabled":false,"defaultEnabled":false,"stage":"stable"}))
                    .collect();
                let next = match case.as_str() {
                    "feature-overflow" => {
                        for index in 0..66 {
                            data.push(json!({"name":format!("extra-{index}"),"enabled":false,"defaultEnabled":false,"stage":"stable"}));
                        }
                        Value::Null
                    }
                    "feature-repeat-cursor" => json!("repeat"),
                    "feature-ten-pages" => json!(format!("page-{feature_pages}")),
                    _ => Value::Null,
                };
                result(id, json!({"data":data,"nextCursor":next}));
            }
            "hooks/list" => {
                assert_eq!(params, &json!({"cwds":[root]}));
                result(
                    id,
                    json!({"data":[{"cwd":root,"errors":[],"hooks":[],"warnings":[]}]}),
                );
            }
            "plugin/list" => {
                assert_eq!(
                    params,
                    &json!({"cwds":[root],"forceRefetch":false,"marketplaceKinds":["local"]})
                );
                result(
                    id,
                    json!({"marketplaces":[],"marketplaceLoadErrors":[],"featuredPluginIds":[]}),
                );
            }
            "app/installed" => {
                assert_eq!(params, &json!({"forceRefresh":false,"threadId":null}));
                result(
                    id,
                    json!({"apps":[{"id":"connector_openai_codex_document_control","enabled":false,"callable":false,"runtimeName":null}]}),
                );
            }
            "mcpServerStatus/list" => {
                assert_eq!(params["limit"], 100);
                assert!(params["threadId"].is_null());
                assert_eq!(params["detail"], "toolsAndAuthOnly");
                let data = ["node_repl", "openaiDeveloperDocs"]
                    .into_iter()
                    .map(|name| json!({"name":name,"authStatus":"unknown","resourceTemplates":[],"resources":[],"tools":{},"toolsError":null,"runtimeStatus":"disabled","serverInfo":null,"pluginId":null}))
                    .collect::<Vec<_>>();
                result(id, json!({"data":data,"nextCursor":null}));
            }
            "account/read" => {
                assert_eq!(params, &json!({"refreshToken":false}));
                result(
                    id,
                    json!({"account":{"type":"chatgpt","email":"PRIVATE_EMAIL","planType":"pro"},"requiresOpenaiAuth":true}),
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
                match case.as_str() {
                    "rate-limit-rpc-error" => send(
                        json!({"id":id,"error":{"code":-32000,"message":"PRIVATE_RATE_LIMIT_ERROR"}}),
                    ),
                    "rate-limit-negative" => result(
                        id,
                        json!({"rateLimits":{"primary":{"usedPercent":-1},"secondary":{"usedPercent":0}}}),
                    ),
                    _ => result(
                        id,
                        json!({"rateLimits":{"primary":{"usedPercent":0},"secondary":{"usedPercent":0}}}),
                    ),
                }
            }
            _ => panic!("unexpected outbound method: {method}"),
        }
    }
}
