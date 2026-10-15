# M-11 · Mid-rebase commit request names the rebase

| | |
|---|---|
| **Part** | 3 · Stuck states |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ screen never shows 'checkout a branch'
- ✅ screen shows 'rebase'
- ✅ did not exit 0 silently
- ✅ no panic / raw error chain

## What a human should judge

The answer is about the rebase (continue/abort), never 'checkout a branch'.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Commit mid-rebase refused clearly, naming the rebase options, exit 1.

- Output: "✗  A rebase is in progress. Back out with `gitrust "abort rebase"`, or resolve the conflicts and `gitrust "continue rebase"`." The message is plain and specific, with no "checkout a branch" misroute.
- Exit 1, instant, nothing changed. The first line "⚡  Commit everything" is printed before the refusal, which is slightly odd but harmless.
