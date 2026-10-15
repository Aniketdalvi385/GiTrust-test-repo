# M-09 · Abort rebase restores exactly

| | |
|---|---|
| **Part** | 2 · Divergence |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:16 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ HEAD back at the pre-rebase tip
- ✅ status shows no rebase
- ✅ no panic / raw error chain

## What a human should judge

Back to exactly where you were; status no longer talks about a rebase.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Abort rebase returns to the original HEAD; status shows no rebase.

- "Abort the rebase" shows a one-step plan, then "Rebase aborted — back to the original HEAD", exit 0.
- Status afterwards has no rebase text: "1 ahead · 1 behind", with a sensible hint, "Diverged from upstream… Pull first: gitrust "pull"".
