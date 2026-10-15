# M-19 · Squash last 3: same content, one commit

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ 2 fewer commits
- ✅ tree identical
- ✅ no panic / raw error chain

## What a human should judge

Asks for the squashed message; tree identical afterwards.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Squash works and tree is identical, but message prompt and plan rendering are messy.

- Prompt "? Squashed commit message (3 commits): commit 3 / commit 2 / commit 1" is pre-filled with the three old messages joined. The result is a combined message, not a user-written one, so this is borderline against "never drafts messages". The multi-line pre-fill is awkward to edit.
- The test's typed text was appended with no separator ("commit 1three in one"), so the pre-fill is not selected or cleared. The plan shows a multi-line message, which breaks the plan layout.
- Final screen has a stray, truncated progress line `○  squash    last 3 → "commit 3 / commit 2` before the ✓ line.
- Behaviour right: "Squashed the last 3 commits into one", 2 fewer commits, tree identical, exit 0.
