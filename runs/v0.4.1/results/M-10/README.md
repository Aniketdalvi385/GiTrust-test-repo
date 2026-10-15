# M-10 · Sync feature with main

| | |
|---|---|
| **Part** | 2 · Divergence |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ feature contains main's commit
- ✅ no bare --force
- ✅ no panic / raw error chain

## What a human should judge

Target resolves to main; rebase on an unpublished branch needs no force push.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Sync rebases onto main with no push; closing note is a bit confusing.

- "sync with main" shows "⚡  Update from main" and the same numbered rebase/merge menu, then a one-step rebase plan with no push step. Result: "Rebased onto origin/main", on feature, exit 0.
- The no-force-push behaviour is good, but the trailing note comes after the "Next:" line and reads confusingly: "Not pushed — pushing this rebased branch needs a force push; re-run and confirm, or push manually with `git push --force-with-lease`." "Re-run and confirm" does not say what to re-run, and the README says the branch is unpublished, so it is unclear why a force push is mentioned.
- Raw "Successfully rebased and updated refs/heads/feature." leaks through.
