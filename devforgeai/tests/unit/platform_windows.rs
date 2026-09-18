use super::*;

#[test]
fn invalid_native_process_and_token_handles_return_errors() {
    let mut invalid = DetachedChild(std::ptr::null_mut());
    assert!(invalid.try_wait().is_err());
    assert!(unsafe { token_identity(std::ptr::null_mut()) }.is_err());
    // Dropping an invalid handle is defined by CloseHandle as a failed close.
}
