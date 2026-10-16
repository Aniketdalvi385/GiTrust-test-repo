Verdict: PASS-WITH-NOTES
Summary: Abort returns exactly to the pre-rebase commit, status clean; the result reports a backup the plan never mentioned.

- "⚡  Abort the rebase", plan "●  rebase    abort  ⚠", Enter, "→ Rebase aborted — back to the original HEAD", "✓ Done · on main, ↑1 ↓1", exit 0; HEAD back at the pre-rebase tip.
- Status has no rebase talk: "On branch main · tracking origin/main · 1 ahead · 1 behind", "Nothing to commit, working tree clean.", "→ Diverged from upstream (1 ahead, 1 behind). Pull first: gitrust "pull"".
- Note (new in v0.5.0): the result adds "A backup of the discarded changes is in ~/.gitrust/trash/20261016-112512 for 7 days." Backing up first is right (convention 10), but the plan ("●  rebase    abort  ⚠") gave no hint of a discard or backup, and here the user had changed nothing — the only "changes" were the conflicted app.txt git left. Other backing-up plans say so before Enter; this line could at least name the file so it doesn't read as lost work.
- v0.4.1 notes: both were positive and still hold ("Rebase aborted — back to the original HEAD", the "Pull first: gitrust "pull"" hint).
