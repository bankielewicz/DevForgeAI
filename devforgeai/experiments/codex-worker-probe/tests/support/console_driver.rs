//! Independent hidden-console driver for an actual CTRL_C_EVENT.
use std::{
    ffi::OsStr,
    fs,
    os::windows::ffi::OsStrExt,
    path::Path,
    process::{Command, Stdio},
    ptr::null,
    time::{Duration, Instant},
};
use windows_sys::Win32::{
    Foundation::CloseHandle,
    System::{
        Console::{CTRL_C_EVENT, GenerateConsoleCtrlEvent, SetConsoleCtrlHandler},
        Threading::*,
    },
};
fn wide(s: &OsStr) -> Vec<u16> {
    s.encode_wide().chain(Some(0)).collect()
}
fn main() {
    let args: Vec<_> = std::env::args().collect();
    if args[1] == "--child" {
        unsafe {
            assert_ne!(SetConsoleCtrlHandler(None, 1), 0);
        }
        let mut harness = Command::new(&args[2])
            .args(["run", "--request", &args[3]])
            .stdin(Stdio::piped())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .unwrap();
        let ready = Path::new(&args[3]).parent().unwrap().join("signal-ready");
        let deadline = Instant::now() + Duration::from_secs(10);
        while !ready.exists() {
            assert!(Instant::now() < deadline);
            std::thread::sleep(Duration::from_millis(5));
        }
        unsafe {
            assert_ne!(GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0), 0);
        }
        let status = harness.wait().unwrap();
        fs::write(
            ready.with_file_name("console-observation.json"),
            format!(
                "{{\"event\":\"CTRL_C_EVENT\",\"exit\":{}}}",
                status.code().unwrap()
            ),
        )
        .unwrap();
        std::process::exit(status.code().unwrap());
    }
    let exe = std::env::current_exe().unwrap();
    let exe_w = wide(exe.as_os_str());
    let line = format!(
        "\"{}\" --child \"{}\" \"{}\"",
        exe.display(),
        args[1],
        args[2]
    );
    let mut line_w = wide(OsStr::new(&line));
    unsafe {
        let mut si: STARTUPINFOW = std::mem::zeroed();
        si.cb = std::mem::size_of_val(&si) as u32;
        si.dwFlags = STARTF_USESHOWWINDOW;
        si.wShowWindow = 0;
        let mut pi: PROCESS_INFORMATION = std::mem::zeroed();
        assert_ne!(
            CreateProcessW(
                exe_w.as_ptr(),
                line_w.as_mut_ptr(),
                null(),
                null(),
                0,
                CREATE_NEW_CONSOLE,
                null(),
                null(),
                &si,
                &mut pi
            ),
            0
        );
        assert_eq!(WaitForSingleObject(pi.hProcess, 20000), 0);
        let mut code = 0;
        assert_ne!(GetExitCodeProcess(pi.hProcess, &mut code), 0);
        CloseHandle(pi.hThread);
        CloseHandle(pi.hProcess);
        std::process::exit(code as i32);
    }
}
