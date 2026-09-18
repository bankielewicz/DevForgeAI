//! Single-writer cache. Only the published pointer makes staged records visible.
use crate::protocol::{ErrorCode, ProtocolError, Result};
use rusqlite::{Connection, OptionalExtension, params};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::path::Path;

pub struct Store {
    connection: Connection,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StoredFile {
    pub path: String,
    pub sha256: Option<String>,
    pub bytes: Option<Vec<u8>>,
    pub record: Value,
}

fn sql(error: rusqlite::Error) -> ProtocolError {
    let code = match error.sqlite_error_code() {
        Some(rusqlite::ErrorCode::DatabaseCorrupt | rusqlite::ErrorCode::NotADatabase) => {
            ErrorCode::StorageCorrupt
        }
        _ => ErrorCode::InternalError,
    };
    ProtocolError::new(code, error.to_string())
}

impl Store {
    pub fn open(directory: &Path) -> Result<Self> {
        let path = directory.join("index.sqlite3");
        let connection = Connection::open(&path).map_err(sql)?;
        let version: i64 = connection
            .pragma_query_value(None, "user_version", |row| row.get(0))
            .map_err(sql)?;
        if version > 1 {
            return Err(ProtocolError::new(
                ErrorCode::StorageCorrupt,
                "Newer unsupported database schema; no downgrade performed",
            ));
        }
        let integrity: String = connection
            .query_row("PRAGMA quick_check", [], |row| row.get(0))
            .map_err(sql)?;
        if integrity != "ok" {
            return Err(ProtocolError::new(
                ErrorCode::StorageCorrupt,
                "Database integrity check failed",
            ));
        }
        if version == 0 && path.metadata().map(|m| m.len() > 0).unwrap_or(false) {
            std::fs::copy(
                &path,
                directory.join(format!("schema-backup-{}.sqlite3", uuid::Uuid::new_v4())),
            )
            .map_err(|e| ProtocolError::new(ErrorCode::InternalError, e.to_string()))?;
        }
        connection.execute_batch("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA synchronous=FULL;
            CREATE TABLE IF NOT EXISTS generations(id TEXT PRIMARY KEY, project TEXT NOT NULL, published INTEGER NOT NULL DEFAULT 0, summary TEXT NOT NULL DEFAULT '{}');
            CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY, current TEXT, previous TEXT);
            CREATE TABLE IF NOT EXISTS snapshots(hash TEXT PRIMARY KEY, bytes BLOB NOT NULL);
            CREATE TABLE IF NOT EXISTS files(generation TEXT NOT NULL REFERENCES generations(id) ON DELETE CASCADE, path TEXT NOT NULL, hash TEXT REFERENCES snapshots(hash), record TEXT NOT NULL, PRIMARY KEY(generation,path));
            CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY, payload TEXT NOT NULL, response TEXT NOT NULL, created INTEGER NOT NULL);
            CREATE VIRTUAL TABLE IF NOT EXISTS source_fts USING fts5(generation UNINDEXED, path UNINDEXED, code, tokenize='unicode61');
            PRAGMA user_version=1;") .map_err(sql)?;
        Ok(Self { connection })
    }
    pub fn begin_generation(&mut self, project: &str, id: &str) -> Result<()> {
        self.connection
            .execute(
                "INSERT INTO generations(id,project) VALUES(?1,?2)",
                params![id, project],
            )
            .map_err(sql)?;
        Ok(())
    }
    pub fn stage_file(&mut self, generation: &str, file: &StoredFile) -> Result<()> {
        let transaction = self.connection.transaction().map_err(sql)?;
        let published: i64 = transaction
            .query_row(
                "SELECT published FROM generations WHERE id=?1",
                [generation],
                |row| row.get(0),
            )
            .map_err(sql)?;
        if published != 0 {
            return Err(ProtocolError::new(
                ErrorCode::InvalidArgument,
                "Published generations are immutable",
            ));
        }
        if let (Some(hash), Some(bytes)) = (&file.sha256, &file.bytes) {
            if crate::index::digest(bytes) != *hash {
                return Err(ProtocolError::new(
                    ErrorCode::InvalidArgument,
                    "Snapshot hash mismatch",
                ));
            }
            transaction
                .execute(
                    "INSERT OR IGNORE INTO snapshots(hash,bytes) VALUES(?1,?2)",
                    params![hash, bytes],
                )
                .map_err(sql)?;
            transaction
                .execute(
                    "INSERT INTO source_fts(generation,path,code) VALUES(?1,?2,?3)",
                    params![generation, file.path, String::from_utf8_lossy(bytes)],
                )
                .map_err(sql)?;
        }
        transaction
            .execute(
                "INSERT INTO files(generation,path,hash,record) VALUES(?1,?2,?3,?4)",
                params![generation, file.path, file.sha256, file.record.to_string()],
            )
            .map_err(sql)?;
        transaction.commit().map_err(sql)
    }
    pub fn current(&self, project: &str) -> Result<Option<String>> {
        self.connection
            .query_row(
                "SELECT current FROM projects WHERE id=?1",
                [project],
                |row| row.get(0),
            )
            .optional()
            .map_err(sql)
    }
    pub fn summary(&self, project: &str) -> Result<Option<Value>> {
        let text: Option<String> = self.connection.query_row("SELECT g.summary FROM generations g JOIN projects p ON p.current=g.id WHERE p.id=?1", [project], |row| row.get(0)).optional().map_err(sql)?;
        text.map(|text| {
            serde_json::from_str(&text)
                .map_err(|e| ProtocolError::new(ErrorCode::StorageCorrupt, e.to_string()))
        })
        .transpose()
    }
    pub fn source(&self, generation: &str, path: &str) -> Result<Option<Vec<u8>>> {
        self.connection.query_row("SELECT s.bytes FROM snapshots s JOIN files f ON s.hash=f.hash JOIN generations g ON g.id=f.generation WHERE f.generation=?1 AND f.path=?2 AND g.published=1", params![generation,path], |row| row.get(0)).optional().map_err(sql)
    }
    pub fn cached_file(&self, generation: &str, path: &str, hash: &str) -> Result<Option<Value>> {
        let record: Option<String> = self
            .connection
            .query_row(
                "SELECT record FROM files WHERE generation=?1 AND path=?2 AND hash=?3",
                params![generation, path, hash],
                |row| row.get(0),
            )
            .optional()
            .map_err(sql)?;
        record
            .map(|text| {
                serde_json::from_str(&text)
                    .map_err(|e| ProtocolError::new(ErrorCode::StorageCorrupt, e.to_string()))
            })
            .transpose()
    }
    pub fn publish(&mut self, project: &str, generation: &str, summary: &Value) -> Result<()> {
        let transaction = self.connection.transaction().map_err(sql)?;
        let count = transaction.execute("UPDATE generations SET published=1,summary=?3 WHERE id=?1 AND project=?2 AND published=0", params![generation,project,summary.to_string()]).map_err(sql)?;
        if count != 1 {
            return Err(ProtocolError::new(
                ErrorCode::InvalidArgument,
                "Generation is absent, foreign or already published",
            ));
        }
        transaction.execute("INSERT INTO projects(id,current) VALUES(?1,?2) ON CONFLICT(id) DO UPDATE SET previous=current,current=excluded.current", params![project,generation]).map_err(sql)?;
        transaction.execute("DELETE FROM source_fts WHERE generation IN (SELECT id FROM generations WHERE project=?1 AND published=1 AND id NOT IN (SELECT current FROM projects WHERE id=?1 UNION SELECT previous FROM projects WHERE id=?1 AND previous IS NOT NULL))", [project]).map_err(sql)?;
        transaction.execute("DELETE FROM generations WHERE project=?1 AND published=1 AND id NOT IN (SELECT current FROM projects WHERE id=?1 UNION SELECT previous FROM projects WHERE id=?1 AND previous IS NOT NULL)", [project]).map_err(sql)?;
        transaction.execute("DELETE FROM snapshots WHERE hash NOT IN (SELECT hash FROM files WHERE hash IS NOT NULL)", []).map_err(sql)?;
        transaction.commit().map_err(sql)
    }
    pub fn abandon(&mut self, generation: &str) -> Result<()> {
        let transaction = self.connection.transaction().map_err(sql)?;
        transaction.execute("DELETE FROM source_fts WHERE generation IN (SELECT id FROM generations WHERE id=?1 AND published=0)", [generation]).map_err(sql)?;
        transaction
            .execute(
                "DELETE FROM generations WHERE id=?1 AND published=0",
                [generation],
            )
            .map_err(sql)?;
        transaction.execute("DELETE FROM snapshots WHERE hash NOT IN (SELECT hash FROM files WHERE hash IS NOT NULL)", []).map_err(sql)?;
        transaction.commit().map_err(sql)
    }
    pub fn discard_interrupted(&mut self) -> Result<()> {
        self.connection.execute_batch("BEGIN; DELETE FROM source_fts WHERE generation IN (SELECT id FROM generations WHERE published=0); DELETE FROM generations WHERE published=0; DELETE FROM snapshots WHERE hash NOT IN (SELECT hash FROM files WHERE hash IS NOT NULL); COMMIT;").map_err(sql)
    }
    pub fn remove_project(&mut self, project: &str) -> Result<()> {
        let transaction = self.connection.transaction().map_err(sql)?;
        transaction.execute("DELETE FROM source_fts WHERE generation IN (SELECT id FROM generations WHERE project=?1)",[project]).map_err(sql)?;
        transaction
            .execute("DELETE FROM projects WHERE id=?1", [project])
            .map_err(sql)?;
        transaction
            .execute("DELETE FROM generations WHERE project=?1", [project])
            .map_err(sql)?;
        transaction.execute("DELETE FROM snapshots WHERE hash NOT IN (SELECT hash FROM files WHERE hash IS NOT NULL)",[]).map_err(sql)?;
        transaction.commit().map_err(sql)
    }
    pub fn remember_request(
        &mut self,
        id: &str,
        payload: &str,
        response: &Value,
        now: i64,
    ) -> Result<()> {
        let transaction = self.connection.transaction().map_err(sql)?;
        transaction
            .execute(
                "DELETE FROM requests WHERE created <= ?1",
                [now.saturating_sub(86400)],
            )
            .map_err(sql)?;
        transaction
            .execute(
                "INSERT INTO requests(id,payload,response,created) VALUES(?1,?2,?3,?4)",
                params![id, payload, response.to_string(), now],
            )
            .map_err(sql)?;
        transaction.commit().map_err(sql)
    }
    pub fn replay_request(&self, id: &str, payload: &str, now: i64) -> Result<Option<Value>> {
        let record: Option<(String, String, i64)> = self
            .connection
            .query_row(
                "SELECT payload,response,created FROM requests WHERE id=?1",
                [id],
                |row| Ok((row.get(0)?, row.get(1)?, row.get(2)?)),
            )
            .optional()
            .map_err(sql)?;
        if let Some((old, response, created)) = record {
            if now.saturating_sub(created) >= 86400 {
                return Ok(None);
            }
            if old != payload {
                return Err(ProtocolError::new(
                    ErrorCode::RequestIdConflict,
                    "Request ID already bound to another payload",
                ));
            }
            return serde_json::from_str(&response)
                .map(Some)
                .map_err(|e| ProtocolError::new(ErrorCode::StorageCorrupt, e.to_string()));
        }
        Ok(None)
    }
}
