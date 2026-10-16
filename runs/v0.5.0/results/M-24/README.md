# M-24 · A dropped stash surfaces

| | |
|---|---|
| **Part** | 6 · Forensics |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ rescue branch has the wip change
- ✅ no internal 'index on …' row (F17)
- ✅ no panic / raw error chain

## What a human should judge

The dropped stash is listed — without git's internal 'index on …' commit beside it (F17) — and can be restored to a branch.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
