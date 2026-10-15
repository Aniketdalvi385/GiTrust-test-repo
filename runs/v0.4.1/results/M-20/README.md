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
