# M-04 · Scoped push: only the login files

| | |
|---|---|
| **Part** | 1 · Everyday |
| **Model** | yes |
| **Flagship** | ★ yes |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ login.txt pushed
- ✅ readme.txt NOT pushed
- ✅ readme.txt still uncommitted
- ✅ the quoted message is the commit's subject
- ✅ no panic / raw error chain

## What a human should judge

The topic survives the quoted message (F5): the picker pre-selects the login files, shows +N −M and a reason per file; readme.txt not pre-selected; 'login page' is offered as the message; only login files reach the remote.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
