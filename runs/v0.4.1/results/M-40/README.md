# M-40 · Clean tree: 'commit everything' stops before asking

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:43 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ screen shows 'Nothing to commit'
- ✅ screen never shows 'message'
- ✅ no panic / raw error chain

## What a human should judge

Says nothing to commit before any message prompt.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
