# M-47 · Bring back a stash when there is none: plain message, exit 1

| | |
|---|---|
| **Part** | 1 · Everyday |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ screen says 'There are no stashed changes to bring back.'
- ✅ blocked before any plan
- ✅ the working tree is untouched
- ✅ no panic / raw error chain

## What a human should judge

Blocked before any plan, in plain words (F4); no libgit2 'refs/stash' error chain; the uncommitted edit untouched.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
