# M-45 · Rebase finished with plain git: no stale banner, --recover undoes nothing

| | |
|---|---|
| **Part** | 2 · Divergence |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 15:58 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ paused on the conflict (exit ≠ 0)
- ✅ git is mid-rebase
- ✅ git finished the rebase (on top of the teammate's commit)
- ✅ status exits 0
- ✅ status shows no 'interrupted pipeline' banner
- ✅ status doesn't send you to --recover
- ✅ --recover exits 1 (nothing to restore, D4)
- ✅ --recover left HEAD where git's rebase put it
- ✅ the resolution is kept
- ✅ no panic / raw error chain
- ✅ no panic / raw error chain

## What a human should judge

After the conflict pause the user finishes with plain `git rebase --continue`. The next command shows no 'interrupted pipeline' banner, and `--recover` says there's nothing to restore (exit 1) instead of resetting the branch to before the rebase (F7).

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: F7 is fixed: after the rebase was finished with plain git, status shows no banner and `--recover` restores nothing (exit 1, HEAD kept). Polish remains: the pause looks like a failure and doesn't say the push didn't run, plus a "pipeline" jargon line.

- Right: the pause exits 1 and names the file: "Paused on conflicts in app.txt — nothing is lost. Resolve it, then `gitrust "continue rebase"`, or `gitrust "abort rebase"` to return to where you started." After plain `git rebase --continue`, status (exit 0) shows no "interrupted pipeline" banner and doesn't mention --recover. It says "On branch main · tracking origin/main · 1 ahead … → 1 unpushed commit(s). Try: gitrust "push"". `--recover` then prints one plain line and exits 1, with HEAD where git's rebase left it.
- Pause styling: a deliberate, calm pause is shown with two failure marks, "✗  rebase    onto origin/main" and "✗  Paused on conflicts…". The plan's second step (push → origin/main) isn't mentioned, so the user isn't told the push didn't run. They only learn it later from status ("1 unpushed commit(s)").
- Copy (convention 11): "No interrupted GiTrust pipeline found for this repo." "Pipeline" is internal vocabulary; everywhere else the screens say "Plan". The pointer to "find my lost work" is good.
- Polish: "1 unpushed commit(s)" has a lazy plural, and the 2-row menu's help line says "1–9" (see M-34).
