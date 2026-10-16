# M-18 · Undo 3 commits halts with guidance

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ HEAD unchanged
- ✅ screen shows 'squash'
- ✅ no 'Undo the last commit' echo (F17)
- ✅ no panic / raw error chain

## What a human should judge

Guidance (squash / revert / undo one) before anything else — not an 'Undo the last commit' echo for a 3-commit request (F17); nothing changes.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
