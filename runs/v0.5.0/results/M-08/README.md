# M-08 · Rebase conflict → calm pause → continue

| | |
|---|---|
| **Part** | 2 · Divergence |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 15:58 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ paused with a non-zero exit
- ✅ screen shows 'nothing is lost'
- ✅ screen shows 'continue rebase'
- ✅ the pause names the conflicted file (F17)
- ✅ the pause says the push didn't run
- ✅ git is mid-rebase
- ✅ no panic / raw error chain
- ✅ continue rebase exits 0
- ✅ rebase finished
- ✅ no 'interrupted pipeline' banner (F7)
- ✅ after continuing, the push is the next step
- ✅ no raw git output 'Successfully rebased' (run 1)
- ✅ no raw git output 'Enumerating objects' (run 1)
- ✅ no raw git output 'Removing' (run 1)
- ✅ no raw git output 'Successfully rebased' (run 2)
- ✅ no raw git output 'Enumerating objects' (run 2)
- ✅ no raw git output 'Removing' (run 2)
- ✅ no panic / raw error chain

## What a human should judge

Pause message names the file, says nothing is lost, names continue/abort; exit ≠ 0. Continuing shows no 'interrupted pipeline' banner (the pause handed off, F7).

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Conflict pause names app.txt, no git noise, exit 1; continue is clean with no banner; nothing says the push is still to do.

- Pause: "✗  Paused on conflicts in app.txt — nothing is lost. Resolve it, then `gitrust "continue rebase"`, or `gitrust "abort rebase"` to return to where you started." — one plain message, file named, exit 1, git left mid-rebase.
- "continue rebase" after resolving: "⚡  Continue the rebase", one-step plan, Enter, "→ Rebase continued", "✓ Done · on main, ↑1 ↓0", exit 0 — no "interrupted pipeline" banner, no git output.
- Note: the request was "push" and the plan's push step never ran, but neither screen says so. The pause only mentions the rebase, and after continuing the hint is "Next: gitrust "status"" although the branch is "↑1" (a plain commit at ↑1 gets "Next: gitrust "push"", M-03). "✓ Done" can be read as the push done.
- Minor: a deliberate pause is drawn as two failures — "✗  rebase    onto origin/main" then "✗  Paused on conflicts…" — less calm than the words.
- v0.4.1 notes: all fixed — the file is named ("in app.txt", was "in 1 file(s)"); the raw "Auto-merging app.txtorigin/mainRebasing (1/1)" / "hint:" lines and run 2's "[detached HEAD …]" / "Successfully rebased…" are gone; the "⚠  An interrupted pipeline was found … Run 'gitrust --recover'" banner no longer appears on continue; the stale "Consider pulling first" plan warning is gone.
