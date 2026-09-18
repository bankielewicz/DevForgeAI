use devforgeai_codex_worker_probe::{request, runner};
use serde_json::{Value, json};
use std::{fs, path::PathBuf};

const PHYSICAL: &str = r"C:\Users\bryan\.codex\packages\standalone\releases\0.154.0-x86_64-pc-windows-msvc\bin\codex.exe";
const PINNED_SHA256: &str = "be96b992178b1e467c225800da0d65f2c86d5eba1ef0b14632f65db381cbdfde";

fn qa_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(3)
        .expect("QA root")
        .to_path_buf()
}

fn base_native(run_id: &str) -> (PathBuf, PathBuf, PathBuf, Value) {
    let trial = qa_root()
        .join("docs/plan/framework-worker-trials")
        .join(run_id);
    let fixture = trial.join("fixture");
    fs::create_dir_all(&fixture).expect("create QA schema2 fixture");
    fs::write(fixture.join("task.json"), request::TASK).expect("write exact task bytes");
    let input = trial.join("request.json");
    let review = trial.join("review.json");
    let value = json!({
        "schema_version": 2,
        "project_id": "qa-project",
        "checkout_id": "qa-checkout",
        "work_id": "qa-work",
        "run_id": run_id,
        "candidate_sha256": request::digest(request::TASK),
        "checkout_root": fixture,
        "run_dir": trial.join("run"),
        "worker_executable": PHYSICAL,
        "worker_sha256": PINNED_SHA256,
        "adapter": "codex-0.154.0-stdio",
        "scenario": "complete",
        "profile": {
            "model": "gpt-6-astra",
            "effort": "high",
            "review_ref": review,
            "review_sha256": "0".repeat(64),
            "launch_policy_id": "proposed-but-unqualified-v1",
            "launch_policy_sha256": "1".repeat(64)
        }
    });
    (trial, input, review, value)
}

fn write_json(path: &PathBuf, value: &Value) {
    fs::write(path, serde_json::to_vec(value).unwrap()).unwrap();
}

#[test]
fn qa_schema2_is_closed_native_only_and_caller_argv_is_never_data() {
    let temp = tempfile::tempdir_in(qa_root()).expect("QA parser tempdir");
    let input = temp.path().join("request.json");
    let (trial, _, _, base) = base_native("QA-S2-parser-base");
    let mut cases = Vec::new();

    let mut peer_v2 = base.clone();
    peer_v2["adapter"] = json!("peer");
    peer_v2["profile"] = Value::Null;
    cases.push(("peer-v2", peer_v2));

    let mut legacy_with_policy = base.clone();
    legacy_with_policy["schema_version"] = json!(1);
    cases.push(("legacy-with-policy", legacy_with_policy));

    for field in ["launch_policy_id", "launch_policy_sha256"] {
        let mut missing = base.clone();
        missing["profile"].as_object_mut().unwrap().remove(field);
        cases.push((field, missing));
    }

    let mut null_policy = base.clone();
    null_policy["profile"]["launch_policy_sha256"] = Value::Null;
    cases.push(("null-policy", null_policy));

    let mut injected_argv = base.clone();
    injected_argv["profile"]["argv"] = json!(["--dangerously-ignore-policy"]);
    cases.push(("caller-argv", injected_argv));

    let mut unknown_top = base;
    unknown_top["command"] = json!("cmd /c anything");
    cases.push(("unknown-top-level", unknown_top));

    for (label, case) in cases {
        write_json(&input, &case);
        assert!(
            request::validate(&input).is_err(),
            "{label} must reject before any run directory or spawn"
        );
        assert!(!trial.join("run").exists());
    }
}

#[test]
fn qa_valid_schema2_identity_is_intake_only_and_profile_fails_before_spawn() {
    let run_id = "QA-S2-fail-closed-20260915";
    let (trial, input, review, mut value) = base_native(run_id);
    write_json(&input, &value);
    let mut admitted = request::validate(&input).expect("exact schema2 identity intake");
    assert!(!trial.join("run").exists());

    let review_value = json!({
        "schema_version": 2,
        "reviewer": "independent QA synthetic review",
        "trial_selection_ref": "not native authorization",
        "codex_sha256": PINNED_SHA256,
        "checkout_root": trial.join("fixture"),
        "model": "gpt-6-astra",
        "effort": "high",
        "profile_sources": [],
        "findings": {
            "native_read_only_available": true,
            "no_external_tool_or_hook_effects": true,
            "codex_managed_chatgpt": true,
            "no_custom_provider": true
        },
        "launch_policy_id": "proposed-but-unqualified-v1",
        "launch_policy_sha256": "1".repeat(64)
    });
    write_json(&review, &review_value);
    let review_hash = request::hash_file(&review).unwrap();
    value["profile"]["review_sha256"] = json!(review_hash.clone());
    admitted.profile["review_sha256"] = json!(review_hash);
    assert_eq!(admitted.verify_review().unwrap_err(), "profile_unqualified");
    write_json(&input, &value);

    let mut events = Vec::new();
    let (code, terminal) = runner::run(&input, Default::default(), &mut |event| {
        events.push(event.clone())
    })
    .expect("fail-closed runner result");
    assert_eq!(code, 3);
    assert_eq!(terminal["reason"], "profile_unqualified");
    assert_eq!(terminal["outcome"], "blocked");
    assert!(
        events
            .iter()
            .all(|event| { event["kind"] != "spawn_intent" && event["kind"] != "server_started" })
    );
    assert_eq!(
        fs::read(trial.join("fixture/task.json")).unwrap(),
        request::TASK
    );
    let journal = fs::read_to_string(trial.join("run/journal.jsonl")).unwrap();
    assert!(!journal.contains("spawn_intent"));
    assert!(!journal.contains("server_started"));
}
