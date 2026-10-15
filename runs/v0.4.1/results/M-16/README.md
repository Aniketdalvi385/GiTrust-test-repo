# M-16 · Undo → throw away: type to confirm, trash backup

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | no |
| **Flagship** | ★ yes |
| **Run** | auto · 2026-10-15 17:42 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ commit gone
- ✅ working tree clean
- ✅ trash backup written
- ✅ screen shows 'backup'
- ✅ no panic / raw error chain

## What a human should judge

A typed confirmation before anything happens; the success line names the backup.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
