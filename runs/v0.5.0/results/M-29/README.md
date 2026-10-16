# M-29 · Model down: warning, full menu, refusals

| | |
|---|---|
| **Part** | 7 · Meta |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ screen shows "isn't running"
- ✅ menu lists operations by title
- ✅ Esc at the menu exits 1
- ✅ screen shows 'Canceled — nothing was done.'
- ✅ --yes refuses (exit 1)
- ✅ --yes refusal doesn't paste the menu prompt (F15)
- ✅ screen says "can't tell which operation you mean"
- ✅ no terminal → exit 1
- ✅ screen shows 'no terminal to ask in'
- ✅ no-terminal advice for a menu doesn't suggest --yes (F17)
- ✅ status still works
- ✅ no panic / raw error chain
- ✅ no panic / raw error chain
- ✅ no panic / raw error chain

## What a human should judge

Warning names the fix; a menu of operations by title; --yes refuses with its own plain message for a model that's down (F15), no-terminal without suggesting --yes (F17) — both exit 1; status still instant.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
