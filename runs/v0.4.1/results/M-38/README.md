# M-38 · No terminal, a question needed: plain message, exit 1

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:19 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ screen shows 'no terminal to ask in'
- ✅ no panic / raw error chain

## What a human should judge

One readable line, no 'caused by'.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
