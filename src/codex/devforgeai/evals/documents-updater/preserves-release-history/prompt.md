---
description: "VER-05: a config key rename plus an untagged manifest bump to 1.1.0 keeps published releases byte-identical, adds a breaking Unreleased entry with no version or date, and fixes docs outside the diff."
tags: [documents-updater, ver-05]
max_turns: 60
timeout_seconds: 1200
allowed_tools: [exec_command, apply_patch, request_user_input]
---
I renamed the poll_interval setting to poll_interval_seconds. Update the documentation and the
changelog to match.
