Verdict: PASS-WITH-NOTES
Summary: By hand: diverged push → plain rebase/merge choice with both hints whole, rebase + push in one plan, no warning, no git output; the push line is drawn twice.

- "Your branch and origin/main have diverged (↑1 ↓1). Rebase or merge?" with "[1] Rebase — your commit goes on top of theirs; best if it's only yours" and "[2] Merge — adds a merge commit; safer if others have your commits", neither cut. One Enter at a 2-step plan; linear history, in sync with origin, exit 0.
- Note: "○  push → origin/main" stays above "✓  push" (see M-37).
- The first hand run (2026-10-16) failed the menu-hint check because manual runs recorded no per-step screens — a suite bug, fixed in `b8a1733`; this record is the re-run.
- v0.4.1 notes: the "Consider pulling first" warning, the cut hints and the raw "Successfully rebased…" / "Enumerating objects…" lines are gone.
