# M-38 · No terminal, a question needed: plain message, exit 1

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ screen shows 'no terminal to ask in'
- ✅ the advice for a choice doesn't suggest --yes (F17)
- ✅ no panic / raw error chain

## What a human should judge

One readable line, no 'caused by'; it's a choice, so the advice is to run it in a terminal — not --yes, which never chooses (F17).

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
