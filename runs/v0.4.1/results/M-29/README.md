# M-29 · Model down: warning, full menu, refusals

| | |
|---|---|
| **Part** | 7 · Meta |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:39 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ screen shows "isn't running"
- ✅ menu lists operations by title
- ✅ Esc at the menu exits 1
- ✅ screen shows 'Canceled — nothing was done.'
- ✅ --yes refuses (exit 1)
- ✅ screen shows 'Choices'
- ✅ no terminal → exit 1
- ✅ screen shows 'no terminal to ask in'
- ✅ status still works
- ✅ no panic / raw error chain
- ✅ no panic / raw error chain
- ✅ no panic / raw error chain

## What a human should judge

Warning names the fix; a menu of operations by title; --yes and no-terminal refuse with exit 1; status still instant.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
