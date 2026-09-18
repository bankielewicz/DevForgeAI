use devforgeai_codex_worker_probe::{
    journal,
    runner::{self, Options},
};
use serde_json::json;
use std::{
    io::{Read, Write},
    path::Path,
    sync::{
        Arc, OnceLock,
        atomic::{AtomicU8, Ordering},
    },
};
use windows_sys::Win32::System::Console::{CTRL_BREAK_EVENT, CTRL_C_EVENT, SetConsoleCtrlHandler};
static CONTROL: OnceLock<Arc<AtomicU8>> = OnceLock::new();
unsafe extern "system" fn console(event: u32) -> i32 {
    if event == CTRL_C_EVENT || event == CTRL_BREAK_EVENT {
        if let Some(control) = CONTROL.get() {
            control.store(1, Ordering::SeqCst);
        }
        1
    } else {
        0
    }
}
fn diagnostic(reason: &str, code: i32) -> i32 {
    let _ = writeln!(std::io::stderr(), "{}", json!({"error":reason}));
    code
}
fn execute(args: &[String]) -> i32 {
    match args {
        [command, flag, input] if command == "run" && flag == "--request" => {
            if !Path::new(input).is_absolute() {
                return diagnostic("invalid_path", 2);
            }
            let options = Options::default();
            let control = options.control.clone();
            let _ = CONTROL.set(control.clone());
            unsafe {
                SetConsoleCtrlHandler(None, 0);
            }
            if unsafe { SetConsoleCtrlHandler(Some(console), 1) } == 0 {
                return diagnostic("control_setup_failed", 4);
            }
            std::thread::spawn(move || {
                let mut stdin = std::io::stdin().lock();
                let mut bytes = Vec::new();
                let mut byte = [0];
                loop {
                    match stdin.read(&mut byte) {
                        Ok(0) => {
                            control.store(1, Ordering::SeqCst);
                            return;
                        }
                        Ok(_) => {
                            bytes.push(byte[0]);
                            if bytes.len() > 1024 {
                                control.store(2, Ordering::SeqCst);
                                return;
                            }
                            if byte[0] == b'\n' {
                                control.store(
                                    if bytes == b"{\"op\":\"cancel\"}\n" {
                                        1
                                    } else {
                                        2
                                    },
                                    Ordering::SeqCst,
                                );
                                return;
                            }
                        }
                        Err(_) => {
                            control.store(2, Ordering::SeqCst);
                            return;
                        }
                    }
                }
            });
            match runner::run(Path::new(input), options, &mut |event| {
                let _ = writeln!(std::io::stdout(), "{event}");
                let _ = std::io::stdout().flush();
            }) {
                Ok((code, terminal)) => {
                    if terminal["reason"] == "evidence_write_failed" {
                        diagnostic("evidence_write_failed", code)
                    } else {
                        code
                    }
                }
                Err(reason) => diagnostic(
                    &reason,
                    if reason == "evidence_write_failed" {
                        4
                    } else {
                        2
                    },
                ),
            }
        }
        [command, dir_flag, dir, after_flag, after, limit_flag, limit]
            if command == "inspect"
                && dir_flag == "--run-dir"
                && after_flag == "--after"
                && limit_flag == "--limit" =>
        {
            if !Path::new(dir).is_absolute() {
                return diagnostic("invalid_path", 2);
            }
            let (Ok(after), Ok(limit)) = (after.parse::<u64>(), limit.parse::<usize>()) else {
                return diagnostic("invalid_cursor", 2);
            };
            match journal::inspect(Path::new(dir), after, limit) {
                Ok(value) => {
                    let _ = writeln!(std::io::stdout(), "{value}");
                    0
                }
                Err(reason) => diagnostic(&reason, if reason == "invalid_cursor" { 2 } else { 4 }),
            }
        }
        _ => diagnostic("invalid_arguments", 2),
    }
}
fn main() -> std::process::ExitCode {
    let args: Vec<_> = std::env::args().skip(1).collect();
    std::process::ExitCode::from(execute(&args) as u8)
}
