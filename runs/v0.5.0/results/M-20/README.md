# M-20 · Fix a pushed commit's message: escalate + lease

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ message fixed on the remote
- ✅ remote == local
- ✅ screen never shows '--force '
- ✅ typed confirmation asked at the plan (the plan is above it)
- ✅ nothing asks again after the typed value
- ✅ no raw git output 'Successfully rebased'
- ✅ no raw git output 'Enumerating objects'
- ✅ no raw git output 'Removing'
- ✅ no panic / raw error chain

## What a human should judge

Explains a force push is needed; one confirmation — the branch name typed at the plan (D1); uses --force-with-lease; no raw git output.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
