# M-14 · Switching away would strand a commit → guard

| | |
|---|---|
| **Part** | 3 · Stuck states |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 15:58 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ the detached commit is on a branch
- ✅ saved-work holds the detached commit
- ✅ on main afterwards (the request was 'checkout main')
- ✅ no 'your request runs on' the branch it leaves
- ✅ screen says 'then you switch to main'
- ✅ rescue menu is numbered
- ✅ rescue menu has no Cancel row
- ✅ rescue offers 'Create a branch here to keep this work'
- ✅ the plan shows the new branch 'saved-work'
- ✅ no panic / raw error chain

## What a human should judge

Says the commit would be stranded and offers a branch first (numbered menu, no Cancel row); the plan is: make the branch, then switch to main (F6, F10); nothing lost. The copy says the branch keeps the commit and the switch then leaves it.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Guard saves the stranded commit on a branch inside the plan, then switches to main; the rescue copy wrongly says the request runs on the new branch.

- "⚡  Switch to “main”" with a clear warning: "You have 1 commit(s) here that are on NO branch — switching away now would strand them." Numbered menu, no Cancel row: "[1] Create a branch here to keep this work  — your request then runs on it", "[1–9 or ↑↓ + Enter to choose · Esc cancel]".
- The branch is part of the plan: "●  branch    saved-work  ⚠" then "●  checkout  main  ⚠", one Enter, "→ Created branch saved-work", "→ Switched to main", "✓ Done · on main, ↑0 ↓0"; saved-work holds the detached commit; exit 0.
- Copy: for a switch request, "your request then runs on it" and "↳ Your request runs on a new branch "saved-work" — created when you confirm the plan." are false — the request (switch to main) leaves saved-work behind, as the plan right below shows. The text is the generic rescue copy written for commit-style requests (right in M-13). Behaviour and plan are right, so this is copy, not a failure.
- Minor copy: "1 commit(s)" and the shouty "on NO branch".
- v0.4.1 notes: fixed — numbered, no "Cancel" row, and the confusing "Switch back to your previous branch (no changes made)" row is gone; the branch is no longer created before the plan (was "✓ Created and switched to branch 'rescue-worksaved-work'" above a one-step plan; now it is the plan's first step). "rescue-worksaved-work" was the harness typing after the editable default; it now clears "rescue-work", so the branch is "saved-work".
