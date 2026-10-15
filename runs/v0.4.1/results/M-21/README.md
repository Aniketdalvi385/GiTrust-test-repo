# M-21 · A failing pre-commit hook blocks the commit

| | |
|---|---|
| **Part** | 5 · Hooks |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:53 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ non-zero exit
- ✅ screen shows 'LINT FAILED'
- ✅ no new commit
- ✅ no panic / raw error chain

## What a human should judge

Says hooks were detected; the hook's output is shown; nothing committed; exit ≠ 0. Note: after the failure a 'Pick one: Show / Cancel' menu appears.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
