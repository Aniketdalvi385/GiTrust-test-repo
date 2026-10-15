# M-14 · Switching away would strand a commit → guard

| | |
|---|---|
| **Part** | 3 · Stuck states |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ the detached commit is on a branch
- ✅ no panic / raw error chain

## What a human should judge

Says the commit would be stranded and offers a branch first; nothing lost.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Guard warns stranded commit, saves branch first, then switches; menu nits.

- Clear warning: "You have 1 commit(s) here that are on NO branch — switching away now would strand them." A branch is created first (rescue-worksaved-work) and the commit is preserved. Then "Switched to main", exit 0.
- Same menu nits as M-13: a "Cancel" row, unnumbered, and the awkward option "Switch back to your previous branch (no changes made)" which is confusing when the user asked to go to main.
- The branch is created before the plan is confirmed. The default name "rescue-work" was appended to in the harness ("rescue-worksaved-work"), as in M-13.
