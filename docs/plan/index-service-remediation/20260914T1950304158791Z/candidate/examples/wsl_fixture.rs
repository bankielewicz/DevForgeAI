//! Native test relay: isolates the real CLI's data without changing production defaults.
fn main() -> std::process::ExitCode {
    let executable = std::env::current_exe().unwrap();
    let build = executable.parent().unwrap().parent().unwrap();
    let data = build.join("wsl-bridge-fixture-data");
    let status = std::process::Command::new(build.join("devforgeai"))
        .env("DEVFORGEAI_INDEX_DATA", data)
        .args(std::env::args_os().skip(1))
        .status()
        .unwrap();
    std::process::ExitCode::from(status.code().unwrap_or(8) as u8)
}
