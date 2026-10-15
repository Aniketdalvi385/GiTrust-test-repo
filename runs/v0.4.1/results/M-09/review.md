Verdict: PASS
Summary: Abort rebase returns to the original HEAD; status shows no rebase.

- "Abort the rebase" shows a one-step plan, then "Rebase aborted — back to the original HEAD", exit 0.
- Status afterwards has no rebase text: "1 ahead · 1 behind", with a sensible hint, "Diverged from upstream… Pull first: gitrust "pull"".
