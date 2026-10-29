# M-06-manual · Diverged push → rebase → pushed

| | |
|---|---|
| **Part** | 2 · Divergence |
| **Model** | no |
| **Flagship** | ★ yes |
| **Run** | manual · 2026-10-29 10:47 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ in sync with origin (0 0)
- ✅ teammate commit below mine
- ✅ linear history (no merge commit)
- ✅ menu hints aren't cut off with '…' (F17)
- ✅ no 'Consider pulling first' (F13)
- ✅ no raw git output 'Successfully rebased'
- ✅ no raw git output 'Enumerating objects'
- ✅ no raw git output 'Removing'
- ✅ no panic / raw error chain

## What a human should judge

The rebase/merge choice explains both in plain words, hints not cut off; rebase + push in one go; no 'pull first' warning on a plan that already rebases; no raw git output.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
