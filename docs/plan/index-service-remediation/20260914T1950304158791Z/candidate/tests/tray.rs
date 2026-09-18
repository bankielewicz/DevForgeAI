use devforgeai_index::tray::{PollState, Preferences};
use devforgeai_index::{
    protocol::{ErrorCode, Response},
    tray::status_text,
};
use serde_json::json;
use std::time::{Duration, Instant};

#[test]
fn status_view_explains_pause_freshness_counts_and_errors() {
    let response = Response::success("id", json!({"indexing_mode":"paused"}));
    let display = status_text(
        "local",
        &response,
        &[json!({"id":"p","name":"Demo","root":"C:/demo"})],
        &[
            json!({"project_id":"p","coverage":"partial","freshness":"dirty","text_count":3,"structural_count":2,"excluded_count":4,"skipped_count":1,"failed_count":1,"jobs":[{"kind":"rescan","outcome":"queued"}]}),
        ],
    );
    for required in [
        "local",
        "Paused",
        "Demo",
        "partial",
        "dirty",
        "3 text",
        "2 structural",
        "4 excluded",
        "1 skipped",
        "1 failed",
        "rescan: queued",
    ] {
        assert!(display.contains(required), "missing {required}: {display}");
    }
    assert!(!display.contains("protocol_version"));
    let failed = Response::failure("id", ErrorCode::ServiceUnavailable, "Daemon is stopped");
    let display = status_text("Ubuntu", &failed, &[], &[]);
    assert!(display.contains("SERVICE_UNAVAILABLE"));
    assert!(display.contains("Daemon is stopped"));
}

#[test]
fn tray_startup_defaults_are_opt_in_and_polling_is_bounded() {
    let defaults = Preferences::default();
    assert!(!defaults.launch_at_sign_in);
    assert!(!defaults.start_local_daemon);
    let now = Instant::now();
    let mut state = PollState::new(now);
    assert!(state.begin(now, true));
    assert!(!state.begin(now + Duration::from_secs(60), true));
    state.finish(now, true, false);
    assert!(!state.begin(now + Duration::from_secs(4), true));
    assert!(state.begin(now + Duration::from_secs(5), true));
    state.finish(now + Duration::from_secs(5), true, true);
    assert!(!state.begin(now + Duration::from_secs(34), true));
    assert!(state.begin(now + Duration::from_secs(35), true));
}

#[test]
fn tray_provenance_tracks_each_project_and_handles_unknown_values() {
    let response = Response::success("r", json!({"daemon_state":"running"}));
    let projects = [
        json!({"id":"p","name":"One"}),
        json!({"id":"q","name":"Two"}),
    ];
    let known = json!({"project_id":"p","current_generation":"generation-alpha","last_reconciliation":1700000000});
    let unknown = json!({"project_id":"q","current_generation":null,"last_reconciliation":null});
    let display = status_text("local", &response, &projects, &[unknown, known]);
    assert!(display.contains("Current generation: generation-alpha"));
    assert!(display.contains("Last reconciliation (Unix seconds, UTC): 1700000000"));
    let second = display.split("Two").nth(1).unwrap();
    assert!(second.contains("Current generation: unknown"));
    assert!(second.contains("Last reconciliation (Unix seconds, UTC): unknown"));
    assert!(!second.contains("generation-alpha"));
    let changed = status_text(
        "local",
        &response,
        &projects[..1],
        &[
            json!({"project_id":"p","current_generation":"generation-beta","last_reconciliation":1700000060}),
        ],
    );
    assert!(changed.contains("generation-beta"));
    assert!(changed.contains("1700000060"));
    assert!(!changed.contains("generation-alpha"));
    for status in [
        json!({"project_id":"p"}),
        json!({"project_id":"p","current_generation":false,"last_reconciliation":"invalid"}),
    ] {
        let text = status_text("local", &response, &projects[..1], &[status]);
        assert!(text.contains("Current generation: unknown"));
        assert!(text.contains("Last reconciliation (Unix seconds, UTC): unknown"));
    }
    let epoch = status_text(
        "local",
        &response,
        &projects[..1],
        &[json!({"project_id":"p","current_generation":"g0","last_reconciliation":0})],
    );
    assert!(epoch.contains("Last reconciliation (Unix seconds, UTC): 0"));
}

#[test]
fn tray_status_distinguishes_acknowledgment_stopping_degraded_and_details() {
    for (data, expected) in [
        (json!({}), "Connected — request acknowledged"),
        (json!({"daemon_state":"stopping"}), "Stopping"),
        (json!({"already_running":true}), "Running"),
        (json!({"degraded":true}), "Cache needs recovery"),
    ] {
        let display = status_text("fixture", &Response::success("r", data), &[], &[]);
        assert!(display.contains(expected));
        assert!(display.contains("No registered projects."));
    }
    let error =
        devforgeai_index::protocol::ProtocolError::new(ErrorCode::JobConflict, "Existing job")
            .details(json!({"job_id":"running-job"}));
    let display = status_text("fixture", &Response::from_error("r", error), &[], &[]);
    assert!(display.contains("JOB_CONFLICT"));
    assert!(display.contains("running-job"));
    let display = status_text(
        "fixture",
        &Response::success("r", json!({})),
        &[json!({"id":"p"})],
        &[json!({"project_id":"different"})],
    );
    assert!(display.contains("Unnamed project"));
    assert!(!display.contains("Coverage:"));
    let now = Instant::now();
    let mut polling = PollState::new(now);
    assert!(polling.begin(now, false));
    polling.finish(now, false, false);
    assert!(!polling.begin(now + Duration::from_secs(29), false));
    assert!(polling.begin(now + Duration::from_secs(30), false));
}
