mod support;
use devforgeai_codex_worker_probe::request;
use serde_json::{Value, json};
use std::fs;
#[test]
fn reviewed_native_profile_sources_and_findings_are_checked_without_launch() {
    let f = support::Fixture::new("WF-17");
    let mut r = f.request.clone();
    r.adapter = "codex-0.154.0-stdio".into();
    let source = f.root.path().join("synthetic-policy.txt");
    fs::write(&source, b"synthetic policy only").unwrap();
    let path = f.root.path().join("review.json");
    let base = json!({"schema_version":1,"reviewer":"test operator","trial_selection_ref":"synthetic offline validation only","codex_sha256":r.worker_sha256,
        "checkout_root":r.checkout_root,"model":"test-model","effort":"test-effort","profile_sources":[{"path":source,"sha256":request::hash_file(&source).unwrap()}],
        "findings":{"native_read_only_available":true,"no_external_tool_or_hook_effects":true,"codex_managed_chatgpt":true,"no_custom_provider":true}});
    let bind = |r: &mut request::Request, v: &Value| {
        let bytes = serde_json::to_vec(v).unwrap();
        fs::write(&path, &bytes).unwrap();
        r.profile = json!({"model":"test-model","effort":"test-effort","review_ref":path,"review_sha256":request::digest(&bytes)});
    };
    bind(&mut r, &base);
    assert!(r.verify_review().is_ok());
    fs::remove_file(r.checkout_root.join("peer-case.txt")).unwrap();
    {
        let mut j = devforgeai_codex_worker_probe::journal::Journal::create(&r).unwrap();
        j.append("admitted", json!({})).unwrap();
        assert_eq!(
            devforgeai_codex_worker_probe::journal::inspect(&r.run_dir, 0, 100).unwrap()["state"],
            "admitted"
        );
        fs::write(r.run_dir.join("profile-review.json"), b"changed snapshot").unwrap();
        assert_eq!(
            devforgeai_codex_worker_probe::journal::inspect(&r.run_dir, 0, 100).unwrap_err(),
            "evidence_corrupt"
        );
    }
    for (key, bad) in [
        ("schema_version", json!(2)),
        ("reviewer", json!("")),
        ("trial_selection_ref", json!("")),
        ("codex_sha256", json!("0".repeat(64))),
        ("checkout_root", json!(f.root.path())),
        ("model", json!("substitute")),
        ("effort", json!("other")),
        ("extra", json!(true)),
    ] {
        let mut v = base.clone();
        v[key] = bad;
        bind(&mut r, &v);
        assert!(r.verify_review().is_err(), "{key}");
    }
    for key in [
        "native_read_only_available",
        "no_external_tool_or_hook_effects",
        "codex_managed_chatgpt",
        "no_custom_provider",
    ] {
        let mut v = base.clone();
        v["findings"][key] = json!(false);
        bind(&mut r, &v);
        assert!(r.verify_review().is_err());
    }
    let mut v = base.clone();
    v["profile_sources"] = json!([base["profile_sources"][0], base["profile_sources"][0]]);
    bind(&mut r, &v);
    assert!(r.verify_review().is_err());
    bind(&mut r, &base);
    fs::write(&source, b"changed policy").unwrap();
    assert!(r.verify_review().is_err());
    fs::write(&path, b"changed review").unwrap();
    assert!(r.verify_review().is_err());
    r.profile =
        json!({"model":"","effort":"high","review_ref":path,"review_sha256":"0".repeat(64)});
    assert!(r.profile().is_err());
    r.profile = json!({"model":"a","effort":"","review_ref":path,"review_sha256":"0".repeat(64)});
    assert!(r.profile().is_err());
    r.profile = json!({"model":"a","effort":"high","review_ref":path,"review_sha256":"bad"});
    assert!(r.profile().is_err());
    assert!(!f.root.path().join("peer-trace.jsonl").exists());
}

#[test]
fn credential_store_is_not_an_admissible_profile_source() {
    let f = support::Fixture::new("WF-17");
    let mut r = f.request.clone();
    r.adapter = "codex-0.154.0-stdio".into();
    let auth = f.root.path().join("auth.json");
    fs::write(&auth, b"synthetic credential fixture").unwrap();
    let path = f.root.path().join("review.json");
    let review = json!({"schema_version":1,"reviewer":"test","trial_selection_ref":"synthetic","codex_sha256":r.worker_sha256,"checkout_root":r.checkout_root,"model":"m","effort":"high",
        "profile_sources":[{"path":auth,"sha256":request::digest(b"synthetic credential fixture")}],"findings":{"native_read_only_available":true,"no_external_tool_or_hook_effects":true,"codex_managed_chatgpt":true,"no_custom_provider":true}});
    let bytes = serde_json::to_vec(&review).unwrap();
    fs::write(&path, &bytes).unwrap();
    r.profile = json!({"model":"m","effort":"high","review_ref":path,"review_sha256":request::digest(&bytes)});
    assert!(r.verify_review().is_err());
}

#[test]
fn unavailable_review_retains_incomplete_evidence_without_reading_credentials() {
    let f = support::Fixture::new("WF-17");
    let mut r = f.request.clone();
    r.adapter = "codex-0.154.0-stdio".into();
    fs::remove_file(r.checkout_root.join("peer-case.txt")).unwrap();
    r.profile = json!({"model":"m","effort":"high","review_ref":f.root.path().join("missing-review.json"),"review_sha256":"0".repeat(64)});
    assert!(r.verify_review().is_err());
    let mut j = devforgeai_codex_worker_probe::journal::Journal::create(&r).unwrap();
    j.append("admitted", json!({})).unwrap();
    assert_eq!(
        devforgeai_codex_worker_probe::journal::inspect(&r.run_dir, 0, 100).unwrap_err(),
        "evidence_incomplete"
    );
}
