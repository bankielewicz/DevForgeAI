//! Controlled external-process boundary fixture. Never launches WSL or another process.
use std::{fs, io::{Read, Write}};
fn main() {
    let root = std::env::current_exe().unwrap().parent().unwrap().to_owned();
    let mode = fs::read_to_string(root.join("mode")).unwrap();
    let args: Vec<_> = std::env::args().skip(1).collect();
    let mut log = fs::OpenOptions::new().create(true).append(true).open(root.join("arguments")).unwrap();
    writeln!(log, "{args:?}").unwrap();
    if args == ["--list", "--running", "--quiet"] {
        let number = fs::read_to_string(root.join("inventory-count")).ok().and_then(|v| v.parse::<u32>().ok()).unwrap_or(0) + 1;
        fs::write(root.join("inventory-count"), number.to_string()).unwrap();
        if mode == "inventory-failed" { std::process::exit(1); }
        if mode == "stopped" || mode == "race" && number == 2 { return; }
        let distribution = fs::read_to_string(root.join("distribution")).unwrap();
        let value = format!("\u{feff}{distribution}\r\n");
        if mode == "utf8" { print!("{value}"); }
        else { for unit in value.encode_utf16() { std::io::stdout().write_all(&unit.to_le_bytes()).unwrap(); } }
        return;
    }
    let mut input = Vec::new();
    std::io::stdin().read_to_end(&mut input).unwrap();
    fs::write(root.join("request"), input).unwrap();
    if mode == "timeout" { std::thread::sleep(std::time::Duration::from_secs(2)); return; }
    if mode == "oversized" { let _ = std::io::stdout().write_all(&vec![b'x'; 8 * 1024 * 1024 + 1]); return; }
    std::io::stdout().write_all(&fs::read(root.join("response")).unwrap()).unwrap();
}
