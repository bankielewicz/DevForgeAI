use devforgeai_codex_worker_probe::process_windows::OwnedProcess;
use std::{path::Path, time::Duration};
#[test]
fn native_atomic_job_and_verified_stop() {
    let root = tempfile::tempdir().unwrap();
    let mut child = OwnedProcess::spawn(
        Path::new(env!("CARGO_BIN_EXE_protocol-peer")),
        &[],
        root.path(),
    )
    .unwrap();
    assert_eq!(child.active().unwrap(), 1);
    assert!(child.stop(Duration::from_secs(5)));
    assert_eq!(child.active().unwrap(), 0);
}
