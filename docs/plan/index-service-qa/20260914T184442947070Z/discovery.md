# Read-only planning discovery

Native project C:\Projects\DevForgeAI; date2026-09-14; root has no .git. devforgeai has48 scoped non-target files, Cargo.toml/Cargo.lock, src/tests/examples/fixtures/queries/licenses/schemas/packaging and release binaries. No subordinate AGENTS.md found by scoped rg (no matches is not a tool failure). Existing source hash inventory is source-manifest.json; release identities are build-manifest.json.

Read commands included Get-Content of the selected spec, repository AGENTS.md, QA skill/reference/templates, companion query context, enforcement boundary, README/Cargo.toml and selected test bodies; rg file/attribute/function discovery; exact retained source passages are in criteria.json. A first broad rg included target/prior evidence and truncated tool output; it was not used to establish completeness. Scoped follow-up reads/inventory supplied these facts.

Observed commands and results:
- cargo --version: exit0; cargo1.97.1(c980f4866 2026-06-30).
- rustc --version: exit0; rustc1.97.1(8bab26f4f 2026-07-14).
- cargo llvm-cov --version: exit0; cargo-llvm-cov0.8.4.
- cargo llvm-cov --help: exit0; options for JSON, output-path, fail-under-lines, all-targets, ignore-filename-regex, locked/offline inspected. No coverage run.
- rustup target list --installed: exit0; i686-unknown-linux-musl, x86_64-pc-windows-msvc, x86_64-unknown-linux-gnu.
- $PSVersionTable.PSVersion.ToString():7.6.6.
- Initial Get-CimInstance Win32_OperatingSystem and wsl --list --verbose: sandbox access denied; result preserved in conversation, no successful qualification.
- Escalated "Get-CimInstance Win32_OperatingSystem | Format-List Caption,Version,OSArchitecture; wsl --list --verbose": aggregate exit0, Windows11 Pro10.0.26200/64-bit; Ubuntu and docker-desktop stopped, WSL2. No Linux executable launched.
- Get-Command ssh: sandbox exposes C:\Users\bryan\.sbx-denybin\ssh.bat; Python importlib find_spec reports paramiko absent. No dependencies installed.
- Authorized SSH read-only connection requested to me@192.168.245.128, supplied native checkout /home/me/Projects/index-qualification.iIHbKX/DevForgeAI/devforgeai. Pending result. Known-host scratch path selected C:\Projects\DevForgeAI\tmp\qa-index-ssh-known-hosts-20260914. Password never included in saved artifacts. No remote product tests/builds or writes authorized in this plan.
- File discovery/hash scripts used Python solely to read metadata/bytes and assemble documentation inputs. They are not product tests or executable QA harnesses.

Some initial inspection commands were batched; individual unreported shell exit codes/timestamps are unavailable and are not reconstructed. Actual source sizes/digests are verified at publication. Tool outputs for read-only discovery remain conversation evidence; these notes do not masquerade as case-bound runtime receipts.

## Completed SSH read-only discovery

First attempt exited1 after password prompt/server closure, with no remote command evidence. One bounded password-only retry succeeded (exit0). Final aggregate digest command also exited0. Authentication secret was provided only to the interactive prompt and is not retained here.

- Host: me@192.168.245.128, ED25519 SHA256:gZPEHCf0xDw80+8LrhvuhtUZ6mTsAAjoxMCatleEF40 (first-use key stored in the named scratch known-host file).
- Resolved checkout: /home/me/Projects/index-qualification.iIHbKX/DevForgeAI/devforgeai.
- /etc/os-release: Ubuntu26.04.1 LTS; uname -m:x86_64.
- command -v cargo:/usr/bin/cargo; cargo1.93.1(083ac5135 2025-12-15); rustc1.93.1(01f6ddf75 2026-02-11); cargo-llvm-cov0.9.1.
-48 file source canonical SHA256 manifest digest:67cab74432203b4f03874d19ec0652a6dcc2903227203b5c4b521c9d74b79419, equal to selected Windows candidate.
-Canonicalization: C-locale byte order of relative POSIX file names, exclude ./target subtree; each record is SHA256 + two ASCII spaces + ./relative/path + LF; SHA256 the entire concatenation. Initial local WindowsPath default sort produced a different ordering; explicit byte sorting resolved it. No source bytes were changed.
-Remote/local AGENTS.md hash both d47868fef2b87df0b2c065cfe235cfe9f12fcf9eeffa7af1f0973d7d21916fa7; no subordinate AGENTS.md was returned by remote discovery.
-Remote spec hash b1886c7bf237f823b2f83a8b37c1288ca26880ecfc58771568b38750e8855897 differs from selected local spec 52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4. Remote copy is not selected and was not modified. Use selected local contract bytes for assessment; bind access to those bytes in later remote execution.
-An attempted git-directory status print was expanded by the outer shell and returned True, not a valid remote status; remote Git metadata remains unverified. No Git candidate claim is based on it.
-Remote binaries, native linker/cache, child profiles and complete Linux collector isolation remain unverified. No product build/test, installation, startup change, SSH remote write or WSL launch occurred. All SSH sessions completed; no owned remote process remains.

