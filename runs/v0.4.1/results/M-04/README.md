# M-04 · Scoped push: only the login files

| | |
|---|---|
| **Part** | 1 · Everyday |
| **Model** | yes |
| **Flagship** | ★ yes |
| **Run** | auto · 2026-10-15 17:50 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ login.txt pushed
- ✅ readme.txt NOT pushed
- ✅ readme.txt still uncommitted
- ✅ no panic / raw error chain

## What a human should judge

Picker pre-selects the login files, shows +N −M and a reason per file; readme.txt not pre-selected; only login files reach the remote.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
