#![cfg(windows)]
use devforgeai_index::platform::windows::wide;
use std::{
    fs,
    path::Path,
    process::{Child, Command, Stdio},
    thread,
    time::{Duration, Instant},
};
use windows_sys::Win32::Storage::Xps::PrintWindow;
use windows_sys::Win32::{Foundation::*, Graphics::Gdi::*, UI::WindowsAndMessaging::*};
struct OwnedProcesses<'a> {
    tray: Child,
    data: &'a Path,
    window: HWND,
}
impl Drop for OwnedProcesses<'_> {
    fn drop(&mut self) {
        unsafe {
            if !self.window.is_null() {
                PostMessageW(self.window, WM_COMMAND, 213, 0);
            }
        }
        let _ = Command::new(env!("CARGO_BIN_EXE_devforgeai"))
            .env("DEVFORGEAI_INDEX_DATA", self.data)
            .args(["daemon", "stop", "--json"])
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .status();
        let deadline = Instant::now() + Duration::from_secs(3);
        while self.tray.try_wait().ok().flatten().is_none() && Instant::now() < deadline {
            thread::sleep(Duration::from_millis(20));
        }
        if self.tray.try_wait().ok().flatten().is_none() {
            let _ = self.tray.kill();
            let _ = self.tray.wait();
        }
    }
}
unsafe fn control_text(window: HWND, id: i32) -> String {
    unsafe {
        let control = GetDlgItem(window, id);
        if control.is_null() {
            return String::new();
        }
        let mut bytes = vec![0u16; 65536];
        let mut length = 0usize;
        assert_ne!(
            SendMessageTimeoutW(
                control,
                WM_GETTEXT,
                bytes.len(),
                bytes.as_mut_ptr() as isize,
                SMTO_ABORTIFHUNG,
                2000,
                &mut length
            ),
            0
        );
        String::from_utf16_lossy(&bytes[..length])
    }
}
unsafe fn text(window: HWND) -> String {
    unsafe { control_text(window, 105) }
}
unsafe fn wait_for(window: HWND, needle: &str) {
    unsafe {
        let end = Instant::now() + Duration::from_secs(15);
        loop {
            let value = text(window);
            if value.contains(needle) {
                return;
            }
            assert!(Instant::now() < end, "UI did not show {needle}: {value}");
            thread::sleep(Duration::from_millis(20));
        }
    }
}
unsafe fn answer_dialog(pid: u32, title: &str, answer: i32) {
    unsafe {
        let end = Instant::now() + Duration::from_secs(5);
        loop {
            let dialog = FindWindowW(wide("#32770").as_ptr(), wide(title).as_ptr());
            if !dialog.is_null() {
                let mut owner = 0;
                GetWindowThreadProcessId(dialog, &mut owner);
                assert_eq!(owner, pid, "Never answer another process's dialog");
                PostMessageW(dialog, WM_COMMAND, answer as usize, 0);
                while IsWindow(dialog) != 0 {
                    assert!(Instant::now() < end, "Owned dialog did not close: {title}");
                    thread::sleep(Duration::from_millis(20));
                }
                return;
            }
            assert!(Instant::now() < end, "Missing owned dialog {title}");
            thread::sleep(Duration::from_millis(20));
        }
    }
}
unsafe fn screenshot(window: HWND, path: &Path) {
    unsafe {
        let mut rect: RECT = std::mem::zeroed();
        assert_ne!(GetWindowRect(window, &mut rect), 0);
        let width = rect.right - rect.left;
        let height = rect.bottom - rect.top;
        let dc = GetWindowDC(window);
        let memory = CreateCompatibleDC(dc);
        let bitmap = CreateCompatibleBitmap(dc, width, height);
        let previous = SelectObject(memory, bitmap);
        assert_ne!(PrintWindow(window, memory, 2), 0);
        SelectObject(memory, previous);
        let mut info: BITMAPINFO = std::mem::zeroed();
        info.bmiHeader.biSize = 40;
        info.bmiHeader.biWidth = width;
        info.bmiHeader.biHeight = height;
        info.bmiHeader.biPlanes = 1;
        info.bmiHeader.biBitCount = 32;
        info.bmiHeader.biCompression = BI_RGB;
        let mut pixels = vec![0u8; (width * height * 4) as usize];
        assert_ne!(
            GetDIBits(
                memory,
                bitmap,
                0,
                height as u32,
                pixels.as_mut_ptr().cast(),
                &mut info,
                DIB_RGB_COLORS
            ),
            0
        );
        let mut bytes = Vec::new();
        bytes.extend(b"BM");
        bytes.extend((54 + pixels.len() as u32).to_le_bytes());
        bytes.extend([0u8; 4]);
        bytes.extend(54u32.to_le_bytes());
        bytes.extend(40u32.to_le_bytes());
        bytes.extend(width.to_le_bytes());
        bytes.extend(height.to_le_bytes());
        bytes.extend(1u16.to_le_bytes());
        bytes.extend(32u16.to_le_bytes());
        bytes.extend([0u8; 24]);
        bytes.extend(pixels);
        fs::write(path, bytes).unwrap();
        DeleteObject(bitmap);
        DeleteDC(memory);
        ReleaseDC(window, dc);
    }
}

