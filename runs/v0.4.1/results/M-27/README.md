# M-27 · Backup can't be written → nothing deleted

| | |
|---|---|
| **Part** | 6 · Forensics |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:43 |
| **Automatic checks** | ❌ failed |

## Checks

- ✅ non-zero exit
- ✅ untracked file still there
- ❌ no panic / raw error chain — `caused by:`

## What a human should judge

Refuses, names the backup failure; the file still exists.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: FAIL
Summary: Safe refusal (file kept, exit 1) but prints a raw "caused by:" error chain.

- Safe: with the trash dir unwritable, nothing is deleted, the file survives and exit is 1. This is the correct fail-closed behaviour.
- Breaks the no-raw-error-chain rule: "✗  Failed to create trash dir /var/folders/.../home/.gitrust/trash/20261015-174311" followed by "   caused by: Permission denied (os error 13)". The automatic check failed on this, and I agree.
- The message appears twice (once under the step, once as the final ✗ line). It has a long absolute path that wraps mid-word.
- It never says "nothing was deleted" or what to do next (for example, fix permissions on ~/.gitrust). Suggested copy: "Couldn't back up your files first, so nothing was deleted. Check that ~/.gitrust/trash is writable."
