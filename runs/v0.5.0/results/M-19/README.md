# M-19 · Squash last 3: same content, one commit

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ 2 fewer commits
- ✅ tree identical
- ✅ the message is exactly what was typed (D3: no pre-filled subjects)
- ✅ no panic / raw error chain

## What a human should judge

Asks for the squashed message with an empty prompt, the old subjects listed above it (D3); tree identical afterwards.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
