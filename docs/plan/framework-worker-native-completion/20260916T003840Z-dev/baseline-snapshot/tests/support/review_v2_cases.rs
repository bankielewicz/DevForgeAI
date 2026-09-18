use super::*;
use crate::launch_policy;
use serde_json::{Value, json};
use std::{cell::Cell, fs, path::PathBuf};

struct ReviewCase {
    _root: tempfile::TempDir,
    request: Request,
    review_path: PathBuf,
    inventory_path: PathBuf,
    source_path: PathBuf,
    review: Value,
    inventory: Value,
}

impl ReviewCase {
    fn new(name: &str) -> Self {
        let base = std::env::var_os("WF_TEST_EVIDENCE")
            .map(PathBuf::from)
            .unwrap_or_else(std::env::temp_dir);
        fs::create_dir_all(&base).unwrap();
        let root = tempfile::Builder::new()
            .prefix(name)
            .tempdir_in(base)
            .unwrap();
        let fixture = root.path().join("fixture");
        fs::create_dir(&fixture).unwrap();
        let fixture = resolve(&fixture).unwrap();
        let source_path = root.path().join("config.toml");
        fs::write(&source_path, b"synthetic source bytes\n").unwrap();
        let source_path = resolve(&source_path).unwrap();
        let inventory_path = root.path().join("source-inventory.json");
        let inventory = json!({
            "schema_version": 1,
            "fixture_cwd": fixture,
            "roots": {
                "ancestor_root": root.path(),
                "workspace_root": root.path(),
                "user_codex_root": root.path().join("user"),
                "program_data_codex_root": root.path().join("program-data"),
                "plugin_cache_root": root.path().join("plugins")
            },
            "entries": [{
                "family": "user",
                "path": source_path,
                "state": "file",
                "sha256": hash_file(&source_path).unwrap(),
                "bytes": fs::metadata(&source_path).unwrap().len(),
                "items": null
            }]
        });
        fs::write(&inventory_path, serde_json::to_vec(&inventory).unwrap()).unwrap();
        let review_path = root.path().join("review.json");
        let worker_sha = "a".repeat(64);
        let review = json!({
            "schema_version": 2,
            "reviewer": "operator",
            "trial_selection_ref": "selected WN-01/WN-02",
            "codex_sha256": worker_sha,
            "checkout_root": fixture,
            "model": "gpt-6-astra",
            "effort": "high",
            "profile_sources": [{
                "path": source_path,
                "sha256": hash_file(&source_path).unwrap()
            }],
            "findings": {
                "native_read_only_available": true,
                "no_external_tool_or_hook_effects": true,
                "codex_managed_chatgpt": true,
                "no_custom_provider": true
            },
            "launch_policy_id": launch_policy::ID,
            "launch_policy_sha256": launch_policy::digest(),
            "source_inventory_ref": inventory_path,
            "source_inventory_sha256": hash_file(&inventory_path).unwrap()
        });
        let mut case = Self {
            _root: root,
            request: Request {
                schema_version: 2,
                project_id: "p".into(),
                checkout_id: "c".into(),
                work_id: "w".into(),
                run_id: "r".into(),
                candidate_sha256: "b".repeat(64),
                checkout_root: fixture,
                run_dir: PathBuf::from(r"C:\not-created"),
                worker_executable: PathBuf::from(r"C:\not-used.exe"),
                worker_sha256: worker_sha,
                adapter: launch_policy::ADAPTER.into(),
                scenario: "complete".into(),
                profile: Value::Null,
            },
            review_path,
            inventory_path,
            source_path,
            review,
            inventory,
        };
        case.bind();
        case
    }

    fn bind(&mut self) {
        self.bind_bytes(serde_json::to_vec(&self.review).unwrap());
    }

    fn bind_bytes(&mut self, bytes: Vec<u8>) {
        fs::write(&self.review_path, &bytes).unwrap();
        self.request.profile = json!({
            "model": "gpt-6-astra",
            "effort": "high",
            "review_ref": self.review_path,
            "review_sha256": digest(&bytes),
            "launch_policy_id": launch_policy::ID,
            "launch_policy_sha256": launch_policy::digest()
        });
    }

