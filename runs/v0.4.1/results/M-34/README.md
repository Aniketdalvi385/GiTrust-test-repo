# M-34 · Numbered menu: a digit chooses at once

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:19 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ commit gone
- ✅ changes unstaged in files
- ✅ no panic / raw error chain

## What a human should judge

9 (no such row) is ignored; the right digit picks immediately.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Invalid digit ignored; digit 2 picks instantly and unstages correctly.

- Numbered menu ignored the out-of-range key (no change on screen), then "2" chose "Undo, keep the changes in my files" with no Enter needed.
- Plan: "reset  move the branch back to eca5b65 — changes stay in files  ⚠"; result "Moved the branch back — the changes are in your files", exit 0.
- Clear follow-up: Next: gitrust "status".
