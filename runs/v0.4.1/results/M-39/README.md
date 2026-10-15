# M-39 · Status mid-rebase says what to do

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ screen shows 'Rebase in progress'
- ✅ screen shows 'app.txt'
- ✅ screen shows 'continue rebase'
- ✅ no panic / raw error chain

## What a human should judge

Names the rebase, the conflicted file, and the continue/abort phrases.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Mid-rebase status names rebase, conflicted file, and continue/abort phrases.

- "⚠ Rebase in progress — stopped at commit 1 of 1", "1 conflicted file (listed below) — edit it and remove the <<<<<<< / >>>>>>> markers.", then `gitrust "continue rebase"` or `gitrust "abort rebase"`, and "Conflicted:  ! app.txt". Exit 0 is right for a read-only status.
- Minor: "Last commit: 3346b9e "teammate: app"" is the upstream commit during a rebase, which could confuse; low priority.
