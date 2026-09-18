#[path = "../fixtures/generator.rs"]
mod generator;

#[test]
fn benchmark_fixture_is_seeded_and_has_exact_file_and_byte_counts() {
    let first = tempfile::tempdir().unwrap();
    let second = tempfile::tempdir().unwrap();
    let a = generator::generate(first.path(), 10, 20000, 20260913).unwrap();
    let b = generator::generate(second.path(), 10, 20000, 20260913).unwrap();
    assert_eq!(a, b);
    assert_eq!(a.len(), 10);
    assert_eq!(a.iter().map(|entry| entry.bytes).sum::<usize>(), 20000);
    let mut groups = std::collections::BTreeMap::new();
    for entry in a {
        *groups.entry(entry.language).or_insert(0) += 1;
    }
    assert_eq!(groups.len(), 5);
    assert!(groups.values().all(|count| *count == 2));
}
