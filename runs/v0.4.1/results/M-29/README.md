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

## Review

Verdict: PASS-WITH-NOTES
Summary: Model-down warning and refusals are safe; --yes message is clunky and long.

- PTY run: "The Kev model server isn't running at http://127.0.0.1:9." plus a fix line, then a full titled menu; Esc gives "↪  Canceled — nothing was done." exit 1. Good.
- No-terminal run prints the single plain line "This needs an answer, and there's no terminal to ask in..." exit 1. Good.
- --yes refusal reads "--yes won't choose for you — The local model isn't available — pick what you want to do (type to filter):" - the menu prompt is pasted in mid-sentence (stray capital, "type to filter" is meaningless without a terminal), followed by a ~35-item "Choices:" dump. Works but is noisy; trim to the reason and the next step.
- The model-down menu is unnumbered (more than 9 options), consistent with the convention. Status ("⚡  Show status", exit 0) works instantly.
