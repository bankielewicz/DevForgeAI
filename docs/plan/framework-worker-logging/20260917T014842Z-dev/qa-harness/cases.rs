use devforgeai_codex_worker_probe::process_windows::OwnedProcess;
use std::{path::Path,time::{Duration,Instant}};
#[test]
fn real_windows_invalid_utf8_and_unterminated_line_preserve_exact_bytes() {
    let base=std::env::var_os("WF_TEST_EVIDENCE").unwrap();
    std::fs::create_dir_all(&base).unwrap();
    let root=tempfile::tempdir_in(&base).unwrap().keep();
    let mut child=OwnedProcess::spawn(Path::new(env!("CARGO_BIN_EXE_raw-capture-peer")),&[],&root).unwrap();
    child.close_input();
    let bound=Instant::now()+Duration::from_secs(3);
    while child.exit_code().is_none() && Instant::now()<bound {std::thread::sleep(Duration::from_millis(2));}
    assert_eq!(child.exit_code(),Some(23));
    assert!(child.drain_until(bound));
    let capture=child.capture();
    assert_eq!(capture.stdout.bytes,16);
    assert_eq!(capture.stderr.bytes,1);
    // Independent SHA256 oracle from system Python hashlib over the literal fixture bytes.
    let expected:serde_json::Value=serde_json::from_str(include_str!("expected.json")).unwrap();
    assert_eq!(capture.stdout.sha256,expected["stdout_sha256"]);
    assert_eq!(capture.stderr.sha256,expected["stderr_sha256"]);
    assert!(!capture.stdout.utf8_valid && !capture.stderr.utf8_valid);
    assert_eq!(capture.stdout.lines,1);
    assert_eq!(capture.stdout.final_line_bytes,14);
    assert!(capture.drain_complete);
    let stopped=child.stop(Duration::from_secs(1));
    assert!(stopped); assert_eq!(child.active(),Ok(0)); assert_eq!(child.exit_code(),Some(23));
    std::fs::write(root.join("observed.json"),serde_json::to_vec_pretty(&serde_json::json!({"capture":capture,"pre_stop_exit_code":23,"post_stop_exit_code":child.exit_code(),"tree_stopped":stopped})).unwrap()).unwrap();
}
