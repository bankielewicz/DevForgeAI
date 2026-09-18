use super::*;
use std::{
    io::{self, Cursor},
    sync::mpsc,
};

fn exercise(bytes: Vec<u8>, stderr: bool, capacity: usize) -> (Summary, Vec<Incoming>, usize) {
    let (tx, rx) = mpsc::sync_channel(capacity);
    let state: Shared = Default::default();
    reader(
        Cursor::new(bytes),
        stderr,
        tx,
        Arc::new(AtomicUsize::new(0)),
        state.clone(),
    )
    .join()
    .unwrap();
    let s = state.lock().unwrap();
    (s.summary(), rx.try_iter().collect(), s.chunks.len())
}
#[test]
fn chunk_independent_hash_invalid_utf8_and_final_line() {
    let bytes = vec![0xff, b'a', b'\n', 0xe2, 0x82];
    let (s, messages, _) = exercise(bytes.clone(), false, 32);
    assert_eq!(s.sha256, request::digest(&bytes));
    assert_eq!(s.bytes, 5);
    assert!(s.eof);
    assert!(!s.utf8_valid);
    assert_eq!(s.lines, 1);
    assert_eq!(s.final_line_bytes, 2);
    assert!(
        messages
            .iter()
            .any(|m| matches!(m, Incoming::Error("protocol_error")))
    );
    let mut s = State::default();
    for b in "€🙂\n".as_bytes() {
        s.update(&[*b], false);
    }
    assert!(s.summary().utf8_valid);
    assert_eq!(s.summary().sha256, request::digest("€🙂\n".as_bytes()));
    assert_eq!(s.summary().lines, 1);
    assert_eq!(s.summary().max_line_bytes, 7);
}
#[test]
fn exact_and_over_combined_byte_line_queue_and_detail_budgets() {
    for n in [MAX_OUTPUT, MAX_OUTPUT + 1] {
        let bytes = vec![b'a'; n];
        let (s, _, detail) = exercise(bytes.clone(), true, 32);
        assert_eq!(s.bytes, n);
        assert_eq!(s.sha256, request::digest(&bytes));
        assert_eq!(s.byte_overflow, n > MAX_OUTPUT);
        assert_eq!(s.eof, n == MAX_OUTPUT);
        assert_eq!(detail, MAX_DETAIL);
        assert!(s.detail_dropped > 0);
        assert!(s.classification_truncated);
    }
    for n in [MAX_LINE, MAX_LINE + 1] {
        let mut bytes = vec![b'a'; n];
        bytes.push(b'\n');
        let (s, _, _) = exercise(bytes, false, 32);
        assert_eq!(s.line_overflow, n > MAX_LINE);
        assert!(s.eof);
    }
    for n in [128, 129] {
        let (s, _, _) = exercise(vec![b'\n'; n], false, 128);
        assert_eq!(s.queue_overflow, n > 128);
        assert_eq!(s.queue_high_water, 128);
        assert!(s.eof);
    }
    let mut s = State::default();
    for _ in 0..MAX_DETAIL {
        s.update(b"x", false);
    }
    assert_eq!(s.summary().detail_dropped, 0);
    s.update(b"x", false);
    assert_eq!(s.summary().detail_dropped, 1);
}
#[test]
fn reader_error_disconnected_consumer_and_closed_classifier() {
    struct Broken;
    impl Read for Broken {
        fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
            Err(io::Error::other("CANARY_SECRET_29417"))
        }
    }
    let (tx, rx) = mpsc::sync_channel(1);
    let state: Shared = Default::default();
    reader(
        Broken,
        true,
        tx,
        Arc::new(AtomicUsize::new(0)),
        state.clone(),
    )
    .join()
    .unwrap();
    assert!(matches!(
        rx.recv().unwrap(),
        Incoming::Error("pipe_read_failed")
    ));
    assert_eq!(state.lock().unwrap().error(), Some("pipe_read_failed"));
    assert!(!state.lock().unwrap().summary().eof);
    assert!(
        !serde_json::to_string(&state.lock().unwrap().summary())
            .unwrap()
            .contains("CANARY_SECRET_29417")
    );
    let (s, _, _) = exercise(vec![b'\n'; 129], false, 1);
    assert!(s.queue_overflow);
    for (bytes, expected) in [
        (
            b"Error: config.toml:1:2: unknown configuration field `history.notify`".as_slice(),
            "strict_config_rejected",
        ),
        (
            b"Error: invalid transport\nin `mcp_servers.\"node_repl\"`".as_slice(),
            "configuration_parse_failed",
        ),
        (
            b"invalid transport mcp_servers. account CANARY_SECRET_29417".as_slice(),
            "unclassified",
        ),
        (b"Error: unknown thing".as_slice(), "unclassified"),
    ] {
        let (s, _, _) = exercise(bytes.to_vec(), true, 32);
        assert_eq!(serde_json::to_value(s.category).unwrap(), expected);
    }
}
#[test]
fn summary_validation_rejects_forged_incomplete_hash_and_eof() {
    let (s, _, _) = exercise(vec![], false, 32);
    let mut c = Capture {
        stdout: s.clone(),
        stderr: s,
        drain_complete: true,
    };
    assert!(c.validate().is_ok());
    c.stdout.sha256 = "bad".into();
    assert!(c.validate().is_err());
    c.stdout.sha256 = request::digest(b"changed");
    assert!(c.validate().is_err());
    c.stdout.sha256 = request::digest(b"");
    c.stdout.eof = false;
    assert!(c.validate().is_err());
    c.drain_complete = false;
    assert!(c.validate().is_ok());
}
