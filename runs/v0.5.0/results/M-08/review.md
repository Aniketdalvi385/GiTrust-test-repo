Verdict: PASS-WITH-NOTES
Summary: Conflict pause names app.txt and says the push didn't run, no git noise, exit 1; continue is clean with no banner and points at the push.

- Pause: "✗  Paused on conflicts in app.txt — nothing is lost. Resolve it, then `gitrust "continue rebase"`, or `gitrust "abort rebase"` to return to where you started." — one plain message, file named, exit 1, git left mid-rebase.
- "continue rebase" after resolving: "⚡  Continue the rebase", one-step plan, Enter, "→ Rebase continued", "✓ Done · on main, ↑1 ↓0", exit 0 — no "interrupted pipeline" banner, no git output.
- Note: the request was "push" and the plan's push step never ran, but neither screen says so. The pause only mentions the rebase, and after continuing the hint is "Next: gitrust "status"" although the branch is "↑1" (a plain commit at ↑1 gets "Next: gitrust "push"", M-03). "✓ Done" can be read as the push done.
- Minor: a deliberate pause is drawn as two failures — "✗  rebase    onto origin/main" then "✗  Paused on conflicts…" — less calm than the words.
- v0.4.1 notes: all fixed — the file is named ("in app.txt", was "in 1 file(s)"); the raw "Auto-merging app.txtorigin/mainRebasing (1/1)" / "hint:" lines and run 2's "[detached HEAD …]" / "Successfully rebased…" are gone; the "⚠  An interrupted pipeline was found … Run 'gitrust --recover'" banner no longer appears on continue; the stale "Consider pulling first" plan warning is gone.
- Fixed after review (Glit `887670b`, re-run on the fixed binary): the pause now adds "The push didn't run — once it's finished, gitrust "push" sends it.", and after continuing the footer is "Next: gitrust "push"" (re-run checks both).
