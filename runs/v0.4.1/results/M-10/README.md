# M-10 · Sync feature with main

| | |
|---|---|
| **Part** | 2 · Divergence |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ feature contains main's commit
- ✅ no bare --force
- ✅ no panic / raw error chain

## What a human should judge

Target resolves to main; rebase on an unpublished branch needs no force push.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
