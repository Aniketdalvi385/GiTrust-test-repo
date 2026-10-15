# M-13 · Commit on a detached HEAD → rescue to a branch

| | |
|---|---|
| **Part** | 3 · Stuck states |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:52 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ now on a branch
- ✅ no panic / raw error chain

## What a human should judge

Not a dead end: offers to make a branch here; the work ends up on it.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Detached-HEAD commit rescued onto a branch; menu has Cancel row.

- The warning is clear: "You are in DETACHED HEAD state… Any commit you make here will be orphaned (lose-able) unless you save it." The work ends up on a branch and the commit succeeds, exit 0.
- Convention break: the menu has a "Cancel" row, and is not numbered despite having 3 options. The help line is "[↑↓ move · Enter choose · Esc cancel]". The wording "Create a branch HERE" is shouty.
- The branch name prompt is pre-filled "rescue-work" and the typed text was appended, giving "rescue-workrescued". This is probably a harness artefact, but it shows the default is editable text, not replaced.
- The branch is created and changes staged ("✓ Created and switched to branch…", "✓ Staged your current changes…") before the plan is shown or confirmed. If the user then pressed q, those changes would remain. Worth reviewing.
