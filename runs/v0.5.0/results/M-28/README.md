# M-28 · --recover with nothing to recover points to forensics

| | |
|---|---|
| **Part** | 6 · Forensics |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1 (D4: nothing was recovered)
- ✅ screen shows 'find my lost work'
- ✅ no panic / raw error chain

## What a human should judge

Says there's nothing interrupted and suggests 'find my lost work'; exit 1 — an operation that didn't happen (D4).

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
