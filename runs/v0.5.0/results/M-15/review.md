Verdict: PASS-WITH-NOTES
Summary: Undo names the commit, four numbered options with consequences, keeps changes staged; two hints still cut with "…".

- "⚡  Undo the last commit", "? Undo 586c41c "feat: the mistake" — what should happen to its changes?" — commit named; four numbered rows with consequences, no Cancel row, Esc in the help line.
- "[1] Undo, keep the changes staged" → plan "●  undo      586c41c "feat: the mistake"  ⚠", one Enter, "→ Undid commit 586c41c "feat: the mistake" (files re-staged)", "✓ Done · on main, ↑0 ↓0"; exit 0; commit gone, app.txt staged.
- Polish: rows 2 and 4 are still cut — "its changes stay in your files, unstag…" and "⚠⚠  — both go (git keeps them ~90 days) · you'll type to con…". They're cut at column 100 on a 110-column screen (the menu caps its width at 100), so a wider terminal won't show the rest — and the hidden part is the dangerous row's "you'll type to confirm".
- v0.4.1 notes: commit naming, four numbered options and the staged result still hold. "option 2 and 4 descriptions are cut off with '…'" — still there, same words.
