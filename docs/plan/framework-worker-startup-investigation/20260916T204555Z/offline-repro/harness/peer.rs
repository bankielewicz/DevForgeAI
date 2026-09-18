use serde_json::{Value, json};
use std::io::{BufRead, Write};

const STDERR_BLOCK: &[u8] = b"synthetic-startup-failure: early exit\n";

fn main() {
    let mode = std::env::args().nth(1).expect("mode");
    std::io::stderr().write_all(STDERR_BLOCK).unwrap();
    std::io::stderr().flush().unwrap();
    if mode == "early-exit" {
        std::process::exit(23);
    }
    assert_eq!(mode, "control");
    // Give the independent stderr reader time to enqueue metadata before stdout.
    std::thread::sleep(std::time::Duration::from_millis(100));
    for line in std::io::stdin().lock().lines() {
        let value: Value = serde_json::from_str(&line.unwrap()).unwrap();
        let method = value["method"].as_str().unwrap_or("");
        assert!(!method.starts_with("thread/") && !method.starts_with("turn/"));
        if method == "initialize" {
            println!("{}", json!({"id":value["id"],"result":{"synthetic":"initialize-ok"}}));
            std::io::stdout().flush().unwrap();
        }
    }
}