#[test]
fn native_tray_window_controls_and_exit_preserve_daemon() {
    unsafe {
        let data = tempfile::tempdir().unwrap();
        let source = tempfile::tempdir().unwrap();
        fs::write(
            source.path().join("fixture.py"),
            "def native_fixture():\n    return 1\n",
        )
        .unwrap();
        assert!(
            FindWindowW(wide("DevForgeAIIndexTrayV1").as_ptr(), std::ptr::null()).is_null(),
            "An existing tray must not be modified by this fixture"
        );
        let child = Command::new(env!("CARGO_BIN_EXE_devforgeai-tray"))
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .stdin(Stdio::null())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .unwrap();
        let mut owned = OwnedProcesses {
            tray: child,
            data: data.path(),
            window: std::ptr::null_mut(),
        };
        let end = Instant::now() + Duration::from_secs(10);
        loop {
            let window = FindWindowW(wide("DevForgeAIIndexTrayV1").as_ptr(), std::ptr::null());
            if !window.is_null() {
                let mut pid = 0;
                GetWindowThreadProcessId(window, &mut pid);
                assert_eq!(pid, owned.tray.id());
                owned.window = window;
                break;
            }
            assert!(Instant::now() < end);
            thread::sleep(Duration::from_millis(20));
        }
        let window = owned.window;
        wait_for(window, "SERVICE_UNAVAILABLE");
        SendMessageW(window, WM_COMMAND, 201, 0);
        wait_for(window, "Running");
        assert_ne!(
            SendMessageW(
                GetDlgItem(window, 103),
                WM_SETTEXT,
                0,
                wide(source.path()).as_ptr() as isize
            ),
            0
        );
        assert_ne!(
            SendMessageW(
                GetDlgItem(window, 104),
                WM_SETTEXT,
                0,
                wide("Native UI fixture").as_ptr() as isize
            ),
            0
        );
        SendMessageW(window, WM_COMMAND, 205, 0);
        wait_for(window, "Native UI fixture");
        assert!(control_text(window, 102).contains("Native UI fixture"));
        wait_for(window, "1 text");
        let projects = Command::new(env!("CARGO_BIN_EXE_devforgeai"))
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .args(["project", "list", "--json"])
            .output()
            .unwrap();
        let projects: serde_json::Value = serde_json::from_slice(&projects.stdout).unwrap();
        let project = projects["data"]["projects"][0]["id"].as_str().unwrap();
        let indexed = Command::new(env!("CARGO_BIN_EXE_devforgeai"))
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .args(["index", "status", "--project", project, "--json"])
            .output()
            .unwrap();
        let indexed: serde_json::Value = serde_json::from_slice(&indexed.stdout).unwrap();
        let generation = indexed["data"]["current_generation"].as_str().unwrap();
        wait_for(window, generation);
        wait_for(
            window,
            &format!(
                "Last reconciliation (Unix seconds, UTC): {}",
                indexed["data"]["last_reconciliation"].as_i64().unwrap()
            ),
        );
        SendMessageW(window, WM_COMMAND, 202, 0);
        wait_for(window, "Paused");
        if let Some(root) = std::env::var_os("DEVFORGEAI_GUI_EVIDENCE") {
            let root = std::path::PathBuf::from(root);
            fs::create_dir_all(&root).unwrap();
            screenshot(window, &root.join("tray-paused.bmp"));
            fs::write(root.join("tray-status.txt"), text(window)).unwrap();
        }
        // Paused work remains queued and can be cancelled without hidden Resume.
        SendMessageW(window, WM_COMMAND, 206, 0);
        wait_for(window, "rescan: queued");
        SendMessageW(window, WM_COMMAND, 208, 0);
        wait_for(window, "request acknowledged");
        SendMessageW(window, WM_COMMAND, 208, 0);
        wait_for(window, "No active job");
        SendMessageW(
            GetDlgItem(window, 106),
            WM_SETTEXT,
            0,
            wide("*.ignored\r\n\r\ncache/**").as_ptr() as isize,
        );
        SendMessageW(window, WM_COMMAND, 210, 0);
        wait_for(window, "request acknowledged");
        let updated = Command::new(env!("CARGO_BIN_EXE_devforgeai"))
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .args(["project", "list", "--json"])
            .output()
            .unwrap();
        let updated: serde_json::Value = serde_json::from_slice(&updated.stdout).unwrap();
        assert_eq!(
            updated["data"]["projects"][0]["config"]["exclusions"],
            serde_json::json!(["*.ignored", "cache/**"])
        );
        SendMessageW(window, WM_COMMAND, 207, 0);
        wait_for(window, "reindex: queued");
        SendMessageW(window, WM_COMMAND, 203, 0);
        wait_for(window, "1 text");
        // Duplicate launches focus the same window and never create another owner.
        let duplicate = Command::new(env!("CARGO_BIN_EXE_devforgeai-tray"))
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .status()
            .unwrap();
        assert!(duplicate.success());
        let launched = Command::new(env!("CARGO_BIN_EXE_devforgeai"))
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .args(["tray", "--json"])
            .output()
            .unwrap();
        assert!(launched.status.success());
        assert_eq!(
            FindWindowW(wide("DevForgeAIIndexTrayV1").as_ptr(), std::ptr::null()),
            window
        );
        SendMessageW(window, WM_CLOSE, 0, 0);
        assert_eq!(IsWindowVisible(window), 0);
        SendMessageW(window, WM_COMMAND, 212, 0);
        assert_ne!(IsWindowVisible(window), 0);
        SendMessageW(window, WM_COMMAND, 213, 0);
        owned.window = std::ptr::null_mut();
        let end = Instant::now() + Duration::from_secs(5);
        while owned.tray.try_wait().unwrap().is_none() {
            assert!(Instant::now() < end);
            thread::sleep(Duration::from_millis(20));
        }
        let output = Command::new(env!("CARGO_BIN_EXE_devforgeai"))
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .args(["daemon", "status", "--json"])
            .output()
            .unwrap();
        let response: serde_json::Value = serde_json::from_slice(&output.stdout).unwrap();
        assert_eq!(response["data"]["daemon_state"], "running");
    }
}

