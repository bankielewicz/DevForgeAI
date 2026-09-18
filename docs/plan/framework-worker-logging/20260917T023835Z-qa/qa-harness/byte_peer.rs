use std::{io::{self, BufRead, Write}, time::Duration};
use serde_json::json;
fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mut out = io::stdout().lock();
    let mut err = io::stderr().lock();
    match args[0].as_str() {
        "silent" => {}
        "config" => err.write_all(b"Error: qa-settings:7:3: unknown configuration field `QA_CANARY_config_7391`\n").unwrap(),
        "mcp" => err.write_all(b"Error: invalid transport\nin `mcp_servers.QA_CANARY_transport_7391`\n").unwrap(),
        "negative" => err.write_all(b"NotError: invalid transport\nin `mcp_servers.QA_CANARY_negative_7391`\n").unwrap(),
        "utf8" => {
            for b in b"\xff\nqa-last-line\xe2\x82" {
                out.write_all(&[*b]).unwrap(); out.flush().unwrap();
                std::thread::sleep(Duration::from_millis(1));
            }
            err.write_all(b"\xfe\n").unwrap();
        }
        "flood" => err.write_all(&vec![b'q';700001]).unwrap(),
        "line" => {out.write_all(&vec![b'z';args[1].parse().unwrap()]).unwrap();out.write_all(b"\n").unwrap();}
        "queue" => out.write_all(&vec![b'\n';args[1].parse().unwrap()]).unwrap(),
        "bytes" => err.write_all(&vec![b'b';args[1].parse().unwrap()]).unwrap(),
        "argv" => {out.write_all(serde_json::to_string(&args[1..]).unwrap().as_bytes()).unwrap();out.write_all(b"\n").unwrap();}
        "secret-request" => {
            let line = io::stdin().lock().lines().next().unwrap().unwrap();
            let request: serde_json::Value = serde_json::from_str(&line).unwrap();
            assert_eq!(request["method"], "initialize");
            writeln!(out,"{}",json!({"id":"QA_CANARY_id_7391","method":"QA_CANARY_method_7391","params":{"path":"C:/QA_CANARY_path_7391","token":"Bearer sk-QA_CANARY_token_7391","prompt":"QA_CANARY_prompt_7391"}})).unwrap();
            out.flush().unwrap();
            err.write_all(b"Bearer sk-QA_CANARY_stderr_7391 account QA_CANARY_account_7391").unwrap();
            err.flush().unwrap();
            let reply = io::stdin().lock().lines().next().unwrap().unwrap();
            let reply: serde_json::Value = serde_json::from_str(&reply).unwrap();
            assert_eq!(reply["id"],"QA_CANARY_id_7391");
            assert_eq!(reply["error"]["code"],-32601);
        }
        _ => panic!("unknown QA-only fixture"),
    }
    out.flush().unwrap();err.flush().unwrap();
    std::process::exit(29);
}

