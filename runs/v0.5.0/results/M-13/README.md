# M-13 · Commit on a detached HEAD → rescue to a branch

| | |
|---|---|
| **Part** | 3 · Stuck states |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 15:58 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ now on the new branch
- ✅ the work is committed on it
- ✅ rescue menu is numbered
- ✅ rescue menu has no Cancel row
- ✅ rescue offers 'Create a branch here to keep this work'
- ✅ the plan shows the new branch 'rescued'
- ✅ no panic / raw error chain

## What a human should judge

Not a dead end: a numbered menu (no Cancel row) offers to make a branch here; the branch is the plan's first step, not done before it (F6, F10); the work ends up on it.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Detached-HEAD commit: numbered rescue menu without Cancel, the branch is the plan's first step, work committed on it.

- "✦  Commit everything · 1.2s", a plain warning ("⚠  You are in DETACHED HEAD state." / "Currently at commit 98b2daa — not on any branch."), and a numbered menu with a consequence per row and no Cancel row: "[1] Create a branch here to keep this work  — your request then runs on it", "[2] Switch to main and leave this commit  — your request is not carried out", Esc in the help line.
- Nothing happens before the plan: "↳ Your request runs on a new branch "rescued" — created when you confirm the plan.", the quote is offered as "? Commit message (edit or accept): detached work", and the plan lists "●  branch    rescued", "●  checkout  rescued", "●  stage     all modified files", "●  commit    "detached work"". One Enter; "✓ Done · 1 commit on rescued"; exit 0.
- v0.4.1 notes: all fixed — the un-numbered menu with a "Cancel" row and shouty "Create a branch HERE to save work" are now the numbered rows above; the branch and staging no longer happen before the plan (v0.4.1 printed "✓ Created and switched to branch…" / "✓ Staged your current changes…" above the plan; now "→ Created branch rescued" comes only after Enter). "rescue-workrescued" was the harness typing after the editable default "rescue-work"; the harness now clears it, so the branch is "rescued".
