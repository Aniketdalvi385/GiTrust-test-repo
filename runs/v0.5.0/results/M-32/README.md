# M-32 · q at the plan cancels; stray keys are ignored

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ screen shows 'Canceled'
- ✅ nothing committed
- ✅ no panic / raw error chain

## What a human should judge

A stray key does nothing; q cancels; exit 1.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
