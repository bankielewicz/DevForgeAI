# Preserve provider hook sources

The four pending hook configuration and runtime-requirement JSON files are copied unchanged from the shared checkout. They are a separate draft dependent on the shared foundation PR: https://github.com/bankielewicz/DevForgeAI/pull/1.

Independent source review matched their command/event interface to CLI baseline `4859a279784f902d5f9dabcb0664907b24b297a5`; this is not observed native hook delivery. The companion follow-up is https://github.com/bankielewicz/DevForge/pull/1.

`source-identities.json` records the exact four selected files. Existing framework structural checks passed and reported the declared provider runtime requirements with the runtime host NOT_VERIFIED. No hooks were executed, trusted, installed or activated. No orchestration, native evaluation or operational adoption is authorized by this source-preservation PR. The MVP documents were checked in the unchanged shared base.
