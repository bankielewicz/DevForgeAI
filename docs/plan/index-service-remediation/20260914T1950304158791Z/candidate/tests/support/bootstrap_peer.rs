//! Finite bootstrap failure fixture; no daemon, IPC or other process is started.
use std::fs;
fn main() {
    let root = std::env::current_exe().unwrap().parent().unwrap().to_owned();
    if fs::read_to_string(root.join("mode")).unwrap() == "exit" { std::process::exit(23); }
    fs::write(root.join("started"), b"owned fixture").unwrap();
    std::thread::sleep(std::time::Duration::from_millis(500));
    fs::write(root.join("finished"), b"not force killed").unwrap();
}
