use devforgeai_codex_worker_probe::oracle;

const EXPECTED: &str = include_str!("fixtures/expected.json");

#[test]
fn exact_independent_result() {
    assert!(oracle::matches(EXPECTED));
    assert!(oracle::matches(&EXPECTED.replace(':', " : ")));
}

#[test]
fn rejects_invalid_results() {
    for text in [
        "",
        "{}",
        "null",
        "{\"results\":[]}",
        "{\"results\":[],\"results\":[]}",
    ] {
        assert!(!oracle::matches(text));
    }
    assert!(!oracle::matches(
        &EXPECTED.replace("cancelled", "dispatched")
    ));
    assert!(!oracle::matches(&EXPECTED.replacen(
        "{",
        "{\"extra\":true,",
        1
    )));
    assert!(!oracle::matches(
        &EXPECTED.replace("\"id\":\"A\"", "\"id\":\"A\",\"id\":\"A\"")
    ));
}
