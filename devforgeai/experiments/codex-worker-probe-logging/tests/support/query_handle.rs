use super::*;
// Test-only OS stimulus from the retained QA technique. No QueryInformationJobObject interception.
pub(crate) fn without_query<T>(
    process: &mut OwnedProcess,
    action: impl FnOnce(&mut OwnedProcess) -> T,
) -> T {
    let mut duplicate = null_mut();
    unsafe {
        assert_ne!(
            DuplicateHandle(
                GetCurrentProcess(),
                process.job.as_raw_handle(),
                GetCurrentProcess(),
                &mut duplicate,
                0x0008,
                0,
                0
            ),
            0
        );
    }
    let restricted = owned(duplicate).unwrap();
    let original = std::mem::replace(&mut process.job, restricted);
    let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| action(process)));
    let restricted = std::mem::replace(&mut process.job, original);
    drop(restricted);
    match result {
        Ok(v) => v,
        Err(p) => std::panic::resume_unwind(p),
    }
}
