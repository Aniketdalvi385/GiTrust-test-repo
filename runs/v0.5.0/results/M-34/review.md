Verdict: PASS-WITH-NOTES
Summary: 9 was ignored and 2 chose "keep the changes in my files" at once; the commit was undone with its changes unstaged, exit 0. The menu hint offers digits the menu doesn't have.

- The behaviour is right: after "9" the screen is unchanged, "2" picked "Undo, keep the changes in my files" without Enter, the plan "reset     move the branch back to 9465a2b — changes stay in files  ⚠" ran on Enter, and the result is "→ Moved the branch back — the changes are in your files", exit 0. The menu is numbered and has no Cancel row.
- Copy: the help line "[1–9 or ↑↓ + Enter to choose · Esc cancel]" sits under a 4-row menu. It invites exactly the key this test shows doing nothing (9). "1–4" would be accurate. The same fixed "1–9" appears on every numbered menu in this run, including 2-row ones.
- Polish (convention 3): two hints are cut at the terminal width, "its changes stay in your files, unstag…" and "you'll type to con…".
- v0.4.1 notes: none of its notes were problems (all three confirmed the behaviour), and all of it is unchanged: the out-of-range key is ignored, the digit picks at once, and the next step is shown (Next: gitrust "status").