#[test]
fn native_tray_confirmation_cancellation_and_stop_exit_are_scoped() {
    unsafe {
        let data = tempfile::tempdir().unwrap();
        let source = tempfile::tempdir().unwrap();
        fs::write(source.path().join("keep.txt"), b"preserved").unwrap();
        assert!(FindWindowW(wide("DevForgeAIIndexTrayV1").as_ptr(), std::ptr::null()).is_null());
        let child = Command::new(env!("CARGO_BIN_EXE_devforgeai-tray"))
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .stdin(Stdio::null())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .unwrap();
        let mut owned = OwnedProcesses {
            tray: child,
            data: data.path(),
            window: std::ptr::null_mut(),
        };
        let deadline = Instant::now() + Duration::from_secs(10);
        loop {
            let window = FindWindowW(wide("DevForgeAIIndexTrayV1").as_ptr(), std::ptr::null());
            if !window.is_null() {
                let mut pid = 0;
                GetWindowThreadProcessId(window, &mut pid);
                assert_eq!(pid, owned.tray.id());
                owned.window = window;
                break;
            }
            assert!(Instant::now() < deadline);
            thread::sleep(Duration::from_millis(20));
        }
        let window = owned.window;
        wait_for(window, "SERVICE_UNAVAILABLE");
        // A settings dialog can be cancelled without changing any startup setting.
        PostMessageW(window, WM_COMMAND, 215, 0);
        answer_dialog(owned.tray.id(), "Explicit startup preference", IDCANCEL);
        PostMessageW(window, WM_COMMAND, 215, 0);
        answer_dialog(owned.tray.id(), "Explicit startup preference", IDNO);
        answer_dialog(owned.tray.id(), "Local daemon preference", IDCANCEL);
        assert!(!data.path().join("tray-settings.json").exists());
        SendMessageW(window, WM_COMMAND, 201, 0);
        wait_for(window, "Running");
        SendMessageW(window, WM_COMMAND, 206, 0);
        wait_for(window, "Select a registered project first");
        SendMessageW(
            GetDlgItem(window, 103),
            WM_SETTEXT,
            0,
            wide(source.path()).as_ptr() as isize,
        );
        SendMessageW(
            GetDlgItem(window, 104),
            WM_SETTEXT,
            0,
            wide("Remove fixture").as_ptr() as isize,
        );
        SendMessageW(window, WM_COMMAND, 205, 0);
        wait_for(window, "1 text");
        PostMessageW(window, WM_COMMAND, 209, 0);
        answer_dialog(owned.tray.id(), "Confirm cache removal", IDNO);
        assert!(text(window).contains("Remove fixture"));
        PostMessageW(window, WM_COMMAND, 209, 0);
        answer_dialog(owned.tray.id(), "Confirm cache removal", IDYES);
        wait_for(window, "No registered projects.");
        assert_eq!(
            fs::read(source.path().join("keep.txt")).unwrap(),
            b"preserved"
        );
        // Native menu is created and dismissed in this owned window only.
        PostMessageW(window, WM_APP + 2, 0, WM_RBUTTONUP as isize);
        thread::sleep(Duration::from_millis(100));
        PostMessageW(window, WM_CANCELMODE, 0, 0);
        thread::sleep(Duration::from_millis(50));
        SendMessageW(window, WM_CLOSE, 0, 0);
        SendMessageW(window, WM_APP + 2, 0, WM_LBUTTONDBLCLK as isize);
        assert_ne!(IsWindowVisible(window), 0);
        PostMessageW(window, WM_COMMAND, 204, 0);
        answer_dialog(owned.tray.id(), "Stop local", IDNO);
        PostMessageW(window, WM_COMMAND, 214, 0);
        answer_dialog(owned.tray.id(), "Stop local", IDYES);
        let deadline = Instant::now() + Duration::from_secs(15);
        while owned.tray.try_wait().unwrap().is_none() {
            assert!(Instant::now() < deadline);
            thread::sleep(Duration::from_millis(20));
        }
        owned.window = std::ptr::null_mut();
        let output = Command::new(env!("CARGO_BIN_EXE_devforgeai"))
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .args(["daemon", "status", "--json"])
            .output()
            .unwrap();
        assert_eq!(
            serde_json::from_slice::<serde_json::Value>(&output.stdout).unwrap()["data"]["daemon_state"],
            "stopped"
        );
        assert!(!data.path().join("tray-settings.json").exists());
    }
}
