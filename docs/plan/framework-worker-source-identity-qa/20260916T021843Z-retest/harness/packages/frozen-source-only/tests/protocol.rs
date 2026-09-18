mod support;
use serde_json::json;
fn check(case: &str, exit: i32) -> support::Fixture {
    let f = support::Fixture::new(case);
    let result = f.run();
    assert_eq!(result.0, exit, "{case}: {}", result.1);
    let trace = f.trace();
    assert_eq!(
        trace.iter().filter(|v| v["method"] == "initialize").count(),
        1
    );
    assert!(trace.iter().filter(|v| v["method"] == "turn/start").count() <= 1);
    f
}
#[test]
fn wf_01() {
    let f = check("WF-01", 0);
    let trace = f.trace();
    assert_eq!(
        trace.iter().filter(|v| v["method"] == "turn/start").count(),
        1
    );
}
#[test]
fn wf_02() {
    for i in 1..=2 {
        let f = check(&format!("WF-02-{i}"), 3);
        assert!(!f.trace().iter().any(|v| v["method"] == "turn/start"));
    }
}
#[test]
fn wf_03() {
    for i in 1..=5 {
        let f = check(&format!("WF-03-{i}"), 3);
        assert!(!f.trace().iter().any(|v| v["method"] == "turn/start"));
    }
}
#[test]
fn wf_04() {
    for i in 1..=5 {
        let f = check(&format!("WF-04-{i}"), 4);
        assert!(f.trace().iter().any(|v| v["method"] == "turn/start"));
        let view =
            devforgeai_codex_worker_probe::journal::inspect(&f.request.run_dir, 0, 100).unwrap();
        assert_eq!(
            view["events"].as_array().unwrap().last().unwrap()["data"]["reason"],
            "protocol_error"
        );
    }
}
#[test]
fn wf_05() {
    check("WF-05", 0);
}
#[test]
fn wf_06() {
    for i in 1..=3 {
        let f = check(&format!("WF-06-{i}"), 4);
        let trace = f.trace();
        let response = trace.iter().find(|v| v["id"] == 900).unwrap();
        if i < 3 {
            assert_eq!(response, &json!({"id":900,"result":{"decision":"cancel"}}));
        } else {
            assert_eq!(response["error"]["code"], -32601);
        }
    }
}
#[test]
fn wf_07() {
    let f = check("WF-07", 4);
    let s = devforgeai_codex_worker_probe::journal::inspect(&f.request.run_dir, 0, 100).unwrap();
    assert!(s.to_string().contains("usageLimitExceeded"));
}
#[test]
fn wf_08() {
    for i in 1..=2 {
        let f = support::Fixture::new(&format!("WF-08-{i}"));
        let (exit, v) = f.run();
        assert_eq!(exit, 0);
        if i == 1 {
            assert_eq!(v["usage"]["total"]["totalTokens"], 17);
        } else {
            assert!(v["usage"].is_null());
        }
    }
}
