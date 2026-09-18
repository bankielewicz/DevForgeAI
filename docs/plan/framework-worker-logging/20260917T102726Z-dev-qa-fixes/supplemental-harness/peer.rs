use std::io::Write;
fn main() {
    // Deliberately malformed UTF8 and a final unterminated stdout line, emitted
    // through real Windows pipes. This executable never starts Codex.
    std::io::stdout().write_all(b"\xff\nunterminated\xe2\x82").unwrap();
    std::io::stdout().flush().unwrap();
    std::io::stderr().write_all(b"\xfe").unwrap();
    std::io::stderr().flush().unwrap();
    std::process::exit(23);
}
