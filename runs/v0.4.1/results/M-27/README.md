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
