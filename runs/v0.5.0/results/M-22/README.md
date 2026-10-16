# M-22 · Revert succeeds despite the same hook

| | |
|---|---|
| **Part** | 5 · Hooks |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ one new (revert) commit
- ✅ other.txt gone
- ✅ no separate (Y/n) question — just the plan (F9)
- ✅ the plan names the commit's subject
- ✅ no raw git output 'Successfully rebased'
- ✅ no raw git output 'Enumerating objects'
- ✅ no raw git output 'Removing'
- ✅ no raw git output 'delete mode'
- ✅ no panic / raw error chain

## What a human should judge

Matches git: revert doesn't run pre-commit, so it succeeds. One confirmation — the plan, which names the commit by its subject, not just its SHA (D1, F17); no raw git output.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
