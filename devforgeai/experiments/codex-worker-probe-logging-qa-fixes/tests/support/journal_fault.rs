use super::*;
pub(crate) fn deny_optional_writes(journal: &mut Journal, dir: &Path) {
    // CreateFile on an existing directory fails. This exercises the real optional
    // sink failure, not the mandatory journal failure injector.
    let absent = dir.join("inaccessible-log-target");
    journal.diagnostics = logging::Sink::new(&absent, Level::Debug);
}
