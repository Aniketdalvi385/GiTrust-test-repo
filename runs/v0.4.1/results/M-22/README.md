# M-22 · Revert succeeds despite the same hook

| | |
|---|---|
| **Part** | 5 · Hooks |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:51 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ one new (revert) commit
- ✅ other.txt gone
- ✅ no panic / raw error chain

## What a human should judge

Matches git: revert doesn't run pre-commit, so it succeeds. Note: revert asks its own (Y/n) question instead of the one-key plan prompt every other operation uses.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
