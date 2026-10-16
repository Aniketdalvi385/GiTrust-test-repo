# M-10 · Sync feature with main

| | |
|---|---|
| **Part** | 2 · Divergence |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 15:58 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ feature contains main's commit
- ✅ no bare --force
- ✅ no 're-run and confirm' note (F17)
- ✅ no raw git output 'Successfully rebased'
- ✅ no raw git output 'Enumerating objects'
- ✅ no raw git output 'Removing'
- ✅ no panic / raw error chain

## What a human should judge

Target resolves to main; rebase on an unpublished branch needs no force push; the closing note says how to push (not 're-run and confirm'); no raw git output.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Sync rebases feature onto origin/main with no push or force; the closing note is now clear but still sits after "Next:".

- "⚡  Update from main" (honest echo), "Fetching origin… ✓", menu adapted to a feature branch ("[1] Rebase  — your commit goes on top; a pushed branch needs a force push"), one-step plan "●  rebase    onto origin/main  ⚠" with no push, "→ Rebased onto origin/main", "✓ Done · on feature", exit 0; feature contains main's commit.
- Polish: the advice follows the Next line and repeats the step — "Next: gitrust "status"" then "Rebased onto origin/main. This branch isn't on the remote yet — publish it with gitrust "publish"." Two different next steps, the useful one last; "Next: gitrust "publish"" would read better.
- v0.4.1 notes: the confusing "Not pushed — pushing this rebased branch needs a force push; re-run and confirm, or push manually with `git push --force-with-lease`" is fixed (plain publish advice, no force push for an unpublished branch); its position after "Next:" is still there. "Successfully rebased and updated refs/heads/feature." no longer appears.
