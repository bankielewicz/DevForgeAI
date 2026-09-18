// External deterministic protocol peer. No runtime-module imports or runner predicates.
use serde_json::{Value, json};
use std::{
    fs::{self, OpenOptions},
    io::{self, BufRead, Write},
    path::PathBuf,
};
fn send(v: Value) {
    println!("{v}");
    io::stdout().flush().unwrap();
}
fn result(id: &Value, v: Value) {
    send(json!({"id":id,"result":v}));
}
fn completed(status: &str, text: Option<String>) -> Value {
    let items = text.map_or(vec![], |s| {
        vec![json!({"type":"agentMessage","id":"message-1","phase":"final_answer","text":s})]
    });
    json!({"method":"turn/completed","params":{"threadId":"thread-1","turn":{"id":"turn-1","status":status,"items":items,"error":if status=="failed" {json!({"message":"synthetic limit","codexErrorInfo":"usageLimitExceeded"})} else {Value::Null}}}})
}
fn main() {
    let args: Vec<_> = std::env::args().collect();
    if args.get(1).is_some_and(|s| s == "--hold") {
        loop {
            std::thread::sleep(std::time::Duration::from_secs(60));
        }
    }
    if args.len() == 1 {
        for line in io::stdin().lock().lines() {
            println!("{}", line.unwrap());
        }
        return;
    }
    assert_eq!(args.len(), 3);
    assert_eq!(args[1], "--fixture-root");
    let root = PathBuf::from(&args[2]);
    let case = fs::read_to_string(root.join("peer-case.txt")).unwrap();
    let parts: Vec<_> = case.trim().split('-').collect();
    let number: usize = parts[1].parse().unwrap();
    let sub: usize = parts.get(2).map_or(1, |s| s.parse().unwrap());
    let mut trace = OpenOptions::new()
        .create_new(true)
        .write(true)
        .open(root.parent().unwrap().join("peer-trace.jsonl"))
        .unwrap();
    let expected = include_str!("../fixtures/expected.json").to_string();
    let prompt = include_str!("../fixtures/prompt.txt");
    let output_schema: Value =
        serde_json::from_str(include_str!("../fixtures/output-schema.json")).unwrap();
    let mut stage = 0;
    let mut request_id = 1;
    let mut pages = 0;
    let mut turns = 0;
    let _descendant = if number == 13 || number == 14 || number == 16 && sub >= 90 {
        let child = std::process::Command::new(std::env::current_exe().unwrap())
            .arg("--hold")
            .stdin(std::process::Stdio::null())
            .stdout(std::process::Stdio::inherit())
            .stderr(std::process::Stdio::inherit())
            .spawn()
            .unwrap();
        fs::write(
            root.parent().unwrap().join("peer-pids.json"),
            json!({"peer":std::process::id(),"descendant":child.id()}).to_string(),
        )
        .unwrap();
        Some(child)
    } else {
        None
    };
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        let v: Value = serde_json::from_str(&line).unwrap();
        writeln!(trace, "{line}").unwrap();
        trace.sync_all().unwrap();
        if v["id"] == 900 {
            if sub < 3 {
                assert_eq!(v, json!({"id":900,"result":{"decision":"cancel"}}));
            } else {
                assert_eq!(v["error"]["code"], -32601);
            }
            continue;
        }
        let method = v["method"].as_str().unwrap();
        let p = &v["params"];
        let id = &v["id"];
        assert!(v.get("jsonrpc").is_none());
        if method != "initialized" {
            assert_eq!(id.as_u64().unwrap(), request_id);
            request_id += 1;
        }
        match method {
            "initialize" => {
                // initialize is request ID 1; initialized consumes no client ID.
                assert_eq!(stage, 0);
                if number == 16 && sub >= 90 {
                    send(
                        json!({"id":"q".repeat(262144),"method":"unsupported/request","params":{}}),
                    );
                    fs::write(root.parent().unwrap().join("full-pipe-ready"), b"ready").unwrap();
                    loop {
                        std::thread::sleep(std::time::Duration::from_secs(1));
                    }
                }
                if number == 4 && sub >= 90 {
                    let code = match sub {
                        90 => json!({"private":"DEV_PRIVATE_SENTINEL_9201"}),
                        91 => json!("DEV_PRIVATE_SENTINEL_9201"),
                        92 => json!(1.5),
                        _ => json!(-32603),
                    };
                    send(
                        json!({"id":id,"error":{"code":code,"message":"DEV_PRIVATE_SENTINEL_9201","data":{"private":"DEV_PRIVATE_SENTINEL_9201"}}}),
                    );
                    continue;
                }
                if number == 4 {
                    match sub {
                        6 => {
                            send(json!({"id":id,"jsonrpc":"2.0","result":{}}));
                            continue;
                        }
                        7 => {
                            send(json!({"id":true,"result":{}}));
                            continue;
                        }
                        8 => {
                            send(json!({"id":id,"result":{},"error":{"code":-1}}));
                            continue;
                        }
                        9 => {
                            send(json!({"id":false,"method":"unsupported","params":{}}));
                            continue;
                        }
                        10 => {
                            send(json!({"method":5,"params":{}}));
                            continue;
                        }
                        11 => {
                            for _ in 0..33 {
                                send(json!({"method":"unknown","params":{}}));
                            }
                            continue;
                        }
                        22 => return,
                        23 => {
                            print!("{{partial");
                            io::stdout().flush().unwrap();
                            return;
                        }
                        24 => {
                            send(json!({"id":id,"error":{"code":-1,"message":"synthetic"}}));
                            continue;
                        }
                        _ => {}
                    }
                }
                assert_eq!(
                    p,
                    &json!({"clientInfo":{"name":"devforgeai_worker_probe","version":"0.1.0"},"capabilities":{"experimentalApi":false}})
                );
                if number == 16 {
                    match sub {
                        1 => loop {
                            std::thread::sleep(std::time::Duration::from_secs(1));
                        },
                        2 => {
                            print!("{}", "x".repeat(1024 * 1024 + 1));
                            io::stdout().flush().unwrap();
                            continue;
                        }
                        3 => {
                            let block = vec![b'x'; 8192];
                            for _ in 0..1100 {
                                io::stderr().write_all(&block).unwrap();
                            }
                            continue;
                        }
                        _ => {}
                    }
                }
                result(id, json!({"userAgent":"synthetic-peer"}));
                if number == 1 && sub == 2 {
                    result(id, json!({"userAgent":"synthetic-peer"}));
                }
                stage = 1;
            }
            "initialized" => {
                assert_eq!(stage, 1);
                assert_eq!(p, &json!({}));
                stage = 2;
            }
            "account/read" => {
                assert_eq!(stage, 2);
                assert_eq!(p, &json!({"refreshToken":false}));
                if number == 3 && sub == 6 {
                    send(json!({"id":id,"error":{"code":-1}}));
                    continue;
                }
                let account = if number == 3 {
                    match sub {
                        1 => Value::Null,
                        2 => json!({"type":"apiKey"}),
                        3 => {
                            json!({"type":"chatgpt","email":"private@example.invalid","planType":"plus"})
                        }
                        _ => json!({"type":"chatgpt","planType":"pro"}),
                    }
                } else {
                    json!({"type":"chatgpt","email":"private@example.invalid","planType":"pro"})
                };
                result(id, json!({"account":account,"requiresOpenaiAuth":true}));
                stage += 1;
            }
            "model/list" => {
                assert_eq!(stage, 3);
                pages += 1;
                assert_eq!(p["limit"], 100);
                if number == 3 && sub == 7 {
                    send(json!({"id":id,"error":{"code":-1}}));
                    continue;
                }
                if number == 3 && (sub == 10 || sub == 9 && pages == 1) {
                    result(id, json!({"data":[],"nextCursor":"next"}));
                    continue;
                }
                if number == 3 && sub == 11 {
                    result(id, json!({"data":[],"nextCursor":5}));
                    continue;
                }
                if number == 3 && sub == 12 {
                    result(id, json!({"data":vec![json!({});101],"nextCursor":null}));
                    continue;
                }
                let models = if number == 3 && sub == 4 {
                    vec![]
                } else {
                    vec![
                        json!({"id":"test-model","model":"test-model","supportedReasoningEfforts":if number==3 && sub==5 {json!([])} else {json!([{"reasoningEffort":"test-effort","description":"synthetic"}])}}),
                    ]
                };
                result(id, json!({"data":models,"nextCursor":null}));
                stage += 1;
            }
            "account/rateLimits/read" => {
                assert_eq!(stage, 4);
                assert_eq!(p, &json!({}));
                if number == 3 && sub == 13 {
                    send(json!({"id":id,"error":{"code":-1}}));
                    stage += 1;
                    continue;
                }
                if number == 3 && sub == 14 {
                    result(id, json!({"rateLimits":{"primary":{"usedPercent":100}}}));
                    stage += 1;
                    continue;
                }
                result(
                    id,
                    json!({"rateLimits":{"primary":{"usedPercent":0},"secondary":null}}),
                );
                stage += 1;
            }
            "thread/start" => {
                assert_eq!(stage, 5);
                assert_eq!(
                    p,
                    &json!({"model":"test-model","modelProvider":"openai","cwd":root,"sandbox":"read-only","approvalPolicy":"never","approvalsReviewer":"user","ephemeral":true})
                );
                let reply = json!({"thread":{"id":"thread-1"},"cwd":root,"model":"test-model","modelProvider":"openai","approvalPolicy":if number==2 && sub==1 {"on-request"}else{"never"},"approvalsReviewer":"user","sandbox":{"type":if number==2 && sub==2 {"workspaceWrite"}else{"readOnly"},"networkAccess":false}});
                let mut reply = reply;
                if number == 4 && sub == 12 {
                    reply["thread"]["id"] = json!("");
                }
                result(id, reply);
                stage += 1;
            }
            "turn/start" => {
                turns += 1;
                assert_eq!(turns, 1);
                assert_eq!(stage, 6);
                assert_eq!(
                    p,
                    &json!({"threadId":"thread-1","model":"test-model","effort":"test-effort","cwd":root,"approvalPolicy":"never","approvalsReviewer":"user","sandboxPolicy":{"type":"readOnly","networkAccess":false},"input":[{"type":"text","text":prompt}],"outputSchema":output_schema})
                );
                if number == 5 {
                    send(
                        json!({"method":"turn/started","params":{"threadId":"thread-1","turn":{"id":"turn-1","status":"inProgress","items":[],"error":null}}}),
                    );
                    send(completed("completed", Some(expected.clone())));
                    if sub == 3 || sub == 4 {
                        let mut duplicate = completed("completed", Some(expected.clone()));
                        if sub == 4 {
                            duplicate["params"]["turn"]["status"] = json!("failed");
                        }
                        send(duplicate);
                    }
                    if sub == 2 {
                        send(
                            json!({"method":"turn/started","params":{"threadId":"wrong","turn":{"id":"turn-1","status":"inProgress","items":[]}}}),
                        );
                    }
                }
                result(
                    id,
                    json!({"turn":{"id":"turn-1","status":"inProgress","items":[],"error":null}}),
                );
                stage += 1;
                if matches!(number, 13..=15) {
                    continue;
                }
                if number == 16 && sub == 4 {
                    loop {
                        send(json!({"method":"peer/heartbeat","params":{}}));
                        std::thread::sleep(std::time::Duration::from_millis(50));
                    }
                }
                if number == 4 {
                    if sub >= 13 {
                        let base = json!({"threadId":"thread-1","turnId":"turn-1"});
                        let mut p = base;
                        let method = match sub {
                            13 => {
                                p["item"] = json!({"id":"tool","type":"commandExecution"});
                                "item/started"
                            }
                            14 => {
                                p["item"] = json!({"id":"tool","type":"fileChange"});
                                "item/completed"
                            }
                            15 => {
                                p["item"] = json!({"id":"message-1","type":"agentMessage","phase":"final_answer","text":expected});
                                send(json!({"method":"item/completed","params":p}));
                                p["item"]["text"] = json!("changed");
                                "item/completed"
                            }
                            16 => {
                                p["itemId"] = json!("message-1");
                                p["delta"] = json!(false);
                                "item/agentMessage/delta"
                            }
                            17 => {
                                p["tokenUsage"] = json!({"total":{"totalTokens":-1}});
                                "thread/tokenUsage/updated"
                            }
                            18 => {
                                p["turn"] = json!({"id":"turn-1","status":"completed"});
                                "turn/started"
                            }
                            19 => {
                                p["turn"] = json!({"id":"turn-1","status":"inProgress","items":[]});
                                "turn/completed"
                            }
                            20 => {
                                send(completed("interrupted", None));
                                continue;
                            }
                            21 => {
                                p["item"] = json!({"id":"message-1","type":"agentMessage","phase":"bad","text":"x"});
                                "item/completed"
                            }
                            _ => unreachable!(),
                        };
                        send(json!({"method":method,"params":p}));
                        continue;
                    }
                    match sub {
                        1 | 2 => {
                            let mut v = completed("completed", Some(expected.clone()));
                            if sub == 1 {
                                v["params"]["threadId"] = json!("wrong");
                            } else {
                                v["params"]["turn"]["id"] = json!("wrong");
                            }
                            send(v);
                        }
                        3 => {
                            println!("{{not json");
                            io::stdout().flush().unwrap();
                        }
                        4 => result(id, json!({"turn":{"id":"other-turn"}})),
                        _ => result(&json!(500), json!({})),
                    }
                    continue;
                }
                if number == 6 {
                    send(
                        json!({"id":900,"method":match sub {1=>"item/commandExecution/requestApproval",2=>"item/fileChange/requestApproval",_=>"unrecognized/request"},"params":{"threadId":"thread-1","turnId":"turn-1"}}),
                    );
                    continue;
                }
                if number == 7 {
                    if sub >= 90 {
                        let marker = "DEV_PRIVATE_SENTINEL_9201";
                        let category = match sub {
                            90 => json!({"unexpectedPrivateField":marker}),
                            91 => json!({"httpConnectionFailed":{"httpStatusCode":marker}}),
                            92 => json!({"activeTurnNotSteerable":{"turnKind":marker}}),
                            93 => {
                                json!({"httpConnectionFailed":{"httpStatusCode":503,"private":marker}})
                            }
                            94 => {
                                json!({"activeTurnNotSteerable":{"turnKind":"review","private":marker}})
                            }
                            95 => json!({"responseStreamDisconnected":{"httpStatusCode":null}}),
                            96 => json!({"responseTooManyFailedAttempts":{}}),
                            97 => json!({"responseStreamConnectionFailed":{"httpStatusCode":429}}),
                            98 => json!(marker),
                            99 => json!({"httpConnectionFailed":{"httpStatusCode":65536}}),
                            100 => json!({"httpConnectionFailed":{"httpStatusCode":-1}}),
                            101 => json!({"httpConnectionFailed":null}),
                            102 => json!({"httpConnectionFailed":{},"private":marker}),
                            103 => json!({"activeTurnNotSteerable":{}}),
                            _ => json!([marker]),
                        };
                        let mut done = completed("failed", None);
                        done["params"]["turn"]["error"] = json!({"message":marker,"codexErrorInfo":category,"additionalDetails":marker});
                        send(done);
                        continue;
                    }
                    send(completed("failed", None));
                    continue;
                }
                if number == 8 && (sub == 1 || sub == 3) {
                    let mut count = json!({"totalTokens":17,"inputTokens":10,"cachedInputTokens":2,"outputTokens":7,"reasoningOutputTokens":3});
                    if sub == 3 {
                        count["email"] = json!("untrusted-private@example.invalid");
                    }
                    let usage = json!({"method":"thread/tokenUsage/updated","params":{"threadId":"thread-1","turnId":"turn-1","tokenUsage":{"total":count,"last":count}}});
                    send(usage.clone());
                    send(usage);
                }
                if number == 5 {
                    result(
                        id,
                        json!({"turn":{"id":"turn-1","status":"inProgress","items":[],"error":null}}),
                    );
                }
                if number == 19 && sub == 1 {
                    fs::write(root.join("task.json"), b"changed").unwrap();
                }
                if number == 1 && sub == 2 {
                    let item = json!({"id":"message-1","type":"agentMessage","text":expected,"phase":null});
                    send(
                        json!({"method":"item/started","params":{"threadId":"thread-1","turnId":"turn-1","item":item}}),
                    );
                    send(
                        json!({"method":"item/agentMessage/delta","params":{"threadId":"thread-1","turnId":"turn-1","itemId":"message-1","delta":"ignored deltas"}}),
                    );
                    send(
                        json!({"method":"item/completed","params":{"threadId":"thread-1","turnId":"turn-1","item":item}}),
                    );
                    send(
                        json!({"method":"item/completed","params":{"threadId":"thread-1","turnId":"turn-1","item":{"id":"reasoning","type":"reasoning"}}}),
                    );
                    let mut done = completed("completed", Some(expected.clone()));
                    done["params"]["turn"]["items"][0]["phase"] = Value::Null;
                    send(done);
                    continue;
                }
                let output = if number == 18 {
                    match sub {
                        1 => Some("{\"results\":[]}".into()),
                        2 => None,
                        _ => Some(expected.replacen("{", "{\"extra\":true,", 1)),
                    }
                } else {
                    Some(expected.clone())
                };
                send(completed("completed", output));
                if number == 1 && sub == 3 {
                    std::process::exit(9);
                }
            }
            "turn/interrupt" => {
                assert_eq!(p, &json!({"threadId":"thread-1","turnId":"turn-1"}));
                if number == 15 {
                    continue;
                }
                result(id, json!({}));
                send(completed("interrupted", None));
                stage += 1;
            }
            _ => panic!("unexpected outbound method"),
        }
    }
}
