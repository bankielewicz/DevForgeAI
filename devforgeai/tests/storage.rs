use devforgeai_index::index::digest;
use devforgeai_index::storage::{Store, StoredFile};
use serde_json::json;
use tempfile::tempdir;

fn file(text: &str) -> StoredFile {
    StoredFile {
        path: "main.py".into(),
        sha256: Some(digest(text.as_bytes())),
        bytes: Some(text.as_bytes().to_vec()),
        record: json!({"state":"indexed","language":"python"}),
    }
}

#[test]
fn unpublished_and_cancelled_generation_never_replace_current() {
    let temp = tempdir().unwrap();
    let mut store = Store::open(temp.path()).unwrap();
    store.begin_generation("project", "first").unwrap();
    store.stage_file("first", &file("before")).unwrap();
    assert!(store.current("project").unwrap().is_none());
    store
        .publish("project", "first", &json!({"coverage":"complete"}))
        .unwrap();
    store.begin_generation("project", "second").unwrap();
    store.stage_file("second", &file("after")).unwrap();
    assert_eq!(store.current("project").unwrap().as_deref(), Some("first"));
    store.abandon("second").unwrap();
    assert_eq!(
        store.source("first", "main.py").unwrap().unwrap(),
        b"before"
    );
    drop(store);
    assert_eq!(
        Store::open(temp.path())
            .unwrap()
            .current("project")
            .unwrap()
            .as_deref(),
        Some("first")
    );
}

#[test]
fn retention_keeps_exactly_two_published_generations_and_deletes_only_cache() {
    let temp = tempdir().unwrap();
    let mut store = Store::open(temp.path()).unwrap();
    for generation in ["one", "two", "three"] {
        store.begin_generation("project", generation).unwrap();
        store.stage_file(generation, &file(generation)).unwrap();
        store.publish("project", generation, &json!({})).unwrap();
    }
    assert!(store.source("one", "main.py").unwrap().is_none());
    assert_eq!(store.source("two", "main.py").unwrap().unwrap(), b"two");
    assert_eq!(store.source("three", "main.py").unwrap().unwrap(), b"three");
    store.remove_project("project").unwrap();
    assert!(store.current("project").unwrap().is_none());
    assert!(store.source("three", "main.py").unwrap().is_none());
}

#[test]
fn mutation_retries_survive_restart_and_payload_changes_conflict() {
    let temp = tempdir().unwrap();
    let mut store = Store::open(temp.path()).unwrap();
    store
        .remember_request("id", "payload", &json!({"job_id":"one"}), 100)
        .unwrap();
    assert_eq!(
        store.replay_request("id", "payload", 101).unwrap(),
        Some(json!({"job_id":"one"}))
    );
    assert!(store.replay_request("id", "changed", 101).is_err());
    drop(store);
    let store = Store::open(temp.path()).unwrap();
    assert!(
        store
            .replay_request("id", "payload", 100 + 86400)
            .unwrap()
            .is_none()
    );
}

#[test]
fn newer_schema_and_corruption_are_refused_without_destroying_bytes() {
    let temp = tempdir().unwrap();
    let store = Store::open(temp.path()).unwrap();
    drop(store);
    let path = temp.path().join("index.sqlite3");
    let connection = rusqlite::Connection::open(&path).unwrap();
    connection.pragma_update(None, "user_version", 99).unwrap();
    drop(connection);
    let before = std::fs::read(&path).unwrap();
    assert!(Store::open(temp.path()).is_err());
    assert_eq!(std::fs::read(&path).unwrap(), before);
    let corrupt = tempdir().unwrap();
    std::fs::write(corrupt.path().join("index.sqlite3"), b"invalid database").unwrap();
    assert!(Store::open(corrupt.path()).is_err());
    assert_eq!(
        std::fs::read(corrupt.path().join("index.sqlite3")).unwrap(),
        b"invalid database"
    );
}

#[test]
fn invalid_snapshots_and_foreign_publications_roll_back() {
    let temp = tempdir().unwrap();
    let mut store = Store::open(temp.path()).unwrap();
    store.begin_generation("p", "a").unwrap();
    let mut bad = file("bytes");
    bad.sha256 = Some("wrong".into());
    assert!(store.stage_file("a", &bad).is_err());
    assert!(store.publish("other", "a", &json!({})).is_err());
    assert!(store.current("p").unwrap().is_none());
    store.stage_file("a", &file("valid")).unwrap();
    store
        .publish("p", "a", &json!({"coverage":"complete"}))
        .unwrap();
    assert!(store.stage_file("a", &file("changed")).is_err());
    assert!(store.publish("p", "a", &json!({})).is_err());
    assert_eq!(store.source("a", "main.py").unwrap().unwrap(), b"valid");
    store.abandon("a").unwrap();
    assert_eq!(store.current("p").unwrap().as_deref(), Some("a"));
    assert_eq!(store.summary("p").unwrap().unwrap()["coverage"], "complete");
    assert!(store.summary("absent").unwrap().is_none());
    assert!(
        store
            .cached_file("a", "main.py", "wrong")
            .unwrap()
            .is_none()
    );
}

#[test]
fn sqlite_reader_keeps_its_generation_while_writer_publishes_and_collects() {
    let temp = tempdir().unwrap();
    let mut store = Store::open(temp.path()).unwrap();
    store.begin_generation("p", "one").unwrap();
    store.stage_file("one", &file("original")).unwrap();
    store.publish("p", "one", &json!({})).unwrap();
    let reader = rusqlite::Connection::open_with_flags(
        temp.path().join("index.sqlite3"),
        rusqlite::OpenFlags::SQLITE_OPEN_READ_ONLY,
    )
    .unwrap();
    reader.execute_batch("BEGIN").unwrap();
    let before: String = reader
        .query_row("SELECT current FROM projects WHERE id='p'", [], |row| {
            row.get(0)
        })
        .unwrap();
    assert_eq!(before, "one");
    for id in ["two", "three"] {
        store.begin_generation("p", id).unwrap();
        store.stage_file(id, &file(id)).unwrap();
        store.publish("p", id, &json!({})).unwrap();
    }
    let bytes:Vec<u8>=reader.query_row("SELECT s.bytes FROM snapshots s JOIN files f ON s.hash=f.hash WHERE f.generation='one'",[],|row|row.get(0)).unwrap();
    assert_eq!(bytes, b"original");
    reader.execute_batch("COMMIT").unwrap();
    assert!(store.source("one", "main.py").unwrap().is_none());
}
