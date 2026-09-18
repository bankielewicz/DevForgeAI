mod support;
use devforgeai_codex_worker_probe::request;
use serde_json::json;
use std::{fs, path::PathBuf};

// NI-T01: admission only. This test never starts Codex or approves a profile.
#[test]
fn v2_pinned_physical_identity_is_admitted() {
    let workspace = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(3)
        .unwrap()
        .to_path_buf();
    let parent = workspace.join("docs/plan/framework-worker-trials");
    fs::create_dir_all(&parent).unwrap();
    let temp = tempfile::Builder::new()
        .prefix("NI-admission-")
        .tempdir_in(parent)
        .unwrap();
    let root = temp.path().to_path_buf();
    let fixture = root.join("fixture");
    fs::create_dir(&fixture).unwrap();
    fs::write(fixture.join("task.json"), request::TASK).unwrap();
    let input = root.join("request.json");
    let value = json!({"schema_version":2,"project_id":"p","checkout_id":"c","work_id":"w",
        "run_id":root.file_name().unwrap().to_str().unwrap(),"candidate_sha256":request::digest(request::TASK),
        "checkout_root":fixture,"run_dir":root.join("run"),
        "worker_executable":r"C:\Users\bryan\.codex\packages\standalone\releases\0.154.0-x86_64-pc-windows-msvc\bin\codex.exe",
        "worker_sha256":"be96b992178b1e467c225800da0d65f2c86d5eba1ef0b14632f65db381cbdfde",
        "adapter":"codex-0.154.0-stdio","scenario":"complete",
        "profile":{"model":"gpt-6-astra","effort":"high","review_ref":root.join("unqualified-review.json"),
        "review_sha256":"0".repeat(64),"launch_policy_id":"codex-0.154.0-readonly-no-external-tools-v1",
        "launch_policy_sha256":"0".repeat(64)}});
    fs::write(&input, serde_json::to_vec_pretty(&value).unwrap()).unwrap();
    if std::env::var_os("WF_TEST_EVIDENCE").is_some() {
        let _ = temp.keep();
    }
    let admitted = request::validate(&input)
        .expect("NI-T01 exact physical worker identity must admit v2 input");
    assert_eq!(
        admitted.worker_executable,
        request::resolve(PathBuf::from(value["worker_executable"].as_str().unwrap()).as_path())
            .unwrap()
    );
    assert!(
        admitted.verify_review().is_err(),
        "admission must not approve an unqualified profile"
    );
    assert!(!root.join("run").exists());
    // Even caller-written all-true findings cannot enable an unqualified v2 policy.
    let review = root.join("unqualified-review.json");
    let mut review_value = json!({"schema_version":2,"reviewer":"synthetic test only",
        "trial_selection_ref":"not a native authorization","codex_sha256":value["worker_sha256"],
        "checkout_root":fixture,"model":"gpt-6-astra","effort":"high","profile_sources":[],
        "findings":{"native_read_only_available":true,"no_external_tool_or_hook_effects":true,
            "codex_managed_chatgpt":true,"no_custom_provider":true},
        "launch_policy_id":value["profile"]["launch_policy_id"],
        "launch_policy_sha256":value["profile"]["launch_policy_sha256"]});
    let mut reviewed = admitted;
    for version in [2, 1] {
        review_value["schema_version"] = json!(version);
        if version == 1 {
            review_value
                .as_object_mut()
                .unwrap()
                .remove("launch_policy_id");
            review_value
                .as_object_mut()
                .unwrap()
                .remove("launch_policy_sha256");
        }
        fs::write(&review, serde_json::to_vec(&review_value).unwrap()).unwrap();
        reviewed.profile["review_sha256"] = json!(request::hash_file(&review).unwrap());
        assert!(reviewed.verify_review().is_err());
    }
    fs::write(&input, serde_json::to_vec_pretty(&reviewed).unwrap()).unwrap();
    let mut events = Vec::new();
    let (code, terminal) =
        devforgeai_codex_worker_probe::runner::run(&input, Default::default(), &mut |v| {
            events.push(v.clone())
        })
        .unwrap();
    assert_eq!(code, 3);
    assert_eq!(terminal["reason"], "profile_unqualified");
    assert!(
        events
            .iter()
            .all(|v| v["kind"] != "spawn_intent" && v["kind"] != "server_started")
    );
}

#[test]
fn schema_two_peer_and_legacy_profile_extensions_are_rejected() {
    let f = support::Fixture::new("WF-17");
    let mut value = serde_json::to_value(&f.request).unwrap();
    value["schema_version"] = json!(2);
    fs::write(&f.input, value.to_string()).unwrap();
    assert!(request::validate(&f.input).is_err());
    value["schema_version"] = json!(1);
    value["adapter"] = json!("codex-0.154.0-stdio");
    value["profile"] = json!({"model":"m","effort":"high","review_ref":f.input,
        "review_sha256":"0".repeat(64),"launch_policy_id":"injected","launch_policy_sha256":"0".repeat(64)});
    fs::write(&f.input, value.to_string()).unwrap();
    assert!(request::validate(&f.input).is_err());
}

#[test]
fn native_profile_schema_is_closed_and_requires_both_policy_fields() {
    let f = support::Fixture::new("WF-17");
    let base = serde_json::to_value(&f.request).unwrap();
    let profile = json!({"model":"m","effort":"high","review_ref":f.input,
        "review_sha256":"0".repeat(64),"launch_policy_id":"selected","launch_policy_sha256":"0".repeat(64)});
    for field in [
        "launch_policy_id",
        "launch_policy_sha256",
        "model",
        "review_sha256",
    ] {
        let mut value = base.clone();
        value["schema_version"] = json!(2);
        value["adapter"] = json!("codex-0.154.0-stdio");
        value["profile"] = profile.clone();
        value["profile"].as_object_mut().unwrap().remove(field);
        assert!(
            serde_json::from_value::<request::Request>(value).is_err(),
            "missing {field}"
        );
    }
    for field in ["launch_policy_id", "launch_policy_sha256"] {
        let mut value = base.clone();
        value["profile"] = profile.clone();
        value["profile"][field] = serde_json::Value::Null;
        assert!(
            serde_json::from_value::<request::Request>(value).is_err(),
            "null {field}"
        );
    }
    let mut value = base;
    value["profile"] = profile;
    value["profile"]["argv"] = json!(["--dangerous"]);
    assert!(serde_json::from_value::<request::Request>(value).is_err());
}
