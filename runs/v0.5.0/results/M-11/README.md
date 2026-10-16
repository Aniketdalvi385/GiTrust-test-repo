# M-11 · Mid-rebase commit request names the rebase

| | |
|---|---|
| **Part** | 3 · Stuck states |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ screen never shows 'checkout a branch'
- ✅ screen shows 'rebase'
- ✅ did not exit 0 silently
- ✅ no panic / raw error chain

## What a human should judge

The answer is about the rebase (continue/abort), never 'checkout a branch'.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
