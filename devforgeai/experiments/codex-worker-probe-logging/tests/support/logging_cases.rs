use super::*;
use std::fs;
#[test]
fn optional_sink_failure_and_event_byte_caps_are_non_authoritative() {
    let dir = tempfile::tempdir().unwrap();
    fs::create_dir(dir.path().join("diagnostics.jsonl")).unwrap();
    let mut sink = Sink::new(dir.path(), Level::Debug);
    sink.record(
        Level::Minimal,
        Record::Phase {
            phase: Phase::Admitted,
            elapsed_ms: 0,
        },
    );
    let status = sink.finish();
    assert!(status.diagnostics_incomplete);
    assert_eq!(status.dropped, 1);
    let dir = tempfile::tempdir().unwrap();
    let mut sink = Sink::new(dir.path(), Level::Debug);
    for _ in 0..MAX_EVENTS {
        sink.record(
            Level::Minimal,
            Record::Phase {
                phase: Phase::Admitted,
                elapsed_ms: 0,
            },
        );
    }
    assert_eq!(sink.events, MAX_EVENTS);
    assert!(!sink.incomplete);
    sink.record(
        Level::Minimal,
        Record::Phase {
            phase: Phase::Admitted,
            elapsed_ms: 0,
        },
    );
    assert!(sink.finish().diagnostics_incomplete);
    let dir = tempfile::tempdir().unwrap();
    let mut sink = Sink::new(dir.path(), Level::Debug);
    sink.write(&vec![b'x'; MAX_BYTES]);
    assert_eq!(sink.bytes, MAX_BYTES);
    assert!(!sink.incomplete);
    sink.write(b"x");
    assert!(sink.finish().diagnostics_incomplete);
    let dir = tempfile::tempdir().unwrap();
    let mut sink = Sink::new(dir.path(), Level::Debug);
    // A read-only handle provokes a real WriteFile denial without altering product outcomes.
    sink.file = Some(File::open(dir.path().join("diagnostics.jsonl")).unwrap());
    sink.record(
        Level::Minimal,
        Record::Phase {
            phase: Phase::Admitted,
            elapsed_ms: 0,
        },
    );
    assert!(sink.finish().diagnostics_incomplete);
}
#[test]
fn sink_levels_and_inspector_reject_missing_changed_or_partial_evidence() {
    for level in [Level::Off, Level::Minimal, Level::Verbose, Level::Debug] {
        let dir = tempfile::tempdir().unwrap();
        let mut sink = Sink::new(dir.path(), level);
        sink.record(
            Level::Minimal,
            Record::Phase {
                phase: Phase::Admitted,
                elapsed_ms: 1,
            },
        );
        sink.record(
            Level::Verbose,
            Record::Rpc {
                rpc: Rpc::Other,
                elapsed_ms: 2,
                failed: true,
            },
        );
        sink.record(
            Level::Debug,
            Record::Chunk {
                stream: crate::capture::Stream::Stderr,
                chunk: &crate::capture::Chunk {
                    bytes: 3,
                    sha256: request::digest(b"abc"),
                },
            },
        );
        let status = sink.finish();
        assert_eq!(status.events, level as usize);
        let binding = Binding {
            level,
            sha256: request::digest(b"config"),
        };
        assert!(inspect(dir.path(), Some(&binding), &status).is_ok());
        let mut bad = status.clone();
        bad.bytes += 1;
        assert!(inspect(dir.path(), Some(&binding), &bad).is_err());
        bad = status.clone();
        bad.events += 1;
        assert!(inspect(dir.path(), Some(&binding), &bad).is_err());
        bad = status.clone();
        bad.level = if level == Level::Off {
            Level::Debug
        } else {
            Level::Off
        };
        assert!(inspect(dir.path(), Some(&binding), &bad).is_err());
        fs::write(dir.path().join("diagnostics.jsonl"), b"not-json\n").unwrap();
        assert!(inspect(dir.path(), Some(&binding), &status).is_err());
    }
    for bytes in [
        b"{}\n".as_slice(),
        b"broken\n",
        b"{\"schema_version\":1,\"record\":{}}",
        b"{\"schema_version\":1,\"record\":{}}\n",
    ] {
        let dir = tempfile::tempdir().unwrap();
        fs::write(dir.path().join("diagnostics.jsonl"), bytes).unwrap();
        let status = Status {
            level: Level::Debug,
            bytes: bytes.len(),
            events: 0,
            sha256: request::digest(bytes),
            diagnostics_incomplete: false,
            dropped: 0,
        };
        assert!(
            inspect(
                dir.path(),
                Some(&Binding {
                    level: Level::Debug,
                    sha256: request::digest(b"")
                }),
                &status
            )
            .is_err()
        );
    }
}
