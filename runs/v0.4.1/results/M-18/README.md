# M-18 · Undo 3 commits halts with guidance

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ HEAD unchanged
- ✅ screen shows 'squash'
- ✅ no panic / raw error chain

## What a human should judge

Guidance (squash / revert / undo one); nothing changes.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
