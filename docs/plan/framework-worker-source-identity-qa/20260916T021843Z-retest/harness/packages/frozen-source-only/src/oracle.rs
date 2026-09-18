use serde::Deserialize;

#[derive(Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
struct ResultSet {
    results: Vec<Entry>,
}

#[derive(Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
struct Entry {
    id: String,
    final_state: String,
    outcomes: Vec<String>,
}

/// Compare against the separately published verifier artifact, never worker assertions.
pub fn matches(text: &str) -> bool {
    let expected = include_str!("../tests/fixtures/expected.json");
    match (
        serde_json::from_str::<ResultSet>(text),
        serde_json::from_str::<ResultSet>(expected),
    ) {
        (Ok(actual), Ok(expected)) => actual == expected,
        _ => false,
    }
}
