mod support;
use devforgeai_codex_worker_probe::{
    journal::{self, Journal},
    request,
};
use serde_json::json;
use std::fs;

#[test]
fn inspection_distinguishes_preflight_from_a_completed_turn() {
    let mut fixture = support::Fixture::new("WF-11");
    let review = fixture.root.path().join("review.json");
    fs::write(&review, b"{}").unwrap();
    fixture.request.schema_version = 2;
    fixture.request.adapter = "codex-0.154.0-stdio".into();
    fs::remove_file(fixture.request.checkout_root.join("peer-case.txt")).unwrap();
    fixture.request.profile = json!({"model":"gpt-6-astra","effort":"high","review_ref":review,"review_sha256":request::digest(b"{}"),"launch_policy_id":"p","launch_policy_sha256":"0".repeat(64)});
    let mut journal = Journal::create(&fixture.request).unwrap();
    journal.append("admitted", json!({})).unwrap();
    journal
        .append(
            "worker_event",
            json!({"method":"native_identity_rechecked"}),
        )
        .unwrap();
    journal.append("spawn_intent", json!({})).unwrap();
    journal
        .append("server_started", json!({"pid_observation":123}))
        .unwrap();
    for stage in [
        "config",
        "requirements",
        "features",
        "hooks",
        "plugins",
        "apps",
        "mcp",
    ] {
        journal
            .append("worker_event", json!({"preflight":stage,"observation":{}}))
            .unwrap();
    }
    journal
        .append("profile_checked", json!({"mode":"chatgpt","plan":"pro"}))
        .unwrap();
    journal
        .append(
            "process_exit",
            json!({"worker_exit_code":0,"tree_stopped":true}),
        )
        .unwrap();
    let terminal = json!({"outcome":"preflight_checked","reason":"preflight_checked","thread_id":null,"turn_id":null,"worker_exit_code":0,"tree_stopped":true,"fixture_unchanged":true,"oracle":"not_evaluated","usage":null,"open_work":["w"]});
    journal.append("terminal", terminal).unwrap();
    drop(journal);
    let original = fs::read(fixture.request.run_dir.join("journal.jsonl")).unwrap();
    let result = journal::inspect(&fixture.request.run_dir, 0, 100).unwrap();
    assert_eq!(result["state"], "preflight_checked");
    assert_eq!(
        fs::read(fixture.request.run_dir.join("journal.jsonl")).unwrap(),
        original
    );
    for (before, after) in [
        ("\"oracle\":\"not_evaluated\"", "\"oracle\":\"match\""),
        ("\"thread_id\":null", "\"thread_id\":\"forged\""),
        ("\"tree_stopped\":true", "\"tree_stopped\":false"),
        ("\"preflight\":\"hooks\"", "\"preflight\":\"unknown\""),
    ] {
        let changed = String::from_utf8(original.clone())
            .unwrap()
            .replace(before, after);
        fs::write(fixture.request.run_dir.join("journal.jsonl"), changed).unwrap();
        assert_eq!(
            journal::inspect(&fixture.request.run_dir, 0, 100).unwrap_err(),
            "evidence_corrupt"
        );
    }
}
