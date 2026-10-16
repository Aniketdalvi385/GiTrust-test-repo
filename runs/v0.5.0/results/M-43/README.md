# M-43 · 'merge develop into feature' brings in develop, not main

| | |
|---|---|
| **Part** | 2 · Divergence |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 15:58 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ still on feature
- ✅ the menu opens on Merge, the request's word
- ✅ feature isn't published by the merge
- ✅ feature contains develop's commit
- ✅ feature does NOT contain main's new commit
- ✅ screen says 'Update from develop'
- ✅ no panic / raw error chain

## What a human should judge

⚡ the echo names the real source ('Update from develop'); the menu opens on Merge, the word the request used; the plan merges develop — never main (F19) — and doesn't publish feature, which was never pushed; feature ends with develop's commit and without main's.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: F19 is fixed: "⚡ Update from develop" merges origin/develop, not main, and feature stays on feature (exit 0). But "merge" still gets a "Rebase or merge?" menu with Rebase preselected, and the plan publishes a never-pushed branch.

- Right: the echo names the real source, "⚡  Update from develop", and the plan step is "merge     origin/develop → "Merge origin/develop into feature"". The result is "→ Merged origin/develop (merge commit recorded)", and the checks confirm develop's commit is in feature and main's is not.
- The request's verb is ignored: the user said "merge", yet the screen asks "? Your branch and origin/develop have diverged (↑1 ↓1). Rebase or merge?" with the cursor on "> [1] Rebase". Pressing Enter at that menu would plan a rebase the user didn't ask for (the plan would still show it before anything runs). intent.rs says an explicit "rebase" preselects Rebase, i.e. the strategy captured from the words is meant to set the menu's default, but reconcile_flow_from never receives the strategy, so the default is always Rebase.
- The plan does more than was asked: "●  push      → origin/feature (set upstream)" adds a push of feature, a branch that was never pushed, so Enter publishes it to origin ("→ Pushed to origin/feature (upstream set)"). It is honest (shown in the plan, skippable with "[s] don't push"), so it isn't unsafe. But it looks unintended: for an unpublished branch the Rebase path deliberately doesn't push ("This branch isn't on the remote yet — publish it with gitrust "publish""). The Merge path's "push only if not behind its own upstream" check treats a missing upstream as "not behind".
- Polish: "○  push      → origin/feature (set upstream)" stays on screen above the "✓ push" line (see M-37). The 2-row menu's help line says "1–9" (see M-34).
