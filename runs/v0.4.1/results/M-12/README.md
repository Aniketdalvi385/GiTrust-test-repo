# M-12 · Commit a resolved merge: two parents

| | |
|---|---|
| **Part** | 3 · Stuck states |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:39 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ 2 parents
- ✅ merge finished
- ✅ no panic / raw error chain

## What a human should judge

Git's merge message is offered; the commit has two parents.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Merge commit offered git's own message; two parents created.

- "✦  Commit staged files · 18.8s" names the understanding with a time. The prompt is "Commit message (edit or accept): Merge branch 'side'", prefilled from git's MERGE_MSG, so GiTrust drafts nothing.
- Plan has one commit step with [e] edit. The result is "Committed: Merge branch 'side' (602c5eb→b591584)", exit 0. The checks confirm 2 parents.
- The 18.8s model time is slow but is the model's cost, not a bug.
