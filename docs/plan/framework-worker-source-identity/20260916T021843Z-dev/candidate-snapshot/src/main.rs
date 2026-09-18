use devforgeai_codex_worker_probe::{
    journal, profile_sources, request,
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
        [command, flag, input]
            if (command == "run" || command == "preflight") && flag == "--request" =>
        {
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
            let operation = if command == "preflight" {
                runner::preflight
            } else {
                runner::run
            };
            match operation(Path::new(input), options, &mut |event| {
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
        [command, flag, input] if command == "profile-sources" && flag == "--checkout-root" => {
            let root = match request::resolve(Path::new(input)) {
                Ok(root) => root,
                Err(reason) => return diagnostic(&reason, 2),
            };
            let workspace = Path::new(env!("CARGO_MANIFEST_DIR"))
                .ancestors()
                .nth(3)
                .unwrap();
            let expected =
                match request::resolve(&workspace.join("docs/plan/framework-worker-trials")) {
                    Ok(expected) => expected,
                    Err(reason) => return diagnostic(&reason, 2),
                };
            if root.file_name().is_none_or(|name| name != "fixture")
                || root.parent().and_then(Path::parent) != Some(expected.as_path())
                || !root
                    .parent()
                    .and_then(Path::file_name)
                    .and_then(|s| s.to_str())
                    .is_some_and(request::valid_id)
            {
                return diagnostic("invalid_trial_layout", 2);
            }
            if std::fs::read_dir(&root).map(|entries| entries.count()).ok() != Some(1)
                || request::bounded_read(&root.join("task.json"), 65536)
                    .ok()
                    .as_deref()
                    != Some(request::TASK)
            {
                return diagnostic("invalid_fixture", 2);
            }
            match profile_sources::collect(&root).and_then(|inventory| {
                serde_json::to_value(inventory).map_err(|_| "profile_unqualified".into())
            }) {
                Ok(inventory) => {
                    let _ = writeln!(std::io::stdout(), "{inventory}");
                    0
                }
                Err(reason) => diagnostic(&reason, 3),
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
