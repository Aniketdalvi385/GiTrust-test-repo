# M-08 · Rebase conflict → calm pause → continue

| | |
|---|---|
| **Part** | 2 · Divergence |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:39 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ paused with a non-zero exit
- ✅ screen shows 'nothing is lost'
- ✅ screen shows 'continue rebase'
- ✅ git is mid-rebase
- ✅ no panic / raw error chain
- ✅ continue rebase exits 0
- ✅ rebase finished
- ✅ no panic / raw error chain

## What a human should judge

Pause message names the file, says nothing is lost, names continue/abort; exit ≠ 0.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
