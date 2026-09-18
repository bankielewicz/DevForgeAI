#![cfg(windows)]
//! Process-isolated registry fixture. The real Windows Run key is read only.
//! This integration-test binary contains one test; HKCU redirection affects only it.
use devforgeai_index::{
    platform::{Paths, windows::wide},
    tray,
};
use windows_sys::Win32::{Foundation::*, System::Registry::*};

const RUN: &str = r"Software\Microsoft\Windows\CurrentVersion\Run";
const VALUE: &str = "DevForgeAIIndexTray";

struct Key(HKEY);
impl Drop for Key {
    fn drop(&mut self) {
        unsafe {
            RegCloseKey(self.0);
        }
    }
}
struct Fixture {
    real_user: Key,
    root: Key,
    name: String,
    redirected: bool,
}
impl Drop for Fixture {
    fn drop(&mut self) {
        unsafe {
            if self.redirected {
                assert_eq!(
                    RegOverridePredefKey(HKEY_CURRENT_USER, std::ptr::null_mut()),
                    0
                );
            }
            // A single GUID-owned leaf; never delete the shared Software parent or Run key.
            assert!(self.name.starts_with(r"Software\DevForgeAI-Index-Test-"));
            let status = RegDeleteTreeW(self.real_user.0, wide(&self.name).as_ptr());
            assert!(status == 0 || status == ERROR_FILE_NOT_FOUND);
        }
    }
}
unsafe fn create(parent: HKEY, name: &str) -> Key {
    unsafe {
        let mut key = std::ptr::null_mut();
        assert_eq!(
            RegCreateKeyExW(
                parent,
                wide(name).as_ptr(),
                0,
                std::ptr::null(),
                REG_OPTION_VOLATILE,
                KEY_ALL_ACCESS,
                std::ptr::null(),
                &mut key,
                std::ptr::null_mut()
            ),
            0
        );
        Key(key)
    }
}
unsafe fn read_startup(parent: HKEY) -> Option<(u32, Vec<u8>)> {
    unsafe {
        let mut key = std::ptr::null_mut();
        let status = RegOpenKeyExW(parent, wide(RUN).as_ptr(), 0, KEY_QUERY_VALUE, &mut key);
        if status == ERROR_FILE_NOT_FOUND {
            return None;
        }
        assert_eq!(status, 0);
        let key = Key(key);
        let mut length = 0;
        let mut kind = 0;
        let status = RegQueryValueExW(
            key.0,
            wide(VALUE).as_ptr(),
            std::ptr::null(),
            &mut kind,
            std::ptr::null_mut(),
            &mut length,
        );
        if status == ERROR_FILE_NOT_FOUND {
            return None;
        }
        assert_eq!(status, 0);
        let mut bytes = vec![0; length as usize];
        assert_eq!(
            RegQueryValueExW(
                key.0,
                wide(VALUE).as_ptr(),
                std::ptr::null(),
                &mut kind,
                bytes.as_mut_ptr(),
                &mut length
            ),
            0
        );
        bytes.truncate(length as usize);
        Some((kind, bytes))
    }
}

#[test]
fn startup_registry_contract_uses_only_a_volatile_redirected_hive() {
    unsafe {
        let mut actual = std::ptr::null_mut();
        assert_eq!(RegOpenCurrentUser(KEY_ALL_ACCESS, &mut actual), 0);
        let real_user = Key(actual);
        let before = read_startup(real_user.0);
        let name = format!(r"Software\DevForgeAI-Index-Test-{}", uuid::Uuid::new_v4());
        eprintln!("Owned volatile registry fixture: HKCU\\{name}");
        let root = create(real_user.0, &name);
        let mut fixture = Fixture {
            real_user,
            root,
            name,
            redirected: false,
        };
        drop(create(fixture.root.0, RUN));
        assert_eq!(RegOverridePredefKey(HKEY_CURRENT_USER, fixture.root.0), 0);
        fixture.redirected = true;
        let data = tempfile::tempdir().unwrap();
        let paths = Paths::at(data.path().to_owned()).unwrap();
        let defaults = tray::preferences(&paths).unwrap();
        assert!(!defaults.launch_at_sign_in && !defaults.start_local_daemon);
        // Missing value removal is idempotent; then inspect exact quoted UTF-16 bytes.
        assert!(
            !tray::set_preferences(&paths, Some(false), None)
                .unwrap()
                .launch_at_sign_in
        );
        let saved = tray::set_preferences(&paths, Some(true), Some(false)).unwrap();
        assert!(saved.launch_at_sign_in && !saved.start_local_daemon);
        let executable = std::env::current_exe()
            .unwrap()
            .with_file_name("devforgeai-tray.exe");
        let expected: Vec<u8> = wide(format!("\"{}\"", executable.display()))
            .into_iter()
            .flat_map(u16::to_le_bytes)
            .collect();
        assert_eq!(read_startup(fixture.root.0), Some((REG_SZ, expected)));
        assert!(
            !tray::set_preferences(&paths, Some(false), None)
                .unwrap()
                .launch_at_sign_in
        );
        assert_eq!(read_startup(fixture.root.0), None);
        assert_eq!(RegDeleteKeyW(fixture.root.0, wide(RUN).as_ptr()), 0);
        assert!(tray::set_preferences(&paths, Some(true), None).is_err());
        assert!(
            !tray::preferences(&paths).unwrap().launch_at_sign_in,
            "failed registry operation must not save a preference"
        );
        assert_eq!(
            read_startup(fixture.real_user.0),
            before,
            "real Run value changed while fixture was active"
        );
        assert_eq!(
            RegOverridePredefKey(HKEY_CURRENT_USER, std::ptr::null_mut()),
            0
        );
        fixture.redirected = false;
        assert_eq!(read_startup(HKEY_CURRENT_USER), before);
        let name = fixture.name.clone();
        drop(fixture);
        let mut removed = std::ptr::null_mut();
        assert_eq!(
            RegOpenKeyExW(
                HKEY_CURRENT_USER,
                wide(name).as_ptr(),
                0,
                KEY_READ,
                &mut removed
            ),
            ERROR_FILE_NOT_FOUND
        );
    }
}
