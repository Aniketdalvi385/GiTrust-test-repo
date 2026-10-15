# M-20 · Fix a pushed commit's message: escalate + lease

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:39 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ message fixed on the remote
- ✅ remote == local
- ✅ screen never shows '--force '
- ✅ no panic / raw error chain

## What a human should judge

Explains a force push is needed; typed confirmation; uses --force-with-lease.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Reword of pushed commit escalates correctly with lease; raw git output leaks.

- Explains the situation: "Heads up: the target commit is already published…" and "pushing it needs a force push". Requires typing 'main'. The Safety line says "Uses --force-with-lease", and the screen never shows a bare --force. Remote matches local.
- Plan shows 2 steps (amend, force push) with ⚠ and ⛔ marks. This is good.
- The plan prompt "[Enter] run · [q] cancel" still follows the typed confirm, so it is confirmed twice.
- Raw git progress leaks inline: `○  force push→ origin/main (with-lease)Enumerating objects: 5, done.` … `+ 2d4ff2a...c1b3764 main -> main (forced update)`, glued onto the step line. Also the ⛔ "Irreversible" label is shown although the old SHA stays in the reflog.
