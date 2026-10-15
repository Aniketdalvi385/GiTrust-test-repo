# M-15 · Undo: four plain options, keep staged

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ names the commit
- ✅ four options
- ✅ commit gone
- ✅ changes staged
- ✅ no panic / raw error chain

## What a human should judge

Question names the commit; four options with consequences; numbered.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Undo menu names the commit, four numbered options, keeps changes staged.

- First line "⚡  Undo the last commit"; question names the commit: `Undo 956d19c "feat: the mistake" — what should happen to its changes?`
- Four numbered options, each with a consequence; help line "[1–9 or ↑↓ + Enter to choose · Esc cancel]" matches convention, no Cancel row.
- Result "Undid commit 956d19c "feat: the mistake" (files re-staged)", exit 0, matches the choice made.
- Minor: option 2 and 4 descriptions are cut off with "…" ("unstag…", "you'll type to con…"), which hides the typed-confirm warning on the dangerous row.
