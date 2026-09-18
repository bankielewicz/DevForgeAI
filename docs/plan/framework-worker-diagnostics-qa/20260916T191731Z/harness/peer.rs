mod fixture_config;
use serde_json::{json, Value};
use std::{fs::{File, OpenOptions}, io::{BufRead, Write}, os::windows::process::CommandExt, path::PathBuf, process::{Command, Stdio}};

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.get(1).map(String::as_str) == Some("--leaf") { return; }
    assert_eq!(args.len(), 4);
    let mode = &args[1];
    let root = PathBuf::from(&args[2]);
    let canary = &args[3];
    let mut trace = OpenOptions::new().create_new(true).write(true).open(root.join("trace.jsonl")).unwrap();
    for line in std::io::stdin().lock().lines() {
        let value: Value = serde_json::from_str(&line.unwrap()).unwrap();
        writeln!(trace, "{value}").unwrap(); trace.flush().unwrap();
        let method = value["method"].as_str().unwrap_or("");
        assert!(!method.starts_with("thread/") && !method.starts_with("turn/"), "unexpected work");
        if method == "initialized" { continue; }
        if (mode == "descendant-init" && method == "initialize") || (mode == "descendant-config" && method == "config/read") {
            let status = Command::new(std::env::current_exe().unwrap()).arg("--leaf")
                .creation_flags(0x00000008).stdin(Stdio::null()).stdout(Stdio::null()).stderr(Stdio::null()).status().unwrap();
            assert!(status.success());
            File::create(root.join("child-exited")).unwrap().write_all(b"child exit observed\n").unwrap();
        }
        if mode == "hang" { std::thread::sleep(std::time::Duration::from_secs(30)); return; }
        if (mode == "error-init" && method == "initialize") || (mode == "error-config" && method == "config/read") {
            println!("{}", json!({"id":value["id"],"error":{"code":-32009,"message":canary,"data":{"unknown":{"private":canary}}},"unknown":canary}));
        } else if mode == "server-request" && method == "initialize" {
            println!("{}", json!({"id":"qa-server-request","method":"qa/unsupported","params":{"unknown":{"private":canary}}}));
        } else if method == "config/read" {
            let mut config = fixture_config::response(&root.join("fixture/task.json"), canary);
            if mode == "bad-config" { config["config"]["approval_policy"] = json!(canary); }
            println!("{}", json!({"id":value["id"],"result":config}));
        } else if method == "configRequirements/read" {
            // Stop AFTER successful config projection, without emulating other inventory endpoints.
            println!("{}", json!({"id":value["id"],"error":{"code":-32010,"message":canary}}));
        } else {
            println!("{}", json!({"id":value["id"],"result":{"unknown":{"private":canary}}}));
        }
        std::io::stdout().flush().unwrap();
    }
}
