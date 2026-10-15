# M-17 · --yes cannot undo

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:39 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ HEAD untouched
- ✅ screen shows 'Choices'
- ✅ no panic / raw error chain

## What a human should judge

Refuses to choose for you, lists the choices, exit 1.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
