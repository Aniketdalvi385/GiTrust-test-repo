Verdict: PASS
Summary: Mid-rebase status names rebase, conflicted file, and continue/abort phrases.

- "⚠ Rebase in progress — stopped at commit 1 of 1", "1 conflicted file (listed below) — edit it and remove the <<<<<<< / >>>>>>> markers.", then `gitrust "continue rebase"` or `gitrust "abort rebase"`, and "Conflicted:  ! app.txt". Exit 0 is right for a read-only status.
- Minor: "Last commit: 3346b9e "teammate: app"" is the upstream commit during a rebase, which could confuse; low priority.
