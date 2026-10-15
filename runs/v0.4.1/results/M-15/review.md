Verdict: PASS
Summary: Undo menu names the commit, four numbered options, keeps changes staged.

- First line "⚡  Undo the last commit"; question names the commit: `Undo 956d19c "feat: the mistake" — what should happen to its changes?`
- Four numbered options, each with a consequence; help line "[1–9 or ↑↓ + Enter to choose · Esc cancel]" matches convention, no Cancel row.
- Result "Undid commit 956d19c "feat: the mistake" (files re-staged)", exit 0, matches the choice made.
- Minor: option 2 and 4 descriptions are cut off with "…" ("unstag…", "you'll type to con…"), which hides the typed-confirm warning on the dangerous row.
