#![cfg_attr(windows, windows_subsystem = "windows")]
fn main() {
    if let Err(error) = devforgeai_index::tray::run() {
        eprintln!("{error}");
        std::process::exit(error.code.exit_code());
    }
}
