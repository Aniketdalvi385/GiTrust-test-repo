Verdict: PASS-WITH-NOTES
Summary: F7 is fixed: after the rebase was finished with plain git, status shows no banner and `--recover` restores nothing (exit 1, HEAD kept). The pause now says the push didn't run; the two ✗ marks and "pipeline" remain.

- Right: the pause exits 1 and names the file: "Paused on conflicts in app.txt — nothing is lost. Resolve it, then `gitrust "continue rebase"`, or `gitrust "abort rebase"` to return to where you started." After plain `git rebase --continue`, status (exit 0) shows no "interrupted pipeline" banner and doesn't mention --recover. It says "On branch main · tracking origin/main · 1 ahead … → 1 unpushed commit(s). Try: gitrust "push"". `--recover` then prints one plain line and exits 1, with HEAD where git's rebase left it.
- Pause styling: a deliberate, calm pause is shown with two failure marks, "✗  rebase    onto origin/main" and "✗  Paused on conflicts…". The plan's second step (push → origin/main) isn't mentioned, so the user isn't told the push didn't run. They only learn it later from status ("1 unpushed commit(s)").
- Copy (convention 11): "No interrupted GiTrust pipeline found for this repo." "Pipeline" is internal vocabulary; everywhere else the screens say "Plan". The pointer to "find my lost work" is good.
- Polish: "1 unpushed commit(s)" has a lazy plural, and the 2-row menu's help line says "1–9" (see M-34).
- Fixed after review (Glit `887670b`, re-run on the fixed binary): the pause adds "The push didn't run — once it's finished, gitrust "push" sends it."
