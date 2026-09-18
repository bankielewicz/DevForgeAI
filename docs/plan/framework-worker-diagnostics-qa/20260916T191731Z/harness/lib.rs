// Test-only topology. Every included production module remains the original file.
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/diagnostic.rs"]
pub mod diagnostic;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/effective_profile.rs"]
pub mod effective_profile;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/journal.rs"]
pub mod journal;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/launch_policy.rs"]
pub mod launch_policy;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/native_identity.rs"]
pub mod native_identity;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/oracle.rs"]
pub mod oracle;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/profile_sources.rs"]
pub mod profile_sources;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/request.rs"]
pub mod request;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/runner.rs"]
pub mod runner;

pub mod process_windows {
    include!("C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/process_windows.rs");

    #[cfg(test)]
    pub(crate) fn qa_without_query<T>(process: &mut OwnedProcess, action: impl FnOnce(&mut OwnedProcess) -> T) -> T {
        // Installed Windows SDK 10.0.26100.0/um/winnt.h:12741.
        const JOB_OBJECT_TERMINATE: u32 = 0x0008;
        let mut duplicate = std::ptr::null_mut();
        // Real duplicate of the SAME owned job. No API interception or fabricated error.
        // Retain TERMINATE only, deliberately omitting JOB_OBJECT_QUERY.
        unsafe {
            assert_ne!(DuplicateHandle(GetCurrentProcess(), process.job.as_raw_handle(),
                GetCurrentProcess(), &mut duplicate, JOB_OBJECT_TERMINATE, 0, 0), 0);
        }
        let restricted = owned(duplicate).unwrap();
        let original = std::mem::replace(&mut process.job, restricted);
        let outcome = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| action(process)));
        let restricted = std::mem::replace(&mut process.job, original);
        drop(restricted);
        match outcome {
            Ok(result) => result,
            Err(panic) => std::panic::resume_unwind(panic),
        }
    }
}

pub mod protocol {
    include!("C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/protocol.rs");
    #[cfg(test)]
    #[path = "C:/Projects/DevForgeAI/docs/plan/framework-worker-diagnostics-qa/20260916T191731Z/harness/session_cases.rs"]
    mod qa_cases;
}

#[cfg(test)]
mod config_cases;
#[cfg(test)]
mod fixture_config;