    fn bind_inventory(&mut self) {
        fs::write(
            &self.inventory_path,
            serde_json::to_vec(&self.inventory).unwrap(),
        )
        .unwrap();
        self.review["source_inventory_sha256"] = json!(hash_file(&self.inventory_path).unwrap());
        self.bind();
    }

    fn verify(&self, require_all_findings: bool) -> Result<Vec<PathBuf>> {
        self.request
            .verify_review_v2_with(require_all_findings, |_| Ok(()))
    }
}

#[test]
fn preflight_accepts_false_findings_while_run_requires_all_true() {
    let mut case = ReviewCase::new("NI-T08-review-findings-");
    case.review["findings"]["no_external_tool_or_hook_effects"] = json!(false);
    case.bind();
    assert_eq!(case.verify(false).unwrap(), vec![case.source_path.clone()]);
    assert_eq!(case.verify(true).unwrap_err(), "profile_unqualified");

    case.review["findings"]["no_external_tool_or_hook_effects"] = json!(true);
    case.bind();
    assert_eq!(case.verify(true).unwrap(), vec![case.source_path]);
}

#[test]
fn v2_review_is_closed_and_binds_all_selected_identities() {
    let mut case = ReviewCase::new("NI-T08-review-closed-");
    for (field, bad) in [
        ("schema_version", json!(1)),
        ("reviewer", json!("")),
        ("trial_selection_ref", json!("")),
        ("codex_sha256", json!("0".repeat(64))),
        ("checkout_root", json!(case._root.path())),
        ("model", json!("substitute")),
        ("effort", json!("medium")),
        ("launch_policy_id", json!("caller-selected")),
        ("launch_policy_sha256", json!("0".repeat(64))),
        ("source_inventory_ref", Value::Null),
        ("source_inventory_sha256", json!("0".repeat(64))),
    ] {
        let original = case.review[field].clone();
        case.review[field] = bad;
        case.bind();
        assert_eq!(
            case.verify(false).unwrap_err(),
            "profile_unqualified",
            "{field}"
        );
        case.review[field] = original;
    }
    for field in [
        "schema_version",
        "reviewer",
        "trial_selection_ref",
        "codex_sha256",
        "checkout_root",
        "model",
        "effort",
        "profile_sources",
        "findings",
        "launch_policy_id",
        "launch_policy_sha256",
        "source_inventory_ref",
        "source_inventory_sha256",
    ] {
        let mut value = case.review.clone();
        value.as_object_mut().unwrap().remove(field);
        case.bind_bytes(serde_json::to_vec(&value).unwrap());
        assert_eq!(
            case.verify(false).unwrap_err(),
            "profile_unqualified",
            "{field}"
        );
    }
    for field in [
        "schema_version",
        "reviewer",
        "trial_selection_ref",
        "codex_sha256",
        "checkout_root",
        "model",
        "effort",
        "profile_sources",
        "findings",
        "launch_policy_id",
        "launch_policy_sha256",
        "source_inventory_ref",
        "source_inventory_sha256",
    ] {
        let mut value = case.review.clone();
        value[field] = Value::Null;
        case.bind_bytes(serde_json::to_vec(&value).unwrap());
        assert_eq!(
            case.verify(false).unwrap_err(),
            "profile_unqualified",
            "null {field}"
        );
    }
    for field in [
        "native_read_only_available",
        "no_external_tool_or_hook_effects",
        "codex_managed_chatgpt",
        "no_custom_provider",
    ] {
        for mutation in ["missing", "null"] {
            let mut value = case.review.clone();
            if mutation == "missing" {
                value["findings"].as_object_mut().unwrap().remove(field);
            } else {
                value["findings"][field] = Value::Null;
            }
            case.bind_bytes(serde_json::to_vec(&value).unwrap());
            assert_eq!(
                case.verify(false).unwrap_err(),
                "profile_unqualified",
                "{mutation} findings.{field}"
            );
        }
    }
    let mut extra = case.review.clone();
    extra["unexpected"] = json!(true);
    case.bind_bytes(serde_json::to_vec(&extra).unwrap());
    assert_eq!(case.verify(false).unwrap_err(), "profile_unqualified");

    let mut source_extra = case.review.clone();
    source_extra["profile_sources"][0]["unexpected"] = json!(true);
    case.bind_bytes(serde_json::to_vec(&source_extra).unwrap());
    assert_eq!(case.verify(false).unwrap_err(), "profile_unqualified");
    for field in ["path", "sha256"] {
        let mut value = case.review.clone();
        value["profile_sources"][0]
            .as_object_mut()
            .unwrap()
            .remove(field);
        case.bind_bytes(serde_json::to_vec(&value).unwrap());
        assert_eq!(case.verify(false).unwrap_err(), "profile_unqualified");
    }

    let encoded = serde_json::to_string(&case.review).unwrap();
    case.bind_bytes(format!(r#"{{"reviewer":"duplicate",{}"#, &encoded[1..]).into_bytes());
    assert_eq!(case.verify(false).unwrap_err(), "profile_unqualified");
}

#[test]
fn request_profile_and_review_policy_bindings_cannot_diverge() {
    let mut case = ReviewCase::new("NI-T08-review-policy-");
    case.request.profile["model"] = json!("other");
    assert_eq!(case.verify(false).unwrap_err(), "profile_unqualified");
    case.request.profile["model"] = json!("gpt-6-astra");
    case.request.profile["launch_policy_id"] = json!("other");
    assert_eq!(case.verify(false).unwrap_err(), "profile_unqualified");
    case.request.profile["launch_policy_id"] = json!(launch_policy::ID);
    case.request.profile["launch_policy_sha256"] = json!("0".repeat(64));
    assert_eq!(case.verify(false).unwrap_err(), "profile_unqualified");
}

#[test]
fn profile_sources_exactly_cover_inventory_file_bindings() {
    let mut case = ReviewCase::new("NI-T08-review-coverage-");
    let binding = case.review["profile_sources"][0].clone();
    for sources in [
        json!([]),
        json!([binding.clone(), binding.clone()]),
        json!([{"path":case.source_path,"sha256":"0".repeat(64)}]),
        json!([binding.clone(), {"path":case.review_path,"sha256":hash_file(&case.review_path).unwrap()}]),
    ] {
        case.review["profile_sources"] = sources;
        case.bind();
        assert_eq!(case.verify(false).unwrap_err(), "profile_unqualified");
    }
    case.review["profile_sources"] = json!([binding]);
    case.bind();
    assert_eq!(case.verify(false).unwrap(), vec![case.source_path]);
}

#[test]
fn inventory_digest_shape_fixture_and_freshness_are_mandatory() {
    let mut case = ReviewCase::new("NI-T10-review-freshness-");
    case.review["source_inventory_sha256"] = json!("0".repeat(64));
    case.bind();
    assert_eq!(case.verify(false).unwrap_err(), "profile_unqualified");

    case.review["source_inventory_sha256"] = json!(hash_file(&case.inventory_path).unwrap());
    let original_fixture = case.inventory["fixture_cwd"].clone();
    case.inventory["fixture_cwd"] = json!(case._root.path());
    case.bind_inventory();
    assert_eq!(case.verify(false).unwrap_err(), "profile_unqualified");

    case.inventory["fixture_cwd"] = original_fixture;
    case.inventory["unknown"] = json!(true);
    case.bind_inventory();
    assert_eq!(case.verify(false).unwrap_err(), "profile_unqualified");
    case.inventory.as_object_mut().unwrap().remove("unknown");
    case.bind_inventory();

    let called = Cell::new(false);
    let error = case
        .request
        .verify_review_v2_with(false, |_| {
            called.set(true);
            Err("profile_source_drift".into())
        })
        .unwrap_err();
    assert!(called.get());
    assert_eq!(error, "profile_unqualified");
}
