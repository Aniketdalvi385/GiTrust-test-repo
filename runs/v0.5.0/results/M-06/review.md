Verdict: PASS-WITH-NOTES
Summary: Diverged push: plain rebase/merge choice, rebase + push in one plan, no warning or git noise; push line drawn twice.

- "⚡  Push to origin", "Fetching origin… ✓", "? Your branch and origin/main have diverged (↑1 ↓1). Rebase or merge?" with "[1] Rebase  — your commit goes on top of theirs; best if it's only yours" and "[2] Merge  — adds a merge commit; safer if others have your commits" — numbered, hints whole, no Cancel row, Esc in the help line.
- Plan "●  rebase    onto origin/main  ⚠" + "●  push      → origin/main  ⚠", "[Enter] run · [s] don't push · [q] cancel", no warning block. Result "→ Rebased onto origin/main", "→ Pushed 1 commit(s) to origin/main", "✓ Done · on main, ↑0 ↓0"; linear history; exit 0.
- Polish (new since v0.4.1): "○  push      → origin/main" remains above "✓  push      → origin/main", so the push reads as listed twice; "1 commit(s)".
- v0.4.1 notes: all fixed — hints no longer cut ("best if it's only yours", "safer if others have your commits" end in full); "Consider pulling first to avoid a non-fast-forward rejection" is gone from the plan; "Successfully rebased and updated refs/heads/main." no longer appears. Outcome still right.
